import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    print("Welcome to the StudioHead Simulation Engine")
    print("Initializing GUI...")
    
    app = QApplication(sys.argv)
    
    # Optional: Set global styles of the app here if needed
    app.setStyle("Fusion") 
    
    window = MainWindow()
    # Window show logic is handled in MainWindow.__init__ (showFullScreen), but usually good to call show() here to be explicit
    # window.show() 
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
