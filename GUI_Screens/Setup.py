# GUI_Screens/Setup.py

"""
Main Screen for hackintoshify GUI tool
Author: PanCakeeYT (Abdelrahman)
Date: December 2025s
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QMessageBox, QFrame, QSizePolicy, QCheckBox
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QPen
from PySide6.QtCore import Qt

class Setup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hackintoshify | Setup")
        self.setGeometry(100, 100, 1000, 700)
        self.current_theme = 'Dark'
        self._build_ui()
        self.apply_theme(self.current_theme)

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        