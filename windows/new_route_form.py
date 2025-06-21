import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QListWidget, QListWidgetItem, QCheckBox
)
from database import create_connection

class RotaForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Nova Rota")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        
        # Nome da Rota
        self.layout.addWidget(QLabel("Nome da Rota:"))
        self.nome_input = QLineEdit()
        self.layout.addWidget(self.nome_input)

        # Lista de Veículos
        self.layout.addWidget(QLabel("Selecione os Veículos para a Rota:"))
        self.veiculos_list = QListWidget()
        self.layout.addWidget(self.veiculos_list)

        # Botão Criar
        self.btn_criar = QPushButton("Criar Rota")
        self.btn_criar.clicked.connect(self.criar_rota)
        self.layout.addWidget(self.btn_criar)

        self.setLayout(self.layout)
        self.carregar_veiculos_disponiveis()

    def carregar_veiculos_disponiveis(self):
        """Carrega os veículos e seus motoristas na lista com checkboxes."""
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                sql = """
                    SELECT v.id, v.placa, v.modelo, u.nome as entregador_nome
                    FROM veiculos v
                    LEFT JOIN users u ON v.entregador_id = u.id
                    ORDER BY v.placa
                """
                cursor.execute(sql)
                veiculos = cursor.fetchall()

            for veiculo in veiculos:
                item_text = f"{veiculo['placa']} - {veiculo['modelo']} (Motorista: {veiculo['entregador_nome'] or 'N/A'})"
                item = QListWidgetItem()
                checkbox = QCheckBox(item_text)
                checkbox.setProperty("veiculo_id", veiculo['id'])
                self.veiculos_list.addItem(item)
                self.veiculos_list.setItemWidget(item, checkbox)

        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível carregar os veículos: {e}")
        finally:
            if conn: conn.close()

    def criar_rota(self):
        nome_rota = self.nome_input.text().strip()
        if not nome_rota:
            QMessageBox.warning(self, "Atenção", "O nome da rota é obrigatório.")
            return

        veiculos_selecionados_ids = []
        for i in range(self.veiculos_list.count()):
            item = self.veiculos_list.item(i)
            checkbox = self.veiculos_list.itemWidget(item)
            if checkbox and checkbox.isChecked():
                veiculos_selecionados_ids.append(checkbox.property("veiculo_id"))

        if not veiculos_selecionados_ids:
            QMessageBox.warning(self, "Atenção", "Selecione pelo menos um veículo para a rota.")
            return

        conn = None
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                # 1. Inserir a nova rota
                cursor.execute("INSERT INTO rotas (nome) VALUES (%s)", (nome_rota,))
                rota_id = cursor.lastrowid

                # 2. Associar os veículos à rota na tabela de ligação
                for veiculo_id in veiculos_selecionados_ids:
                    cursor.execute("INSERT INTO rota_veiculos (rota_id, veiculo_id) VALUES (%s, %s)", (rota_id, veiculo_id))
            
            conn.commit()
            QMessageBox.information(self, "Sucesso", f"Rota '{nome_rota}' criada com sucesso!")
            self.nome_input.clear()
            # Desmarcar checkboxes
            for i in range(self.veiculos_list.count()):
                item = self.veiculos_list.item(i)
                checkbox = self.veiculos_list.itemWidget(item)
                if checkbox: checkbox.setChecked(False)

        except Exception as e:
            if conn: conn.rollback()
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao criar rota: {e}")
        finally:
            if conn: conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = RotaForm()
    form.show()
    sys.exit(app.exec())
