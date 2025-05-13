from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

class MapWidget(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 450)
        self.load_map()
        
    def load_map(self):
        # Caminho para o arquivo HTML do mapa
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(current_dir, "map.html")
        
        # Verificar se o arquivo existe
        if os.path.exists(map_path):
            self.load(QUrl.fromLocalFile(map_path))
        else:
            # Criar um mapa básico usando OpenStreetMap
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8" />
                <title>Mapa</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                <style>
                    body { margin: 0; padding: 0; }
                    #map { position: absolute; top: 0; bottom: 0; width: 100%; }
                </style>
            </head>
            <body>
                <div id="map"></div>
                <script>
                    var map = L.map('map').setView([-25.4284, -49.2733], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(map);
                </script>
            </body>
            </html>
            """
            self.setHtml(html)

class MapWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualização do Mapa")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        try:
            # Tentar criar o widget de mapa
            self.map_widget = MapWidget(self)
            layout.addWidget(self.map_widget)
        except Exception as e:
            # Em caso de erro, mostrar uma mensagem
            error_label = QLabel(f"Erro ao carregar o mapa: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)
