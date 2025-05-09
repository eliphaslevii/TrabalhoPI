import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFormLayout, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSettings

from auth_service import AuthService
from database import create_connection, migrate_database
from main_admin import MainAdmin
from main_gestor import MainGestor
from main_entregador import MainEntregador

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.settings = QSettings("PI", "App")
        self._build_ui()
        self._load_credentials()
        self.input_user.setFocus()

    def _build_ui(self):
        layout = QFormLayout()

        self.input_user = QLineEdit()
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.login)

        self.remember_me = QCheckBox("Lembrar-me")
        self.show_password_cb = QCheckBox("Mostrar senha")
        self.show_password_cb.stateChanged.connect(self._toggle_password_visibility)

        opts = QHBoxLayout()
        opts.addWidget(self.remember_me)
        opts.addStretch()
        opts.addWidget(self.show_password_cb)

        layout.addRow(QLabel("Usuário:"), self.input_user)
        layout.addRow(QLabel("Senha:"), self.input_pass)
        layout.addRow(opts)
        layout.addRow(self.login_button)

        self.setLayout(layout)

    def login(self):
        user = self.input_user.text().strip()
        pwd = self.input_pass.text().strip()

        if not user or not pwd:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha.")
            return

        if AuthService.validate_credentials(user, pwd):
            if self.remember_me.isChecked():
                self.settings.setValue("username", user)
                self.settings.setValue("password", pwd)
                self.settings.setValue("remember", True)
            else:
                self.settings.clear()

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nivel FROM users WHERE nome=%s", (user,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            nivel = row[0] if row else None

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
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")
            self.input_pass.clear()

    def _load_credentials(self):
        if self.settings.value("remember", False, type=bool):
            self.input_user.setText(self.settings.value("username", ""))
            self.input_pass.setText(self.settings.value("password", ""))
            self.remember_me.setChecked(True)

    def _toggle_password_visibility(self, state):
        mode = QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password
        self.input_pass.setEchoMode(mode)

if __name__ == "__main__":
    from database import migrate_database
    migrate_database()

    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
