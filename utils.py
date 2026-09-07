#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py - ව්‍යාපෘතියේ පොදු උපකාරී ශ්‍රිත අඩංගු මොඩියුලය.
"""

import os
import time
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List

from constants import FILE_CATEGORIES


def get_category(filename: str) -> str:
    """
    ගොනුවක නම අනුව එහි ප්‍රවර්ගය නිර්ණය කරයි.
    
    Args:
        filename: ගොනුවේ නම (උදා: "photo.jpg")
    
    Returns:
        ගොනුවේ ප්‍රවර්ගය (උදා: "🖼️ Images")
    """
    ext: str = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "📁 Others"


def get_file_hash(filepath: str, chunk_size: int = 8192) -> Optional[str]:
    """
    ගොනුවක MD5 Hash අගය ගණනය කරයි.
    
    Args:
        filepath: ගොනුවේ සම්පූර්ණ මාර්ගය
        chunk_size: එකවර කියවන byte ප්‍රමාණය
    
    Returns:
        MD5 hash string හෝ දෝෂයක් ඇති විට None
    """
    hash_md5: hashlib.md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (PermissionError, IOError, OSError):
        return None


def get_file_age_days(filepath: str) -> int:
    """
    ගොනුවේ වයස දින වලින් ගණනය කරයි.
    
    Args:
        filepath: ගොනුවේ සම්පූර්ණ මාර්ගය
    
    Returns:
        ගොනුවේ වයස දින වලින් (දෝෂයක් ඇති විට 0)
    """
    try:
        mtime: float = os.path.getmtime(filepath)
        return int((time.time() - mtime) / (60 * 60 * 24))
    except (OSError, PermissionError):
        return 0


def format_size(size_bytes: int) -> str:
    """
    Bytes අගය පහසුවෙන් කියවිය හැකි ආකාරයට පරිවර්තනය කරයි.
    
    Args:
        size_bytes: byte ප්‍රමාණය
    
    Returns:
        ආකෘතිගත ප්‍රමාණය (උදා: "1.5 GB", "250 MB")
    """
    if size_bytes < 0:
        return "0 B"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def is_valid_path(path: str) -> bool:
    """
    ලබා දී ඇති මාර්ගය වලංගු දැයි පරීක්ෂා කරයි.
    
    Args:
        path: පරීක්ෂා කළ යුතු මාර්ගය
    
    Returns:
        මාර්ගය වලංගු නම් True, නැතනම් False
    """
    return os.path.exists(path) and os.path.isdir(path)


def ensure_directory(path: str) -> bool:
    """
    බහාලුමක් නොමැති නම් එය නිර්මාණය කරයි.
    
    Args:
        path: නිර්මාණය කළ යුතු බහාලුමේ මාර්ගය
    
    Returns:
        සාර්ථක නම් True, නැතනම් False
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except OSError:
        return False


def get_file_info(filepath: str) -> Optional[Dict[str, Any]]:
    """
    ගොනුවක මූලික තොරතුරු ලබා ගනී.
    
    Args:
        filepath: ගොනුවේ සම්පූර්ණ මාර්ගය
    
    Returns:
        ගොනුවේ තොරතුරු අඩංගු dictionary හෝ None
    """
    try:
        stat: os.stat_result = os.stat(filepath)
        return {
            "path": filepath,
            "name": os.path.basename(filepath),
            "size": stat.st_size,
            "category": get_category(os.path.basename(filepath)),
            "age_days": get_file_age_days(filepath),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
        }
    except (PermissionError, OSError):
        return None
