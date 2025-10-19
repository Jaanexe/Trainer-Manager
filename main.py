#!/usr/bin/env python3
"""
Game Trainer Manager - Main entry point
Local-only, secure trainer file management application.
"""

import sys
import logging
from pathlib import Path

from app.ui.main_window import MainWindow
from app.core.config import Config
from app.core.logger import setup_logger

def main():
    config = Config()
    setup_logger(config.log_file, config.debug_mode)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Game Trainer Manager")
    
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    window = MainWindow(config)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
