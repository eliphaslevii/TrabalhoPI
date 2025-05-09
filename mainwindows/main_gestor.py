import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QListWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Página de visualização de rotas
class VisualizarRotasPage(QWidget):
    def __init__(self, mostrar_mapa_callback):
        super().__init__()
        layout = QVBoxLayout()

        self.lista_rotas = QListWidget()
        self.lista_rotas.addItems(["Rota 1 - 01/05", "Rota 2 - 02/05", "Rota 3 - 03/05"])
        layout.addWidget(QLabel("📋 Rotas Disponíveis:"))
        layout.addWidget(self.lista_rotas)

        botao_ver_mapa = QPushButton("Ver Rota no Mapa")
        botao_ver_mapa.clicked.connect(lambda: mostrar_mapa_callback(self.lista_rotas.currentItem()))
        layout.addWidget(botao_ver_mapa)

        self.setLayout(layout)

# Página do mapa (rota)
class MapaRotaPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://www.openstreetmap.org"))  # Exemplo temporário
        layout.addWidget(QLabel("🗺️ Mapa da Rota"))
        layout.addWidget(self.webview)
        self.setLayout(layout)

# Janela principal do Gestor
class GestorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Gestor")
        self.setGeometry(100, 100, 1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.visualizar_rotas_page = VisualizarRotasPage(self.mostrar_mapa_rota)
        self.mapa_rota_page = MapaRotaPage()

        self.stack.addWidget(self.visualizar_rotas_page)  # index 0
        self.stack.addWidget(self.mapa_rota_page)         # index 1

        self.stack.setCurrentIndex(0)

    def mostrar_mapa_rota(self, item_selecionado):
        if item_selecionado:
            rota_nome = item_selecionado.text()
            print(f"Gestor selecionou: {rota_nome}")
            self.stack.setCurrentIndex(1)
        else:
            print("Nenhuma rota selecionada.")

# Execução
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GestorWindow()
    window.show()
    sys.exit(app.exec_())
