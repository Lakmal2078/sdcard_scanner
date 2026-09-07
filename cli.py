#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cli.py - Command Line Argument parsing සහ validation සිදු කරයි.
"""

import argparse
import sys
from typing import List, Optional, Set

from constants import (
    APP_NAME, APP_VERSION, DEFAULT_SCAN_PATH, DEFAULT_OUTPUT_DIR,
    DEFAULT_TOP_FILES, DEFAULT_OLD_FILE_DAYS, DEFAULT_WORKERS,
    DEFAULT_FORMATS, SUPPORTED_FORMATS
)
from utils import is_valid_path


def create_parser() -> argparse.ArgumentParser:
    """
    Command Line Argument parser එක නිර්මාණය කරයි.
    
    Returns:
        සැකසූ argparse.ArgumentParser instance එක
    """
    parser = argparse.ArgumentParser(
        prog="sdcard_scanner",
        description=f"📱 {APP_NAME} v{APP_VERSION} — Advanced Storage Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
උදාහරණ:
  python main.py
  python main.py --path /sdcard/DCIM
  python main.py --path /sdcard/ --format html csv json
  python main.py --output /sdcard/Documents/ --top 50
  python main.py --exclude ".cache,temp,backup"
  python main.py --no-duplicates --workers 8
        """
    )
    
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=DEFAULT_SCAN_PATH,
        help=f"Scan කරනු ලබන බහාලුමේ මාර්ගය (පෙරනිමි: {DEFAULT_SCAN_PATH})"
    )
    
    parser.add_argument(
        "-f", "--format",
        nargs="+",
        choices=SUPPORTED_FORMATS,
        default=DEFAULT_FORMATS,
        help=f"වාර්තා ආකෘතිය/ආකෘති (පෙරනිමි: {DEFAULT_FORMATS})"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"වාර්තාව සේව් කරන බහාලුම (පෙරනිමි: {DEFAULT_OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "-t", "--top",
        type=int,
        default=DEFAULT_TOP_FILES,
        help=f"වාර්තාවේ පෙන්වන විශාලතම ගොනු ගණන (පෙරනිමි: {DEFAULT_TOP_FILES})"
    )
    
    parser.add_argument(
        "--old-days",
        type=int,
        default=DEFAULT_OLD_FILE_DAYS,
        help=f"පැරණි ගොනු ලෙස සැලකිය යුතු දින ගණන (පෙරනිමි: {DEFAULT_OLD_FILE_DAYS})"
    )
    
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"සමාන්තර thread ගණන (පෙරනිමි: {DEFAULT_WORKERS})"
    )
    
    parser.add_argument(
        "-e", "--exclude",
        type=str,
        default="",
        help="මග හැරිය යුතු බහාලුම්/ගොනු (comma-separated, උදා: '.cache,temp,backup')"
    )
    
    parser.add_argument(
        "--no-duplicates",
        action="store_true",
        help="ඩුප්ලිකේට් ගොනු පරීක්ෂාව අක්‍රිය කරයි"
    )
    
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Progress bar අක්‍රිය කරයි"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"{APP_NAME} v{APP_VERSION}"
    )
    
    return parser


def parse_arguments() -> argparse.Namespace:
    """
    Command Line Arguments parse කර වලංගුතාව පරීක්ෂා කරයි.
    
    Returns:
        Parse කරන ලද arguments අඩංගු Namespace object එක
    
    Raises:
        SystemExit: අවලංගු arguments ඇති විට
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # මාර්ග වලංගුතාව පරීක්ෂා කිරීම
    if not is_valid_path(args.path):
        print(f"⚠️ දෝෂය: '{args.path}' බහාලුම සොයාගත නොහැක හෝ වලංගු නොවේ.")
        sys.exit(1)
    
    # Exclude list parse කිරීම
    if args.exclude:
        args.exclude_list: Set[str] = set(
            item.strip() for item in args.exclude.split(',') if item.strip()
        )
    else:
        args.exclude_list = set()
    
    # Workers ගණන පරීක්ෂාව
    if args.workers < 1:
        print("⚠️ දෝෂය: Workers ගණන 1 ට වැඩි විය යුතුය.")
        sys.exit(1)
    
    # Top ගණන පරීක්ෂාව
    if args.top < 1:
        print("⚠️ දෝෂය: Top ගණන 1 ට වැඩි විය යුතුය.")
        sys.exit(1)
    
    return args
