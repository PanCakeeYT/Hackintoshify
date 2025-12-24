from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt


class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings - Hackintoshify")
        self.setGeometry(120, 120, 480, 320)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        theme_label = QLabel("Theme")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Light", "Dark"])
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)

        self.verbose_chk = QCheckBox("Enable verbose logging")
        layout.addWidget(self.verbose_chk)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def save(self):
        # Save logic and apply theme to parent if possible
        theme = self.theme_combo.currentText()
        verbose = self.verbose_chk.isChecked()

        parent = self.parent()
        if parent and hasattr(parent, 'apply_theme'):
            try:
                parent.apply_theme(theme)
            except Exception as exc:
                QMessageBox.warning(self, "Apply theme failed", f"Failed to apply theme: {exc}")

        QMessageBox.information(self, "Settings saved", f"Theme: {theme}\nVerbose logging: {verbose}")
        self.close()
