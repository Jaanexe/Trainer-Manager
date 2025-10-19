"""Tests for configuration management."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.config import Config


class TestConfig:
    """Test Config class."""
    
    @pytest.fixture
    def temp_config(self):
        """Create temporary config directory."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_initialization(self, temp_config):
        """Test Config initialization."""
        config_file = temp_config / "config.json"
        config = Config(str(config_file))
        
        assert config.allow_network_updates == False
        assert config.language == "en"
        assert config.debug_mode == False
    
    def test_get_set(self, temp_config):
        """Test getting and setting config values."""
        config_file = temp_config / "config.json"
        config = Config(str(config_file))
        
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
    
    def test_allow_network_updates_property(self, temp_config):
        """Test allow_network_updates property."""
        config_file = temp_config / "config.json"
        config = Config(str(config_file))
        
        assert config.allow_network_updates == False
        config.set("allow_network_updates", True)
        assert config.allow_network_updates == True
    
    def test_language_property(self, temp_config):
        """Test language property."""
        config_file = temp_config / "config.json"
        config = Config(str(config_file))
        
        assert config.language == "en"
        config.set("language", "zh")
        assert config.language == "zh"
    
    def test_debug_mode_property(self, temp_config):
        """Test debug_mode property."""
        config_file = temp_config / "config.json"
        config = Config(str(config_file))
        
        assert config.debug_mode == False
        config.set("debug_mode", True)
        assert config.debug_mode == True
    
    def test_paths_properties(self, temp_config):
        """Test path properties."""
        config_file = temp_config / "config.json"
        config = Config(str(config_file))
        
        assert isinstance(config.trainers_path, Path)
        assert isinstance(config.quarantine_path, Path)
    
    def test_save_and_load(self, temp_config):
        """Test saving and loading config."""
        config_file = temp_config / "config.json"
        
        config1 = Config(str(config_file))
        config1.set("test_key", "test_value")
        
        config2 = Config(str(config_file))
        assert config2.get("test_key") == "test_value"
