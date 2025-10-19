"""Tests for adding trainer files."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.trainer_manager import TrainerFileManager


class TestAddTrainerFeature:
    """Test the add trainer feature."""
    
    @pytest.fixture
    def temp_trainers(self):
        """Create temporary trainers directory."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def temp_source(self):
        """Create temporary source directory with test files."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_add_exe_file(self, temp_trainers, temp_source):
        """Test adding a valid .exe file."""
        # Create a test .exe file
        source_file = temp_source / "test_trainer.exe"
        source_file.write_bytes(b"MZ" + b"\x00" * 100)
        
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.add_trainer(source_file)
        
        assert success
        assert (temp_trainers / "test_trainer.exe").exists()
        assert "added" in message.lower()
    
    def test_add_multiple_trainers(self, temp_trainers, temp_source):
        """Test adding multiple trainer files."""
        manager = TrainerFileManager(temp_trainers)
        
        # Create and add multiple files
        for i in range(3):
            source_file = temp_source / f"trainer_{i}.exe"
            source_file.write_bytes(b"MZ" + b"\x00" * 100)
            success, _ = manager.add_trainer(source_file)
            assert success
        
        # Verify all files were added
        trainers = manager.list_trainers()
        assert len(trainers) == 3
    
    def test_add_non_exe_file(self, temp_trainers, temp_source):
        """Test that non-.exe files are rejected."""
        source_file = temp_source / "not_trainer.txt"
        source_file.write_text("This is not an exe")
        
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.add_trainer(source_file)
        
        assert not success
        assert ".exe" in message.lower()
    
    def test_add_duplicate_trainer(self, temp_trainers, temp_source):
        """Test that duplicate trainers are rejected."""
        source_file = temp_source / "trainer.exe"
        source_file.write_bytes(b"MZ" + b"\x00" * 100)
        
        manager = TrainerFileManager(temp_trainers)
        
        # Add first time
        success1, _ = manager.add_trainer(source_file)
        assert success1
        
        # Try to add again
        success2, message = manager.add_trainer(source_file)
        assert not success2
        assert "already exists" in message.lower()
    
    def test_add_nonexistent_file(self, temp_trainers):
        """Test that nonexistent files are rejected."""
        source_file = Path("/nonexistent/trainer.exe")
        
        manager = TrainerFileManager(temp_trainers)
        success, message = manager.add_trainer(source_file)
        
        assert not success
        assert "not found" in message.lower()
    
    def test_add_preserves_file_content(self, temp_trainers, temp_source):
        """Test that file content is preserved when adding."""
        content = b"MZ" + b"\x90" * 100
        source_file = temp_source / "trainer.exe"
        source_file.write_bytes(content)
        
        manager = TrainerFileManager(temp_trainers)
        manager.add_trainer(source_file)
        
        dest_file = temp_trainers / "trainer.exe"
        assert dest_file.read_bytes() == content
    
    def test_add_trainer_with_special_chars(self, temp_trainers, temp_source):
        """Test adding trainer with special characters in filename."""
        source_file = temp_source / "trainer_v1.0_final.exe"
        source_file.write_bytes(b"MZ" + b"\x00" * 100)
        
        manager = TrainerFileManager(temp_trainers)
        success, _ = manager.add_trainer(source_file)
        
        assert success
        assert (temp_trainers / "trainer_v1.0_final.exe").exists()
