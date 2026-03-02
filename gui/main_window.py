from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from gui.landing_page import LandingPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudioHead Simulation Engine")
        
        # Set Full Screen
        self.showFullScreen()
        
        # Central widget is a StackedWidget to allow switching between views (Landing, New Game, Editor, etc.)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Initialize Landing Page
        self.landing_page = LandingPage(self)
        self.central_widget.addWidget(self.landing_page)
        
        # Set Current View
        self.central_widget.setCurrentWidget(self.landing_page)

    def keyPressEvent(self, event):
        # Escape to close for now (useful during dev/testing)
        if event.key() == Qt.Key.Key_Escape:
            self.close()
