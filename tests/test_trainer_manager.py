"""Tests for trainer file management."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.trainer_manager import TrainerFileManager


class TestTrainerFileManager:
    """Test TrainerFileManager class."""
    
    @pytest.fixture
    def temp_trainers(self):
        """Create temporary trainers directory."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def test_trainer(self, temp_trainers):
        """Create a test trainer file."""
        trainer_file = temp_trainers / "test_trainer.exe"
        trainer_file.write_bytes(b"MZ" + b"\x00" * 100)
        return trainer_file
    
    def test_initialization(self, temp_trainers):
        """Test TrainerFileManager initialization."""
        manager = TrainerFileManager(temp_trainers)
        assert manager.trainers_path == temp_trainers
        assert manager.trainers_path.exists()
    
    def test_list_trainers_empty(self, temp_trainers):
        """Test listing trainers when directory is empty."""
        manager = TrainerFileManager(temp_trainers)
        trainers = manager.list_trainers()
        assert trainers == []
    
    def test_list_trainers(self, temp_trainers, test_trainer):
        """Test listing trainers."""
        manager = TrainerFileManager(temp_trainers)
        trainers = manager.list_trainers()
        assert len(trainers) == 1
        assert trainers[0].name == "test_trainer.exe"
    
    def test_add_trainer(self, temp_trainers):
        """Test adding a trainer."""
        source_dir = Path(temp_trainers) / "source"
        source_dir.mkdir()
        source_file = source_dir / "new_trainer.exe"
        source_file.write_bytes(b"MZ" + b"\x00" * 100)
        
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.add_trainer(source_file)
        
        assert success
        assert (temp_trainers / "new_trainer.exe").exists()
    
    def test_add_trainer_duplicate(self, temp_trainers, test_trainer):
        """Test adding a duplicate trainer."""
        source_dir = Path(temp_trainers) / "source"
        source_dir.mkdir()
        source_file = source_dir / "test_trainer.exe"
        source_file.write_bytes(b"MZ" + b"\x00" * 100)
        
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.add_trainer(source_file)
        
        assert not success
        assert "already exists" in message
    
    def test_add_trainer_non_exe(self, temp_trainers):
        """Test adding a non-exe file."""
        source_dir = Path(temp_trainers) / "source"
        source_dir.mkdir()
        source_file = source_dir / "test.txt"
        source_file.write_text("test")
        
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.add_trainer(source_file)
        
        assert not success
        assert ".exe" in message
    
    def test_remove_trainer(self, temp_trainers, test_trainer):
        """Test removing a trainer."""
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.remove_trainer("test_trainer.exe")
        
        assert success
        assert not test_trainer.exists()
    
    def test_remove_trainer_not_found(self, temp_trainers):
        """Test removing a non-existent trainer."""
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.remove_trainer("nonexistent.exe")
        
        assert not success
        assert "not found" in message
    
    def test_rename_trainer(self, temp_trainers, test_trainer):
        """Test renaming a trainer."""
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.rename_trainer("test_trainer.exe", "renamed_trainer.exe")
        
        assert success
        assert (temp_trainers / "renamed_trainer.exe").exists()
        assert not test_trainer.exists()
    
    def test_rename_trainer_not_found(self, temp_trainers):
        """Test renaming a non-existent trainer."""
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.rename_trainer("nonexistent.exe", "new_name.exe")
        
        assert not success
        assert "not found" in message
    
    def test_get_trainer_path(self, temp_trainers):
        """Test getting trainer path."""
        manager = TrainerFileManager(temp_trainers)
        path = manager.get_trainer_path("test.exe")
        
        assert path == temp_trainers / "test.exe"
