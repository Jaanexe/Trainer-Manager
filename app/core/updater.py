"""Metadata update management for Game Trainer Manager."""

import logging
import time
import hashlib
from pathlib import Path
from typing import Tuple
from urllib.request import urlopen
from urllib.error import URLError

logger = logging.getLogger(__name__)

class MetadataUpdater:
    """Manages safe metadata updates with validation and rollback."""
    
    # Update sources (safe, read-only CSV files)
    UPDATE_SOURCES = {
        "trainers_list": "https://raw.githubusercontent.com/Karasukaigan/game-trainer-manager/main/app/resources/trainers_list.csv",
        "game_names": "https://raw.githubusercontent.com/Karasukaigan/game-trainer-manager/main/app/resources/game_names_merged.csv",
        "abbreviations": "https://raw.githubusercontent.com/Karasukaigan/game-trainer-manager/main/app/resources/abbreviation.csv",
    }
    
    # Update interval: 2 days (in seconds)
    UPDATE_INTERVAL = 2 * 24 * 3600
    
    def __init__(self, resources_path: Path, config):
        self.resources_path = resources_path
        self.config = config
        self.backup_path = resources_path / ".backup"
        self.backup_path.mkdir(exist_ok=True)
    
    def should_update(self) -> bool:
        """Check if metadata should be updated."""
        if not self.config.allow_network_updates:
            logger.info("Network updates disabled")
            return False
        
        last_update = self.config.get("last_metadata_update", 0)
        time_since_update = time.time() - last_update
        
        if time_since_update < self.UPDATE_INTERVAL:
            logger.info(f"Update not due (last: {time_since_update/3600:.1f} hours ago)")
            return False
        
        logger.info("Update is due")
        return True
    
    def auto_update(self) -> Tuple[bool, str]:
        """Automatically update metadata if conditions are met."""
        if not self.should_update():
            return False, "Update not due or network disabled"
        
        logger.info("Starting automatic metadata update")
        return self.update_metadata()
    
    def manual_update(self) -> Tuple[bool, str]:
        """Manually trigger metadata update."""
        logger.info("Starting manual metadata update")
        return self.update_metadata()
    
    def update_metadata(self) -> Tuple[bool, str]:
        """Update all metadata files with validation."""
        try:
            # Create backup of current files
            if not self._backup_current_metadata():
                return False, "Failed to create backup"
            
            # Download and validate each file
            success_count = 0
            for file_key, url in self.UPDATE_SOURCES.items():
                success, message = self._download_and_validate(file_key, url)
                if success:
                    success_count += 1
                    logger.info(f"Updated {file_key}: {message}")
                else:
                    logger.warning(f"Failed to update {file_key}: {message}")
            
            if success_count == 0:
                self._restore_backup()
                return False, "Failed to update any files"
            
            # Update timestamp
            self.config.set("last_metadata_update", time.time())
            logger.info(f"Metadata update complete: {success_count}/{len(self.UPDATE_SOURCES)} files")
            
            return True, f"Updated {success_count}/{len(self.UPDATE_SOURCES)} files"
        
        except Exception as e:
            logger.error(f"Update failed: {e}")
            self._restore_backup()
            return False, str(e)
    
    def _backup_current_metadata(self) -> bool:
        """Backup current metadata files."""
        try:
            for file_key in self.UPDATE_SOURCES.keys():
                source = self._get_file_path(file_key)
                if source.exists():
                    dest = self.backup_path / source.name
                    import shutil
                    shutil.copy2(source, dest)
                    logger.info(f"Backed up {source.name}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    def _restore_backup(self) -> bool:
        """Restore metadata from backup."""
        try:
            for file_key in self.UPDATE_SOURCES.keys():
                source = self._get_file_path(file_key)
                backup = self.backup_path / source.name
                if backup.exists():
                    import shutil
                    shutil.copy2(backup, source)
                    logger.info(f"Restored {source.name} from backup")
            return True
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def _download_and_validate(self, file_key: str, url: str) -> Tuple[bool, str]:
        """Download file and validate it."""
        try:
            # Download file
            logger.info(f"Downloading {file_key} from {url}")
            response = urlopen(url, timeout=10)
            content = response.read().decode('utf-8')
            
            if not content:
                return False, "Empty file"
            
            # Validate CSV format
            lines = content.strip().split('\n')
            if len(lines) < 2:
                return False, "Invalid CSV format (too few lines)"
            
            # Check header
            headers = lines[0].split(',')
            if not headers:
                return False, "Invalid CSV format (no headers)"
            
            # Save file
            dest = self._get_file_path(file_key)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Compute checksum
            checksum = self._compute_checksum(dest)
            logger.info(f"Downloaded {file_key}: {len(lines)} lines, checksum: {checksum[:16]}...")
            
            return True, f"{len(lines)} lines"
        
        except URLError as e:
            return False, f"Network error: {e}"
        except Exception as e:
            return False, str(e)
    
    def _get_file_path(self, file_key: str) -> Path:
        """Get path for metadata file."""
        file_map = {
            "trainers_list": "trainers_list.csv",
            "game_names": "game_names_merged.csv",
            "abbreviations": "abbreviation.csv",
        }
        return self.resources_path / file_map.get(file_key, "")
    
    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
