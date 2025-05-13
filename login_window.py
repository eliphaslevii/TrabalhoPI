import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QHBoxLayout, QFormLayout,
    QToolTip, QProgressBar
)
from PyQt5.QtCore import Qt, QSettings, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QIcon, QPainter, QPen
from database import migrate_database
from auth_service import AuthService
from main_window import MainWindow
from login_styles import get_dark_theme_styles, get_light_theme_styles


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
        
        # Configurar tema inicial
        self.is_dark_theme = self.settings.value("dark_theme", False, type=bool)
        
        # Configurar a janela para ser inicialmente transparente
        self.setWindowOpacity(0)
        
        self.setup_ui()
        self._load_credentials()
        self._apply_theme()
        
        # Iniciar a animação após um pequeno delay
        QTimer.singleShot(100, self._start_animation)

    def _get_theme_styles(self):
        if self.is_dark_theme:
            return get_dark_theme_styles()
        else:
            return get_light_theme_styles()

    def _apply_theme(self):
        self.setStyleSheet(self._get_theme_styles())
        self.settings.setValue("dark_theme", self.is_dark_theme)

    def _toggle_theme(self):
        try:
            self.is_dark_theme = not self.is_dark_theme
            self._apply_theme()
            self._update_theme_button_icon()
        except Exception as e:
            print(f"Erro ao alternar tema: {str(e)}")

    def setup_ui(self):
        try:
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(30, 30, 30, 30)
            layout.setAlignment(Qt.AlignCenter)

            # Botão de alternar tema com efeito hover
            self.theme_button = QPushButton()
            self.theme_button.setFixedSize(25, 25)
            self.theme_button.setObjectName("theme_button")
            self.theme_button.clicked.connect(self._toggle_theme)
            self._update_theme_button_icon()

            # Layout para o botão de tema com margens ajustadas
            theme_layout = QHBoxLayout()
            theme_layout.setContentsMargins(0, -45, -50, 0)
            theme_layout.addStretch()
            theme_layout.addWidget(self.theme_button)
            layout.addLayout(theme_layout)

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
            form_layout.setLabelAlignment(Qt.AlignLeft)
            form_layout.setFormAlignment(Qt.AlignLeft)
            form_layout.setContentsMargins(0, 0, 0, 0)
            form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

            # Campo de usuário
            self.input_user = QLineEdit()
            self.input_user.setPlaceholderText("username")
            self.input_user.setMinimumHeight(35)
            self.input_user.setMinimumWidth(250)
            self.input_user.setToolTip("Digite seu nome de usuário")
            self.input_user.returnPressed.connect(self.login)
            self.input_user.setAlignment(Qt.AlignLeft)
            self.input_user.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    padding-left: 10px;
                    text-align: left;
                }
            """)

            # Campo de senha
            self.input_pass = QLineEdit()
            self.input_pass.setEchoMode(QLineEdit.Password)
            self.input_pass.setPlaceholderText("password")
            self.input_pass.setMinimumHeight(35)
            self.input_pass.setMinimumWidth(250)
            self.input_pass.setToolTip("Digite sua senha")
            self.input_pass.returnPressed.connect(self.login)
            self.input_pass.setAlignment(Qt.AlignLeft)
            self.input_pass.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    padding-left: 10px;
                    text-align: left;
                }
            """)

            # Criar labels com ícones
            user_label = QLabel()
            user_pixmap = QPixmap("img/user.png")
            user_pixmap = user_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            user_label.setPixmap(user_pixmap)

            pass_label = QLabel()
            pass_pixmap = QPixmap("img/padlockk.png")
            pass_pixmap = pass_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pass_label.setPixmap(pass_pixmap)

            form_layout.addRow(user_label, self.input_user)
            form_layout.addRow(pass_label, self.input_pass)

            # Checkboxes
            checkbox_layout = QVBoxLayout()
            checkbox_layout.setSpacing(10)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            
            self.remember_me = QCheckBox("Remember me")
            self.remember_me.setToolTip("Save your credentials for next login")
            self.remember_me.stateChanged.connect(self._toggle_remember_me)
            
            self.show_password_cb = QCheckBox("Show password")
            self.show_password_cb.setToolTip("Show/hide the entered password")
            self.show_password_cb.stateChanged.connect(self._toggle_password_visibility)
            
            checkbox_layout.addWidget(self.remember_me)
            checkbox_layout.addWidget(self.show_password_cb)

            # Barra de progresso (inicialmente oculta)
            self.progress_bar = QProgressBar()
            self.progress_bar.setVisible(False)
            self.progress_bar.setFixedHeight(3)
            self.progress_bar.setFixedWidth(250)
            self.progress_bar.setTextVisible(False)

            # Botão de login
            self.btn_login = QPushButton("Entrar")
            self.btn_login.setMinimumHeight(40)
            self.btn_login.setMinimumWidth(250)
            self.btn_login.clicked.connect(self.login)
            self.btn_login.setToolTip("Clique para fazer login (ou pressione Enter)")

            layout.addLayout(form_layout)
            layout.addLayout(checkbox_layout)
            layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
            layout.addSpacing(10)
            layout.addWidget(self.btn_login, alignment=Qt.AlignCenter)

            self.setLayout(layout)
        except Exception as e:
            print(f"Erro ao configurar UI: {str(e)}")

    def _toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.input_pass.setEchoMode(QLineEdit.Normal)
            self.show_password_cb.setText("Show password")
        else:
            self.input_pass.setEchoMode(QLineEdit.Password)
            self.show_password_cb.setText("Show password")

    def _toggle_remember_me(self, state):
        if state == Qt.Checked:
            self.remember_me.setText("Remember me")
        else:
            self.remember_me.setText("Remember me")

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

    def _start_animation(self):
        # Criar animação de opacidade
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)  # 500ms
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Criar animação de posição
        self.pos_animation = QPropertyAnimation(self, b"pos")
        self.pos_animation.setDuration(500)  # 500ms
        start_pos = self.pos()
        self.pos_animation.setStartValue(start_pos + QPoint(0, 20))  # Começa 20 pixels abaixo
        self.pos_animation.setEndValue(start_pos)
        self.pos_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Iniciar ambas as animações
        self.fade_animation.start()
        self.pos_animation.start()

    def _update_theme_button_icon(self):
        try:
            # Definir os caminhos dos ícones
            moon_path = "img/moon.png"
            sun_path = "img/sun.png"
            
            # Carregar o ícone apropriado
            icon_path = moon_path if not self.is_dark_theme else sun_path
            icon = QIcon(icon_path)
            
            if not icon.isNull():
                self.theme_button.setIcon(icon)
                self.theme_button.setIconSize(QSize(20, 20))
                
        except Exception as e:
            print(f"Erro ao atualizar ícone do tema: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
