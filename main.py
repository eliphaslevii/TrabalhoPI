import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from auth_service import AuthService  # Importa a camada de serviço


# THREAD DE AUTENTICAÇÃO
class AuthThread(QThread):
    result = pyqtSignal(bool)

    def _init_(self, user, password):
        super()._init_()
        self.user = user
        self.password = password

    def run(self):
        success = AuthService.validate_credentials(self.user, self.password)
        self.result.emit(success)


# TELA DE LOGIN
class LoginWindow(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_user = QLabel("Usuário:")
        self.label_user.setAlignment(Qt.AlignCenter)
        self.input_user = QLineEdit()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)

        self.label_pass = QLabel("Senha:")
        self.label_pass.setAlignment(Qt.AlignCenter)
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        user = self.input_user.text()
        password = self.input_pass.text()

        self.login_button.setEnabled(False)
        self.login_button.setText("Verificando...")

        self.auth_thread = AuthThread(user, password)
        self.auth_thread.result.connect(self.auth_finished)
        self.auth_thread.start()

    def auth_finished(self, success):
        if success:
            QMessageBox.information(self, "Login", "Login bem-sucedido!")
        else:
            QMessageBox.critical(self, "Erro", "Usuário ou senha inválidos.")

        self.login_button.setEnabled(True)
        self.login_button.setText("Entrar")


if _name_ == "_main_":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
