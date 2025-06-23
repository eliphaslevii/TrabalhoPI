import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout, QFormLayout,
    QToolTip, QProgressBar, QMainWindow, QFrame
)
from PyQt5.QtCore import Qt, QSettings, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QIcon, QPainter, QPen
from database import migrate_database
from auth_service import AuthService
from main_window import MainWindow
from login_styles import get_login_styles


# Criar banco de dados e tabelas ao iniciar
migrate_database()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.settings = QSettings("PI", "App")
        self.setup_ui()
        self.load_credentials()

    def setup_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(0, 0, 380, 500)
        self.setStyleSheet(get_login_styles())
        
        # Layout centralizado
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)

        # Título
        title_label = QLabel("Sistema de Gestão")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addStretch(1)
        
        # Campo de usuário com ícone
        user_layout = QHBoxLayout()
        user_icon = QLabel()
        user_pixmap = QPixmap('img/user.png').scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        user_icon.setPixmap(user_pixmap)
        user_icon.setStyleSheet("background: transparent; border: none;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome de usuário")
        user_layout.addWidget(user_icon)
        user_layout.addWidget(self.username_input)
        main_layout.addLayout(user_layout)

        # Campo de senha com ícone
        pass_layout = QHBoxLayout()
        pass_icon = QLabel()
        pass_pixmap = QPixmap('img/padlockk.png').scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pass_icon.setPixmap(pass_pixmap)
        pass_icon.setStyleSheet("background: transparent; border: none;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(pass_icon)
        pass_layout.addWidget(self.password_input)
        main_layout.addLayout(pass_layout)

        # Checkbox "Lembrar-me"
        self.remember_me_checkbox = QCheckBox("Lembrar-me")
        main_layout.addWidget(self.remember_me_checkbox)
        main_layout.addStretch(1)

        # Botão de Login
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)
        main_layout.addWidget(self.login_button)
        
        main_layout.addStretch(2)

        center_layout.addLayout(main_layout)
        center_layout.addStretch()
        self.setLayout(center_layout)

    def load_credentials(self):
        """Carrega as credenciais salvas se 'Lembrar-me' estiver ativo."""
        if self.settings.value("remember", False, type=bool):
            self.username_input.setText(self.settings.value("username", ""))
            self.password_input.setText(self.settings.value("password", ""))
            self.remember_me_checkbox.setChecked(True)

    def save_credentials(self, username, password):
        """Salva as credenciais se 'Lembrar-me' estiver marcado."""
        if self.remember_me_checkbox.isChecked():
            self.settings.setValue("username", username)
            self.settings.setValue("password", password)
            self.settings.setValue("remember", True)
        else:
            # Limpa as configurações se não for para lembrar
            self.settings.remove("username")
            self.settings.remove("password")
            self.settings.remove("remember")

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        # Desabilitar botão para feedback
        self.login_button.setEnabled(False)

        # Simular delay de autenticação
        QTimer.singleShot(800, lambda: self._process_login(username, password))

    def _process_login(self, user, pwd):
        if self.auth_service.validate_credentials(user, pwd):
            self.save_credentials(user, pwd)
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.close()
        else:
            self.login_attempts += 1
            QMessageBox.warning(self, "Falha no Login", "Usuário ou senha incorretos.")
        
        # Reabilitar botão
        self.login_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('img/pacote.png'))
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec_())
