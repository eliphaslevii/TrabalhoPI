from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt
from auth_service import AuthService

class MainWindow(QMainWindow):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.is_admin = AuthService.is_admin(username)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Sistema de Rotas")
        self.setGeometry(100, 100, 800, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Mensagem de boas-vindas
        welcome_label = QLabel(f"Bem-vindo, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Menu bar (apenas para admin)
        if self.is_admin:
            self.setup_menu_bar()

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

    def add_user(self):
        QMessageBox.information(self, "Adicionar Usuário", "Função em desenvolvimento")

    def manage_routes(self):
        QMessageBox.information(self, "Gerenciar Rotas", "Função em desenvolvimento")

    def view_reports(self):
        QMessageBox.information(self, "Relatórios", "Função em desenvolvimento") 