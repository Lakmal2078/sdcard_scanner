#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - SDCard Scanner ව්‍යාපෘතියේ ප්‍රධාන entry point.

සියලුම මොඩියුල ඒකාබද්ධ කරමින් සම්පූර්ණ scanning සහ report generation
ක්‍රියාවලිය මෙහෙයවයි.

Author: Lakmal
Version: 3.0.0
"""

import sys
import os
from typing import List, Dict, Any

from constants import APP_NAME, APP_VERSION, APP_AUTHOR
from cli import parse_arguments
from scanner import scan_directory_fast
from duplicates import find_duplicates_parallel
from report_generator import generate_html_report, export_to_csv, export_to_json
from utils import format_size, ensure_directory


def print_banner() -> None:
    """යෙදුමේ banner එක මුද්‍රණය කරයි"""
    print("=" * 65)
    print(f"📱 {APP_NAME} v{APP_VERSION} — Advanced Storage Report")
    print(f"   සාදන ලද්දේ {APP_AUTHOR} විසින්")
    print("=" * 65)


def print_config(args) -> None:
    """වින්‍යාස තොරතුරු මුද්‍රණය කරයි"""
    print(f"📂 Scan මාර්ගය   : {args.path}")
    print(f"💾 Output මාර්ගය  : {args.output}")
    print(f"📋 ආකෘතිය       : {', '.join(f.upper() for f in args.format)}")
    print(f"🏆 Top ගොනු       : {args.top}")
    print(f"🕰️  පැරණි දින සීමාව: {args.old_days}")
    print(f"⚡ Workers        : {args.workers}")
    print(f"🚫 ඩුප්ලිකේට්     : {'අක්‍රිය' if args.no_duplicates else 'සක්‍රිය'}")
    if args.exclude_list:
        print(f"🔕 Exclusions     : {', '.join(args.exclude_list)}")
    print("=" * 65)


def main() -> None:
    """
    ප්‍රධාන ක්‍රියාකාරීත්වය මෙහෙයවයි.
    
    ක්‍රියාවලිය:
    1. Arguments parse කිරීම
    2. Directory scanning
    3. Duplicate detection (සක්‍රිය නම්)
    4. Report generation
    """
    # Arguments parse කිරීම
    args = parse_arguments()
    
    # Output බහාලුම සහතික කිරීම
    if not ensure_directory(args.output):
        print(f"⚠️ දෝෂය: Output බහාලුම සෑදිය නොහැක: {args.output}")
        sys.exit(1)
    
    # Banner සහ config මුද්‍රණය
    print_banner()
    print_config(args)
    
    # පියවර 1: Scan කිරීම
    files_data: List[Dict[str, Any]]
    skipped: int
    files_data, skipped = scan_directory_fast(
        target_path=args.path,
        extra_exclude=args.exclude_list,
        show_progress=not args.no_progress
    )
    
    if not files_data:
        print("\n⚠️ කිසිදු ගොනුවක් හමු නොවීය.")
        sys.exit(0)
    
    total_size: int = sum(f["size"] for f in files_data)
    print(f"\n✅ සාර්ථකව scan කරන ලදී:")
    print(f"   ෆයිල් ගණන     : {len(files_data):,}")
    print(f"   සම්පූර්ණ ප්‍රමාණය : {format_size(total_size)}")
    print(f"   මග හැරි ගොනු  : {skipped}")
    
    # පියවර 2: ඩුප්ලිකේට් සොයා ගැනීම
    duplicates: List[Dict[str, Any]] = []
    if not args.no_duplicates:
        duplicates = find_duplicates_parallel(
            files_data=files_data,
            max_workers=args.workers,
            show_progress=not args.no_progress
        )
        if duplicates:
            wasted: int = sum(d["size"] * (d["count"] - 1) for d in duplicates)
            print(f"\n🔁 ඩුප්ලිකේට් කාණ්ඩ {len(duplicates)}ක් හමුවිය.")
            print(f"   අපතේ යන මුළු ඉඩ: {format_size(wasted)}")
        else:
            print(f"\n✅ ඩුප්ලිකේට් ගොනු හමු නොවීය.")
    else:
        print("\n⏭️  ඩුප්ලිකේට් පරීක්ෂාව අක්‍රියයි.")
    
    # පියවර 3: වාර්තා ජනනය
    print(f"\n📊 වාර්තා සාදමින්...")
    for fmt in args.format:
        if fmt == "html":
            out = generate_html_report(
                files_data=files_data,
                duplicates=duplicates,
                skipped=skipped,
                target_path=args.path,
                output_dir=args.output,
                top_n=args.top,
                old_days=args.old_days
            )
            if out:
                print(f"   ✅ HTML වාර්තාව: {out}")
        elif fmt == "csv":
            out = export_to_csv(files_data, args.output)
            if out:
                print(f"   ✅ CSV වාර්තාව : {out}")
        elif fmt == "json":
            out = export_to_json(files_data, duplicates, args.output)
            if out:
                print(f"   ✅ JSON වාර්තාව: {out}")
    
    print("\n" + "=" * 65)
    print("✅ සියලුම කාර්යයන් සාර්ථකව අවසන් විය!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ පරිශීලකයා විසින් ක්‍රියාවලිය අවලංගු කරන ලදී.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ අනපේක්ෂිත දෝෂයක් ඇතිවිය: {e}")
        sys.exit(1)
