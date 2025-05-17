from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox, QPushButton,
    QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QSpinBox, QTextEdit, QDialogButtonBox, QStackedWidget,
    QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QSettings, QDate
from PyQt5.QtGui import QIcon, QFont
from auth_service import AuthService
from main_styles import get_dark_theme_styles, get_light_theme_styles
from database import create_connection
from map_widget import MapWidget
from PyQt5.QtWidgets import QApplication

class MainWindow(QMainWindow):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.settings = QSettings("PI", "App")
        self.is_dark_theme = self.settings.value("dark_theme", False, type=bool)
        self.setup_ui()
        self._apply_theme()

    def setup_ui(self):
        self.setWindowTitle("Sistema de Gerenciamento de Rotas")
        self.setGeometry(100, 100, 800, 600)
        self.setup_menu_bar()
        self.setup_status_bar()

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 0, 20, 20)  # Margem superior 0
        main_layout.setSpacing(0)  # Sem espaçamento entre widgets

        # Layout de topo com grid para centralizar o label
        top_grid = QGridLayout()
        top_grid.setContentsMargins(0, 0, 0, 0)
        top_grid.setColumnStretch(0, 1)
        top_grid.setColumnStretch(1, 2)
        top_grid.setColumnStretch(2, 1)

        # Mensagem de boas-vindas centralizada
        welcome_label = QLabel(f"Bem-vindo, {self.username}!")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setAlignment(Qt.AlignCenter)
        font = welcome_label.font()
        font.setPointSize(18)
        font.setBold(True)
        welcome_label.setFont(font)
        top_grid.addWidget(welcome_label, 0, 0, 1, 3, alignment=Qt.AlignHCenter)

        # Botão de alternar tema no canto direito
        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(30, 30)
        self.theme_button.setObjectName("theme_button")
        self.theme_button.clicked.connect(self._toggle_theme)
        self._update_theme_button_icon()
        top_grid.addWidget(self.theme_button, 0, 2, alignment=Qt.AlignRight)

        main_layout.addLayout(top_grid)

        # Tabela de rotas
        self.routes_table = QTableWidget()
        self.routes_table.setColumnCount(5)
        self.routes_table.setHorizontalHeaderLabels(["ID", "Nome", "Data", "Status", "Entregador"])
        self.routes_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.routes_table)

        # Mapa integrado
        self.map_widget = MapWidget(self)
        main_layout.addWidget(self.map_widget)

        # Botões de ação
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)  # Espaço entre os botões
        self.add_route_btn = QPushButton("Nova Rota")
        self.add_route_btn.clicked.connect(self.show_new_route)
        buttons_layout.addWidget(self.add_route_btn)
        self.add_delivery_btn = QPushButton("Nova Entrega")
        self.add_delivery_btn.clicked.connect(self.show_new_delivery)
        buttons_layout.addWidget(self.add_delivery_btn)
        self.refresh_btn = QPushButton("Atualizar")
        self.refresh_btn.clicked.connect(self.show_update_routes)
        buttons_layout.addWidget(self.refresh_btn)
        main_layout.addLayout(buttons_layout)

    def setup_menu_bar(self):
        menubar = self.menuBar()

        if self.username == "admin":
            # Menu Configurações (apenas admin)
            settings_menu = menubar.addMenu("Configurações")
            system_settings_action = QAction("Configuração de Sistema", self)
            system_settings_action.triggered.connect(self.show_system_settings)
            settings_menu.addAction(system_settings_action)
            exit_action = QAction("Sair", self)
            exit_action.triggered.connect(self.logout)
            settings_menu.addAction(exit_action)
        else:
            # Menus próprios para entregador (sem 'Ver Mapa')
            from windows import MyDeliveriesWindow, MyPerformanceWindow

            entregas_menu = menubar.addMenu("Minhas Entregas")
            entregas_action = QAction("Abrir", self)
            entregas_action.triggered.connect(lambda: self._abrir_janela_dialog(MyDeliveriesWindow, "Minhas Entregas"))
            entregas_menu.addAction(entregas_action)

            desempenho_menu = menubar.addMenu("Meu Desempenho")
            desempenho_action = QAction("Abrir", self)
            desempenho_action.triggered.connect(lambda: self._abrir_janela_dialog(MyPerformanceWindow, "Meu Desempenho"))
            desempenho_menu.addAction(desempenho_action)

            # Menu Configurações apenas com Sair
            settings_menu = menubar.addMenu("Configurações")
            exit_action = QAction("Sair", self)
            exit_action.triggered.connect(self.logout)
            settings_menu.addAction(exit_action)

    def _toggle_theme(self):
        try:
            self.is_dark_theme = not self.is_dark_theme
            self._apply_theme()
            self._update_theme_button_icon()
        except Exception as e:
            print(f"Erro ao alternar tema: {str(e)}")

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
                # Remover qualquer setStyleSheet manual para o botão de tema
                self.theme_button.setStyleSheet("")
        except Exception as e:
            print(f"Erro ao atualizar ícone do tema: {str(e)}")

    def _apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(get_dark_theme_styles())
        else:
            self.setStyleSheet(get_light_theme_styles())
        self.settings.setValue("dark_theme", self.is_dark_theme)

    def logout(self):
        reply = QMessageBox.question(self, "Sair", "Deseja realmente sair?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close() 

    def setup_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Pronto")

    def show_new_route(self):
        # Implementar lógica para nova rota
        pass

    def show_new_delivery(self):
        # Implementar lógica para nova entrega
        pass

    def show_update_routes(self):
        # Implementar lógica para atualizar rotas
        pass

    def show_system_settings(self):
        from windows import SystemSettingsWindow
        dialog = SystemSettingsWindow(self)
        dialog.exec_()

    def _abrir_janela_dialog(self, DialogClass, titulo):
        dialog = DialogClass(self)
        dialog.setWindowTitle(titulo)
        dialog.exec_()