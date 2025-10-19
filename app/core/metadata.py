"""Metadata management for trainers and games."""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Trainer:
    """Represents a trainer file with metadata."""
    name: str
    game: str
    version: str
    author: str
    url: str
    checksum: str = ""
    local_path: str = ""

@dataclass
class Game:
    """Represents a game with trainers."""
    name: str
    abbreviation: str = ""
    trainers: List[Trainer] = None
    
    def __post_init__(self):
        if self.trainers is None:
            self.trainers = []

class MetadataManager:
    """Manages CSV metadata for trainers and games."""
    
    def __init__(self, resources_path: Path):
        self.resources_path = resources_path
        self.resources_path.mkdir(parents=True, exist_ok=True)
        
        self.trainers_list_path = resources_path / "trainers_list.csv"
        self.games_list_path = resources_path / "game_names_merged.csv"
        self.abbreviations_path = resources_path / "abbreviation.csv"
        
        self.trainers: Dict[str, Trainer] = {}
        self.games: Dict[str, Game] = {}
        self.abbreviations: Dict[str, str] = {}
        
        self._ensure_default_csvs()
        self.load_all()
    
    def _ensure_default_csvs(self):
        """Create default CSV files if they don't exist."""
        if not self.trainers_list_path.exists():
            self._create_default_trainers_csv()
        
        if not self.games_list_path.exists():
            self._create_default_games_csv()
        
        if not self.abbreviations_path.exists():
            self._create_default_abbreviations_csv()
    
    def _create_default_trainers_csv(self):
        """Create default trainers_list.csv."""
        with open(self.trainers_list_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "game", "version", "author", "url", "checksum"])
            writer.writerow(["Example Trainer", "Example Game", "1.0", "Author", "https://example.com", ""])
    
    def _create_default_games_csv(self):
        """Create default game_names_merged.csv."""
        with open(self.games_list_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["game_id", "game_name", "platform"])
            writer.writerow(["1", "Example Game", "PC"])
    
    def _create_default_abbreviations_csv(self):
        """Create default abbreviation.csv."""
        with open(self.abbreviations_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["abbreviation", "full_name"])
            writer.writerow(["EG", "Example Game"])
    
    def load_all(self):
        """Load all metadata from CSV files."""
        try:
            self.load_trainers()
            self.load_games()
            self.load_abbreviations()
            logger.info("Metadata loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
    
    def load_trainers(self):
        """Load trainers from CSV."""
        self.trainers.clear()
        try:
            with open(self.trainers_list_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row.get("name"):
                        trainer = Trainer(
                            name=row.get("name", ""),
                            game=row.get("game", ""),
                            version=row.get("version", ""),
                            author=row.get("author", ""),
                            url=row.get("url", ""),
                            checksum=row.get("checksum", "")
                        )
                        self.trainers[trainer.name] = trainer
            logger.info(f"Loaded {len(self.trainers)} trainers")
        except Exception as e:
            logger.error(f"Failed to load trainers: {e}")
    
    def load_games(self):
        """Load games from CSV."""
        self.games.clear()
        try:
            with open(self.games_list_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row.get("game_name"):
                        game = Game(
                            name=row.get("game_name", ""),
                            abbreviation=row.get("game_id", "")
                        )
                        self.games[game.name] = game
            logger.info(f"Loaded {len(self.games)} games")
        except Exception as e:
            logger.error(f"Failed to load games: {e}")
    
    def load_abbreviations(self):
        """Load abbreviations from CSV."""
        self.abbreviations.clear()
        try:
            with open(self.abbreviations_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row.get("abbreviation"):
                        abbr = row.get("abbreviation", "")
                        full = row.get("full_name", "")
                        self.abbreviations[abbr] = full
            logger.info(f"Loaded {len(self.abbreviations)} abbreviations")
        except Exception as e:
            logger.error(f"Failed to load abbreviations: {e}")
    
    def get_trainers_for_game(self, game_name: str) -> List[Trainer]:
        """Get all trainers for a specific game."""
        return [t for t in self.trainers.values() if t.game.lower() == game_name.lower()]
    
    def validate_csv_schema(self, csv_path: Path) -> Tuple[bool, str]:
        """Validate CSV schema and content."""
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    return False, "CSV has no headers"
                
                row_count = 0
                for row in reader:
                    if not row:
                        continue
                    row_count += 1
                
                return True, f"Valid CSV with {row_count} rows"
        except Exception as e:
            return False, str(e)
