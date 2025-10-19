[![Download Latest](https://img.shields.io/github/v/release/Jaanexe/Trainer-Manager?color=brightgreen&label=Download&logo=github)](https://github.com/Jaanexe/Trainer-Manager/releases/latest)

# Game Trainer Manager

A lightweight, secure, local-first application for managing game trainer files (.exe). Built with Python and PySide6, featuring multi-language support, metadata management, and optional security scanning.

**⚠️ IMPORTANT: This application is for educational purposes only. Always use trainers responsibly and review the [Security Model](#security-model) before use.**

## Features

- **Local-First Design**: Operates entirely offline by default. Network features are opt-in only.
- **Trainer Management**: Add, remove, rename, and organize .exe trainer files.
- **Metadata Management**: Import and manage trainer metadata from CSV files (trainers_list.csv, game_names_merged.csv, abbreviation.csv).
- **Multi-Language Support**: English and Simplified Chinese UI.
- **Security-First Approach**:
  - SHA256 checksum generation and verification.
  - Optional Windows Defender and ClamAV integration.
  - Quarantine folder for downloaded files.
  - Never auto-executes files.
- **Search & Autocomplete**: Quick game and trainer lookup.
- **Steam Integration**: One-click Steam launch (steam:// links).
- **Settings Panel**: Configure language, network updates, scanning, and paths.

## Installation

### Prerequisites

- Python 3.11 or later
- Windows 10/11 (or Linux/macOS with minor adjustments)

### Setup

1. **Clone or download the repository**:
   ```bash
   git clone <repo-url>
   cd game-trainer-manager
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or: source venv/bin/activate  # On Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### From Source

```bash
python main.py
```

### From PyInstaller Build

```bash
dist\GameTrainerManager.exe
```

## Usage

### Main Window

- **Left Pane**: Game list with search functionality.
- **Right Pane**: Trainers for the selected game.
- **Action Buttons**:
  - **Open Folder**: Opens the trainers directory in File Explorer.
  - **Download**: Opens the trainer source URL in your default browser.
  - **Delete**: Removes a trainer file (with confirmation).
  - **Settings**: Opens the settings dialog.

### Settings

- **Language**: Switch between English and Simplified Chinese.
- **Allow Network Updates**: Enable/disable network connectivity for metadata updates.
- **Auto-scan Downloads**: Automatically scan downloaded files with configured scanner.
- **Quarantine Path**: Location for downloaded files before approval.
- **Trainers Path**: Location of your trainer files.

### Workflow: Download & Quarantine

1. Select a trainer from the list.
2. Click **Download** to open the source URL in your browser.
3. Manually download the file to the quarantine folder.
4. The app will compute SHA256 and optionally scan the file.
5. Once approved, move the file to the main trainers folder.

## Security Model

### Design Principles

1. **Default = Local-Only**: The app ships with bundled CSV metadata and does not contact the network unless explicitly enabled.
2. **No Auto-Execution**: Trainer files are never automatically run or installed.
3. **Quarantine by Default**: Downloaded files are isolated in a quarantine folder.
4. **Transparent Scanning**: Optional scanner integration returns enumerated results (CLEAN / SUSPICIOUS / ERROR).

### Threat Model

- **Untrusted Remote Files**: All downloaded files are treated as potentially malicious.
- **CSV Injection**: Metadata CSVs are validated for schema and content sanity.
- **File Integrity**: SHA256 checksums are computed and verified.
- **Scanner Integration**: External scanners (Windows Defender, ClamAV) are called as separate processes; no embedded signatures.

### Recommended Security Practices

```
✓ Always run the app in a virtual environment.
✓ Keep network updates off unless you trust the source.
✓ If you download a trainer, keep it in quarantine/ and scan with your AV before running.
✓ Do not run trainers in online competitive games — doing so may violate ToS and lead to bans.
✓ Review downloaded trainer checksums and source URLs manually.
✓ Keep your antivirus software up to date.
✓ Run the app with minimal privileges.
```

## Configuration

Configuration is stored in `config.json` in the application directory:

```json
{
  "allow_network_updates": false,
  "language": "en",
  "debug_mode": false,
  "trainers_path": "C:\\Users\\YourName\\Trainers",
  "quarantine_path": "C:\\Users\\YourName\\Trainers\\quarantine",
  "auto_scan_downloads": true,
  "scanner_type": "windows_defender"
}
```

### Configuration Options

- **allow_network_updates**: Enable/disable network access for CSV updates.
- **language**: UI language ("en" or "zh").
- **debug_mode**: Enable debug logging.
- **trainers_path**: Directory for trainer files.
- **quarantine_path**: Directory for downloaded files awaiting approval.
- **auto_scan_downloads**: Automatically scan files with configured scanner.
- **scanner_type**: Scanner to use ("windows_defender" or "clamav").

## Logging

Logs are written to `trainer_manager.log` with rotating file handler (5 MB max, 3 backups).

Enable debug logging by setting `debug_mode: true` in `config.json`.

## Testing

Run the test suite:

```bash
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

## Building for Distribution

### PyInstaller Build

```bash
pyinstaller build/build.spec
```

Output: `dist/GameTrainerManager.exe`

### Portable Zip

```powershell
.\build\package.ps1
```

Output: `GameTrainerManager-portable.zip`

## Project Structure

```
game-trainer-manager/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── config.json             # Configuration (auto-generated)
├── trainer_manager.log     # Application log
├── app/
│   ├── core/
│   │   ├── config.py       # Configuration management
│   │   ├── logger.py       # Logging setup
│   │   ├── metadata.py     # CSV metadata management
│   │   ├── security.py     # Security & scanning
│   │   └── trainer_manager.py  # File operations
│   ├── ui/
│   │   ├── main_window.py  # Main GUI window
│   │   └── translations.py # Multi-language support
│   └── resources/
│       ├── trainers_list.csv
│       ├── game_names_merged.csv
│       └── abbreviation.csv
├── tests/
│   ├── test_config.py
│   ├── test_metadata.py
│   ├── test_security.py
│   └── test_trainer_manager.py
└── build/
    ├── build.spec          # PyInstaller spec
    └── package.ps1         # Packaging script
```

## Metadata CSV Format

### trainers_list.csv

```csv
name,game,version,author,url,checksum
Example Trainer,Example Game,1.0,Author,https://example.com,abc123...
```

### game_names_merged.csv

```csv
game_id,game_name,platform
1,Example Game,PC
```

### abbreviation.csv

```csv
abbreviation,full_name
EG,Example Game
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Disclaimer

**This application is provided as-is for educational purposes only.** Users are responsible for:

- Ensuring compliance with applicable laws and game ToS.
- Verifying the safety of downloaded trainer files.
- Understanding the risks of using trainers in online games.
- Keeping their system secure and antivirus software updated.

The developers assume no liability for misuse, data loss, or game account bans resulting from trainer use.

## Support

For issues, feature requests, or questions:

1. Check the [SECURITY.md](SECURITY.md) for security-related guidance.
2. Review existing GitHub issues.
3. Open a new issue with detailed information.

## Acknowledgments

Inspired by [Karasukaigan/game-trainer-manager](https://github.com/Karasukaigan/game-trainer-manager).

---

**Last Updated**: 2025  
**Version**: 1.0.0
"# Trainer-Manager" 
