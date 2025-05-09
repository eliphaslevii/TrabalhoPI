from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MainGestor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Gestor")
        self.setGeometry(200, 200, 800, 600)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Bem-vindo, Gestor!")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.webview = QWebEngineView()
        # Exemplo: abre uma página qualquer — você vai trocar depois para seu mapa local
        self.webview.setUrl(QUrl("https://www.openstreetmap.org"))

        layout.addWidget(label)
        layout.addWidget(self.webview)
        self.setLayout(layout)
