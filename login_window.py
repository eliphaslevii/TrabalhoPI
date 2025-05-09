import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFormLayout, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSettings
from auth_service import AuthService

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

        self.label_user = QLabel("Usuário:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Senha:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self._on_login)

        self.remember_me = QCheckBox("Lembrar-me")
        self.show_password_cb = QCheckBox("Mostrar senha")
        self.show_password_cb.stateChanged.connect(self._toggle_password_visibility)

        opts = QHBoxLayout()
        opts.addWidget(self.remember_me)
        opts.addStretch()
        opts.addWidget(self.show_password_cb)

        layout.addRow(self.label_user, self.input_user)
        layout.addRow(self.label_pass, self.input_pass)
        layout.addRow(opts)
        layout.addRow(self.login_button)

        self.setLayout(layout)

    def _on_login(self):
        user = self.input_user.text()
        pwd  = self.input_pass.text()

        if AuthService.validate_credentials(user, pwd):
            QMessageBox.information(self, "Sucesso", "Login efetuado com sucesso!")
            if self.remember_me.isChecked():
                self._save_credentials(user, pwd)
            else:
                self.settings.clear()
            self.close()  # fechará a janela de login; abra aqui sua MainWindow
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")
            self.input_pass.clear()

    def _save_credentials(self, user, pwd):
        self.settings.setValue("username", user)
        self.settings.setValue("password", pwd)
        self.settings.setValue("remember", True)

    def _load_credentials(self):
        if self.settings.value("remember", False, type=bool):
            self.input_user.setText(self.settings.value("username", ""))
            self.input_pass.setText(self.settings.value("password", ""))
            self.remember_me.setChecked(True)

    def _toggle_password_visibility(self, state):
        mode = QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password
        self.input_pass.setEchoMode(mode)

if __name__ == "__main__":
    # Primeiro, garantir que a tabela e usuários existam
    from database import migrate_database
    migrate_database()

    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
