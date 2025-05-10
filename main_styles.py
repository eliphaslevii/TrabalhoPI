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
    """ 