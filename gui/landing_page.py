from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame, QSizePolicy, QSpacerItem, QApplication
)
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor
import os

class LandingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None
        self.logo_path = os.path.join(os.getcwd(), "assets", "LogoImage.png")
        self.load_background()
        self.init_ui()

    def load_background(self):
        if os.path.exists(self.logo_path):
            self.background_pixmap = QPixmap(self.logo_path)

    def paintEvent(self, event):
        if self.background_pixmap:
            painter = QPainter(self)
            # Scale to cover the window (KeepAspectRatioByExpanding)
            # This logic mimics CSS 'background-size: cover'
            scaled = self.background_pixmap.scaled(
                self.size(), 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Calculate center position to crop if necessary
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            
            painter.drawPixmap(x, y, scaled)
        else:
            # Fallback background
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor("#1e1e1e"))

    def init_ui(self):
        # Master Layout (Vertical: Header -> Body)
        master_layout = QVBoxLayout(self)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)

        # --- Top Header Bar ---
        header_frame = QFrame()
        header_frame.setFixedHeight(40) # Thin header
        header_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); border-bottom: 1px solid #444;")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        # Version Label (Centered)
        version_label = QLabel("v0.1.0-alpha")
        version_label.setStyleSheet("color: #aaa; font-size: 14px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addStretch()
        header_layout.addWidget(version_label)
        header_layout.addStretch()
        
        master_layout.addWidget(header_frame)

        # --- Body Area (Menu + Spacer) ---
        body_frame = QFrame()
        # Transparent body to let background show through
        body_frame.setStyleSheet("background-color: transparent;")
        body_layout = QHBoxLayout(body_frame)
        body_layout.setContentsMargins(50, 50, 50, 50) # Margins around the content
        body_layout.setSpacing(20)

        # --- Left Side: Menu Container ---
        menu_container = QFrame()
        menu_container.setObjectName("MenuContainer")
        # Slightly opaque background for readability
        menu_container.setStyleSheet("""
            QFrame#MenuContainer {
                background-color: rgba(20, 20, 20, 0.9);
                border: 1px solid #444;
                border-radius: 10px;
                min-width: 250px;
                max-width: 300px;
            }
            QPushButton {
                background-color: #333333;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 6px;
                text-align: center;
                padding: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                margin-bottom: 8px;
            }
            QPushButton:hover {
                background-color: #444444;
                border-color: #d0191d;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #d0191d;
                border-color: #d0191d;
            }
        """)
        
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(20, 30, 20, 30)
        menu_layout.setSpacing(10)
        
        # Menu Title
        menu_title = QLabel("MENU")
        menu_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_title.setStyleSheet("color: #888; font-weight: bold; letter-spacing: 2px; margin-bottom: 10px;")
        menu_layout.addWidget(menu_title)

        # Buttons
        buttons = [
            ("New Game", self.on_new_game),
            ("Load Game", self.on_load_game),
            ("Databases", self.on_databases),
            ("Database Editor", self.on_editor),
            ("Options", self.on_options),
            ("Credits", self.on_credits),
            ("Exit Game", self.on_exit_game),
        ]
        
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(slot)
            menu_layout.addWidget(btn)

        menu_layout.addStretch() # Push buttons up
        
        body_layout.addWidget(menu_container)
        
        # Spacer to push menu to the left (Right side is empty, showing background logo)
        body_layout.addStretch()

        master_layout.addWidget(body_frame)

    # --- Actions ---
    def on_new_game(self):
        print("New Game clicked")

    def on_load_game(self):
        print("Load Game clicked")
        
    def on_databases(self):
        print("Databases clicked")
        
    def on_editor(self):
        print("Editor clicked")
        
    def on_options(self):
        print("Options clicked")
        
    def on_credits(self):
        print("Credits clicked")

    def on_exit_game(self):
        QApplication.instance().quit()
