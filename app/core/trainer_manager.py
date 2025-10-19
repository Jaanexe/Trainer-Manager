"""Core trainer file management logic."""

import logging
import shutil
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)

class TrainerFileManager:
    """Manages local trainer files."""
    
    def __init__(self, trainers_path: Path):
        self.trainers_path = trainers_path
        self.trainers_path.mkdir(parents=True, exist_ok=True)
    
    def list_trainers(self) -> List[Path]:
        """List all .exe trainer files."""
        try:
            trainers = list(self.trainers_path.glob("*.exe"))
            logger.info(f"Found {len(trainers)} trainer files")
            return sorted(trainers)
        except Exception as e:
            logger.error(f"Failed to list trainers: {e}")
            return []
    
    def add_trainer(self, source_path: Path) -> Tuple[bool, str]:
        """Add a trainer file to the trainers folder."""
        try:
            if not source_path.exists():
                return False, "Source file not found"
            
            if source_path.suffix.lower() != ".exe":
                return False, "Only .exe files are supported"
            
            dest_path = self.trainers_path / source_path.name
            
            if dest_path.exists():
                return False, f"Trainer already exists: {source_path.name}"
            
            shutil.copy2(source_path, dest_path)
            logger.info(f"Added trainer: {source_path.name}")
            return True, f"Trainer added: {source_path.name}"
        
        except Exception as e:
            logger.error(f"Failed to add trainer: {e}")
            return False, str(e)
    
    def remove_trainer(self, trainer_name: str) -> Tuple[bool, str]:
        """Remove a trainer file."""
        try:
            trainer_path = self.trainers_path / trainer_name
            
            if not trainer_path.exists():
                return False, "Trainer not found"
            
            trainer_path.unlink()
            logger.info(f"Removed trainer: {trainer_name}")
            return True, f"Trainer removed: {trainer_name}"
        
        except Exception as e:
            logger.error(f"Failed to remove trainer: {e}")
            return False, str(e)
    
    def rename_trainer(self, old_name: str, new_name: str) -> Tuple[bool, str]:
        """Rename a trainer file."""
        try:
            old_path = self.trainers_path / old_name
            new_path = self.trainers_path / new_name
            
            if not old_path.exists():
                return False, "Trainer not found"
            
            if new_path.exists():
                return False, "New name already exists"
            
            old_path.rename(new_path)
            logger.info(f"Renamed trainer: {old_name} -> {new_name}")
            return True, f"Trainer renamed: {old_name} -> {new_name}"
        
        except Exception as e:
            logger.error(f"Failed to rename trainer: {e}")
            return False, str(e)
    
    def move_trainer(self, trainer_name: str, dest_folder: Path) -> Tuple[bool, str]:
        """Move trainer to another folder."""
        try:
            source_path = self.trainers_path / trainer_name
            
            if not source_path.exists():
                return False, "Trainer not found"
            
            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_path = dest_folder / trainer_name
            
            shutil.move(str(source_path), str(dest_path))
            logger.info(f"Moved trainer: {trainer_name} to {dest_folder}")
            return True, f"Trainer moved to {dest_folder}"
        
        except Exception as e:
            logger.error(f"Failed to move trainer: {e}")
            return False, str(e)
    
    def get_trainer_path(self, trainer_name: str) -> Path:
        """Get full path to a trainer file."""
        return self.trainers_path / trainer_name
