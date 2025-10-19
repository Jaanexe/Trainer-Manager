#!/usr/bin/env python3
"""Quick import test to verify all modules load correctly."""

try:
    from app.core.config import Config
    print("✓ Config module imported")
    
    from app.core.logger import setup_logger
    print("✓ Logger module imported")
    
    from app.core.metadata import MetadataManager, Trainer, Game
    print("✓ Metadata module imported")
    
    from app.core.security import SecurityManager, ScanResult
    print("✓ Security module imported")
    
    from app.core.trainer_manager import TrainerFileManager
    print("✓ TrainerFileManager module imported")
    
    from app.ui.translations import Translator
    print("✓ Translations module imported")
    
    print("\n✅ All modules imported successfully!")
    print("\nApplication is ready to run: python main.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
