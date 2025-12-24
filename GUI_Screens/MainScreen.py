# GUI_Screens/MainScreen.py

"""
Main Screen for hackintoshify GUI tool
Author: PanCakeeYT (Abdelrahman)
Date: December 2025
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QMessageBox, QFrame, QSizePolicy, QCheckBox
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QPen
from PySide6.QtCore import Qt


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hackintoshify")
        self.setGeometry(100, 100, 1000, 700)
        self.current_theme = 'Dark'
        self._build_ui()
        self.apply_theme(self.current_theme)

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Top bar
        top_bar = QFrame()
        top_bar.setObjectName("top_bar")
        top_bar.setFixedHeight(50)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)
        title = QLabel("Hackintoshify")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        top_layout.addWidget(title)
        top_layout.addStretch()
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setFixedSize(100, 36)
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        top_layout.addWidget(self.settings_btn)
        self.main_layout.addWidget(top_bar)

        # Content area
        content_area = QWidget()
        self.main_layout.addWidget(content_area)
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(50, 30, 50, 30)
        content_layout.setSpacing(30)

        # Hero area
        hero_layout = QVBoxLayout()
        hero_layout.setContentsMargins(0, 20, 0, 20)
        hero_title = QLabel("Hackintoshify")
        hero_title.setFont(QFont("Segoe UI", 40, QFont.Bold))
        hero_title.setAlignment(Qt.AlignCenter)
        hero_layout.addWidget(hero_title)
        content_layout.addLayout(hero_layout)

        # Primary action cards
        cards = QGridLayout()
        cards.setSpacing(25)
        self.action_buttons = []
        items = [
            ("Create macOS Installer", "Start the automatic process to create a bootable USB.", "🚀", self.create_installer),
            ("Select macOS Image", "Use an existing macOS installer image.", "💿", self.select_image),
            ("Select EFI", "Use an existing EFI folder for your hardware.", "⚙️", self.select_efi),
            ("Help & Guides", "Read the guides and get help.", "❓", self.open_help),
        ]
        for idx, (text, desc, emoji, handler) in enumerate(items):
            btn = self.create_action_button(text, desc, emoji, handler)
            self.action_buttons.append(btn)
            cards.addWidget(btn, idx // 2, idx % 2)
        content_layout.addLayout(cards)

        # USB contextual buttons
        self.usb_section = QFrame()
        self.usb_section.setObjectName("usb_section")
        self.usb_section.setVisible(False)
        usb_layout = QVBoxLayout(self.usb_section)
        usb_layout.setContentsMargins(0, 20, 0, 0)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("separator")
        usb_layout.addWidget(separator)

        usb_title_layout = QHBoxLayout()
        usb_title_layout.setContentsMargins(0, 20, 0, 10)
        usb_title = QLabel("Connected macOS USB")
        usb_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        usb_title_layout.addWidget(usb_title)
        usb_layout.addLayout(usb_title_layout)
        
        usb_buttons_layout = QHBoxLayout()
        usb_buttons_layout.setSpacing(25)
        self.configure_kexts_btn = self.create_action_button("Configure Kexts", "Manage kexts in the EFI.", "🛠️", self.configure_kexts)
        self.repair_btn = self.create_action_button("Repair EFI", "Repair common EFI issues.", "🔧", self.repair_usb)
        usb_buttons_layout.addWidget(self.configure_kexts_btn)
        usb_buttons_layout.addWidget(self.repair_btn)
        usb_layout.addLayout(usb_buttons_layout)
        content_layout.addWidget(self.usb_section)

        content_layout.addStretch()

        # Simulation Checkbox
        self.usb_sim_checkbox = QCheckBox("Simulate USB with macOS connected")
        self.usb_sim_checkbox.toggled.connect(self.usb_section.setVisible)
        content_layout.addWidget(self.usb_sim_checkbox)

        # Footer
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFixedHeight(40)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        self.footer_label = QLabel("Ready")
        footer_layout.addWidget(self.footer_label)
        self.main_layout.addWidget(footer)

    def create_action_button(self, text, desc, emoji, handler):
        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(120)
        btn.clicked.connect(handler)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setProperty('role', 'action')
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(20, 20, 20, 20)
        title_label = QLabel(f"{text} {emoji}")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        desc_label = QLabel(desc)
        desc_label.setWordWrap(True)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        return btn

    # Actions (placeholders)
    def create_installer(self): QMessageBox.information(self, "Create Installer", "This will start the automatic installer creation process.")
    def select_image(self): QMessageBox.information(self, "Select Image", "Select a macOS installer image.")
    def select_efi(self): QMessageBox.information(self, "Select EFI", "Select an EFI folder.")
    def open_help(self): QMessageBox.information(self, "Help", "Open help and guides.")
    def configure_kexts(self): QMessageBox.information(self, "Configure Kexts", "Manage kexts for the connected USB.")
    def repair_usb(self): QMessageBox.information(self, "Repair USB", "Repair the connected USB drive.")

    def open_settings(self):
        try:
            from .SettingsScreen import SettingsScreen
            dlg = SettingsScreen(parent=self)
            dlg.setWindowModality(Qt.ApplicationModal)
            dlg.show()
            dlg.raise_()
        except Exception as exc:
            QMessageBox.information(self, "Settings", f"Settings screen not available yet:\n{exc}")

    def apply_theme(self, theme_name: str):
        self.current_theme = theme_name
        is_dark = theme_name.lower().startswith('dark')
        
        bg = '#0f172a' if is_dark else '#f1f5f9'
        card = '#1e293b' if is_dark else '#ffffff'
        text = '#f8fafc' if is_dark else '#0f172a'
        muted = '#94a3b8' if is_dark else '#64748b'
        accent = '#38bdf8' if is_dark else '#0ea5e9'
        border = '#334155' if is_dark else '#e2e8f0'
        
        self.setStyleSheet(f"background-color: {bg}; color: {text};")
        self.findChild(QFrame, "top_bar").setStyleSheet(f"background-color: {card}; border-bottom: 1px solid {border};")
        
        # Hero title
        self.findChildren(QLabel)[0].setStyleSheet(f"color: {text};")
        
        self.settings_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {accent}; color: white; border: none; border-radius: 8px; font-weight: 600; padding: 0 10px;}}
            QPushButton:hover {{ background-color: {QColor(accent).lighter(110).name()}; }}
            """)

        button_style = f"""
            QPushButton[role="action"] {{
                background-color: {card};
                border: 1px solid {border};
                border-radius: 12px;
                text-align: left;
                padding: 20px;
            }}
            QPushButton[role="action"]:hover {{ 
                background-color: {QColor(card).lighter(115).name()};
                border-color: {accent};
            }}"""
        for btn in self.findChildren(QPushButton):
            if btn.property('role') == 'action':
                btn.setStyleSheet(button_style)
                for label in btn.findChildren(QLabel):
                    label.setStyleSheet("color: inherit; background: transparent; border: none;")

        self.findChild(QFrame, "footer").setStyleSheet(f"background-color: {card}; border-top: 1px solid {border};")
        self.footer_label.setStyleSheet(f"color: {muted};")
        
        self.usb_sim_checkbox.setStyleSheet(f"color: {muted};")
        self.findChild(QFrame, "usb_section").setStyleSheet("background: transparent; border: none;")
        self.findChild(QFrame, "separator").setStyleSheet(f"background-color: {border};")

    def paintEvent(self, event):
        painter = QPainter(self)
        super().paintEvent(event)
        # No grid pattern for a cleaner look