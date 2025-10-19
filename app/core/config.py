"""Configuration management for Game Trainer Manager."""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

class Config:
    """Manages application configuration with safe defaults."""
    
    DEFAULT_CONFIG = {
        "allow_network_updates": False,
        "language": "en",
        "debug_mode": False,
        "trainers_path": "",
        "quarantine_path": "",
        "auto_scan_downloads": True,
        "scanner_type": "windows_defender",
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.data: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self._load_config()
        self._ensure_paths()
    
    def _load_config(self):
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
                    logger.info(f"Loaded config from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}. Using defaults.")
        else:
            self.save_config()
    
    def _ensure_paths(self):
        """Ensure required paths exist."""
        if not self.data.get("trainers_path"):
            self.data["trainers_path"] = str(Path.home() / "Trainers")
        
        if not self.data.get("quarantine_path"):
            self.data["quarantine_path"] = str(Path.home() / "Trainers" / "quarantine")
        
        Path(self.data["trainers_path"]).mkdir(parents=True, exist_ok=True)
        Path(self.data["quarantine_path"]).mkdir(parents=True, exist_ok=True)
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
                logger.info(f"Saved config to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.data[key] = value
        self.save_config()
    
    @property
    def allow_network_updates(self) -> bool:
        return self.data.get("allow_network_updates", False)
    
    @property
    def language(self) -> str:
        return self.data.get("language", "en")
    
    @property
    def debug_mode(self) -> bool:
        return self.data.get("debug_mode", False)
    
    @property
    def trainers_path(self) -> Path:
        return Path(self.data.get("trainers_path", ""))
    
    @property
    def quarantine_path(self) -> Path:
        return Path(self.data.get("quarantine_path", ""))
    
    @property
    def log_file(self) -> Path:
        return Path("trainer_manager.log")
