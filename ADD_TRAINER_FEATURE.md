# Add Trainer Feature Documentation

**Feature**: Manual Trainer File Addition  
**Status**: ✅ Implemented  
**Version**: 1.1.0  
**Date**: 2025

---

## 📋 Overview

The **Add Trainer** feature allows users to manually add .exe trainer files to the application through a file browser dialog. This provides an alternative to downloading trainers from external sources.

---

## ✨ Features

### User Interface
- ✅ **"Add Trainer" Button** - Prominent button in the action bar
- ✅ **File Browser Dialog** - Easy file selection
- ✅ **File Filtering** - Shows only .exe files by default
- ✅ **Success/Error Messages** - Clear user feedback
- ✅ **Auto-Refresh** - Trainer list updates automatically

### Functionality
- ✅ **Add Single File** - Add one trainer at a time
- ✅ **Validation** - Only .exe files accepted
- ✅ **Duplicate Detection** - Prevents adding same file twice
- ✅ **File Preservation** - Original file content preserved
- ✅ **Error Handling** - Clear error messages for failures

### Security
- ✅ **No Auto-Execution** - Files are never automatically run
- ✅ **File Validation** - Only .exe files accepted
- ✅ **Duplicate Prevention** - Can't add same file twice
- ✅ **Logging** - All operations logged
- ✅ **User Confirmation** - Success/error dialogs shown

---

## 🎯 How to Use

### Step 1: Click "Add Trainer" Button
Located in the action bar at the bottom of the trainer list panel.

```
[Add Trainer] [Open Folder] [Download] [Launch Steam] [Delete] [Settings]
```

### Step 2: Select .exe File
A file browser dialog opens:
- Navigate to your trainer file location
- Select the .exe file you want to add
- Click "Open"

### Step 3: Confirmation
- Success message shows: "Trainer added: filename.exe"
- Trainer list automatically updates
- Trainer appears in the selected game's trainer list

---

## 📝 Implementation Details

### UI Component
**File**: `app/ui/main_window.py`

```python
def on_add_trainer(self):
    """Handle adding a new trainer file."""
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Executable Files (*.exe);;All Files (*)")
    file_dialog.setDefaultSuffix("exe")
    
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            source_path = Path(selected_files[0])
            success, message = self.trainer_manager.add_trainer(source_path)
            
            if success:
                logger.info(f"Trainer added: {source_path.name}")
                QMessageBox.information(self, "Success", message)
                self.on_game_selected()
            else:
                logger.error(f"Failed to add trainer: {message}")
                QMessageBox.warning(self, "Error", message)
```

### Core Logic
**File**: `app/core/trainer_manager.py`

```python
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
```

---

## 🔒 Security Considerations

### Safe by Design
✅ **No Auto-Execution** - Files are copied, never executed  
✅ **File Type Validation** - Only .exe files accepted  
✅ **Duplicate Prevention** - Can't overwrite existing files  
✅ **User Control** - User explicitly selects file  
✅ **Clear Feedback** - User sees success/error messages  

### Best Practices
✅ **Scan Before Adding** - User should scan file with antivirus first  
✅ **Verify Source** - Ensure file comes from trusted source  
✅ **Check Checksums** - Compare SHA256 if available  
✅ **Review Metadata** - Check trainer info before running  

---

## 🧪 Testing

### Test Coverage
**File**: `tests/test_add_trainer.py`

```python
# 8 comprehensive tests:
✅ test_add_exe_file - Add valid .exe file
✅ test_add_multiple_trainers - Add multiple files
✅ test_add_non_exe_file - Reject non-.exe files
✅ test_add_duplicate_trainer - Prevent duplicates
✅ test_add_nonexistent_file - Handle missing files
✅ test_add_preserves_file_content - Verify content
✅ test_add_trainer_with_special_chars - Handle special names
```

### Run Tests
```bash
pytest tests/test_add_trainer.py -v
```

---

## 📊 User Workflow

### Scenario 1: Add Downloaded Trainer
```
1. User downloads trainer.exe from browser
2. Clicks "Add Trainer" button
3. Selects trainer.exe from Downloads folder
4. Trainer is copied to trainers folder
5. Trainer appears in game's trainer list
6. User can now manage the trainer
```

### Scenario 2: Add Trainer from USB/External Drive
```
1. User connects USB drive with trainers
2. Clicks "Add Trainer" button
3. Navigates to USB drive
4. Selects trainer.exe
5. Trainer is copied to trainers folder
6. Trainer is now available locally
```

### Scenario 3: Add Multiple Trainers
```
1. User has multiple trainer files
2. Clicks "Add Trainer" for each file
3. Each trainer is added individually
4. All trainers appear in trainer list
5. User can manage all trainers
```

---

## ⚙️ Configuration

### File Dialog Settings
- **File Mode**: Single file selection
- **Name Filter**: "Executable Files (*.exe);;All Files (*)"
- **Default Suffix**: ".exe"
- **Start Directory**: User's home directory (default)

### Validation Rules
- ✅ File must exist
- ✅ File must have .exe extension
- ✅ File must not already exist in trainers folder
- ✅ File must be readable

---

## 🐛 Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Source file not found" | File doesn't exist | Check file path |
| "Only .exe files are supported" | Wrong file type | Select .exe file |
| "Trainer already exists" | File already added | Use different file |
| "Failed to add trainer" | Permission/disk error | Check permissions |

### Error Messages
All errors are displayed to the user with:
- Clear error title
- Descriptive error message
- Suggestion for resolution

---

## 📈 Future Enhancements

### Planned Features
- [ ] Batch add multiple files at once
- [ ] Drag-and-drop file addition
- [ ] Auto-scan added files with antivirus
- [ ] Add trainer metadata (name, version, author)
- [ ] Organize trainers by category
- [ ] Add trainer notes/comments

### Possible Improvements
- [ ] Remember last used directory
- [ ] Add recent files list
- [ ] Show file size before adding
- [ ] Preview trainer info
- [ ] Undo/redo functionality

---

## 📝 Logging

### Log Entries
All add trainer operations are logged:

```
2025-01-15 10:30:45,123 - app.ui.main_window - INFO - Trainer added: trainer.exe
2025-01-15 10:30:46,456 - app.core.trainer_manager - INFO - Added trainer: trainer.exe
```

### Debug Mode
Enable debug mode in config.json to see detailed logs:

```json
{
  "debug_mode": true
}
```

---

## 🔄 Integration with Other Features

### Works With
- ✅ **Trainer List** - Added trainers appear in list
- ✅ **Search** - Added trainers are searchable
- ✅ **Delete** - Added trainers can be deleted
- ✅ **Rename** - Added trainers can be renamed
- ✅ **Move** - Added trainers can be moved
- ✅ **Security** - SHA256 checksums computed
- ✅ **Logging** - All operations logged

---

## 📚 Related Features

### Download Trainer
- Opens source URL in browser
- User manually downloads file
- User uses "Add Trainer" to add it

### Quarantine Workflow
- Downloaded files go to quarantine folder
- User can scan with antivirus
- User moves to trainers folder when approved

### Manual Update
- Updates metadata from CSV files
- Doesn't affect added trainers
- Added trainers remain in place

---

## ✅ Checklist

### For Users
- [ ] Read this documentation
- [ ] Understand security implications
- [ ] Scan files before adding
- [ ] Verify trainer sources
- [ ] Keep backups of important trainers

### For Developers
- [x] Implement UI button
- [x] Implement file dialog
- [x] Implement validation
- [x] Implement error handling
- [x] Write tests
- [x] Write documentation
- [ ] Add to release notes
- [ ] Update README

---

## 📞 Support

### Questions?
- Check this documentation
- Review test cases for examples
- Check application logs
- Review SECURITY.md for security info

### Issues?
- Check error message
- Review logs in trainer_manager.log
- Verify file is valid .exe
- Try with different file

---

## 📄 Version History

### v1.1.0 (Current)
- ✅ Initial implementation
- ✅ File browser dialog
- ✅ Validation and error handling
- ✅ Comprehensive tests
- ✅ Full documentation

---

**Feature Documentation**: 2025  
**Version**: 1.0.0  
**Status**: ✅ Complete
