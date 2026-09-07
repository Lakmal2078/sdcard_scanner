#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
duplicates.py - ThreadPoolExecutor භාවිතා කරමින් සමාන්තර ඩුප්ලිකේට් ගොනු හඳුනාගැනීම.
"""

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Tuple, Optional

try:
    from tqdm import tqdm
    HAS_TQDM: bool = True
except ImportError:
    HAS_TQDM = False

from utils import get_file_hash, format_size


def find_duplicates_parallel(
    files_data: List[Dict[str, Any]],
    max_workers: int = 4,
    show_progress: bool = True
) -> List[Dict[str, Any]]:
    """
    ThreadPoolExecutor භාවිතා කරමින් සමාන්තර ඩුප්ලිකේට් හඳුනාගැනීම.
    
    Args:
        files_data: scan කරන ලද ගොනු ලැයිස්තුව
        max_workers: සමාන්තර thread ගණන
        show_progress: progress bar පෙන්විය යුතු ද
    
    Returns:
        ඩුප්ලිකේට් කාණ්ඩ ලැයිස්තුව
    """
    print("\n🔎 ඩුප්ලිකේට් ගොනු පරීක්ෂා කරමින්...")
    
    # පියවර 1: ප්‍රමාණය අනුව කාණ්ඩ කිරීම
    size_to_files: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    for f in files_data:
        if f["size"] > 0:
            size_to_files[f["size"]].append(f)
    
    # පියවර 2: Hash කළ යුතු අපේක්ෂකයින් හඳුනාගැනීම
    candidates: List[Dict[str, Any]] = [
        f for files in size_to_files.values()
        if len(files) > 1 for f in files
    ]
    
    if not candidates:
        print("   ✅ ඩුප්ලිකේට් පරීක්ෂාවට අපේක්ෂකයින් නොමැත.")
        return []
    
    print(f"   📦 Hash කළ යුතු ගොනු: {len(candidates):,}")
    
    # පියවර 3: සමාන්තර Hash ගණනය
    def hash_file(file_info: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[str]]:
        """තනි ගොනුවක hash ගණනය කරයි"""
        file_hash: Optional[str] = get_file_hash(file_info["path"])
        return file_info, file_hash
    
    hash_results: List[Tuple[Dict[str, Any], Optional[str]]] = []
    workers: int = min(max_workers, len(candidates))
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(hash_file, f) for f in candidates]
        
        if show_progress and HAS_TQDM:
            for future in tqdm(as_completed(futures),
                               total=len(futures),
                               desc="🔐 Hashing",
                               unit="file",
                               ncols=80):
                result: Tuple[Dict[str, Any], Optional[str]] = future.result()
                if result[1]:
                    hash_results.append(result)
        else:
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result[1]:
                    hash_results.append(result)
                if show_progress and i % 50 == 0:
                    print(f"\r   Progress: {i}/{len(futures)}", end="", flush=True)
            if show_progress:
                print()
    
    # පියවර 4: Hash අනුව කාණ්ඩ කිරීම
    hash_to_files: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for file_info, file_hash in hash_results:
        hash_to_files[file_hash].append(file_info)
    
    # පියවර 5: ඩුප්ලිකේට් ලැයිස්තුගත කිරීම
    duplicates: List[Dict[str, Any]] = []
    for hash_val, dup_files in hash_to_files.items():
        if len(dup_files) > 1:
            size: int = dup_files[0]["size"]
            duplicates.append({
                "size": size,
                "size_formatted": format_size(size),
                "count": len(dup_files),
                "files": [f["path"] for f in dup_files]
            })
    
    # විශාලතම ඩුප්ලිකේට් කාණ්ඩ පළමුව
    duplicates.sort(key=lambda x: x["size"] * x["count"], reverse=True)
    return duplicates
