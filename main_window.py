from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox, QPushButton,
    QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QSpinBox, QTextEdit, QDialogButtonBox, QStackedWidget,
    QGroupBox
)
from PyQt5.QtCore import Qt, QSettings, QDate
from PyQt5.QtGui import QIcon, QFont
from auth_service import AuthService
from main_styles import get_dark_theme_styles, get_light_theme_styles
from database import create_connection
from map_widget import MapWidget
from windows import (
    NewRouteWindow, NewDeliveryWindow, UpdateRoutesWindow,
    ManageCouriersWindow, AssignRoutesWindow, CourierPerformanceWindow,
    ManageDeliveriesWindow, PerformanceReportWindow, AllRoutesMapWindow,
    OptimizeRoutesWindow, TrafficMonitorWindow, RouteHistoryWindow,
    UpdateDeliveryStatusWindow, MyPerformanceWindow, CurrentRouteWindow,
    NavigationWindow, ManageRoutesWindow, ViewRoutesWindow,
    DailyReportWindow, MonthlyReportWindow, ViewAllDeliveriesWindow,
    SystemSettingsWindow, MyDeliveriesWindow, MyProfileWindow
)
from PyQt5.QtWidgets import QApplication

# Páginas do sistema
class RoutesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Stacked Widget para as páginas
        self.stacked_widget = QStackedWidget()
        
        # Página principal de rotas
        self.main_page = QWidget()
        main_layout = QVBoxLayout(self.main_page)
        
        # Tabela de rotas
        self.routes_table = QTableWidget()
        self.routes_table.setColumnCount(5)
        self.routes_table.setHorizontalHeaderLabels(["ID", "Nome", "Data", "Status", "Entregador"])
        self.routes_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.routes_table)

        # Botões de ação
        buttons_layout = QHBoxLayout()
        
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
        
        # Página de Nova Rota
        self.new_route_page = QWidget()
        new_route_layout = QVBoxLayout(self.new_route_page)
        
        # Formulário de Nova Rota
        form_group = QGroupBox("Nova Rota")
        form_layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.entregador_combo = QComboBox()
        self.carregar_entregadores()
        
        form_layout.addRow("Nome da Rota:", self.nome_input)
        form_layout.addRow("Entregador:", self.entregador_combo)
        
        form_group.setLayout(form_layout)
        new_route_layout.addWidget(form_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.save_new_route)
        buttons_layout.addWidget(save_btn)
        
        back_btn = QPushButton("Voltar")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        buttons_layout.addWidget(back_btn)
        
        new_route_layout.addLayout(buttons_layout)
        
        # Página de Nova Entrega
        self.new_delivery_page = QWidget()
        new_delivery_layout = QVBoxLayout(self.new_delivery_page)
        
        # Formulário de Nova Entrega
        form_group = QGroupBox("Nova Entrega")
        form_layout = QFormLayout()
        
        self.rua_input = QLineEdit()
        self.numero_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.estado_input = QLineEdit()
        self.cep_input = QLineEdit()
        self.complemento_input = QTextEdit()
        self.ordem_input = QSpinBox()
        self.ordem_input.setMinimum(1)
        
        form_layout.addRow("Rua:", self.rua_input)
        form_layout.addRow("Número:", self.numero_input)
        form_layout.addRow("Bairro:", self.bairro_input)
        form_layout.addRow("Cidade:", self.cidade_input)
        form_layout.addRow("Estado:", self.estado_input)
        form_layout.addRow("CEP:", self.cep_input)
        form_layout.addRow("Complemento:", self.complemento_input)
        form_layout.addRow("Ordem:", self.ordem_input)
        
        form_group.setLayout(form_layout)
        new_delivery_layout.addWidget(form_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.save_new_delivery)
        buttons_layout.addWidget(save_btn)
        
        back_btn = QPushButton("Voltar")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        buttons_layout.addWidget(back_btn)
        
        new_delivery_layout.addLayout(buttons_layout)
        
        # Página de Atualização
        self.refresh_page = QWidget()
        refresh_layout = QVBoxLayout(self.refresh_page)
        
        # Opções de atualização
        options_group = QGroupBox("Opções de Atualização")
        options_layout = QVBoxLayout()
        
        self.refresh_all_btn = QPushButton("Atualizar Todas as Rotas")
        self.refresh_all_btn.clicked.connect(self.refresh_all_routes)
        options_layout.addWidget(self.refresh_all_btn)
        
        self.refresh_status_btn = QPushButton("Atualizar Status")
        self.refresh_status_btn.clicked.connect(self.refresh_status)
        options_layout.addWidget(self.refresh_status_btn)
        
        options_group.setLayout(options_layout)
        refresh_layout.addWidget(options_group)
        
        # Botão voltar
        back_btn = QPushButton("Voltar")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        refresh_layout.addWidget(back_btn)
        
        # Adicionar todas as páginas ao stacked widget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.new_route_page)
        self.stacked_widget.addWidget(self.new_delivery_page)
        self.stacked_widget.addWidget(self.refresh_page)
        
        layout.addWidget(self.stacked_widget)

    def carregar_entregadores(self):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nome FROM users WHERE nivel = 2")
                    entregadores = cursor.fetchall()
                    for entregador in entregadores:
                        self.entregador_combo.addItem(entregador['nome'], entregador['id'])
            finally:
                conn.close()

    def save_new_route(self):
        # Implementar lógica de salvamento
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.refresh_routes()

    def save_new_delivery(self):
        # Implementar lógica de salvamento
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.refresh_routes()

    def refresh_all_routes(self):
        # Implementar lógica de atualização
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.refresh_routes()

    def refresh_status(self):
        # Implementar lógica de atualização de status
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.refresh_routes()

    def refresh_routes(self):
        # Implementação existente do refresh_routes
        pass

    def show_new_route(self):
        dialog = NewRouteWindow(self)
        dialog.exec_()

    def show_new_delivery(self):
        dialog = NewDeliveryWindow(self)
        dialog.exec_()

    def show_update_routes(self):
        dialog = UpdateRoutesWindow(self)
        dialog.exec_()

class DeliveriesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Página de Entregas")
        layout.addWidget(label)

class ReportsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Página de Relatórios")
        layout.addWidget(label)

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Página de Configurações")
        layout.addWidget(label)

class ProfilePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Página de Perfil")
        layout.addWidget(label)

class MapWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualização do Mapa")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Usar o widget de mapa em vez do placeholder
        self.map_widget = MapWidget(self)
        layout.addWidget(self.map_widget)
        
        # Botões de controle
        buttons_layout = QHBoxLayout()
        
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)

class ThemeDialog(QDialog):
    def __init__(self, parent=None, current_theme=False):
        super().__init__(parent)
        self.setWindowTitle("Alterar Tema")
        self.current_theme = current_theme
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Escolha o tema:")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Botões de tema
        theme_layout = QHBoxLayout()
        
        light_btn = QPushButton("Tema Claro")
        light_btn.setIcon(QIcon("img/sun.png"))
        light_btn.clicked.connect(lambda: self.select_theme(False))
        theme_layout.addWidget(light_btn)
        
        dark_btn = QPushButton("Tema Escuro")
        dark_btn.setIcon(QIcon("img/moon.png"))
        dark_btn.clicked.connect(lambda: self.select_theme(True))
        theme_layout.addWidget(dark_btn)
        
        layout.addLayout(theme_layout)
        
        # Botão de fechar
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def select_theme(self, is_dark):
        self.current_theme = is_dark
        self.accept()

# Janela Principal
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
        self.setWindowTitle("Sistema de Gerenciamento de Rotas")
        self.resize(1000, 650)  # Tamanho menor

        # Centraliza a janela na tela
        frameGm = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())

        self.setWindowIcon(QIcon("img/account.png"))

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Mensagem de boas-vindas
        welcome_label = QLabel(f"Bem-vindo, {self.username}!")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Stacked Widget para as páginas
        self.stacked_widget = QStackedWidget()
        
        # Criar e adicionar páginas
        self.routes_page = RoutesPage()
        self.deliveries_page = DeliveriesPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()
        self.profile_page = ProfilePage()
        
        self.stacked_widget.addWidget(self.routes_page)
        self.stacked_widget.addWidget(self.deliveries_page)
        self.stacked_widget.addWidget(self.reports_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.profile_page)
        
        layout.addWidget(self.stacked_widget)

        # Menu bar
        self.setup_menu_bar()
        self.setup_status_bar()

    def setup_menu_bar(self):
        menubar = self.menuBar()

        if self.is_admin:
            # Menu Rotas (Admin)
            routes_menu = menubar.addMenu("Rotas")
            view_routes_action = QAction("Visualizar Rotas", self)
            view_routes_action.triggered.connect(self.view_routes)
            routes_menu.addAction(view_routes_action)
            manage_routes_action = QAction("Gerenciar Rotas", self)
            manage_routes_action.triggered.connect(self.manage_routes)
            routes_menu.addAction(manage_routes_action)
            assign_routes_action = QAction("Atribuir Rotas", self)
            assign_routes_action.triggered.connect(self.assign_routes)
            routes_menu.addAction(assign_routes_action)

            # Menu Mapa (Admin)
            map_menu = menubar.addMenu("Mapa")
            view_map_action = QAction("Ver Mapa", self)
            view_map_action.triggered.connect(self.view_map)
            map_menu.addAction(view_map_action)
            view_all_routes_action = QAction("Visualizar Todas as Rotas", self)
            view_all_routes_action.triggered.connect(self.view_all_routes_map)
            map_menu.addAction(view_all_routes_action)
            optimize_routes_action = QAction("Otimizar Rotas", self)
            optimize_routes_action.triggered.connect(self.optimize_routes)
            map_menu.addAction(optimize_routes_action)
            traffic_monitor_action = QAction("Monitor de Tráfego", self)
            traffic_monitor_action.triggered.connect(self.monitor_traffic)
            map_menu.addAction(traffic_monitor_action)

            # Menu Entregadores (Admin)
            couriers_menu = menubar.addMenu("Entregadores")
            manage_couriers_action = QAction("Gerenciar Entregadores", self)
            manage_couriers_action.triggered.connect(self.manage_couriers)
            couriers_menu.addAction(manage_couriers_action)
            courier_performance_action = QAction("Desempenho", self)
            courier_performance_action.triggered.connect(self.view_courier_performance)
            couriers_menu.addAction(courier_performance_action)

            # Menu Entregas (Admin)
            deliveries_menu = menubar.addMenu("Entregas")
            view_all_deliveries_action = QAction("Todas as Entregas", self)
            view_all_deliveries_action.triggered.connect(self.view_all_deliveries)
            deliveries_menu.addAction(view_all_deliveries_action)
            manage_deliveries_action = QAction("Gerenciar Entregas", self)
            manage_deliveries_action.triggered.connect(self.manage_deliveries)
            deliveries_menu.addAction(manage_deliveries_action)

            # Menu Relatórios (Admin)
            reports_menu = menubar.addMenu("Relatórios")
            daily_report_action = QAction("Relatório Diário", self)
            daily_report_action.triggered.connect(self.generate_daily_report)
            reports_menu.addAction(daily_report_action)
            monthly_report_action = QAction("Relatório Mensal", self)
            monthly_report_action.triggered.connect(self.generate_monthly_report)
            reports_menu.addAction(monthly_report_action)
            performance_report_action = QAction("Relatório de Desempenho", self)
            performance_report_action.triggered.connect(self.generate_performance_report)
            reports_menu.addAction(performance_report_action)

            # Menu Configurações (Admin)
            settings_menu = menubar.addMenu("Configurações")
            system_settings_action = QAction("Configurações do Sistema", self)
            system_settings_action.triggered.connect(self.show_system_settings)
            settings_menu.addAction(system_settings_action)
            theme_action = QAction("Alterar Tema", self)
            theme_action.triggered.connect(self.show_theme_dialog)
            settings_menu.addAction(theme_action)

        else:
            # Menu Rotas (Entregador)
            routes_menu = menubar.addMenu("Minhas Rotas")
            view_my_routes_action = QAction("Visualizar Rotas", self)
            view_my_routes_action.triggered.connect(self.view_my_current_route)
            routes_menu.addAction(view_my_routes_action)
            route_history_action = QAction("Histórico de Rotas", self)
            route_history_action.triggered.connect(self.view_route_history)
            routes_menu.addAction(route_history_action)

            # Menu Mapa (Entregador)
            map_menu = menubar.addMenu("Mapa")
            view_my_route_action = QAction("Minha Rota Atual", self)
            view_my_route_action.triggered.connect(self.view_my_current_route)
            map_menu.addAction(view_my_route_action)
            navigation_action = QAction("Navegação", self)
            navigation_action.triggered.connect(self.navigation)
            map_menu.addAction(navigation_action)
            view_map_action = QAction("Ver Mapa", self)
            view_map_action.triggered.connect(self.view_map)
            map_menu.addAction(view_map_action)

            # Menu Entregas (Entregador)
            deliveries_menu = menubar.addMenu("Minhas Entregas")
            view_my_deliveries_action = QAction("Entregas do Dia", self)
            view_my_deliveries_action.triggered.connect(self.view_my_deliveries)
            deliveries_menu.addAction(view_my_deliveries_action)
            update_status_action = QAction("Atualizar Status", self)
            update_status_action.triggered.connect(self.update_delivery_status)
            deliveries_menu.addAction(update_status_action)

            # Menu Perfil (Entregador)
            profile_menu = menubar.addMenu("Perfil")
            view_profile_action = QAction("Meu Perfil", self)
            view_profile_action.triggered.connect(self.view_my_profile)
            profile_menu.addAction(view_profile_action)
            performance_action = QAction("Meu Desempenho", self)
            performance_action.triggered.connect(self.view_my_performance)
            profile_menu.addAction(performance_action)

            # Menu Configurações (Entregador)
            settings_menu = menubar.addMenu("Configurações")
            theme_action = QAction("Alterar Tema", self)
            theme_action.triggered.connect(self.show_theme_dialog)
            settings_menu.addAction(theme_action)

        # Menu Sair (Comum para ambos)
        logout_action = QAction("Sair", self)
        logout_action.triggered.connect(self.logout)
        menubar.addAction(logout_action)

    def setup_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Pronto")

    def view_routes(self):
        dialog = ViewRoutesWindow(self)
        dialog.exec_()

    def manage_routes(self):
        dialog = ManageRoutesWindow(self)
        dialog.exec_()

    def generate_daily_report(self):
        dialog = DailyReportWindow(self)
        dialog.exec_()

    def generate_monthly_report(self):
        dialog = MonthlyReportWindow(self)
        dialog.exec_()

    def _apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(get_dark_theme_styles())
        else:
            self.setStyleSheet(get_light_theme_styles())

    def show_system_settings(self):
        dialog = SystemSettingsWindow(self)
        dialog.exec_()

    def show_theme_dialog(self):
        dialog = ThemeDialog(self, self.is_dark_theme)
        if dialog.exec_() == QDialog.Accepted:
            self.is_dark_theme = dialog.current_theme
        self.settings.setValue("dark_theme", self.is_dark_theme)
        self._apply_theme()

    def logout(self):
        reply = QMessageBox.question(self, 'Sair', 
                                   'Tem certeza que deseja sair?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close() 

    # Métodos para Admin
    def manage_couriers(self):
        dialog = ManageCouriersWindow(self)
        dialog.exec_()

    def assign_routes(self):
        dialog = AssignRoutesWindow(self)
        dialog.exec_()

    def view_courier_performance(self):
        dialog = CourierPerformanceWindow(self)
        dialog.exec_()

    def view_all_deliveries(self):
        dialog = ViewAllDeliveriesWindow(self)
        dialog.exec_()

    def manage_deliveries(self):
        dialog = ManageDeliveriesWindow(self)
        dialog.exec_()

    def generate_performance_report(self):
        dialog = PerformanceReportWindow(self)
        dialog.exec_()

    def view_all_routes_map(self):
        dialog = AllRoutesMapWindow(self)
        dialog.exec_()

    def optimize_routes(self):
        dialog = OptimizeRoutesWindow(self)
        dialog.exec_()

    def monitor_traffic(self):
        dialog = TrafficMonitorWindow(self)
        dialog.exec_()

    def view_map(self):
        dialog = MapWindow(self)
        dialog.exec_()

    # Métodos para Entregador
    def view_route_history(self):
        dialog = RouteHistoryWindow(self)
        dialog.exec_()

    def update_delivery_status(self):
        dialog = UpdateDeliveryStatusWindow(self)
        dialog.exec_()

    def view_my_performance(self):
        dialog = MyPerformanceWindow(self)
        dialog.exec_()

    def view_my_current_route(self):
        dialog = CurrentRouteWindow(self)
        dialog.exec_()

    def navigation(self):
        dialog = NavigationWindow(self)
        dialog.exec_()

    def view_my_deliveries(self):
        dialog = MyDeliveriesWindow(self)
        dialog.exec_()

    def view_my_profile(self):
        dialog = MyProfileWindow(self)
        dialog.exec_()