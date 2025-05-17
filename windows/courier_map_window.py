from PyQt5.QtWidgets import QDialog

class CourierMapWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mapa de Entregas")
        self.setFixedSize(400, 400) 