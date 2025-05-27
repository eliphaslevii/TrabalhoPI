from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox, QPushButton,
    QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QSpinBox, QTextEdit, QDialogButtonBox, QStackedWidget,
    QGroupBox, QGridLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QSettings, QDate, QSize
from PyQt5.QtGui import QIcon, QFont
from auth_service import AuthService
from main_styles import get_dark_theme_styles, get_light_theme_styles
from database import create_connection
from map_widget import MapWidget
from PyQt5.QtWidgets import QApplication
from windows import new_delivery_form
from windows.new_delivery_form import DeliveryForm
from windows.new_route_form import RotaForm

class MainWindow(QMainWindow):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.settings = QSettings("PI", "App")
        self.is_dark_theme = self.settings.value("dark_theme", False, type=bool)
        self.setup_ui()
        self._apply_theme()
        self.load_routes_from_db()

    def setup_ui(self):
        self.setWindowTitle("Sistema de Gerenciamento de Rotas")
        self.setGeometry(100, 100, 900, 600)
        self.setup_menu_bar()
        self.setup_status_bar()

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 0, 20, 20)
        main_layout.setSpacing(0)

        # Top Grid Layout
        top_grid = QGridLayout()
        top_grid.setContentsMargins(0, 0, 0, 0)
        top_grid.setColumnStretch(0, 1)
        top_grid.setColumnStretch(1, 2)
        top_grid.setColumnStretch(2, 1)

        welcome_label = QLabel(f"Bem-vindo, {self.username}!")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setAlignment(Qt.AlignCenter)
        font = welcome_label.font()
        font.setPointSize(18)
        font.setBold(True)
        welcome_label.setFont(font)
        top_grid.addWidget(welcome_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)

        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(30, 30)
        self.theme_button.setObjectName("theme_button")
        self.theme_button.clicked.connect(self._toggle_theme)
        self._update_theme_button_icon()
        top_grid.addWidget(self.theme_button, 0, 2, alignment=Qt.AlignRight)

        main_layout.addLayout(top_grid)

        # Tabela de rotas
        self.routes_table = QTableWidget()
        self.routes_table.setColumnCount(6)
        self.routes_table.setHorizontalHeaderLabels([
            "Marcar", "Nome", "Data", "Status", "Entregador", "Visualizar Rota"
        ])
        self.routes_table.horizontalHeader().setStretchLastSection(True)
        self.routes_table.verticalHeader().setVisible(False)
        self.routes_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.routes_table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.routes_table)

        # Botões de ação
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)

        self.add_route_btn = QPushButton("Nova Rota")
        self.add_route_btn.clicked.connect(self.show_new_route)
        buttons_layout.addWidget(self.add_route_btn)

        self.add_delivery_btn = QPushButton("Atribuir Endereços")
        self.add_delivery_btn.clicked.connect(self.show_new_delivery)
        buttons_layout.addWidget(self.add_delivery_btn)

        self.delete_route_btn = QPushButton("Excluir Rota(s)")
        self.delete_route_btn.clicked.connect(self.delete_selected_routes)
        buttons_layout.addWidget(self.delete_route_btn)

        self.refresh_btn = QPushButton("Atualizar")
        self.refresh_btn.clicked.connect(self.load_routes_from_db)
        buttons_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(buttons_layout)

    def setup_menu_bar(self):
        menubar = self.menuBar()
        menubar.clear()

        if self.username == "admin":
            settings_menu = menubar.addMenu("Configurações")

            system_settings_action = QAction("Configuração de Sistema", self)
            system_settings_action.triggered.connect(self.show_system_settings)
            settings_menu.addAction(system_settings_action)

            exit_action = QAction("Sair", self)
            exit_action.triggered.connect(self.logout)
            settings_menu.addAction(exit_action)
        else:
            from windows import MyDeliveriesWindow, MyPerformanceWindow

            entregas_menu = menubar.addMenu("Minhas Entregas")
            entregas_action = QAction("Abrir", self)
            entregas_action.triggered.connect(lambda: self._abrir_janela_dialog(MyDeliveriesWindow, "Minhas Entregas"))
            entregas_menu.addAction(entregas_action)

            desempenho_menu = menubar.addMenu("Meu Desempenho")
            desempenho_action = QAction("Abrir", self)
            desempenho_action.triggered.connect(lambda: self._abrir_janela_dialog(MyPerformanceWindow, "Meu Desempenho"))
            desempenho_menu.addAction(desempenho_action)

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
            moon_path = "img/moon.png"
            sun_path = "img/sun.png"
            icon_path = moon_path if not self.is_dark_theme else sun_path
            icon = QIcon(icon_path)
            if not icon.isNull():
                self.theme_button.setIcon(icon)
                self.theme_button.setIconSize(QSize(20, 20))
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
        self.new_route_win = RotaForm()
        self.new_route_win.show()

    def show_new_delivery(self):
        self.new_route_win = DeliveryForm()
        self.new_route_win.show()

    def show_update_routes(self):
        self.load_routes_from_db()

    def show_system_settings(self):
        from windows import SystemSettingsWindow
        dialog = SystemSettingsWindow(self)
        dialog.exec_()

    def _abrir_janela_dialog(self, DialogClass, titulo):
        dialog = DialogClass(self)
        dialog.setWindowTitle(titulo)
        dialog.exec_()

    def load_routes_from_db(self):
        """
        Busca dados da tabela 'rotas' no banco e atualiza a QTableWidget,
        incluindo o nome do entregador via join na tabela users.
        """
        try:
            conn = create_connection()
            if not conn:
                QMessageBox.warning(self, "Erro", "Falha ao conectar ao banco de dados.")
                return

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT r.id, r.nome, r.data_criacao, r.status, u.nome AS entregador_nome
                    FROM rotas r
                    LEFT JOIN users u ON r.entregador_id = u.id
                    ORDER BY r.data_criacao DESC
                """)
                rows = cursor.fetchall()

                self.routes_table.setRowCount(0)

                for row_index, row in enumerate(rows):
                    self.routes_table.insertRow(row_index)

                    # Coluna 0: Checkbox
                    checkbox = QCheckBox()
                    checkbox.setToolTip("Marcar rota")
                    checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")  # Centralizar checkbox
                    self.routes_table.setCellWidget(row_index, 0, checkbox)

                    # Coluna 1: Nome da rota
                    nome_item = QTableWidgetItem(row['nome'])
                    nome_item.setFlags(nome_item.flags() ^ Qt.ItemIsEditable)
                    self.routes_table.setItem(row_index, 1, nome_item)

                    # Coluna 2: Data formatada
                    data_str = row['data_criacao'].strftime('%d/%m/%Y %H:%M:%S') if row['data_criacao'] else ''
                    data_item = QTableWidgetItem(data_str)
                    data_item.setFlags(data_item.flags() ^ Qt.ItemIsEditable)
                    self.routes_table.setItem(row_index, 2, data_item)

                    # Coluna 3: Status
                    status_item = QTableWidgetItem(row['status'])
                    status_item.setFlags(status_item.flags() ^ Qt.ItemIsEditable)
                    self.routes_table.setItem(row_index, 3, status_item)

                    # Coluna 4: Nome do entregador ou 'Não atribuído'
                    entregador_nome = row['entregador_nome'] if row['entregador_nome'] else 'Não atribuído'
                    entregador_item = QTableWidgetItem(entregador_nome)
                    entregador_item.setFlags(entregador_item.flags() ^ Qt.ItemIsEditable)
                    self.routes_table.setItem(row_index, 4, entregador_item)

                    # Coluna 5: Botão "Visualizar"
                    btn = QPushButton("Visualizar")
                    btn.setProperty("route_id", row['id'])
                    btn.clicked.connect(self.visualizar_rota)
                    self.routes_table.setCellWidget(row_index, 5, btn)

            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Erro ao carregar rotas", f"Não foi possível carregar as rotas:\n{e}")

    def visualizar_rota(self):
        sender = self.sender()
        if sender:
            route_id = sender.property("route_id")
            if route_id:
                # Abrir janela com detalhes da rota
                QMessageBox.information(self, "Visualizar Rota", f"Visualizando detalhes da rota ID: {route_id}")
                # Aqui você pode abrir a janela real de visualização da rota

    def delete_selected_routes(self):
        # Pega os ids das rotas marcadas para exclusão
        selected_route_ids = []
        for row in range(self.routes_table.rowCount()):
            checkbox = self.routes_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                route_name_item = self.routes_table.item(row, 1)
                route_name = route_name_item.text() if route_name_item else ''
                # Para obter o ID da rota, podemos recuperar via botão "Visualizar" que tem propriedade "route_id"
                view_btn = self.routes_table.cellWidget(row, 5)
                if view_btn:
                    route_id = view_btn.property("route_id")
                    if route_id:
                        selected_route_ids.append(route_id)

        if not selected_route_ids:
            QMessageBox.information(self, "Excluir Rotas", "Nenhuma rota selecionada para exclusão.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir {len(selected_route_ids)} rota(s) selecionada(s) e seus endereços vinculados?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            conn = create_connection()
            if not conn:
                QMessageBox.warning(self, "Erro", "Falha ao conectar ao banco de dados.")
                return

            with conn.cursor() as cursor:
                # Desabilitar FK temporariamente, se necessário
                # cursor.execute("SET FOREIGN_KEY_CHECKS=0")  # MySQL ex.

                # Apagar endereços vinculados às rotas selecionadas
                # Supondo tabela 'enderecos' com coluna 'rota_id'
                query_del_enderecos = "DELETE FROM entregas WHERE rota_id IN %s"
                cursor.execute(query_del_enderecos, (tuple(selected_route_ids),))

                # Apagar rotas selecionadas
                query_del_rotas = "DELETE FROM rotas WHERE id IN %s"
                cursor.execute(query_del_rotas, (tuple(selected_route_ids),))

                conn.commit()
                QMessageBox.information(self, "Sucesso", f"{len(selected_route_ids)} rota(s) excluída(s) com sucesso.")
                self.load_routes_from_db()

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao excluir rotas:\n{e}")

        finally:
            if conn:
                conn.close()
