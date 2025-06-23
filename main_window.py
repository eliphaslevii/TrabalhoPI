from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QAction, QMessageBox, QPushButton,
    QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QSpinBox, QTextEdit, QDialogButtonBox, QStackedWidget,
    QGroupBox, QGridLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QSettings, QDate, QSize
from PyQt5.QtGui import QIcon, QFont, QColor
from auth_service import AuthService
from main_styles import get_dark_theme_styles, get_light_theme_styles
from database import create_connection
from map_widget import MapWidget
from PyQt5.QtWidgets import QApplication
from windows import new_delivery_form
from windows.new_delivery_form import DeliveryForm
from windows.new_route_form import RotaForm
from windows.map_gui import MapaRota
from windows.management_window import ManagementWindow
from windows.history_window import HistoryWindow

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
        self.routes_table.setColumnCount(8) # Adicionada uma coluna para o status de problema
        self.routes_table.setHorizontalHeaderLabels([
            "Marcar", "Nome", "Data", "Status", "Problema", "Veículos", "Visualizar", "Ação"
        ])
        self.routes_table.horizontalHeader().setStretchLastSection(True)
        self.routes_table.verticalHeader().setVisible(False)
        self.routes_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.routes_table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.routes_table)

        # Botões de ação
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)

        # Apenas admin pode ver os botões de gerenciamento de rotas
        if self.username == 'admin':
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

        # Menu de Histórico (visível para todos)
        history_menu = menubar.addMenu("Histórico")
        history_action = QAction("Ver Rotas Concluídas", self)
        history_action.triggered.connect(self.show_history_window)
        history_menu.addAction(history_action)

        if self.username == "admin":
            # Adiciona Gerenciamento direto na barra
            management_action = QAction("Gerenciamento", self)
            management_action.triggered.connect(self.show_management_window)
            menubar.addAction(management_action)

            # Adiciona Sair direto na barra
            exit_action = QAction("Sair", self)
            exit_action.triggered.connect(self.logout)
            menubar.addAction(exit_action)
        else:
            # Para entregadores, apenas o menu de configurações com a opção de sair
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

    def iniciar_rota(self):
        """Muda o status de uma rota para 'em andamento'."""
        sender = self.sender()
        if not sender:
            return

        route_id = sender.property("route_id")
        route_name = sender.property("route_name")

        reply = QMessageBox.question(self, 'Confirmar Início',
                                     f"Tem certeza que deseja iniciar a rota '{route_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE rotas SET status = 'em_andamento' WHERE id = %s", (route_id,))
                conn.commit()
                QMessageBox.information(self, "Sucesso", f"Rota '{route_name}' iniciada.")
                self.load_routes_from_db()  # Recarrega a lista
            except Exception as e:
                if conn: conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao iniciar rota: {e}")
            finally:
                if conn: conn.close()

    def relatar_problema(self):
        """Alterna o status de problema de uma rota."""
        sender = self.sender()
        if not sender:
            return

        route_id = sender.property("route_id")
        route_name = sender.property("route_name")
        current_status = sender.property("problema_status")
        
        novo_status = not current_status
        acao = "relatar" if novo_status else "resolver"
        
        reply = QMessageBox.question(self, f'Confirmar Ação',
                                     f"Tem certeza que deseja {acao} um problema para a rota '{route_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE rotas SET problema = %s WHERE id = %s", (novo_status, route_id))
                conn.commit()
                QMessageBox.information(self, "Sucesso", f"Problema {acao} com sucesso.")
                self.load_routes_from_db()
            except Exception as e:
                if conn: conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao {acao} problema: {e}")
            finally:
                if conn: conn.close()

    def finalizar_rota(self):
        """Marca uma rota e todas as suas entregas como concluídas."""
        sender = self.sender()
        if not sender:
            return

        route_id = sender.property("route_id")
        route_name = sender.property("route_name")

        reply = QMessageBox.question(self, 'Confirmar Finalização',
                                     f"Tem certeza que deseja finalizar a rota '{route_name}'?\n"
                                     "Esta ação não pode ser desfeita.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    # Atualiza o status da rota
                    cursor.execute("UPDATE rotas SET status = 'concluida' WHERE id = %s", (route_id,))
                    # Atualiza o status de todas as entregas associadas
                    cursor.execute("UPDATE entregas SET status = 'entregue' WHERE rota_id = %s", (route_id,))
                conn.commit()
                QMessageBox.information(self, "Sucesso", f"Rota '{route_name}' finalizada com sucesso.")
                self.load_routes_from_db() # Recarrega a lista
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao finalizar rota: {e}")
            finally:
                if conn: conn.close()

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

    def show_history_window(self):
        self.history_win = HistoryWindow(self.username)
        self.history_win.show()

    def show_management_window(self):
        from windows.management_window import ManagementWindow
        # Usamos um atributo da instância para manter a janela viva
        self.management_win = ManagementWindow()
        self.management_win.show()

    def _abrir_janela_dialog(self, DialogClass, titulo):
        dialog = DialogClass(self)
        dialog.setWindowTitle(titulo)
        dialog.exec_()

    def load_routes_from_db(self):
        conn = create_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                # Query base para todas as rotas
                if self.username == 'admin':
                    # Admin vê todas as rotas
                    query = """
                        SELECT r.id, r.nome, r.data_criacao, r.status, r.problema
                        FROM rotas r
                        WHERE r.status != 'concluida' 
                        ORDER BY r.data_criacao DESC
                    """
                    params = []
                else:
                    # Entregadores veem apenas rotas onde são motoristas de algum veículo
                    query = """
                        SELECT DISTINCT r.id, r.nome, r.data_criacao, r.status, r.problema
                        FROM rotas r
                        JOIN rota_veiculos rv ON r.id = rv.rota_id
                        JOIN veiculos v ON rv.veiculo_id = v.id
                        JOIN users u ON v.entregador_id = u.id
                        WHERE r.status != 'concluida' 
                        AND u.nome = %s
                        ORDER BY r.data_criacao DESC
                    """
                    params = [self.username]
                
                cursor.execute(query, params)
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

                    # Coluna 4: Problema
                    problema_item = QTableWidgetItem("Sim" if row['problema'] else "Não")
                    problema_item.setFlags(problema_item.flags() ^ Qt.ItemIsEditable)
                    problema_item.setTextAlignment(Qt.AlignCenter)
                    self.routes_table.setItem(row_index, 4, problema_item)

                    # Coluna 5: Veículos associados
                    veiculos_info = self.get_veiculos_rota(row['id'])
                    veiculos_item = QTableWidgetItem(veiculos_info)
                    veiculos_item.setFlags(veiculos_item.flags() ^ Qt.ItemIsEditable)
                    self.routes_table.setItem(row_index, 5, veiculos_item)

                    # Coluna 6: Botão "Visualizar"
                    view_btn = QPushButton("Visualizar")
                    view_btn.setProperty("route_id", row['id'])
                    view_btn.clicked.connect(self.visualizar_rota)
                    self.routes_table.setCellWidget(row_index, 6, view_btn)

                    # Coluna 7: Layout para botões de ação
                    action_widget = QWidget()
                    action_layout = QHBoxLayout(action_widget)
                    action_layout.setContentsMargins(0, 0, 0, 0)
                    action_layout.setSpacing(5)

                    if row['status'] == 'pendente':
                        action_btn = QPushButton("Iniciar")
                        action_btn.clicked.connect(self.iniciar_rota)
                        action_btn.setProperty("route_id", row['id'])
                        action_btn.setProperty("route_name", row['nome'])
                        action_layout.addWidget(action_btn)

                    elif row['status'] == 'em_andamento':
                        finalizar_btn = QPushButton("Finalizar")
                        finalizar_btn.clicked.connect(self.finalizar_rota)
                        finalizar_btn.setProperty("route_id", row['id'])
                        finalizar_btn.setProperty("route_name", row['nome'])
                        action_layout.addWidget(finalizar_btn)
                        
                        problema_btn_text = "Resolver" if row['problema'] else "Problema"
                        problema_btn = QPushButton(problema_btn_text)
                        problema_btn.clicked.connect(self.relatar_problema)
                        problema_btn.setProperty("route_id", row['id'])
                        problema_btn.setProperty("route_name", row['nome'])
                        problema_btn.setProperty("problema_status", row['problema'])
                        action_layout.addWidget(problema_btn)

                    self.routes_table.setCellWidget(row_index, 7, action_widget)
                    
                    # Alerta visual para o admin
                    if self.username == 'admin' and row['problema']:
                        for col in range(self.routes_table.columnCount()):
                            item = self.routes_table.item(row_index, col)
                            if item:
                                item.setBackground(QColor(255, 102, 102, 100)) # Vermelho claro

        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao carregar rotas: {e}")
        finally:
            if conn: conn.close()

    def get_veiculos_rota(self, rota_id):
        """Obtém informações dos veículos associados a uma rota."""
        conn = create_connection()
        if not conn:
            return "N/A"
        
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT v.placa, u.nome as motorista
                    FROM rota_veiculos rv
                    JOIN veiculos v ON rv.veiculo_id = v.id
                    LEFT JOIN users u ON v.entregador_id = u.id
                    WHERE rv.rota_id = %s
                    ORDER BY v.placa
                """
                cursor.execute(sql, (rota_id,))
                veiculos = cursor.fetchall()
                
                if not veiculos:
                    return "Nenhum veículo"
                
                # Formatar lista de veículos
                veiculos_info = []
                for veiculo in veiculos:
                    motorista = veiculo['motorista'] or 'N/A'
                    veiculos_info.append(f"{veiculo['placa']} ({motorista})")
                
                return ", ".join(veiculos_info)
                
        except Exception as e:
            print(f"Erro ao obter veículos da rota: {e}")
            return "Erro"
        finally:
            if conn: conn.close()

    def visualizar_rota(self):
        sender = self.sender()
        if sender:
            route_id = sender.property("route_id")
            if route_id:
                self.mapa_rota = MapaRota(route_id)
                self.mapa_rota.show()
                #commit
    def delete_selected_routes(self):
        # Pega os ids das rotas marcadas para exclusão
        selected_route_ids = []
        for row in range(self.routes_table.rowCount()):
            checkbox = self.routes_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                route_name_item = self.routes_table.item(row, 1)
                route_name = route_name_item.text() if route_name_item else ''
                # Para obter o ID da rota, podemos recuperar via botão "Visualizar" que tem propriedade "route_id"
                view_btn = self.routes_table.cellWidget(row, 6)
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
