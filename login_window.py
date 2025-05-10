import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
import pymysql
from main_admin import MainAdmin
from main_gestor import MainGestor
from main_entregador import MainEntregador
from database import migrate_database

# Criar banco de dados e tabelas ao iniciar
migrate_database()

# Função para criar conexão com MySQL
def create_connection():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="rotas",
            port=3306
        )
        print("[INFO] Conectado ao MySQL via PyMySQL (127.0.0.1:3306)")
        return conn
    except Exception as e:
        print("[ERRO] Falha ao conectar ao MySQL:", e)
        return None

# Validação simples de login
def validate_credentials(user, pwd):
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE nome=%s AND senha=%s", (user, pwd))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print("[ERRO] Erro ao consultar banco:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# Janela de Login
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("→ LoginWindow.__init__()")
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.next_window = None
        self.setup_ui()

    def setup_ui(self):
        print("→ UI construída")
        layout = QVBoxLayout()

        self.label_user = QLabel("Usuário:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Senha:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Entrar")
        self.btn_login.clicked.connect(self.login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)
        print("→ Botão conectado")

    def login(self):
        print("→ login() chamado")
        user = self.input_user.text()
        pwd = self.input_pass.text()
        print(f"[INFO] Tentativa de login: usuário='{user}'")

        if validate_credentials(user, pwd):
            print("[INFO] Login autorizado.")
            conn = create_connection()
            if not conn:
                QMessageBox.critical(self, "Erro", "Falha na conexão com o banco.")
                return

            try:
                cursor = conn.cursor()
                cursor.execute("SELECT nivel FROM users WHERE nome=%s", (user,))
                row = cursor.fetchone()
                nivel = row[0] if row else None
            except Exception as e:
                print(f"{e}")
                QMessageBox.critical(self, "Erro", "Erro ao buscar dados.")
                return
            finally:
                cursor.close()
                conn.close()

            if nivel == 1:
                self.next_window = MainAdmin()
            elif nivel == 2:
                self.next_window = MainGestor()
            elif nivel == 3:
                self.next_window = MainEntregador()
            else:
                QMessageBox.critical(self, "Erro", "Nível de usuário inválido.")
                return

            self.next_window.show()
            self.hide()
        else:
            print("[INFO] Login inválido.")
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

# Execução principal
if __name__ == "__main__":
    print("▶ Inicializando QApplication")
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
