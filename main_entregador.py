from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainEntregador(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Entregador")
        self.setGeometry(200, 200, 400, 300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Bem-vindo, Entregador!")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        info = QLabel("Aqui você verá suas rotas, pedidos e atualizações de entrega.")
        info.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(info)
        self.setLayout(layout)
