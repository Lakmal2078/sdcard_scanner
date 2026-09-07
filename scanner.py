#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scanner.py - os.scandir() සහ tqdm භාවිතා කරමින් වේගවත් බහාලුම් scanning සිදු කරයි.
"""

import os
from collections import deque
from typing import List, Dict, Any, Tuple, Optional, Set

try:
    from tqdm import tqdm
    HAS_TQDM: bool = True
except ImportError:
    HAS_TQDM = False

from constants import SKIP_DIRS, SKIP_FILES
from utils import get_file_info


def should_skip_dir(dirname: str) -> bool:
    """
    බහාලුමක් මග හැරිය යුතු දැයි තීරණය කරයි.
    
    Args:
        dirname: බහාලුමේ නම
    
    Returns:
        මග හැරිය යුතු නම් True
    """
    return dirname in SKIP_DIRS or dirname.startswith('.')


def should_skip_file(filename: str) -> bool:
    """
    ගොනුවක් මග හැරිය යුතු දැයි තීරණය කරයි.
    
    Args:
        filename: ගොනුවේ නම
    
    Returns:
        මග හැරිය යුතු නම් True
    """
    return filename in SKIP_FILES


def scan_directory_fast(
    target_path: str,
    extra_exclude: Optional[Set[str]] = None,
    show_progress: bool = True
) -> Tuple[List[Dict[str, Any]], int]:
    """
    os.scandir() භාවිතා කරමින් වේගවත් recursive scanning සිදු කරයි.
    
    Args:
        target_path: scan කළ යුතු මූලික බහාලුම
        extra_exclude: අමතරව මග හැරිය යුතු බහාලුම්/ගොනු
        show_progress: progress bar පෙන්විය යුතු ද
    
    Returns:
        Tuple[files_data, skipped_count]
        - files_data: scan කරන ලද ගොනු ලැයිස්තුව
        - skipped_count: මග හරින ලද ගොනු/බහාලුම් ගණන
    """
    files_data: List[Dict[str, Any]] = []
    skipped: int = 0
    files_scanned: int = 0
    
    # Custom exclusion list ඒකාබද්ධ කිරීම
    custom_skip_dirs: Set[str] = SKIP_DIRS.copy()
    custom_skip_files: Set[str] = SKIP_FILES.copy()
    if extra_exclude:
        for item in extra_exclude:
            if os.path.isdir(item):
                custom_skip_dirs.add(os.path.basename(item))
            else:
                custom_skip_files.add(os.path.basename(item))
    
    dirs_to_scan: deque = deque([target_path])
    
    # tqdm progress bar setup
    pbar = None
    if show_progress and HAS_TQDM:
        pbar = tqdm(
            desc="🔍 Scanning",
            unit="file",
            ncols=80,
            bar_format='{l_bar}{bar}| {n_fmt}/{postfix[0]} [{elapsed}<{remaining}]',
            postfix=["0 files"]
        )
    
    try:
        while dirs_to_scan:
            current_path: str = dirs_to_scan.popleft()
            try:
                with os.scandir(current_path) as entries:
                    for entry in entries:
                        try:
                            if entry.is_file(follow_symlinks=False):
                                # Skip files check
                                if entry.name in custom_skip_files:
                                    skipped += 1
                                    continue
                                
                                file_info: Optional[Dict[str, Any]] = get_file_info(entry.path)
                                if file_info:
                                    files_data.append(file_info)
                                    files_scanned += 1
                                    
                                    if pbar:
                                        pbar.update(1)
                                        pbar.postfix[0] = f"{files_scanned:,} files"
                                    elif show_progress and files_scanned % 100 == 0:
                                        print(f"\r🔍 Scanning: {files_scanned:,} files",
                                              end="", flush=True)
                                        
                            elif entry.is_dir(follow_symlinks=False):
                                if not should_skip_dir(entry.name) and \
                                   entry.name not in custom_skip_dirs:
                                    dirs_to_scan.append(entry.path)
                                else:
                                    skipped += 1
                        except (PermissionError, OSError):
                            skipped += 1
                            continue
            except (PermissionError, OSError):
                skipped += 1
                continue
    finally:
        if pbar:
            pbar.close()
        elif show_progress and not HAS_TQDM:
            print()
    
    return files_data, skipped
