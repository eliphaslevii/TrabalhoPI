from PyQt5.QtWidgets import QDialog
 
class MyDeliveriesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Minhas Entregas")
        self.setFixedSize(400, 400) 