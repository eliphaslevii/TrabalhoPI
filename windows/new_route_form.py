import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from database import create_connection  # seu módulo de conexão

class RotaForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Rota")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Nome da rota:"))
        self.nome_input = QLineEdit()
        self.layout.addWidget(self.nome_input)

        self.layout.addWidget(QLabel("Entregador:"))
        self.entregador_combo = QComboBox()
        self.layout.addWidget(self.entregador_combo)

        self.btn_criar = QPushButton("Criar Rota")
        self.btn_criar.clicked.connect(self.criar_rota)
        self.layout.addWidget(self.btn_criar)

        self.setLayout(self.layout)

        self.carregar_entregadores()

    def carregar_entregadores(self):
        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nome FROM users WHERE nivel = 2")
                entregadores = cursor.fetchall()
                self.entregador_combo.clear()
                for e in entregadores:
                    self.entregador_combo.addItem(e['nome'], e['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar entregadores:\n{e}")
        finally:
            conn.close()

    def criar_rota(self):
        nome = self.nome_input.text().strip()
        entregador_id = self.entregador_combo.currentData()

        if not nome:
            QMessageBox.warning(self, "Atenção", "Informe o nome da rota.")
            return

        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO rotas (nome, entregador_id) VALUES (%s, %s)",
                    (nome, entregador_id)
                )
                conn.commit()
                QMessageBox.information(self, "Sucesso", "Rota criada com sucesso!")
                self.nome_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar rota:\n{e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = RotaForm()
    form.show()
    sys.exit(app.exec())
