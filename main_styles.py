def get_dark_theme_styles():
    """Retorna uma string QSS para um tema escuro moderno e aprimorado."""
    return """
        QWidget {
            background-color: #2b2b2b;
            color: #f0f0f0;
            font-family: "Segoe UI", "Arial";
            font-size: 10pt;
        }
        QMainWindow {
            background-color: #2b2b2b;
        }
        QMenuBar {
            background-color: #3c3c3c;
            color: #f0f0f0;
        }
        QMenuBar::item:selected {
            background-color: #555;
        }
        QMenu {
            background-color: #3c3c3c;
            border: 1px solid #555;
        }
        QMenu::item:selected {
            background-color: #0078d7;
            color: #ffffff;
        }
        QTableWidget {
            background-color: #3c3c3c;
            border: 1px solid #555;
            gridline-color: #555;
            alternate-background-color: #424242; /* Efeito Zebra */
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:hover {
            background-color: #4f4f4f;
        }
        QHeaderView::section {
            background-color: #555;
            color: #f0f0f0;
            padding: 4px;
            border: 1px solid #3c3c3c;
            font-weight: bold;
        }
        QPushButton {
            background-color: #0078d7;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004578;
        }
        QLineEdit, QSpinBox, QComboBox {
            background-color: #3c3c3c;
            border: 1px solid #555;
            padding: 5px;
            border-radius: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QStatusBar {
            background-color: #3c3c3c;
        }
        QLabel#welcome_label {
            font-size: 16pt;
            font-weight: bold;
            color: #f0f0f0;
        }
    """

def get_light_theme_styles():
    """Retorna uma string QSS para um tema claro moderno e aprimorado."""
    return """
        QWidget {
            background-color: #f0f0f0;
            color: #1e1e1e;
            font-family: "Segoe UI", "Arial";
            font-size: 10pt;
        }
        QMainWindow {
            background-color: #f0f0f0;
        }
        QMenuBar {
            background-color: #e8e8e8;
            color: #1e1e1e;
        }
        QMenuBar::item:selected {
            background-color: #dcdcdc;
        }
        QMenu {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
        }
        QMenu::item:selected {
            background-color: #0078d7;
            color: #ffffff;
        }
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            gridline-color: #e8e8e8;
            alternate-background-color: #f5f5f5; /* Efeito Zebra */
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:hover {
            background-color: #e0e0e0;
        }
        QHeaderView::section {
            background-color: #e8e8e8;
            color: #1e1e1e;
            padding: 4px;
            border: 1px solid #dcdcdc;
            font-weight: bold;
        }
        QPushButton {
            background-color: #0078d7;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004578;
        }
        QLineEdit, QSpinBox, QComboBox {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            padding: 5px;
            border-radius: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QStatusBar {
            background-color: #e8e8e8;
        }
        QLabel#welcome_label {
            font-size: 16pt;
            font-weight: bold;
            color: #1e1e1e;
        }
    """ 