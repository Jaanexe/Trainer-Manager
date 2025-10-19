"""Security and scanning functionality for Game Trainer Manager."""

import hashlib
import logging
import subprocess
from enum import Enum
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)

class ScanResult(Enum):
    """Enumeration of scan result states."""
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
    ERROR = "error"
    NOT_SCANNED = "not_scanned"

class SecurityManager:
    """Handles security operations: checksums, scanning, quarantine."""
    
    def __init__(self, quarantine_path: Path, scanner_type: str = "windows_defender"):
        self.quarantine_path = quarantine_path
        self.quarantine_path.mkdir(parents=True, exist_ok=True)
        self.scanner_type = scanner_type
    
    def compute_sha256(self, file_path: Path) -> str:
        """Compute SHA256 checksum of a file."""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            checksum = sha256_hash.hexdigest()
            logger.info(f"Computed SHA256 for {file_path.name}: {checksum}")
            return checksum
        except Exception as e:
            logger.error(f"Failed to compute SHA256: {e}")
            return ""
    
    def verify_checksum(self, file_path: Path, expected_checksum: str) -> bool:
        """Verify file checksum against expected value."""
        if not expected_checksum:
            logger.warning("No expected checksum provided")
            return False
        
        computed = self.compute_sha256(file_path)
        is_valid = computed.lower() == expected_checksum.lower()
        
        if is_valid:
            logger.info(f"Checksum verified for {file_path.name}")
        else:
            logger.warning(f"Checksum mismatch for {file_path.name}")
        
        return is_valid
    
    def scan_file(self, file_path: Path) -> Tuple[ScanResult, str]:
        """Scan file with configured scanner."""
        if not file_path.exists():
            return ScanResult.ERROR, "File not found"
        
        if self.scanner_type == "windows_defender":
            return self._scan_windows_defender(file_path)
        elif self.scanner_type == "clamav":
            return self._scan_clamav(file_path)
        else:
            logger.warning(f"Unknown scanner type: {self.scanner_type}")
            return ScanResult.NOT_SCANNED, "Scanner not configured"
    
    def _scan_windows_defender(self, file_path: Path) -> Tuple[ScanResult, str]:
        """Scan using Windows Defender (MpCmdRun.exe)."""
        try:
            defender_path = Path("C:\\Program Files\\Windows Defender\\MpCmdRun.exe")
            if not defender_path.exists():
                logger.info("Windows Defender not found")
                return ScanResult.NOT_SCANNED, "Windows Defender not available"
            
            result = subprocess.run(
                [str(defender_path), "-Scan", "-ScanType", "3", "-File", str(file_path)],
                capture_output=True,
                timeout=60,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Windows Defender scan clean: {file_path.name}")
                return ScanResult.CLEAN, "No threats detected"
            else:
                logger.warning(f"Windows Defender found issues: {file_path.name}")
                return ScanResult.SUSPICIOUS, f"Scan returned code {result.returncode}"
        
        except subprocess.TimeoutExpired:
            logger.error("Windows Defender scan timeout")
            return ScanResult.ERROR, "Scan timeout"
        except Exception as e:
            logger.error(f"Windows Defender scan error: {e}")
            return ScanResult.ERROR, str(e)
    
    def _scan_clamav(self, file_path: Path) -> Tuple[ScanResult, str]:
        """Scan using ClamAV (clamscan command)."""
        try:
            result = subprocess.run(
                ["clamscan", "--quiet", str(file_path)],
                capture_output=True,
                timeout=60,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"ClamAV scan clean: {file_path.name}")
                return ScanResult.CLEAN, "No threats detected"
            elif result.returncode == 1:
                logger.warning(f"ClamAV found issues: {file_path.name}")
                return ScanResult.SUSPICIOUS, result.stdout
            else:
                logger.error(f"ClamAV error: {result.stderr}")
                return ScanResult.ERROR, result.stderr
        
        except FileNotFoundError:
            logger.info("ClamAV not found")
            return ScanResult.NOT_SCANNED, "ClamAV not installed"
        except subprocess.TimeoutExpired:
            logger.error("ClamAV scan timeout")
            return ScanResult.ERROR, "Scan timeout"
        except Exception as e:
            logger.error(f"ClamAV scan error: {e}")
            return ScanResult.ERROR, str(e)
    
    def move_to_quarantine(self, file_path: Path) -> Tuple[bool, Path]:
        """Move file to quarantine folder."""
        try:
            if not file_path.exists():
                return False, Path()
            
            dest = self.quarantine_path / file_path.name
            file_path.rename(dest)
            logger.info(f"Moved to quarantine: {file_path.name}")
            return True, dest
        except Exception as e:
            logger.error(f"Failed to move to quarantine: {e}")
            return False, Path()
    
    def is_pe_file(self, file_path: Path) -> bool:
        """Check if file is a PE (Portable Executable) file."""
        try:
            with open(file_path, "rb") as f:
                header = f.read(2)
                return header == b"MZ"
        except Exception as e:
            logger.error(f"Failed to check PE header: {e}")
            return False
