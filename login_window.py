import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from database import migrate_database
from auth_service import AuthService
from main_window import MainWindow

# Criar banco de dados e tabelas ao iniciar
migrate_database()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.setup_ui()

    def setup_ui(self):
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

    def login(self):
        user = self.input_user.text()
        pwd = self.input_pass.text()

        if AuthService.validate_credentials(user, pwd):
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
