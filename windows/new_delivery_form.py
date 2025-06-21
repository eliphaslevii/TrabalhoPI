import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QTimer, QStringListModel
from PyQt5.QtWidgets import QCompleter
from database import create_connection
import re

API_KEY = 'AIzaSyAXPQPmxkGD7X-KL5xGEgaSIfiKNdGrMmg'
AUTOCOMPLETE_URL = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
DETAILS_URL = 'https://maps.googleapis.com/maps/api/place/details/json'


class DeliveryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova Rota")
        self.setFixedSize(500, 400)
        self.latitude = None
        self.longitude = None
        self.init_ui()

        self.autocomplete_timer = QTimer()
        self.autocomplete_timer.setSingleShot(True)
        self.autocomplete_timer.timeout.connect(self.call_autocomplete_api)

        self.place_suggestions = []
        self.autocomplete_model = QStringListModel()
        self.completer = QCompleter(self.autocomplete_model, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.address_input.setCompleter(self.completer)
        self.completer.activated[str].connect(self.on_suggestion_selected)

        self.load_routes()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Address input with autocomplete
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter address...")
        self.address_input.textChanged.connect(self.on_text_changed)
        form_layout.addRow("Address:", self.address_input)

        # Detailed address fields
        self.street = QLineEdit()
        self.number = QLineEdit()
        self.neighborhood = QLineEdit()
        self.city = QLineEdit()
        self.state = QLineEdit()
        self.state.setMaxLength(2)
        self.zip_code = QLineEdit()
        self.complement = QLineEdit()

        self.route_combo = QComboBox()

        form_layout.addRow("Street:", self.street)
        form_layout.addRow("Number:", self.number)
        form_layout.addRow("Neighborhood:", self.neighborhood)
        form_layout.addRow("City:", self.city)
        form_layout.addRow("State (UF):", self.state)
        form_layout.addRow("ZIP Code:", self.zip_code)
        form_layout.addRow("Complement:", self.complement)
        form_layout.addRow("Route:", self.route_combo)

        # Save button
        self.save_button = QPushButton("Save Delivery")
        self.save_button.clicked.connect(self.save_delivery)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def load_routes(self):
        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Could not connect to database.")
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT r.id, r.nome
                    FROM rotas r
                    WHERE r.status = 'pendente'
                    ORDER BY r.data_criacao DESC
                """)
                routes = cursor.fetchall()
                self.route_combo.clear()
                for route in routes:
                    # Obter informações dos veículos da rota
                    veiculos_info = self.get_veiculos_rota(route['id'])
                    display_text = f"{route['nome']} - Veículos: {veiculos_info}"
                    self.route_combo.addItem(display_text, route['id'])
        finally:
            conn.close()

    def get_veiculos_rota(self, rota_id):
        """Obtém informações dos veículos associados a uma rota."""
        conn = create_connection()
        if not conn:
            return "N/A"
        
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT v.placa, u.nome as motorista
                    FROM rota_veiculos rv
                    JOIN veiculos v ON rv.veiculo_id = v.id
                    LEFT JOIN users u ON v.entregador_id = u.id
                    WHERE rv.rota_id = %s
                    ORDER BY v.placa
                """
                cursor.execute(sql, (rota_id,))
                veiculos = cursor.fetchall()
                
                if not veiculos:
                    return "Nenhum veículo"
                
                # Formatar lista de veículos
                veiculos_info = []
                for veiculo in veiculos:
                    motorista = veiculo['motorista'] or 'N/A'
                    veiculos_info.append(f"{veiculo['placa']} ({motorista})")
                
                return ", ".join(veiculos_info)
                
        except Exception as e:
            print(f"Erro ao obter veículos da rota: {e}")
            return "Erro"
        finally:
            if conn: conn.close()

    def on_text_changed(self, text):
        if len(text) < 3:
            self.autocomplete_model.setStringList([])
            return
        self.autocomplete_timer.start(50)

    def call_autocomplete_api(self):
        text = self.address_input.text()
        params = {
            'input': text,
            'types': 'address',
            'components': 'country:br',
            'key': API_KEY
        }
        try:
            resp = requests.get(AUTOCOMPLETE_URL, params=params)
            data = resp.json()
            if data['status'] == 'OK':
                self.place_suggestions = data['predictions']
                suggestions = [item['description'] for item in self.place_suggestions]
                self.autocomplete_model.setStringList(suggestions)
            else:
                self.autocomplete_model.setStringList([])
        except Exception as e:
            print("Erro autocomplete:", e)
            self.autocomplete_model.setStringList([])

    def on_suggestion_selected(self, text):
        for item in self.place_suggestions:
            if item['description'] == text:
                self.fetch_place_details(item['place_id'])
                break

    def fetch_place_details(self, place_id):
        params = {
            'place_id': place_id,
            'fields': 'address_component,formatted_address,geometry',
            'key': API_KEY
        }
        try:
            resp = requests.get(DETAILS_URL, params=params)
            data = resp.json()
            if data['status'] == 'OK':
                components = data['result']['address_components']
                self.fill_address_components(components)

                # Captura latitude e longitude
                location = data['result'].get('geometry', {}).get('location', {})
                self.latitude = location.get('lat')
                self.longitude = location.get('lng')
            else:
                QMessageBox.warning(self, "Error", "Could not fetch address details.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error fetching details: {e}")
    def fill_address_components(self, components):
        self.street.clear()
        self.number.clear()
        self.neighborhood.clear()
        self.city.clear()
        self.state.clear()
        self.zip_code.clear()
        self.complement.clear()

        for comp in components:
            types = comp['types']
            if 'route' in types:
                self.street.setText(comp['long_name'])
            elif 'street_number' in types:
                self.number.setText(comp['long_name'])
            elif 'sublocality_level_1' in types or 'neighborhood' in types:
                self.neighborhood.setText(comp['long_name'])
            elif 'locality' in types or 'administrative_area_level_2' in types:
                self.city.setText(comp['long_name'])
            elif 'administrative_area_level_1' in types:
                self.state.setText(comp['short_name'])
            elif 'postal_code' in types or 'postal_code_prefix' in types:
                self.zip_code.setText(comp['long_name'])

        if not self.zip_code.text():
            full_address = self.address_input.text()
            match = re.search(r'\d{5}-\d{3}', full_address)
            if match:
                self.zip_code.setText(match.group())

    def save_delivery(self):
        address = {
            'street': self.street.text(),
            'number': self.number.text(),
            'neighborhood': self.neighborhood.text(),
            'city': self.city.text(),
            'state': self.state.text(),
            'zip': self.zip_code.text(),
            'complement': self.complement.text()
        }

        if not address['street'] or not address['city'] or not address['state']:
            QMessageBox.warning(self, "Warning", "Please fill in all required address fields.")
            return

        route_id = self.route_combo.currentData()
        if not route_id:
            QMessageBox.warning(self, "Warning", "Please select a route.")
            return

        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Could not connect to the database.")
            return

        try:
            with conn.cursor() as cursor:
                # Insere endereço com latitude e longitude
                cursor.execute("""
                      INSERT INTO enderecos (rua, numero, bairro, cidade, estado, cep, complemento, latitude, longitude)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """, (
                    address['street'],
                    address['number'],
                    address['neighborhood'],
                    address['city'],
                    address['state'],
                    address['zip'],
                    address['complement'],
                    self.latitude,
                    self.longitude
                ))
                address_id = cursor.lastrowid

                cursor.execute("SELECT MAX(ordem) as max_order FROM entregas WHERE rota_id = %s", (route_id,))
                max_order = cursor.fetchone()['max_order'] or 0
                new_order = max_order + 1

                cursor.execute("""
                      INSERT INTO entregas (rota_id, endereco_id, ordem)
                      VALUES (%s, %s, %s)
                  """, (route_id, address_id, new_order))

                conn.commit()
                QMessageBox.information(self, "Success", "Delivery and address saved successfully!")

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Error saving delivery: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DeliveryForm()
    form.show()
    sys.exit(app.exec())
