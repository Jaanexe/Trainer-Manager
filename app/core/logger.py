"""Logging configuration for Game Trainer Manager."""

import logging
import logging.handlers
from pathlib import Path

def setup_logger(log_file: Path, debug: bool = False):
    """Configure rotating file logger."""
    log_level = logging.DEBUG if debug else logging.INFO
    
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
