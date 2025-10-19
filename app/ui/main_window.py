"""Main application window for Game Trainer Manager."""

import logging
import webbrowser
from pathlib import Path
import sys

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel,
    QMessageBox, QFileDialog, QDialog, QComboBox, QCheckBox, QSpinBox
)
from PySide6.QtCore import Qt, QSize
from pathlib import Path

from app.core.config import Config
from app.core.metadata import MetadataManager
from app.core.trainer_manager import TrainerFileManager
from app.core.security import SecurityManager
from app.ui.translations import Translator

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.translator = Translator(config.language)
        
        self.metadata_manager = MetadataManager(Path("app/resources"))
        self.trainer_manager = TrainerFileManager(config.trainers_path)
        self.security_manager = SecurityManager(
            config.quarantine_path,
            config.get("scanner_type", "windows_defender")
        )
        
        self.setWindowTitle(self.translator("title"))
        self.setSize(1000, 600)
        self.setup_ui()
        self.load_trainers()
    
    def setSize(self, width: int, height: int):
        """Set window size."""
        self.resize(width, height)
    
    def setup_ui(self):
        """Setup the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Available Trainers")
        title_font = title_label.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Trainers list
        self.trainers_list = QListWidget()
        self.trainers_list.itemDoubleClicked.connect(self.on_run_trainer)
        main_layout.addWidget(self.trainers_list)
        
        # Action buttons
        buttons_layout = self.create_action_buttons()
        main_layout.addLayout(buttons_layout)
        
        central_widget.setLayout(main_layout)
        self.create_menu_bar()
    
    
    def create_action_buttons(self) -> QHBoxLayout:
        """Create action buttons."""
        layout = QHBoxLayout()
        
        self.btn_add_trainer = QPushButton("Add Trainer")
        self.btn_add_trainer.clicked.connect(self.on_add_trainer)
        
        self.btn_open_folder = QPushButton(self.translator("open_folder"))
        self.btn_open_folder.clicked.connect(self.on_open_folder)
        
        self.btn_run = QPushButton("Run Trainer")
        self.btn_run.clicked.connect(self.on_run_trainer)
        
        self.btn_delete = QPushButton(self.translator("delete"))
        self.btn_delete.clicked.connect(self.on_delete)
        
        self.btn_settings = QPushButton(self.translator("settings"))
        self.btn_settings.clicked.connect(self.on_settings)
        
        layout.addWidget(self.btn_add_trainer)
        layout.addWidget(self.btn_open_folder)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_settings)
        
        return layout
    
    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Exit", self.close)
        
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Settings", self.on_settings)
        
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.on_about)
    
    def load_trainers(self):
        """Load all trainer files from trainers folder."""
        self.trainers_list.clear()
        trainers = self.trainer_manager.list_trainers()
        
        for trainer_path in trainers:
            item = QListWidgetItem(trainer_path.name)
            item.setData(Qt.UserRole, trainer_path)
            self.trainers_list.addItem(item)
        
        logger.info(f"Loaded {len(trainers)} trainers")
    
    def on_add_trainer(self):
        """Handle adding a new trainer file."""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Executable Files (*.exe);;All Files (*)")
        file_dialog.setDefaultSuffix("exe")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                source_path = Path(selected_files[0])
                success, message = self.trainer_manager.add_trainer(source_path)
                
                if success:
                    logger.info(f"Trainer added: {source_path.name}")
                    QMessageBox.information(self, "Success", message)
                    self.load_trainers()
                else:
                    logger.error(f"Failed to add trainer: {message}")
                    QMessageBox.warning(self, "Error", message)
    
    def on_open_folder(self):
        """Open trainers folder."""
        import subprocess
        import sys
        
        try:
            if sys.platform == "win32":
                subprocess.Popen(f'explorer "{self.config.trainers_path}"')
            else:
                subprocess.Popen(["open", str(self.config.trainers_path)])
            logger.info("Opened trainers folder")
        except Exception as e:
            logger.error(f"Failed to open folder: {e}")
            QMessageBox.warning(self, "Error", str(e))
    
    
    def on_run_trainer(self):
        """Handle running a trainer file."""
        selected_items = self.trainers_list.selectedItems()
        if not selected_items:
            return
        
        trainer_name = selected_items[0].text()
        trainer_path = self.trainer_manager.get_trainer_path(trainer_name)
        
        if not trainer_path.exists():
            return
        
        try:
            import subprocess
            import sys
            import os
            
            if sys.platform == "win32":
                # Try to run with admin privileges on Windows
                try:
                    import ctypes
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", str(trainer_path), None, None, 1)
                    logger.info(f"Launched trainer with admin: {trainer_name}")
                except:
                    # Fallback to normal execution if admin fails
                    subprocess.Popen(str(trainer_path))
                    logger.info(f"Launched trainer: {trainer_name}")
            else:
                # For Linux/Mac
                subprocess.Popen(str(trainer_path))
                logger.info(f"Launched trainer: {trainer_name}")
        except Exception as e:
            logger.error(f"Failed to launch trainer: {e}")
            QMessageBox.warning(self, "Error", f"Failed to launch: {e}")
    
    def on_delete(self):
        """Handle delete action."""
        selected_items = self.trainers_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No trainer selected")
            return
        
        trainer_name = selected_items[0].text()
        
        reply = QMessageBox.question(
            self,
            "Confirm",
            self.translator("confirm_delete"),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.trainer_manager.remove_trainer(trainer_name)
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_trainers()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def on_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self, self.config, self.translator)
        if dialog.exec() == QDialog.Accepted:
            self.config.save_config()
            self.translator.set_language(self.config.language)
            logger.info("Settings updated")
    
    
    def on_about(self):
        """Show about dialog."""
        QMessageBox.information(
            self,
            "About",
            "Game Trainer Manager\n\nSimple trainer management tool."
        )

