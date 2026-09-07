#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_generator.py - HTML, CSV, සහ JSON ආකෘති වලින් වාර්තා ජනනය කරයි.
"""

import os
import csv
import json
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional

from constants import APP_NAME, APP_VERSION, APP_AUTHOR
from utils import format_size


def generate_html_report(
    files_data: List[Dict[str, Any]],
    duplicates: List[Dict[str, Any]],
    skipped: int,
    target_path: str,
    output_dir: str,
    top_n: int = 20,
    old_days: int = 365
) -> Optional[str]:
    """
    HTML වාර්තාව ජනනය කර සේව් කරයි.
    
    Args:
        files_data: scan කරන ලද ගොනු ලැයිස්තුව
        duplicates: ඩුප්ලිකේට් කාණ්ඩ ලැයිස්තුව
        skipped: මග හරින ලද ගොනු ගණන
        target_path: scan කළ මාර්ගය
        output_dir: වාර්තාව සේව් කළ යුතු බහාලුම
        top_n: විශාලතම ගොනු කීයක් පෙන්විය යුතු ද
        old_days: පැරණි ගොනු ලෙස සැලකිය යුතු දින ගණන
    
    Returns:
        ජනනය කළ ගොනුවේ මාර්ගය හෝ None
    """
    # ප්‍රවර්ග අනුව ගණනය
    category_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"count": 0, "size": 0})
    for f in files_data:
        category_stats[f["category"]]["count"] += 1
        category_stats[f["category"]]["size"] += f["size"]
    
    # විශාලතම ගොනු
    top_files: List[Dict[str, Any]] = sorted(
        files_data, key=lambda x: x["size"], reverse=True
    )[:top_n]
    
    # පැරණි ගොනු
    old_files: List[Dict[str, Any]] = [
        f for f in files_data if f["age_days"] > old_days
    ]
    old_files.sort(key=lambda x: x["age_days"], reverse=True)
    old_files_top: List[Dict[str, Any]] = old_files[:top_n]
    
    total_size: int = sum(f["size"] for f in files_data)
    
    # HTML අන්තර්ගතය ගොඩනැගීම
    html_content: str = _build_html_content(
        files_data, duplicates, category_stats, top_files,
        old_files, old_files_top, skipped, total_size,
        target_path, top_n, old_days
    )
    
    output_file: str = os.path.join(output_dir, "sdcard_report.html")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        return output_file
    except PermissionError:
        print(f"⚠️ HTML වාර්තාව සෑදීමට අවසර නොමැත: {output_file}")
        return None


def _build_html_content(
    files_data: List[Dict[str, Any]],
    duplicates: List[Dict[str, Any]],
    category_stats: Dict[str, Dict[str, int]],
    top_files: List[Dict[str, Any]],
    old_files: List[Dict[str, Any]],
    old_files_top: List[Dict[str, Any]],
    skipped: int,
    total_size: int,
    target_path: str,
    top_n: int,
    old_days: int
) -> str:
    """HTML අන්තර්ගතය ගොඩනගයි"""
    
    html: str = f"""<!DOCTYPE html>
<html lang="si">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{APP_NAME} Report - {target_path}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', Tahoma, sans-serif;
        background: #0d1117;
        color: #c9d1d9;
        padding: 20px;
        line-height: 1.6;
    }}
    .container {{ max-width: 1100px; margin: 0 auto; }}
    h1 {{
        color: #58a6ff;
        border-bottom: 2px solid #30363d;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}
    h2 {{
        color: #7ee787;
        margin: 25px 0 15px 0;
        font-size: 1.3em;
    }}
    .summary {{
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    .summary-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }}
    .stat-card {{
        background: #0d1117;
        padding: 15px;
        border-radius: 6px;
        border-left: 3px solid #58a6ff;
    }}
    .stat-card .label {{ font-size: 0.85em; color: #8b949e; }}
    .stat-card .value {{ font-size: 1.5em; color: #f0f6fc; font-weight: bold; }}
    table {{
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 20px;
    }}
    th {{
        background: #21262d;
        color: #58a6ff;
        padding: 12px;
        text-align: left;
        font-weight: 600;
    }}
    td {{
        padding: 10px 12px;
        border-top: 1px solid #30363d;
        word-break: break-all;
    }}
    tr:hover {{ background: #1c2128; }}
    .dup-group {{
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 10px;
    }}
    .dup-group .header {{
        color: #f0883e;
        font-weight: bold;
        margin-bottom: 8px;
    }}
    .dup-group ul {{ list-style: none; padding-left: 10px; }}
    .dup-group li {{
        padding: 4px 0;
        color: #8b949e;
        font-size: 0.9em;
        word-break: break-all;
    }}
    .dup-group li::before {{ content: "📄 "; }}
    .footer {{
        margin-top: 30px;
        padding: 15px;
        text-align: center;
        color: #8b949e;
        font-size: 0.85em;
        border-top: 1px solid #30363d;
    }}
    .badge {{
        display: inline-block;
        background: #1f6feb;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.8em;
        margin-left: 5px;
    }}
</style>
</head>
<body>
<div class="container">
    <h1>📱 {APP_NAME} Storage Report</h1>
    <p style="color:#8b949e;">Scan කළ මාර්ගය: <code>{target_path}</code> | 
    ජනනය කළ දිනය: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>

    <div class="summary">
        <div class="summary-grid">
            <div class="stat-card">
                <div class="label">මුළු ගොනු ගණන</div>
                <div class="value">{len(files_data):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">සම්පූර්ණ ප්‍රමාණය</div>
                <div class="value">{format_size(total_size)}</div>
            </div>
            <div class="stat-card">
                <div class="label">මග හැරි ගොනු</div>
                <div class="value">{skipped}</div>
            </div>
            <div class="stat-card">
                <div class="label">ඩුප්ලිකේට් කාණ්ඩ</div>
                <div class="value">{len(duplicates)}</div>
            </div>
            <div class="stat-card">
                <div class="label">පැරණි ගොනු (>{old_days} දින)</div>
                <div class="value">{len(old_files):,}</div>
            </div>
        </div>
    </div>

    <h2>📊 ප්‍රවර්ග අනුව බෙදීම</h2>
    <table>
        <tr><th>ප්‍රවර්ගය</th><th>ගොනු ගණන</th><th>ප්‍රමාණය</th></tr>"""

    for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]["size"], reverse=True):
        html += f"""
        <tr>
            <td>{cat}</td>
            <td>{stats['count']:,}</td>
            <td>{format_size(stats['size'])}</td>
        </tr>"""

    html += """
    </table>

    <h2>🏆 විශාලතම ගොනු</h2>
    <table>
        <tr><th>#</th><th>ගොනුව</th><th>ප්‍රමාණය</th><th>ප්‍රවර්ගය</th></tr>"""

    for i, f in enumerate(top_files, 1):
        html += f"""
        <tr>
            <td>{i}</td>
            <td>{f['path']}</td>
            <td>{format_size(f['size'])}</td>
            <td>{f['category']}</td>
        </tr>"""

    html += "</table>"

    # ඩුප්ලිකේට් කොටස
    if duplicates:
        html += """
    <h2>🔁 ඩුප්ලිකේට් ගොනු</h2>"""
        for dup in duplicates[:30]:
            wasted: int = dup['size'] * (dup['count'] - 1)
            html += f"""
    <div class="dup-group">
        <div class="header">📦 {dup['count']} ගොනු | එක් ගොනුවක ප්‍රමාණය: {dup['size_formatted']} | 
        මුළු අපතේ යන ඉඩ: {format_size(wasted)}</div>
        <ul>"""
            for path in dup['files']:
                html += f"<li>{path}</li>"
            html += "</ul></div>"
    else:
        html += """
    <h2>🔁 ඩුප්ලිකේට් ගොනු</h2>
    <p style="color:#8b949e;padding:15px;background:#161b22;border-radius:6px;">
    ✅ ඩුප්ලිකේට් ගොනු හමු නොවීය.</p>"""

    # පැරණි ගොනු කොටස
    if old_files_top:
        html += f"""
    <h2>🕰️ දින {old_days}ට වඩා පැරණි ගොනු</h2>
    <p style="color:#8b949e;margin-bottom:10px;">මුළු පැරණි ගොනු: {len(old_files):,} | 
    පහත දැක්වෙන්නේ ඉහළම {top_n}:</p>
    <table>
        <tr><th>#</th><th>ගොනුව</th><th>වයස (දින)</th><th>ප්‍රමාණය</th></tr>"""
        for i, f in enumerate(old_files_top, 1):
            html += f"""
        <tr>
            <td>{i}</td>
            <td>{f['path']}</td>
            <td>{f['age_days']}</td>
            <td>{format_size(f['size'])}</td>
        </tr>"""
        html += "</table>"

    html += f"""
    <div class="footer">
        {APP_NAME} v{APP_VERSION} | සාදන ලද්දේ <strong>{APP_AUTHOR}</strong> විසින්
    </div>
</div>
</body>
</html>"""
    
    return html


def export_to_csv(files_data: List[Dict[str, Any]], output_dir: str) -> Optional[str]:
    """
    දත්ත CSV ගොනුවක් ලෙස අපනයනය කරයි.
    
    Args:
        files_data: scan කරන ලද ගොනු ලැයිස්තුව
        output_dir: ගොනුව සේව් කළ යුතු බහාලුම
    
    Returns:
        ජනනය කළ ගොනුවේ මාර්ගය හෝ None
    """
    csv_file: str = os.path.join(output_dir, "sdcard_report.csv")
    try:
        with open(csv_file, mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["path", "name", "size", "category", "age_days", "modified"]
            )
            writer.writeheader()
            for row in files_data:
                writer.writerow(row)
        return csv_file
    except PermissionError:
        print(f"⚠️ CSV ගොනුව සෑදීමට අවසර නොමැත: {csv_file}")
        return None


def export_to_json(
    files_data: List[Dict[str, Any]],
    duplicates: List[Dict[str, Any]],
    output_dir: str
) -> Optional[str]:
    """
    දත්ත JSON ගොනුවක් ලෙස අපනයනය කරයි.
    
    Args:
        files_data: scan කරන ලද ගොනු ලැයිස්තුව
        duplicates: ඩුප්ලිකේට් කාණ්ඩ ලැයිස්තුව
        output_dir: ගොනුව සේව් කළ යුතු බහාලුම
    
    Returns:
        ජනනය කළ ගොනුවේ මාර්ගය හෝ None
    """
    json_file: str = os.path.join(output_dir, "sdcard_report.json")
    try:
        data: Dict[str, Any] = {
            "generated_at": datetime.now().isoformat(),
            "total_files": len(files_data),
            "duplicates_count": len(duplicates),
            "files": files_data,
            "duplicates": duplicates
        }
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return json_file
    except PermissionError:
        print(f"⚠️ JSON ගොනුව සෑදීමට අවසර නොමැත: {json_file}")
        return None
