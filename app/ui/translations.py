"""Multi-language support for Game Trainer Manager."""

import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

class Translator:
    """Handles multi-language translations."""
    
    TRANSLATIONS = {
        "en": {
            "title": "Game Trainer Manager",
            "games": "Games",
            "trainers": "Trainers",
            "search": "Search...",
            "add": "Add",
            "remove": "Remove",
            "rename": "Rename",
            "open_folder": "Open Folder",
            "download": "Download",
            "download_quarantine": "Download & Quarantine",
            "open_browser": "Open in Browser",
            "delete": "Delete",
            "settings": "Settings",
            "language": "Language",
            "allow_network": "Allow Network Updates",
            "auto_scan": "Auto-scan Downloads",
            "scanner": "Scanner Type",
            "quarantine_path": "Quarantine Path",
            "trainers_path": "Trainers Path",
            "update_metadata": "Update Metadata",
            "manual_update": "Manual Update",
            "auto_update": "Enable Auto Update",
            "version": "Version",
            "author": "Author",
            "url": "URL",
            "checksum": "Checksum",
            "scan_result": "Scan Result",
            "clean": "Clean",
            "suspicious": "Suspicious",
            "error": "Error",
            "not_scanned": "Not Scanned",
            "confirm_delete": "Are you sure you want to delete this trainer?",
            "confirm_run": "WARNING: Running trainers in online games may violate ToS and lead to bans. Continue?",
            "file_not_found": "File not found",
            "operation_success": "Operation completed successfully",
            "operation_failed": "Operation failed",
            "about": "About",
            "help": "Help",
            "exit": "Exit",
            "disclaimer": "This application is for educational purposes. Use trainers responsibly.",
        },
        "zh": {
            "title": "游戏训练器管理器",
            "games": "游戏",
            "trainers": "训练器",
            "search": "搜索...",
            "add": "添加",
            "remove": "移除",
            "rename": "重命名",
            "open_folder": "打开文件夹",
            "download": "下载",
            "download_quarantine": "下载并隔离",
            "open_browser": "在浏览器中打开",
            "delete": "删除",
            "settings": "设置",
            "language": "语言",
            "allow_network": "允许网络更新",
            "auto_scan": "自动扫描下载",
            "scanner": "扫描器类型",
            "quarantine_path": "隔离路径",
            "trainers_path": "训练器路径",
            "update_metadata": "更新元数据",
            "manual_update": "手动更新",
            "auto_update": "启用自动更新",
            "version": "版本",
            "author": "作者",
            "url": "URL",
            "checksum": "校验和",
            "scan_result": "扫描结果",
            "clean": "干净",
            "suspicious": "可疑",
            "error": "错误",
            "not_scanned": "未扫描",
            "confirm_delete": "确定要删除此训练器吗？",
            "confirm_run": "警告：在在线游戏中运行训练器可能违反服务条款并导致封禁。继续？",
            "file_not_found": "文件未找到",
            "operation_success": "操作完成成功",
            "operation_failed": "操作失败",
            "about": "关于",
            "help": "帮助",
            "exit": "退出",
            "disclaimer": "此应用程序仅用于教育目的。请负责任地使用训练器。",
        }
    }
    
    def __init__(self, language: str = "en"):
        self.language = language if language in self.TRANSLATIONS else "en"
    
    def set_language(self, language: str):
        """Set active language."""
        if language in self.TRANSLATIONS:
            self.language = language
        else:
            logger.warning(f"Language not supported: {language}")
    
    def get(self, key: str, default: str = "") -> str:
        """Get translated string."""
        return self.TRANSLATIONS[self.language].get(key, default)
    
    def __call__(self, key: str) -> str:
        """Allow translator to be called as a function."""
        return self.get(key)
