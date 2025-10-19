# Game Trainer Manager - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

The GUI should open immediately. That's it!

---

## 🎮 Basic Usage

### Search for a Game
1. Type game name in the search box (left pane)
2. Results filter in real-time
3. Click a game to see its trainers

### Download a Trainer
1. Select a trainer from the list
2. Click **Download** button
3. Your browser opens the source URL
4. Manually download the file

### Manage Trainers
- **Open Folder**: Opens trainer directory in File Explorer
- **Delete**: Removes trainer (with confirmation)
- **Settings**: Configure language, paths, scanning

---

## 🔒 Security First

### Default Safe Behavior
✓ **Local-only** - No network access by default  
✓ **No auto-run** - Never automatically executes .exe files  
✓ **Quarantine** - Downloaded files isolated before approval  
✓ **Scanning** - Optional Windows Defender/ClamAV integration  

### Before Running Any Trainer
1. Keep it in the quarantine folder
2. Scan with your antivirus
3. Review the checksum
4. Only then move to trainers folder

---

## ⚙️ Configuration

### First Launch
- `config.json` is created automatically
- Default settings are safe and conservative
- Modify settings via the Settings dialog

### Key Settings
| Setting | Default | What It Does |
|---------|---------|--------------|
| Allow Network Updates | OFF | Enable only if updating from trusted source |
| Auto-scan Downloads | ON | Automatically scan files with Windows Defender |
| Language | English | Switch to Simplified Chinese (中文) |
| Quarantine Path | ~/Trainers/quarantine | Where downloaded files go |
| Trainers Path | ~/Trainers | Where approved trainers are stored |

---

## 📁 File Locations

```
Windows:
  Trainers: C:\Users\YourName\Trainers
  Quarantine: C:\Users\YourName\Trainers\quarantine
  Config: config.json (app directory)
  Logs: trainer_manager.log (app directory)
```

---

## 🧪 Running Tests

### All Tests
```bash
pytest tests/ -v
```

### With Coverage
```bash
pytest tests/ --cov=app
```

### Specific Test File
```bash
pytest tests/test_security.py -v
```

**Expected Result**: ✓ 35 passed in ~0.3 seconds

---

## 🏗️ Building Executable

### Prerequisites
```bash
pip install pyinstaller
```

### Build
```bash
pyinstaller build/build.spec
```

### Output
```
dist/GameTrainerManager/GameTrainerManager.exe
```

### Create Portable ZIP
```powershell
.\build\package.ps1
```

Output: `GameTrainerManager-portable.zip`

---

## 🐛 Troubleshooting

### Issue: "No module named PySide6"
**Solution**: `pip install PySide6==6.10.0`

### Issue: Application won't start
**Solution**: Check `trainer_manager.log` for error messages

### Issue: Can't find trainers folder
**Solution**: Configure path in Settings dialog

### Issue: Antivirus blocks download
**Solution**: This is normal! Add to quarantine folder manually

---

## 📚 Documentation

- **README.md** - Full user guide
- **SECURITY.md** - Security model and threat analysis
- **BUILD_INSTRUCTIONS.md** - Detailed build guide
- **MANIFEST.md** - Complete file listing
- **PROJECT_SUMMARY.md** - Project overview

---

## ✅ Security Checklist

Before using trainers:

- [ ] Run app in virtual environment
- [ ] Keep network updates OFF unless needed
- [ ] Enable auto-scan in settings
- [ ] Scan downloaded files with antivirus
- [ ] Review checksums manually
- [ ] Never run trainers in online games
- [ ] Keep antivirus software updated

---

## 🎯 Common Workflows

### Workflow 1: Add a New Trainer
1. Download trainer to quarantine folder (manually)
2. App auto-scans (if enabled)
3. Review scan result
4. Move file to trainers folder
5. Update metadata CSV if needed

### Workflow 2: Search for Trainers
1. Open app
2. Type game name in search box
3. Select game from results
4. View trainers for that game
5. Click Download to open source URL

### Workflow 3: Change Language
1. Click Settings button
2. Select "中文" (Chinese) from Language dropdown
3. Click OK
4. UI updates to Chinese

---

## 📞 Getting Help

### Check These First
1. **README.md** - Most common questions answered
2. **SECURITY.md** - Security concerns
3. **trainer_manager.log** - Error messages
4. **Tests** - Usage examples in test files

### Report Issues
1. Check existing GitHub issues
2. Provide error message from log
3. Describe steps to reproduce
4. Include your OS version

---

## 🚀 Next Steps

### For Users
1. ✓ Install dependencies
2. ✓ Run application
3. ✓ Configure settings
4. ✓ Add your first trainer
5. ✓ Review security practices

### For Developers
1. ✓ Review code structure
2. ✓ Run test suite
3. ✓ Read SECURITY.md
4. ✓ Check MANIFEST.md
5. ✓ Build executable

---

## 📋 Feature Summary

### ✓ Implemented
- Local trainer file management
- CSV metadata parsing
- Multi-language UI (EN, ZH)
- SHA256 checksum verification
- Windows Defender/ClamAV integration
- Quarantine workflow
- Settings configuration
- Search and filtering
- Comprehensive logging
- Full test coverage

### ⏳ Future
- Automatic metadata updates
- Game process detection
- Trainer versioning
- Dark mode UI
- Additional languages

---

## 💡 Pro Tips

1. **Organize by Game**: Create subfolders in trainers directory
2. **Regular Backups**: Backup your trainers folder periodically
3. **Check Logs**: Review `trainer_manager.log` for insights
4. **Verify Checksums**: Always compare downloaded file checksums
5. **Update Antivirus**: Keep Windows Defender or ClamAV updated
6. **Read Disclaimers**: Understand risks before using trainers
7. **Test Offline**: Verify app works without network access

---

## ⚠️ Important Warnings

🚫 **DO NOT**
- Run trainers in online competitive games
- Ignore antivirus warnings
- Share trainers without verifying safety
- Disable security features
- Run app with admin privileges unless necessary

✅ **DO**
- Keep trainers in quarantine until verified
- Scan with multiple antivirus tools
- Review checksums manually
- Keep security features enabled
- Run in virtual environment

---

## 📞 Support Resources

| Resource | Purpose |
|----------|---------|
| README.md | User guide and features |
| SECURITY.md | Security model and threat analysis |
| BUILD_INSTRUCTIONS.md | Building from source |
| trainer_manager.log | Application logs and errors |
| Tests | Code examples and usage |

---

## 🎓 Learning Resources

### Understanding the Code
1. Start with `main.py` - Entry point
2. Review `app/core/` - Business logic
3. Check `app/ui/` - GUI components
4. Read `tests/` - Usage examples

### Security Deep Dive
1. Read SECURITY.md - Threat model
2. Review `app/core/security.py` - Implementation
3. Check test cases - Security testing

### Building & Distribution
1. Read BUILD_INSTRUCTIONS.md
2. Review `build/build.spec` - PyInstaller config
3. Check `build/package.ps1` - Packaging script

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**Status**: ✅ Production Ready

For detailed information, see **README.md** or **SECURITY.md**
