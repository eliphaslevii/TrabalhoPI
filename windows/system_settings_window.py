from PyQt5.QtWidgets import QDialog
 
class SystemSettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuração de Sistema")
        self.setFixedSize(400, 400) 