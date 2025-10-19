"""Tests for security functionality."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.security import SecurityManager, ScanResult


class TestSecurityManager:
    """Test SecurityManager class."""
    
    @pytest.fixture
    def temp_quarantine(self):
        """Create temporary quarantine directory."""
        with TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def test_file(self, temp_quarantine):
        """Create a test file."""
        test_file = temp_quarantine / "test.txt"
        test_file.write_text("test content")
        return test_file
    
    def test_initialization(self, temp_quarantine):
        """Test SecurityManager initialization."""
        manager = SecurityManager(temp_quarantine)
        assert manager.quarantine_path == temp_quarantine
        assert manager.quarantine_path.exists()
    
    def test_compute_sha256(self, temp_quarantine, test_file):
        """Test SHA256 computation."""
        manager = SecurityManager(temp_quarantine)
        checksum = manager.compute_sha256(test_file)
        assert len(checksum) == 64
        assert checksum.isalnum()
    
    def test_verify_checksum_valid(self, temp_quarantine, test_file):
        """Test checksum verification with valid checksum."""
        manager = SecurityManager(temp_quarantine)
        expected = manager.compute_sha256(test_file)
        assert manager.verify_checksum(test_file, expected)
    
    def test_verify_checksum_invalid(self, temp_quarantine, test_file):
        """Test checksum verification with invalid checksum."""
        manager = SecurityManager(temp_quarantine)
        assert not manager.verify_checksum(test_file, "invalid_checksum")
    
    def test_verify_checksum_empty(self, temp_quarantine, test_file):
        """Test checksum verification with empty expected checksum."""
        manager = SecurityManager(temp_quarantine)
        assert not manager.verify_checksum(test_file, "")
    
    def test_is_pe_file_false(self, temp_quarantine, test_file):
        """Test PE file detection for non-PE file."""
        manager = SecurityManager(temp_quarantine)
        assert not manager.is_pe_file(test_file)
    
    def test_is_pe_file_true(self, temp_quarantine):
        """Test PE file detection for PE file."""
        pe_file = temp_quarantine / "test.exe"
        pe_file.write_bytes(b"MZ" + b"\x00" * 100)
        
        manager = SecurityManager(temp_quarantine)
        assert manager.is_pe_file(pe_file)
    
    def test_scan_result_enum(self):
        """Test ScanResult enum."""
        assert ScanResult.CLEAN.value == "clean"
        assert ScanResult.SUSPICIOUS.value == "suspicious"
        assert ScanResult.ERROR.value == "error"
        assert ScanResult.NOT_SCANNED.value == "not_scanned"
    
    def test_move_to_quarantine(self, temp_quarantine):
        """Test moving file to quarantine."""
        source_dir = Path(temp_quarantine) / "source"
        source_dir.mkdir()
        source_file = source_dir / "test.txt"
        source_file.write_text("test")
        
        manager = SecurityManager(temp_quarantine)
        success, dest = manager.move_to_quarantine(source_file)
        
        assert success
        assert dest.exists()
        assert not source_file.exists()
