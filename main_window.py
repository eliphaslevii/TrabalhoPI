from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox, QPushButton,
    QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QSpinBox, QTextEdit, QDialogButtonBox, QStackedWidget,
    QGroupBox
)
from PyQt5.QtCore import Qt, QSettings, QDate
from PyQt5.QtGui import QIcon
from auth_service import AuthService
from main_styles import get_dark_theme_styles, get_light_theme_styles
from database import create_connection

# Páginas do sistema
class RoutesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tabela de rotas
        self.routes_table = QTableWidget()
        self.routes_table.setColumnCount(5)
        self.routes_table.setHorizontalHeaderLabels(["ID", "Nome", "Data", "Status", "Entregador"])
        self.routes_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.routes_table)

        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        self.add_route_btn = QPushButton("Nova Rota")
        self.add_route_btn.clicked.connect(self.add_route)
        buttons_layout.addWidget(self.add_route_btn)
        
        self.add_delivery_btn = QPushButton("Nova Entrega")
        self.add_delivery_btn.clicked.connect(self.add_delivery)
        buttons_layout.addWidget(self.add_delivery_btn)
        
        self.refresh_btn = QPushButton("Atualizar")
        self.refresh_btn.clicked.connect(self.refresh_routes)
        buttons_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(buttons_layout)

    def add_route(self):
        dialog = AddRouteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_routes()

    def add_delivery(self):
        dialog = AddDeliveryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_routes()

    def refresh_routes(self):
        # Implementação existente do refresh_routes
        pass

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

# Diálogos
class AddRouteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Nova Rota")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        self.nome_input = QLineEdit()
        self.entregador_combo = QComboBox()
        self.carregar_entregadores()
        
        layout.addRow("Nome da Rota:", self.nome_input)
        layout.addRow("Entregador:", self.entregador_combo)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

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

class AddDeliveryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Nova Entrega")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        self.rua_input = QLineEdit()
        self.numero_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.estado_input = QLineEdit()
        self.cep_input = QLineEdit()
        self.complemento_input = QTextEdit()
        self.ordem_input = QSpinBox()
        self.ordem_input.setMinimum(1)
        
        layout.addRow("Rua:", self.rua_input)
        layout.addRow("Número:", self.numero_input)
        layout.addRow("Bairro:", self.bairro_input)
        layout.addRow("Cidade:", self.cidade_input)
        layout.addRow("Estado:", self.estado_input)
        layout.addRow("CEP:", self.cep_input)
        layout.addRow("Complemento:", self.complemento_input)
        layout.addRow("Ordem:", self.ordem_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

class ViewDeliveriesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualizar Entregas")
        self.setGeometry(200, 200, 800, 600)
        self.setup_ui()
        self.load_deliveries()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tabela de entregas
        self.deliveries_table = QTableWidget()
        self.deliveries_table.setColumnCount(8)
        self.deliveries_table.setHorizontalHeaderLabels([
            "ID", "Rota", "Ordem", "Endereço", "Status", 
            "Data Entrega", "Observações", "Ações"
        ])
        self.deliveries_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.deliveries_table)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Atualizar")
        refresh_btn.clicked.connect(self.load_deliveries)
        buttons_layout.addWidget(refresh_btn)
        
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)

    def load_deliveries(self):
        conn = create_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id, r.nome as rota_nome, e.ordem,
                           CONCAT(ed.rua, ', ', ed.numero, ' - ', ed.bairro, ', ', ed.cidade, '/', ed.estado) as endereco,
                           e.status, e.data_entrega, e.observacoes
                    FROM entregas e
                    JOIN rotas r ON e.rota_id = r.id
                    JOIN enderecos ed ON e.endereco_id = ed.id
                    ORDER BY r.data_criacao DESC, e.ordem
                """)
                entregas = cursor.fetchall()
                
                self.deliveries_table.setRowCount(len(entregas))
                for i, entrega in enumerate(entregas):
                    self.deliveries_table.setItem(i, 0, QTableWidgetItem(str(entrega['id'])))
                    self.deliveries_table.setItem(i, 1, QTableWidgetItem(entrega['rota_nome']))
                    self.deliveries_table.setItem(i, 2, QTableWidgetItem(str(entrega['ordem'])))
                    self.deliveries_table.setItem(i, 3, QTableWidgetItem(entrega['endereco']))
                    self.deliveries_table.setItem(i, 4, QTableWidgetItem(entrega['status']))
                    self.deliveries_table.setItem(i, 5, QTableWidgetItem(str(entrega['data_entrega'] or '')))
                    self.deliveries_table.setItem(i, 6, QTableWidgetItem(entrega['observacoes'] or ''))
                    
                    # Botão de ação
                    action_btn = QPushButton("Atualizar Status")
                    action_btn.clicked.connect(lambda checked, e=entrega: self.update_delivery_status(e))
                    self.deliveries_table.setCellWidget(i, 7, action_btn)
        finally:
            conn.close()

    def update_delivery_status(self, entrega):
        status_dialog = QDialog(self)
        status_dialog.setWindowTitle("Atualizar Status da Entrega")
        layout = QVBoxLayout(status_dialog)
        
        # Combo box para selecionar o novo status
        status_combo = QComboBox()
        status_combo.addItems(['pendente', 'em_andamento', 'entregue', 'cancelada'])
        status_combo.setCurrentText(entrega['status'])
        layout.addWidget(QLabel("Novo Status:"))
        layout.addWidget(status_combo)
        
        # Campo para observações
        obs_edit = QTextEdit()
        obs_edit.setPlaceholderText("Observações (opcional)")
        obs_edit.setText(entrega['observacoes'] or '')
        layout.addWidget(QLabel("Observações:"))
        layout.addWidget(obs_edit)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, status_dialog)
        buttons.accepted.connect(status_dialog.accept)
        buttons.rejected.connect(status_dialog.reject)
        layout.addWidget(buttons)
        
        if status_dialog.exec_() == QDialog.Accepted:
            novo_status = status_combo.currentText()
            observacoes = obs_edit.toPlainText()
            
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            UPDATE entregas 
                            SET status = %s, observacoes = %s,
                                data_entrega = CASE 
                                    WHEN %s = 'entregue' THEN CURRENT_TIMESTAMP 
                                    ELSE data_entrega 
                                END
                            WHERE id = %s
                        """, (novo_status, observacoes, novo_status, entrega['id']))
                        conn.commit()
                        self.load_deliveries()
                        QMessageBox.information(self, "Sucesso", "Status atualizado com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao atualizar status: {str(e)}")
                finally:
                    conn.close()

class ManageRoutesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Rotas")
        self.setGeometry(200, 200, 1000, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        # Filtro de status
        status_label = QLabel("Status:")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Todos", "pendente", "em_andamento", "concluida"])
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_combo)
        
        # Filtro de data
        date_label = QLabel("Data:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.date_edit)
        
        # Botão de filtrar
        filter_btn = QPushButton("Filtrar")
        filter_btn.setIcon(QIcon("img/account.png"))
        filter_layout.addWidget(filter_btn)
        
        # Botão de limpar filtros
        clear_btn = QPushButton("Limpar Filtros")
        clear_btn.setIcon(QIcon("img/account.png"))
        filter_layout.addWidget(clear_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tabela de rotas
        self.routes_table = QTableWidget()
        self.routes_table.setColumnCount(6)
        self.routes_table.setHorizontalHeaderLabels([
            "ID", "Nome", "Data", "Status", "Entregador", "Ações"
        ])
        self.routes_table.horizontalHeader().setStretchLastSection(True)
        self.routes_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.routes_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.routes_table)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        # Botão de adicionar rota
        add_btn = QPushButton("Nova Rota")
        add_btn.setIcon(QIcon("img/account.png"))
        buttons_layout.addWidget(add_btn)
        
        # Botão de editar rota
        edit_btn = QPushButton("Editar Rota")
        edit_btn.setIcon(QIcon("img/account.png"))
        buttons_layout.addWidget(edit_btn)
        
        # Botão de excluir rota
        delete_btn = QPushButton("Excluir Rota")
        delete_btn.setIcon(QIcon("img/account.png"))
        buttons_layout.addWidget(delete_btn)
        
        # Botão de atualizar
        refresh_btn = QPushButton("Atualizar")
        refresh_btn.setIcon(QIcon("img/account.png"))
        buttons_layout.addWidget(refresh_btn)
        
        # Botão de fechar
        close_btn = QPushButton("Fechar")
        close_btn.setIcon(QIcon("img/account.png"))
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        # Conectar sinais
        filter_btn.clicked.connect(self.apply_filters)
        clear_btn.clicked.connect(self.clear_filters)
        add_btn.clicked.connect(self.add_route)
        edit_btn.clicked.connect(self.edit_route)
        delete_btn.clicked.connect(self.delete_route)
        refresh_btn.clicked.connect(self.refresh_routes)
        close_btn.clicked.connect(self.close)
        
        # Carregar dados iniciais
        self.refresh_routes()

    def apply_filters(self):
        status = self.status_combo.currentText()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        self.refresh_routes()

    def clear_filters(self):
        self.status_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        self.refresh_routes()

    def add_route(self):
        dialog = AddRouteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_routes()

    def edit_route(self):
        selected_rows = self.routes_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione uma rota para editar.")
            return
            
        row = selected_rows[0].row()
        route_id = self.routes_table.item(row, 0).text()
        
        # Abrir diálogo de edição
        dialog = AddRouteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_routes()

    def delete_route(self):
        selected_rows = self.routes_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione uma rota para excluir.")
            return
            
        row = selected_rows[0].row()
        route_id = self.routes_table.item(row, 0).text()
        route_name = self.routes_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirmar Exclusão',
            f'Tem certeza que deseja excluir a rota "{route_name}"?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.refresh_routes()

    def refresh_routes(self):
        # Limpar a tabela
        self.routes_table.setRowCount(0)
        
        # Adicionar algumas linhas de exemplo
        for i in range(5):
            row = self.routes_table.rowCount()
            self.routes_table.insertRow(row)
            
            # ID
            self.routes_table.setItem(row, 0, QTableWidgetItem(str(i + 1)))
            
            # Nome
            self.routes_table.setItem(row, 1, QTableWidgetItem(f"Rota {i + 1}"))
            
            # Data
            self.routes_table.setItem(row, 2, QTableWidgetItem(QDate.currentDate().toString("dd/MM/yyyy")))
            
            # Status
            status = ["pendente", "em_andamento", "concluida"][i % 3]
            self.routes_table.setItem(row, 3, QTableWidgetItem(status))
            
            # Entregador
            self.routes_table.setItem(row, 4, QTableWidgetItem(f"Entregador {i + 1}"))
            
            # Ações
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("img/account.png"))
            edit_btn.setToolTip("Editar")
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("img/account.png"))
            delete_btn.setToolTip("Excluir")
            actions_layout.addWidget(delete_btn)
            
            self.routes_table.setCellWidget(row, 5, actions_widget)

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
        self.setGeometry(100, 100, 1200, 800)
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
            view_routes_action.triggered.connect(lambda: self.change_page("routes"))
            routes_menu.addAction(view_routes_action)
            
            manage_routes_action = QAction("Gerenciar Rotas", self)
            manage_routes_action.triggered.connect(self.manage_routes)
            routes_menu.addAction(manage_routes_action)
            
            assign_routes_action = QAction("Atribuir Rotas", self)
            assign_routes_action.triggered.connect(self.assign_routes)
            routes_menu.addAction(assign_routes_action)

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
            view_all_deliveries_action.triggered.connect(lambda: self.change_page("deliveries"))
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
            system_settings_action.triggered.connect(lambda: self.change_page("settings"))
            settings_menu.addAction(system_settings_action)
            
            theme_action = QAction("Alternar Tema", self)
            theme_action.triggered.connect(self._toggle_theme)
            settings_menu.addAction(theme_action)

        else:
            # Menu Rotas (Entregador)
            routes_menu = menubar.addMenu("Minhas Rotas")
            
            view_my_routes_action = QAction("Visualizar Rotas", self)
            view_my_routes_action.triggered.connect(lambda: self.change_page("routes"))
            routes_menu.addAction(view_my_routes_action)
            
            route_history_action = QAction("Histórico de Rotas", self)
            route_history_action.triggered.connect(self.view_route_history)
            routes_menu.addAction(route_history_action)

            # Menu Entregas (Entregador)
            deliveries_menu = menubar.addMenu("Minhas Entregas")
            
            view_my_deliveries_action = QAction("Entregas do Dia", self)
            view_my_deliveries_action.triggered.connect(lambda: self.change_page("deliveries"))
            deliveries_menu.addAction(view_my_deliveries_action)
            
            update_status_action = QAction("Atualizar Status", self)
            update_status_action.triggered.connect(self.update_delivery_status)
            deliveries_menu.addAction(update_status_action)

            # Menu Perfil (Entregador)
            profile_menu = menubar.addMenu("Perfil")
            
            view_profile_action = QAction("Meu Perfil", self)
            view_profile_action.triggered.connect(lambda: self.change_page("profile"))
            profile_menu.addAction(view_profile_action)
            
            performance_action = QAction("Meu Desempenho", self)
            performance_action.triggered.connect(self.view_my_performance)
            profile_menu.addAction(performance_action)

        # Menu Sair (Comum para ambos)
        logout_action = QAction("Sair", self)
        logout_action.triggered.connect(self.logout)
        menubar.addAction(logout_action)

    def change_page(self, page_name):
        page_map = {
            "routes": 0,
            "deliveries": 1,
            "reports": 2,
            "settings": 3,
            "profile": 4
        }
        
        if page_name in page_map:
            self.stacked_widget.setCurrentIndex(page_map[page_name])

    def setup_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Pronto")

    def manage_routes(self):
        dialog = ManageRoutesDialog(self)
        dialog.exec_()

    def add_delivery(self):
        dialog = AddDeliveryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.routes_page.refresh_routes()

    def generate_daily_report(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Relatório Diário")
        layout = QVBoxLayout(dialog)
        
        # Seleção de data
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        layout.addWidget(QLabel("Selecione a data:"))
        layout.addWidget(date_edit)
        
        # Tabela de resultados
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Rota", "Total Entregas", "Entregues", "Pendentes"])
        layout.addWidget(table)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        def load_report():
            selected_date = date_edit.date().toString("yyyy-MM-dd")
            conn = create_connection()
            if not conn:
                return
            
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            r.nome as rota,
                            COUNT(e.id) as total_entregas,
                            SUM(CASE WHEN e.status = 'entregue' THEN 1 ELSE 0 END) as entregues,
                            SUM(CASE WHEN e.status IN ('pendente', 'em_andamento') THEN 1 ELSE 0 END) as pendentes
                        FROM rotas r
                        LEFT JOIN entregas e ON r.id = e.rota_id
                        WHERE DATE(r.data_criacao) = %s
                        GROUP BY r.id, r.nome
                    """, (selected_date,))
                    
                    resultados = cursor.fetchall()
                    table.setRowCount(len(resultados))
                    
                    for i, row in enumerate(resultados):
                        table.setItem(i, 0, QTableWidgetItem(row['rota']))
                        table.setItem(i, 1, QTableWidgetItem(str(row['total_entregas'])))
                        table.setItem(i, 2, QTableWidgetItem(str(row['entregues'])))
                        table.setItem(i, 3, QTableWidgetItem(str(row['pendentes'])))
            finally:
                conn.close()
        
        date_edit.dateChanged.connect(load_report)
        load_report()
        
        dialog.exec_()

    def generate_monthly_report(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Relatório Mensal")
        layout = QVBoxLayout(dialog)
        
        # Seleção de mês/ano
        month_combo = QComboBox()
        for i in range(1, 13):
            month_combo.addItem(QDate(2000, i, 1).toString("MMMM"), i)
        month_combo.setCurrentIndex(QDate.currentDate().month() - 1)
        
        year_spin = QSpinBox()
        year_spin.setRange(2000, 2100)
        year_spin.setValue(QDate.currentDate().year())
        
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Mês:"))
        date_layout.addWidget(month_combo)
        date_layout.addWidget(QLabel("Ano:"))
        date_layout.addWidget(year_spin)
        layout.addLayout(date_layout)
        
        # Tabela de resultados
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Data", "Total Rotas", "Total Entregas", 
            "Entregues", "Taxa de Entrega"
        ])
        layout.addWidget(table)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        def load_report():
            month = month_combo.currentData()
            year = year_spin.value()
            
            conn = create_connection()
            if not conn:
                return
            
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            DATE(r.data_criacao) as data,
                            COUNT(DISTINCT r.id) as total_rotas,
                            COUNT(e.id) as total_entregas,
                            SUM(CASE WHEN e.status = 'entregue' THEN 1 ELSE 0 END) as entregues
                        FROM rotas r
                        LEFT JOIN entregas e ON r.id = e.rota_id
                        WHERE MONTH(r.data_criacao) = %s AND YEAR(r.data_criacao) = %s
                        GROUP BY DATE(r.data_criacao)
                        ORDER BY data
                    """, (month, year))
                    
                    resultados = cursor.fetchall()
                    table.setRowCount(len(resultados))
                    
                    for i, row in enumerate(resultados):
                        table.setItem(i, 0, QTableWidgetItem(str(row['data'])))
                        table.setItem(i, 1, QTableWidgetItem(str(row['total_rotas'])))
                        table.setItem(i, 2, QTableWidgetItem(str(row['total_entregas'])))
                        table.setItem(i, 3, QTableWidgetItem(str(row['entregues'])))
                        
                        # Calcular taxa de entrega
                        taxa = 0
                        if row['total_entregas'] > 0:
                            taxa = (row['entregues'] / row['total_entregas']) * 100
                        table.setItem(i, 4, QTableWidgetItem(f"{taxa:.1f}%"))
            finally:
                conn.close()
        
        month_combo.currentIndexChanged.connect(load_report)
        year_spin.valueChanged.connect(load_report)
        load_report()
        
        dialog.exec_()

    def _apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(get_dark_theme_styles())
        else:
            self.setStyleSheet(get_light_theme_styles())

    def _toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
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
        # Será implementado posteriormente
        pass

    def assign_routes(self):
        # Será implementado posteriormente
        pass

    def view_courier_performance(self):
        # Será implementado posteriormente
        pass

    def manage_deliveries(self):
        # Será implementado posteriormente
        pass

    def generate_performance_report(self):
        # Será implementado posteriormente
        pass

    # Métodos para Entregador
    def view_route_history(self):
        # Será implementado posteriormente
        pass

    def update_delivery_status(self):
        # Será implementado posteriormente
        pass

    def view_my_performance(self):
        # Será implementado posteriormente
        pass 