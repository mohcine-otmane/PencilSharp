#!/usr/bin/env python3
"""
PencilSharp Learning Platform
Main entry point for the application
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.controllers.app_controller import AppController
from src.views.main_window import MainWindow
from subjects_data import SUBJECTS

def main():
    # Initialize PyQt6 application (required for web content)
    qt_app = QApplication(sys.argv)
    
    # Create controller
    controller = AppController()
    
    # Load subject data
    controller.load_subjects(SUBJECTS)
    
    # Create and show main window
    window = MainWindow(controller)
    window.mainloop()
    
    # Clean up PyQt6 application
    qt_app.quit()

if __name__ == "__main__":
    main() 