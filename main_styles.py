def get_dark_theme_styles():
    return """
        QMainWindow {
            background-color: #2b2b2b;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QLabel {
            color: #ffffff;
        }
        
        QLabel#welcome_label {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            padding: 20px;
        }
        
        QMenuBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-bottom: 1px solid #3d3d3d;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 8px 12px;
            margin: 2px 2px;
        }
        
        QMenuBar::item:selected {
            background-color: #3d3d3d;
            border-radius: 4px;
        }
        
        QMenuBar::item:pressed {
            background-color: #4d4d4d;
        }
        
        QStatusBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-top: 1px solid #3d3d3d;
        }
        
        QStatusBar::item {
            border: none;
        }

        QPushButton {
            background-color: #0d47a1;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #1565c0;
        }

        QPushButton:pressed {
            background-color: #0a3d91;
        }

        QPushButton:disabled {
            background-color: #424242;
            color: #757575;
        }

        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {
            background-color: #424242;
            color: white;
            border: 1px solid #616161;
            border-radius: 4px;
            padding: 6px;
        }

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
            border: 1px solid #0d47a1;
        }

        QTableWidget {
            background-color: #424242;
            color: white;
            gridline-color: #616161;
            border: 1px solid #616161;
            border-radius: 4px;
        }

        QTableWidget::item {
            padding: 6px;
        }

        QTableWidget::item:selected {
            background-color: #0d47a1;
        }

        QHeaderView::section {
            background-color: #2b2b2b;
            color: white;
            padding: 6px;
            border: 1px solid #616161;
        }

        QDialog {
            background-color: #2b2b2b;
        }

        QGroupBox {
            border: 1px solid #616161;
            border-radius: 4px;
            margin-top: 12px;
            padding-top: 12px;
        }

        QGroupBox::title {
            color: white;
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px;
        }

        #theme_button {
            border: none;
            background-color: transparent;
            border-radius: 12px;
        }

        #theme_button:hover {
            background-color: rgba(128, 128, 128, 0.15);
        }

        #theme_button:pressed {
            background-color: rgba(128, 128, 128, 0.25);
        }
    """

def get_light_theme_styles():
    return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QWidget {
            background-color: #f5f5f5;
            color: #000000;
        }
        
        QLabel {
            color: #000000;
        }
        
        QLabel#welcome_label {
            font-size: 24px;
            font-weight: bold;
            color: #000000;
            padding: 20px;
        }
        
        QMenuBar {
            background-color: #f5f5f5;
            color: #000000;
            border-bottom: 1px solid #e0e0e0;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 8px 12px;
            margin: 2px 2px;
        }
        
        QMenuBar::item:selected {
            background-color: #e0e0e0;
            border-radius: 4px;
        }
        
        QMenuBar::item:pressed {
            background-color: #d0d0d0;
        }
        
        QStatusBar {
            background-color: #f5f5f5;
            color: #000000;
            border-top: 1px solid #e0e0e0;
        }
        
        QStatusBar::item {
            border: none;
        }

        QPushButton {
            background-color: #1976d2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #1e88e5;
        }

        QPushButton:pressed {
            background-color: #1565c0;
        }

        QPushButton:disabled {
            background-color: #bdbdbd;
            color: #757575;
        }

        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {
            background-color: white;
            color: black;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 6px;
        }

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
            border: 1px solid #1976d2;
        }

        QTableWidget {
            background-color: white;
            color: black;
            gridline-color: #e0e0e0;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }

        QTableWidget::item {
            padding: 6px;
        }

        QTableWidget::item:selected {
            background-color: #1976d2;
            color: white;
        }

        QHeaderView::section {
            background-color: #f5f5f5;
            color: black;
            padding: 6px;
            border: 1px solid #e0e0e0;
        }

        QDialog {
            background-color: #f5f5f5;
        }

        QGroupBox {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            margin-top: 12px;
            padding-top: 12px;
        }

        QGroupBox::title {
            color: black;
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px;
        }

        #theme_button {
            border: none;
            background-color: transparent;
            border-radius: 12px;
        }

        #theme_button:hover {
            background-color: rgba(128, 128, 128, 0.15);
        }

        #theme_button:pressed {
            background-color: rgba(128, 128, 128, 0.25);
        }
    """ 