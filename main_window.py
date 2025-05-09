from PyQt5.QtWidgets import (
    QMainWindow, QMenuBar, QAction, QStackedWidget, QWidget, QVBoxLayout, QApplication
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class MapaPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
       # self.webview.load(QUrl(""))
        layout.addWidget(self.webview)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("admin")

        # Menu
        menubar = self.menuBar()

        menu_mapa = QAction("Mapa", self)
        menu_pedidos = QAction("Pedidos", self)
        menu_entregadores = QAction("Entregadores", self)
        menu_sair = QAction("Sair", self)

        menubar.addAction(menu_mapa)
        menubar.addAction(menu_pedidos)
        menubar.addAction(menu_entregadores)
        menubar.addAction(menu_sair)

        # Stack de páginas
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instâncias das páginas
        self.mapa_page = MapaPage()
        self.pedidos_page = QWidget()  # você pode adicionar widgets depois
        self.entregadores_page = QWidget()

        self.stack.addWidget(self.mapa_page)          # índice 0
        self.stack.addWidget(self.pedidos_page)       # índice 1
        self.stack.addWidget(self.entregadores_page)  # índice 2

        # Conectar ações do menu
        menu_mapa.triggered.connect(lambda: self.exibir_tela("Mapa"))
        menu_pedidos.triggered.connect(lambda: self.exibir_tela("Pedidos"))
        menu_entregadores.triggered.connect(lambda: self.exibir_tela("Entregadores"))
        menu_sair.triggered.connect(self.close)

        # Mostra a tela inicial
        self.exibir_tela("Mapa")

    def exibir_tela(self, nome):
        if nome == "Mapa":
            self.stack.setCurrentIndex(0)
        elif nome == "Pedidos":
            self.stack.setCurrentIndex(1)
        elif nome == "Entregadores":
            self.stack.setCurrentIndex(2)

# Apenas executa se rodar direto este arquivo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
