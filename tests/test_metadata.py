"""Tests for metadata management."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.metadata import MetadataManager, Trainer, Game


class TestMetadataManager:
    """Test MetadataManager class."""
    
    @pytest.fixture
    def temp_resources(self):
        """Create temporary resources directory."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_initialization(self, temp_resources):
        """Test MetadataManager initialization."""
        manager = MetadataManager(temp_resources)
        assert manager.resources_path == temp_resources
        assert manager.trainers_list_path.exists()
        assert manager.games_list_path.exists()
        assert manager.abbreviations_path.exists()
    
    def test_load_trainers(self, temp_resources):
        """Test loading trainers from CSV."""
        manager = MetadataManager(temp_resources)
        manager.load_trainers()
        assert len(manager.trainers) > 0
    
    def test_load_games(self, temp_resources):
        """Test loading games from CSV."""
        manager = MetadataManager(temp_resources)
        manager.load_games()
        assert len(manager.games) > 0
    
    def test_load_abbreviations(self, temp_resources):
        """Test loading abbreviations from CSV."""
        manager = MetadataManager(temp_resources)
        manager.load_abbreviations()
        assert len(manager.abbreviations) > 0
    
    def test_get_trainers_for_game(self, temp_resources):
        """Test getting trainers for a specific game."""
        manager = MetadataManager(temp_resources)
        trainers = manager.get_trainers_for_game("Example Game")
        assert isinstance(trainers, list)
    
    def test_validate_csv_schema(self, temp_resources):
        """Test CSV schema validation."""
        manager = MetadataManager(temp_resources)
        is_valid, message = manager.validate_csv_schema(manager.trainers_list_path)
        assert is_valid
        assert "Valid CSV" in message
    
    def test_trainer_dataclass(self):
        """Test Trainer dataclass."""
        trainer = Trainer(
            name="Test Trainer",
            game="Test Game",
            version="1.0",
            author="Test Author",
            url="https://example.com"
        )
        assert trainer.name == "Test Trainer"
        assert trainer.game == "Test Game"
        assert trainer.version == "1.0"
    
    def test_game_dataclass(self):
        """Test Game dataclass."""
        game = Game(name="Test Game", abbreviation="TG")
        assert game.name == "Test Game"
        assert game.abbreviation == "TG"
        assert game.trainers == []
