#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py - ව්‍යාපෘතියේ නියතයන් සහ පෙරනිමි සැකසුම් අඩංගු මොඩියුලය.
"""

from typing import Dict, Set, List

# ============================================================
# ගොනු ප්‍රවර්ගීකරණය (File Categories)
# ============================================================
FILE_CATEGORIES: Dict[str, Set[str]] = {
    "🖼️ Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".raw"},
    "🎥 Videos": {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".m4v", ".3gp"},
    "🎵 Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"},
    "📄 Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf", ".odt"},
    "📦 Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "📱 APKs": {".apk", ".xapk", ".apkm"},
    "🎮 Games Data": {".obb", ".pak", ".unity3d"},
    "📝 Logs": {".log"},
    "🗜️ Databases": {".db", ".sqlite", ".sql", ".mdb"},
    "📁 Others": set()
}

# ============================================================
# ස්වයංක්‍රීයව මග හැරිය යුතු බහාලුම් (Auto-Skip Directories)
# ============================================================
SKIP_DIRS: Set[str] = {
    '.Trash', '.thumbnails', '.nomedia', 'Android', 'LOST.DIR',
    '.git', '.svn', 'node_modules', '__pycache__', '.cache',
    '.gradle', '.idea', '.vscode', 'System Volume Information',
    '$RECYCLE.BIN', 'Recovery'
}

# ============================================================
# ස්වයංක්‍රීයව මග හැරිය යුතු ගොනු (Auto-Skip Files)
# ============================================================
SKIP_FILES: Set[str] = {
    '.nomedia', '.DS_Store', 'Thumbs.db', 'desktop.ini',
    '.hidden', '.Trashes'
}

# ============================================================
# පෙරනිමි සැකසුම් (Default Settings)
# ============================================================
DEFAULT_SCAN_PATH: str = "/sdcard/"
DEFAULT_OUTPUT_DIR: str = "/sdcard/Download/"
DEFAULT_TOP_FILES: int = 20
DEFAULT_OLD_FILE_DAYS: int = 365
DEFAULT_WORKERS: int = 4
DEFAULT_FORMATS: List[str] = ["html"]

# ============================================================
# වාර්තා ආකෘති (Report Formats)
# ============================================================
SUPPORTED_FORMATS: List[str] = ["html", "csv", "json"]

# ============================================================
# Version Information
# ============================================================
APP_NAME: str = "SDCard Scanner"
APP_VERSION: str = "3.0.0"
APP_AUTHOR: str = "Lakmal"
