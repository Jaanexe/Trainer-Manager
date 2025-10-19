# Security Model & Threat Analysis

## Executive Summary

Game Trainer Manager is designed with **security-first principles**:

1. **Local-only by default** — no network access unless explicitly enabled.
2. **Never auto-executes** — all .exe files require explicit user action.
3. **Quarantine-first workflow** — downloaded files are isolated and scanned before use.
4. **Transparent scanning** — external scanners are called as separate processes.
5. **Integrity verification** — SHA256 checksums for all files.

---

## Threat Model

### Assets Protected

- **User System**: Prevent malware execution, system compromise.
- **User Data**: Prevent data exfiltration or corruption.
- **Game Accounts**: Prevent unauthorized access or bans from ToS violations.

### Threat Actors

1. **Malicious Trainer Authors**: Distribute trojans, keyloggers, or ransomware.
2. **Man-in-the-Middle (MitM)**: Intercept downloads and inject malware.
3. **Accidental User Error**: User runs unverified trainer in online game.

### Attack Vectors

| Vector | Mitigation |
|--------|-----------|
| Malicious .exe file | Quarantine + optional AV scan before execution |
| Malicious CSV metadata | Schema validation + content sanity checks |
| Network interception | HTTPS for downloads (user responsibility) + checksum verification |
| Auto-execution | No auto-run feature; explicit user confirmation required |
| Privilege escalation | App runs with user privileges only |
| Data exfiltration | Local-only by default; no telemetry |

---

## Security Features

### 1. Local-First Architecture

**Default Behavior**: App operates entirely offline.

```json
{
  "allow_network_updates": false
}
```

- Metadata CSVs are bundled with the application.
- No automatic network requests.
- User must explicitly enable "Allow Network Updates" in Settings.

**Rationale**: Reduces attack surface and respects user privacy.

### 2. Quarantine Workflow

**Process**:

1. User downloads trainer from browser (manual step).
2. File is placed in `quarantine/` folder.
3. App computes SHA256 checksum.
4. Optional: Run configured scanner (Windows Defender or ClamAV).
5. User reviews scan result and manually approves.
6. File moved to main trainers folder.

**Code Example**:

```python
# app/core/security.py
def scan_file(self, file_path: Path) -> Tuple[ScanResult, str]:
    if self.scanner_type == "windows_defender":
        return self._scan_windows_defender(file_path)
    # ...
    return ScanResult.NOT_SCANNED, "Scanner not configured"
```

**Rationale**: Prevents accidental execution of untrusted files.

### 3. SHA256 Integrity Verification

**Process**:

1. Compute SHA256 hash of downloaded file.
2. Compare against expected checksum (from CSV metadata).
3. Warn user if mismatch detected.

**Code Example**:

```python
# app/core/security.py
def verify_checksum(self, file_path: Path, expected_checksum: str) -> bool:
    computed = self.compute_sha256(file_path)
    return computed.lower() == expected_checksum.lower()
```

**Rationale**: Detects file tampering or corruption.

### 4. Optional Scanner Integration

**Supported Scanners**:

- **Windows Defender** (MpCmdRun.exe)
- **ClamAV** (clamscan command)

**Behavior**:

- Scanner is called as a separate process (no embedded signatures).
- Results are enumerated: `CLEAN`, `SUSPICIOUS`, `ERROR`, `NOT_SCANNED`.
- User can choose to proceed even if scanner is unavailable.

**Code Example**:

```python
# app/core/security.py
def _scan_windows_defender(self, file_path: Path) -> Tuple[ScanResult, str]:
    defender_path = Path("C:\\Program Files\\Windows Defender\\MpCmdRun.exe")
    if not defender_path.exists():
        return ScanResult.NOT_SCANNED, "Windows Defender not available"
    
    result = subprocess.run(
        [str(defender_path), "-Scan", "-ScanType", "3", "-File", str(file_path)],
        capture_output=True,
        timeout=60
    )
    return ScanResult.CLEAN if result.returncode == 0 else ScanResult.SUSPICIOUS
```

**Rationale**: Leverages existing system security tools without bundling malware signatures.

### 5. CSV Metadata Validation

**Validation Steps**:

1. Check CSV headers match expected schema.
2. Validate row count and content.
3. Sanitize string fields (no code injection).

**Code Example**:

```python
# app/core/metadata.py
def validate_csv_schema(self, csv_path: Path) -> Tuple[bool, str]:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return False, "CSV has no headers"
        # Validate rows...
        return True, f"Valid CSV with {row_count} rows"
```

**Rationale**: Prevents CSV injection or malformed metadata from crashing the app.

### 6. No Auto-Execution

**Guarantees**:

- No `.exe` file is automatically run.
- No process injection or DLL hooking.
- User must explicitly click a trainer file to launch it.

**Code**: No `subprocess.Popen()` or `os.system()` calls for trainer execution in the codebase.

**Rationale**: Prevents accidental malware execution.

### 7. Minimal Permissions

**App Privileges**:

- Runs with user privileges only (no admin required).
- Reads/writes to user home directory.
- Does not modify system files or registry.

**Rationale**: Limits damage from potential compromise.

---

## Configuration Security

### config.json

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

### Best Practices

- **Keep `allow_network_updates` disabled** unless updating from a trusted source.
- **Enable `auto_scan_downloads`** to automatically scan files.
- **Use `windows_defender`** or `clamav` for scanner type.
- **Do not share `config.json`** if it contains sensitive paths.

---

## Adding Custom Scanners

### Adapter Pattern

To add a new scanner (e.g., VirusTotal API):

1. **Extend `SecurityManager`**:

```python
# app/core/security.py
def _scan_virustotal(self, file_path: Path) -> Tuple[ScanResult, str]:
    # Implement VirusTotal API call
    # Return (ScanResult, message)
    pass

def scan_file(self, file_path: Path) -> Tuple[ScanResult, str]:
    if self.scanner_type == "virustotal":
        return self._scan_virustotal(file_path)
    # ...
```

2. **Update `config.json`**:

```json
{
  "scanner_type": "virustotal"
}
```

3. **Test**:

```bash
pytest tests/test_security.py -v
```

### Security Considerations for Custom Scanners

- **Never hardcode API keys** — use environment variables or secure config files.
- **Validate API responses** — assume responses are untrusted.
- **Handle timeouts gracefully** — don't block the UI.
- **Log all scan results** — for audit trails.

---

## Logging & Audit Trail

### Log File

- **Location**: `trainer_manager.log`
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Rotation**: 5 MB max, 3 backups

### Logged Events

- Application startup/shutdown
- File operations (add, remove, rename, move)
- Metadata loads and updates
- Checksum computations and verifications
- Scanner invocations and results
- Configuration changes

### Example Log

```
2025-01-15 10:30:45,123 - app.core.security - INFO - Computed SHA256 for trainer.exe: abc123...
2025-01-15 10:31:02,456 - app.core.security - INFO - Windows Defender scan clean: trainer.exe
2025-01-15 10:31:15,789 - app.core.trainer_manager - INFO - Added trainer: trainer.exe
```

### Debug Mode

Enable debug logging in `config.json`:

```json
{
  "debug_mode": true
}
```

---

## Incident Response

### If You Suspect Malware

1. **Isolate the file**: Move to quarantine folder immediately.
2. **Scan with multiple AV**: Use Windows Defender + ClamAV if available.
3. **Check logs**: Review `trainer_manager.log` for suspicious activity.
4. **Report**: Contact the trainer author or antivirus vendor.

### If You Experience Game Ban

1. **Do not use trainers in online games** — this violates most game ToS.
2. **Review game logs** — check if trainer was detected.
3. **Contact game support** — explain the situation (though bans are usually permanent).

---

## Compliance & Legal

### User Responsibilities

- **Verify trainer legality**: Ensure trainer use complies with game ToS and local laws.
- **Scan before use**: Always scan downloaded files with antivirus software.
- **Avoid online games**: Do not use trainers in competitive or online multiplayer games.
- **Keep system updated**: Maintain OS and antivirus signatures.

### Disclaimer

This application is provided **as-is** for educational purposes. The developers assume no liability for:

- Game account bans or suspensions.
- System compromise or data loss.
- Legal consequences from trainer use.
- Misuse of the application.

---

## Security Checklist

- [ ] Run app in a virtual environment.
- [ ] Keep `allow_network_updates` disabled by default.
- [ ] Enable `auto_scan_downloads` for automatic scanning.
- [ ] Review downloaded file checksums manually.
- [ ] Scan files with multiple AV tools before running.
- [ ] Never run trainers in online competitive games.
- [ ] Keep antivirus software up to date.
- [ ] Review `trainer_manager.log` regularly.
- [ ] Do not share `config.json` with sensitive paths.
- [ ] Report suspicious trainers to antivirus vendors.

---

## References

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Windows Defender MpCmdRun.exe](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-antivirus/command-line-arguments-windows-defender-antivirus)
- [ClamAV User Manual](https://docs.clamav.net/)

---

**Last Updated**: 2025  
**Version**: 1.0.0
