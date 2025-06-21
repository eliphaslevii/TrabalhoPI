from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, 
    QComboBox, QDialogButtonBox, QMessageBox
)
from database import create_connection

class VehicleForm(QDialog):
    def __init__(self, vehicle_id=None):
        super().__init__()
        
        self.vehicle_id = vehicle_id
        self.setWindowTitle("Adicionar Veículo" if not vehicle_id else "Editar Veículo")
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        self.placa_input = QLineEdit()
        self.modelo_input = QLineEdit()
        self.ano_input = QSpinBox()
        self.ano_input.setRange(1990, 2030)
        self.entregador_combo = QComboBox()

        form_layout.addRow("Placa:", self.placa_input)
        form_layout.addRow("Modelo:", self.modelo_input)
        form_layout.addRow("Ano:", self.ano_input)
        form_layout.addRow("Atribuir ao Entregador:", self.entregador_combo)
        layout.addLayout(form_layout)
        
        # Botões
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
        self.load_entregadores()
        if self.vehicle_id:
            self.load_vehicle_data()

    def load_entregadores(self):
        """Carrega a lista de entregadores para o ComboBox."""
        self.entregador_combo.addItem("Nenhum", None) # Opção para desvincular
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nome FROM users WHERE nivel = 2 ORDER BY nome")
                entregadores = cursor.fetchall()
                for e in entregadores:
                    self.entregador_combo.addItem(e['nome'], e['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar entregadores: {e}")
        finally:
            if conn: conn.close()

    def load_vehicle_data(self):
        """Se for edição, carrega os dados do veículo."""
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM veiculos WHERE id = %s", (self.vehicle_id,))
                vehicle = cursor.fetchone()
                if vehicle:
                    self.placa_input.setText(vehicle['placa'])
                    self.modelo_input.setText(vehicle['modelo'])
                    self.ano_input.setValue(vehicle['ano'])
                    if vehicle['entregador_id']:
                        # Encontra o entregador no combobox
                        index = self.entregador_combo.findData(vehicle['entregador_id'])
                        if index != -1:
                            self.entregador_combo.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados do veículo: {e}")
        finally:
            if conn: conn.close()
            
    def get_data(self):
        """Retorna os dados do formulário."""
        return {
            'placa': self.placa_input.text(),
            'modelo': self.modelo_input.text(),
            'ano': self.ano_input.value(),
            'entregador_id': self.entregador_combo.currentData()
        } 