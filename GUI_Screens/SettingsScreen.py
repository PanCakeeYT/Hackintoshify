from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QFrame,
    QFileDialog, QLineEdit, QScrollArea, QWidget, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize, Signal, QRect, Property
from PySide6.QtGui import QFont, QColor, QPainter, QBrush, QPen
import configparser
import os
import sys
import json

def get_config_path():
    if sys.platform == "win32":
        return os.path.join(os.getenv("ProgramData"), "Hackintoshify", "config.ini")
    elif sys.platform == "darwin":
        return "/Library/Application Support/Hackintoshify/config.ini"
    else: # linux
        return os.path.join(os.path.expanduser("~"), ".config", "hackintoshify", "config.ini")

def get_setup_details_path():
    if sys.platform == "win32":
        config_dir = os.path.join(os.getenv("ProgramData"), "Hackintoshify")
    elif sys.platform == "darwin":
        config_dir = "/Library/Application Support/Hackintoshify"
    else:  # Linux
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "hackintoshify")
    return os.path.join(config_dir, "setup_details.json")

class ToggleSwitch(QWidget):
    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setFixedSize(50, 26)
        self.setCursor(Qt.PointingHandCursor)
        
        self._checked = checked
        self._bg_color = QColor("#cbd5e1") # Gray (off) default
        self._circle_pos = 3.0 # Float for smoother animation
        
        # Determine target X for circle
        # Circle size = 20, Padding = 3. 
        # Off pos = 3. On pos = Width - 3 - 20 = 27
        
        self.animation = QPropertyAnimation(self, b"circle_pos", self)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Colors (Set by parent theme usually, but defaults here)
        self.active_color = QColor("#38bdf8")
        self.inactive_color = QColor("#475569")
        self.circle_color = QColor("#ffffff")
        
    def isChecked(self):
        return self._checked
        
    def setChecked(self, checked):
        self._checked = checked
        self._circle_pos = 27.0 if checked else 3.0
        self.update()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._checked = not self._checked
            self.start_animation()
            self.update()
            
    def start_animation(self):
        self.animation.stop()
        if self._checked:
            self.animation.setEndValue(27.0)
        else:
            self.animation.setEndValue(3.0)
        self.animation.start()
        
    def get_circle_pos(self):
        return self._circle_pos
        
    def set_circle_pos(self, value):
        self._circle_pos = value
        self.update()
        
    circle_pos = Property(float, get_circle_pos, set_circle_pos)
    
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Draw Background
        rect = QRect(0, 0, self.width(), self.height())
        if self._checked:
            color = self.active_color
        else:
            color = self.inactive_color
            
        p.setBrush(QBrush(color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(rect, 13, 13)
        
        # Draw Circle
        p.setBrush(QBrush(self.circle_color))
        p.drawEllipse(int(self._circle_pos), 3, 20, 20)
        p.end()

class ModernFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graphics_effect = QGraphicsDropShadowEffect(self)
        self.graphics_effect.setBlurRadius(15)
        self.graphics_effect.setOffset(0, 2)
        self.graphics_effect.setColor(QColor(0,0,0,30))
        self.setGraphicsEffect(self.graphics_effect)

class SmoothScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalScrollBar().setSingleStep(10)
        self.animation = QPropertyAnimation(self.verticalScrollBar(), b"value")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(400) # ms

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        # Default scroll step is often 120. Adjust multiplier for speed.
        scroll_step = -delta 
        
        current_value = self.verticalScrollBar().value()
        target_value = current_value + scroll_step
        
        # Clamp target
        target_value = max(0, min(target_value, self.verticalScrollBar().maximum()))
        
        self.animation.stop()
        self.animation.setStartValue(current_value)
        self.animation.setEndValue(target_value)
        self.animation.start()

class SettingsScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(700, 750)
        
        # Data
        self.config_path = get_config_path()
        self.setup_path = get_setup_details_path()
        self.config = configparser.ConfigParser()
        self.setup_details = {}
        self.current_theme = 'Dark'
        
        self.load_data()
        
         # Determine theme from config
        if 'Settings' in self.config:
            self.current_theme = self.config['Settings'].get('theme', 'Dark')
            
        self._build_ui()
        self.apply_theme(self.current_theme)

        # Entrance Animation
        self.anim_entry = QPropertyAnimation(self, b"windowOpacity")
        self.anim_entry.setDuration(300)
        self.anim_entry.setStartValue(0)
        self.anim_entry.setEndValue(1)
        self.anim_entry.start()

    def load_data(self):
        try:
            self.config.read(self.config_path)
        except Exception:
            pass 

        try:
            if os.path.exists(self.setup_path):
                with open(self.setup_path, 'r') as f:
                    self.setup_details = json.load(f)
        except Exception:
            self.setup_details = {}

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- Header ---
        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 30, 40, 30)
        
        title_box = QVBoxLayout()
        title_box.setSpacing(5)
        title = QLabel("Preferences")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setObjectName("window_title")
        subtitle = QLabel("Customize your Hackintoshify experience")
        subtitle.setFont(QFont("Segoe UI", 12)) 
        subtitle.setObjectName("window_subtitle")
        
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        
        self.main_layout.addWidget(header)

        # --- Content Area ---
        # Use SmoothScrollArea instead of QScrollArea
        scroll_area = SmoothScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setObjectName("scroll_area")
        
        content_container = QWidget()
        content_container.setObjectName("content_container")
        self.content_layout = QVBoxLayout(content_container)
        self.content_layout.setContentsMargins(40, 20, 40, 40)
        self.content_layout.setSpacing(30)
        
        scroll_area.setWidget(content_container)
        self.main_layout.addWidget(scroll_area)

        # --- 1. Appearance ---
        self._add_section_title("Appearance")
        
        self.appearance_frame = ModernFrame()
        self.appearance_frame.setObjectName("card")
        app_layout = QVBoxLayout(self.appearance_frame)
        app_layout.setContentsMargins(25, 25, 25, 25)
        
        # Theme Row
        theme_row = QHBoxLayout()
        theme_lbl_box = QVBoxLayout()
        theme_lbl_box.setSpacing(2)
        theme_main_lbl = QLabel("App Theme")
        theme_main_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        theme_sub_lbl = QLabel("Switch between Dark and Light mode")
        theme_sub_lbl.setObjectName("sub_label")
        theme_lbl_box.addWidget(theme_main_lbl)
        theme_lbl_box.addWidget(theme_sub_lbl)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setFixedWidth(140)
        self.theme_combo.setCursor(Qt.PointingHandCursor)
        self.theme_combo.currentTextChanged.connect(self.preview_theme)
        if 'Settings' in self.config:
            self.theme_combo.setCurrentText(self.config['Settings'].get('theme', 'Dark'))
            
        theme_row.addLayout(theme_lbl_box)
        theme_row.addStretch()
        theme_row.addWidget(self.theme_combo)
        app_layout.addLayout(theme_row)
        
        self.content_layout.addWidget(self.appearance_frame)

        # --- 2. Configuration ---
        self._add_section_title("Paths & Setup")
        
        self.paths_frame = ModernFrame()
        self.paths_frame.setObjectName("card")
        paths_layout = QVBoxLayout(self.paths_frame)
        paths_layout.setContentsMargins(25, 25, 25, 25)
        paths_layout.setSpacing(20)
        
        self.download_path_input = self._add_path_input(paths_layout, "macOS Download Path", 
                                                        self.setup_details.get("download_path", ""))
        
        line = QFrame()
        line.setObjectName("divider")
        line.setFixedHeight(1)
        paths_layout.addWidget(line)
        
        self.efi_path_input = self._add_path_input(paths_layout, "EFI Builds Output", 
                                                   self.setup_details.get("efi_path", ""))

        self.content_layout.addWidget(self.paths_frame)

        # --- 3. System ---
        self._add_section_title("System")
        
        self.sys_frame = ModernFrame()
        self.sys_frame.setObjectName("card")
        sys_layout = QVBoxLayout(self.sys_frame)
        sys_layout.setContentsMargins(25, 25, 25, 25)
        sys_layout.setSpacing(20)

        # Verbose Toggle
        self.verbose_toggle = self._add_toggle_row(sys_layout, "Verbose Logging", 
                                                  "Show detailed logs during operations (useful for debugging)")
        
        line2 = QFrame()
        line2.setObjectName("divider")
        line2.setFixedHeight(1)
        sys_layout.addWidget(line2)

        # Updates Toggle
        self.updates_toggle = self._add_toggle_row(sys_layout, "Automatic Updates", 
                                                   "Check for Hackintoshify updates on startup")
        
        # Set states
        if 'Settings' in self.config:
            self.verbose_toggle.setChecked(self.config['Settings'].getboolean('verbose_logging', False))
            self.updates_toggle.setChecked(self.config['Settings'].getboolean('check_updates', True))

        self.content_layout.addWidget(self.sys_frame)
        self.content_layout.addStretch()

        # --- Footer ---
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(40, 20, 40, 20)
        footer_layout.setSpacing(15)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("secondary_btn")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setObjectName("primary_btn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        
        footer_layout.addStretch()
        footer_layout.addWidget(self.cancel_btn)
        footer_layout.addWidget(self.save_btn)
        self.main_layout.addWidget(footer)

    def _add_section_title(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("section_header")
        self.content_layout.addWidget(lbl)

    def _add_path_input(self, layout, title, current_path):
        # Container layout
        vbox = QVBoxLayout()
        vbox.setSpacing(8)
        
        lbl = QLabel(title)
        lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        
        inp = QLineEdit(current_path)
        inp.setReadOnly(True)
        inp.setObjectName("path_input")
        inp.setFixedHeight(38)
        
        btn = QPushButton("Browse")
        btn.setObjectName("browse_btn")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(80, 38)
        btn.clicked.connect(lambda: self.browse_folder(inp))
        
        hbox.addWidget(inp)
        hbox.addWidget(btn)
        
        vbox.addWidget(lbl)
        vbox.addLayout(hbox)
        
        # Add the vertical layout to the parent layout
        layout.addLayout(vbox)
        return inp

    def _add_toggle_row(self, layout, title, subtitle):
        row = QHBoxLayout()
        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        
        t_lbl = QLabel(title)
        t_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        s_lbl = QLabel(subtitle)
        s_lbl.setObjectName("sub_label")
        s_lbl.setWordWrap(True)
        
        text_box.addWidget(t_lbl)
        text_box.addWidget(s_lbl)
        
        toggle = ToggleSwitch()
        
        row.addLayout(text_box, stretch=1)
        row.addWidget(toggle)
        layout.addLayout(row)
        return toggle

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", line_edit.text() or "")
        if folder:
            line_edit.setText(folder)

    def preview_theme(self, text):
        self.apply_theme(text)

    def save_settings(self):
        if not self.config.has_section('Settings'): self.config.add_section('Settings')
        theme = self.theme_combo.currentText()
        verbose = self.verbose_toggle.isChecked()
        updates = self.updates_toggle.isChecked()
        
        self.config.set('Settings', 'theme', theme)
        self.config.set('Settings', 'verbose_logging', str(verbose))
        self.config.set('Settings', 'check_updates', str(updates))
        
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            parent = self.parent()
            if parent and hasattr(parent, 'apply_theme'):
                parent.apply_theme(theme)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save config.ini:\n{e}")
            return

        new_details = {
            "download_path": self.download_path_input.text(),
            "efi_path": self.efi_path_input.text(),
            "setup_complete": True
        }
        self.setup_details.update(new_details)
        
        try:
            os.makedirs(os.path.dirname(self.setup_path), exist_ok=True)
            with open(self.setup_path, 'w') as f:
                json.dump(self.setup_details, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save setup_details.json:\n{e}")
            return

        self.accept()

    def apply_theme(self, theme_name):
        is_dark = theme_name.lower().startswith('dark')
        
        # Palette
        bg = '#0f172a' if is_dark else '#f8fafc'         # Slate 900 / Slate 50
        header_bg = bg
        card_bg = '#1e293b' if is_dark else '#ffffff'    # Slate 800 / White
        text_main = '#f1f5f9' if is_dark else '#0f172a'  # Slate 100 / Slate 900
        text_sub = '#94a3b8' if is_dark else '#64748b'   # Slate 400 / Slate 500
        accent = '#38bdf8' if is_dark else '#0284c7'     # Sky 400 / Sky 600
        border = '#334155' if is_dark else '#e2e8f0'     # Slate 700 / Slate 200
        input_bg = '#020617' if is_dark else '#f1f5f9'   # Slate 950 / Slate 100
        
        # Adjusted Input BG for cleaner look
        # Slightly darker in light mode for better contrast
        input_bg_css = 'rgba(0,0,0,0.2)' if is_dark else 'rgba(0,0,0,0.08)'

        # Update Toggles
        toggle_inactive = '#334155' if is_dark else '#cbd5e1'
        for toggle in [self.verbose_toggle, self.updates_toggle]:
            toggle.active_color = QColor(accent)
            toggle.inactive_color = QColor(toggle_inactive)
            toggle.update()

        # Update Graphics Effects Shadows
        shadow_color = QColor(0,0,0, 60 if is_dark else 20)
        self.appearance_frame.graphics_effect.setColor(shadow_color)
        self.paths_frame.graphics_effect.setColor(shadow_color)
        self.sys_frame.graphics_effect.setColor(shadow_color)
        
        # Combobox arrow
        accent_enc = accent.replace('#', '%23')
        arrow_icon = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='{accent_enc}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>"

        self.setStyleSheet(f"""
            QDialog {{ background-color: {bg}; color: {text_main}; }}
            
            QFrame#header {{ 
                background-color: {header_bg}; 
            }}
            QFrame#footer {{ 
                background-color: {card_bg}; 
                border-top: 1px solid {border}; 
            }}
            
            /* Scroll Area & Bar */
            QScrollArea {{ background-color: {bg}; border: none; }}
            QScrollBar:vertical {{
                border: none;
                background: {bg};
                width: 8px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {text_sub};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            QWidget#content_container {{ background-color: {bg}; border: none; }}
            QWidget#content_container > QFrame {{ background-color: {card_bg}; }}
            
            /* Typography */
            QLabel {{ color: {text_main}; font-family: 'Segoe UI'; background: transparent; }}
            QLabel#window_title {{ font-weight: 800; }}
            QLabel#window_subtitle {{ color: {text_sub}; }}
            
            QLabel#section_header {{ 
                color: {text_sub}; 
                font-weight: 700; 
                text-transform: uppercase; 
                letter-spacing: 1px; 
                font-size: 13px;
                margin-top: 10px;
                margin-bottom: 5px;
            }}
            
            QLabel#sub_label {{ color: {text_sub}; font-size: 12px; }}
            
            /* Cards */
            QFrame#card {{
                background-color: {card_bg};
                border: 1px solid {border};
                border-radius: 12px;
            }}
            
            QFrame#divider {{
                background-color: {border};
                border: none;
            }}
            
            /* Inputs */
            QLineEdit {{
                background-color: {input_bg_css};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 0 12px;
                color: {text_main};
            }}
            QLineEdit:focus {{ border: 1px solid {accent}; }}
            
            /* Buttons */
            QPushButton#primary_btn {{
                background-color: {accent}; color: #ffffff; border: none; border-radius: 6px;
                padding: 8px 16px; font-weight: 600; font-size: 13px; min-width: 100px;
            }}
            QPushButton#primary_btn:hover {{ opacity: 0.9; }}
            
            QPushButton#secondary_btn {{
                background-color: transparent; color: {text_main}; 
                border: 1px solid {border}; border-radius: 6px; padding: 8px 16px; 
                font-weight: 600; font-size: 13px; min-width: 80px;
            }}
            QPushButton#secondary_btn:hover {{ background-color: {input_bg}; }}
            
            QPushButton#browse_btn {{
                background-color: {input_bg}; color: {accent}; border: 1px solid {border};
                border-radius: 6px; font-weight: 600;
            }}
            QPushButton#browse_btn:hover {{ border-color: {accent}; }}
            
            /* Combo */
            QComboBox {{
                background-color: {input_bg};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 5px 10px;
                color: {text_main};
            }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox::down-arrow {{ image: url("{arrow_icon}"); width: 12px; height: 12px; }}
        """)