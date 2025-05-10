import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout, QFormLayout,
    QToolTip, QProgressBar
)
from PyQt5.QtCore import Qt, QSettings, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QIcon, QPainter, QPen
from database import migrate_database
from auth_service import AuthService
from main_window import MainWindow

# Criar banco de dados e tabelas ao iniciar
migrate_database()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("img/account.png"))
        self.setGeometry(100, 100, 350, 400)
        self.settings = QSettings("PI", "App")
        self.login_attempts = 0
        self.max_attempts = 3
        self.setup_ui()
        self._load_credentials()
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #000000;
                font-size: 11px;
                font-weight: normal;
            }
            QLineEdit {
                padding: 8px;
                padding-left: 35px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
                font-size: 11px;
                text-align: left;
            }
            QLineEdit::placeholder {
                color: rgba(0, 0, 0, 0.3);
                text-align: left;
            }
            QLineEdit:focus {
                border: 2px solid #808080;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QCheckBox {
                color: #000000;
                font-size: 10px;
                font-weight: normal;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 3px;
            }
            QCheckBox::indicator:hover {
                border: 1px solid rgba(128, 128, 128, 0.5);
            }
            QProgressBar {
                border: none;
                background-color: #E0E0E0;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 1px;
            }
        """)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignCenter)

        # Logo
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("img/user.png")
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(
                100, 100,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        layout.addSpacing(10)

        # Formulário
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Campo de usuário
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("username")
        self.input_user.setMinimumHeight(35)
        self.input_user.setMinimumWidth(250)
        self.input_user.setToolTip("Digite seu nome de usuário")
        self.input_user.returnPressed.connect(self.login)

        # Campo de senha
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setPlaceholderText("password")
        self.input_pass.setMinimumHeight(35)
        self.input_pass.setMinimumWidth(250)
        self.input_pass.setToolTip("Digite sua senha")
        self.input_pass.returnPressed.connect(self.login)

        # Criar labels com ícones
        user_label = QLabel()
        user_pixmap = QPixmap("img/user.png")
        user_pixmap = user_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        user_label.setPixmap(user_pixmap)

        pass_label = QLabel()
        pass_pixmap = QPixmap("img/padlockk.png")
        pass_pixmap = pass_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pass_label.setPixmap(pass_pixmap)
        pass_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
            }
        """)

        form_layout.addRow(user_label, self.input_user)
        form_layout.addRow(pass_label, self.input_pass)

        # Checkboxes
        checkbox_layout = QVBoxLayout()
        checkbox_layout.setSpacing(10)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        
        self.remember_me = QCheckBox("Lembrar-me")
        self.remember_me.setToolTip("Salvar suas credenciais para o próximo login")
        self.remember_me.stateChanged.connect(self._toggle_remember_me)
        
        self.show_password_cb = QCheckBox("Mostrar senha")
        self.show_password_cb.setToolTip("Mostrar/ocultar a senha digitada")
        self.show_password_cb.stateChanged.connect(self._toggle_password_visibility)
        
        checkbox_layout.addWidget(self.remember_me)
        checkbox_layout.addWidget(self.show_password_cb)

        # Barra de progresso (inicialmente oculta)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setFixedWidth(250)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #E0E0E0;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 1px;
            }
        """)

        # Botão de login
        self.btn_login = QPushButton("Entrar")
        self.btn_login.setMinimumHeight(40)
        self.btn_login.setMinimumWidth(250)
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setToolTip("Clique para fazer login (ou pressione Enter)")

        # Botão "Esqueci minha senha"
        self.btn_forgot = QPushButton("Esqueci minha senha")
        self.btn_forgot.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2196F3;
                border: none;
                font-size: 12px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #1976D2;
            }
        """)
        self.btn_forgot.clicked.connect(self._forgot_password)

        layout.addLayout(form_layout)
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.btn_login, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_forgot, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.input_pass.setEchoMode(QLineEdit.Normal)
            self.show_password_cb.setText("Mostrar senha")
        else:
            self.input_pass.setEchoMode(QLineEdit.Password)
            self.show_password_cb.setText("Mostrar senha")

    def _toggle_remember_me(self, state):
        if state == Qt.Checked:
            self.remember_me.setText("Lembrar-me")
        else:
            self.remember_me.setText("Lembrar-me")

    def _toggle_show_password(self, state):
        self._update_checkbox_style(self.show_password_cb, state == Qt.Checked)
        self._toggle_password_visibility(state)

    def _save_credentials(self, user, pwd):
        if self.remember_me.isChecked():
            self.settings.setValue("username", user)
            self.settings.setValue("password", pwd)
            self.settings.setValue("remember", True)
        else:
            self.settings.clear()

    def _load_credentials(self):
        if self.settings.value("remember", False, type=bool):
            self.input_user.setText(self.settings.value("username", ""))
            self.input_pass.setText(self.settings.value("password", ""))
            self.remember_me.setChecked(True)

    def _forgot_password(self):
        QMessageBox.information(self, "Recuperar Senha", 
            "Entre em contato com o administrador do sistema para recuperar sua senha.")

    def login(self):
        if self.login_attempts >= self.max_attempts:
            QMessageBox.warning(self, "Erro", 
                "Número máximo de tentativas excedido. Tente novamente mais tarde.")
            return

        user = self.input_user.text()
        pwd = self.input_pass.text()

        if not user or not pwd:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        # Mostrar barra de progresso
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(0)  # Modo indeterminado
        self.btn_login.setEnabled(False)

        # Simular delay de autenticação
        QTimer.singleShot(800, lambda: self._process_login(user, pwd))

    def _process_login(self, user, pwd):
        if AuthService.validate_credentials(user, pwd):
            self._save_credentials(user, pwd)
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.hide()
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            if remaining > 0:
                QMessageBox.warning(self, "Erro", 
                    f"Usuário ou senha inválidos. Tentativas restantes: {remaining}")
            else:
                QMessageBox.warning(self, "Erro", 
                    "Número máximo de tentativas excedido. Tente novamente mais tarde.")

        # Esconder barra de progresso
        self.progress_bar.setVisible(False)
        self.btn_login.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
