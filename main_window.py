from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox, QPushButton,
    QHBoxLayout, QStatusBar
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
from auth_service import AuthService
from main_styles import get_dark_theme_styles, get_light_theme_styles

class MainWindow(QMainWindow):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.is_admin = AuthService.is_admin(username)
        self.settings = QSettings("PI", "App")
        self.is_dark_theme = self.settings.value("dark_theme", False, type=bool)
        self.setup_ui()
        self._apply_theme()

    def setup_ui(self):
        self.setWindowTitle("Route Management System")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon("img/account.png"))

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Mensagem de boas-vindas
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Menu bar (apenas para admin)
        if self.is_admin:
            self.setup_menu_bar()
            self.setup_status_bar()

    def setup_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu Usuários
        user_menu = menubar.addMenu("Usuários")
        add_user_action = QAction("Adicionar Usuário", self)
        add_user_action.triggered.connect(self.add_user)
        user_menu.addAction(add_user_action)

        # Menu Rotas
        routes_menu = menubar.addMenu("Rotas")
        manage_routes_action = QAction("Gerenciar Rotas", self)
        manage_routes_action.triggered.connect(self.manage_routes)
        routes_menu.addAction(manage_routes_action)

        # Menu Relatórios
        reports_menu = menubar.addMenu("Relatórios")
        view_reports_action = QAction("Ver Relatórios", self)
        view_reports_action.triggered.connect(self.view_reports)
        reports_menu.addAction(view_reports_action)

        # Menu Configurações
        settings_menu = menubar.addMenu("Configurações")
        theme_action = QAction("Alternar Tema", self)
        theme_action.triggered.connect(self._toggle_theme)
        settings_menu.addAction(theme_action)

        # Menu Sair
        logout_action = QAction("Sair", self)
        logout_action.triggered.connect(self.logout)
        menubar.addAction(logout_action)

    def setup_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def _apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(get_dark_theme_styles())
        else:
            self.setStyleSheet(get_light_theme_styles())

    def _toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.settings.setValue("dark_theme", self.is_dark_theme)
        self._apply_theme()

    def add_user(self):
        QMessageBox.information(self, "Adicionar Usuário", "Função em desenvolvimento")

    def manage_routes(self):
        QMessageBox.information(self, "Gerenciar Rotas", "Função em desenvolvimento")

    def view_reports(self):
        QMessageBox.information(self, "Relatórios", "Função em desenvolvimento")

    def logout(self):
        reply = QMessageBox.question(self, 'Sair', 
                                   'Tem certeza que deseja sair?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close() 