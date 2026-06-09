import os
import json
from datetime import datetime

# ───────────────────────────────────────────────
# ⚙️  සැකසුම්
# ───────────────────────────────────────────────
SCAN_PATH   = "/sdcard/"
OUTPUT_HTML = "/sdcard/Download/sdcard_report.html"

# Extension → Category mapping
EXT_MAP = {
    ".jpg": "Images",  ".jpeg": "Images", ".png": "Images",
    ".gif": "Images",  ".webp": "Images", ".bmp": "Images",
    ".mp4": "Videos",  ".mkv": "Videos",  ".mov": "Videos",
    ".avi": "Videos",  ".wmv": "Videos",
    ".mp3": "Music",   ".wav": "Music",   ".aac": "Music",
    ".flac": "Music",  ".ogg": "Music",
    ".pdf": "PDFs",
    ".apk": "Apps",    ".xapk": "Apps",
    ".zip": "Archives",".rar": "Archives",".tar": "Archives",
    ".gz": "Archives", ".7z": "Archives",
    ".py": "Code",     ".js": "Code",     ".html": "Code",
    ".ts": "Code",     ".sh": "Code",     ".json": "Code",
    ".css": "Code",    ".xml": "Code",    ".zsh": "Code",
    ".docx": "Documents", ".doc": "Documents", ".txt": "Documents",
    ".pptx": "Documents", ".xlsx": "Documents", ".csv": "Documents",
    ".md": "Documents",   ".toml": "Documents",
    ".keystore": "Security", ".pem": "Security",
    ".key": "Security",      ".cert": "Security",
}

CATEGORY_ICONS = {
    "Images":    "🖼️",
    "Videos":    "🎬",
    "Music":     "🎵",
    "PDFs":      "📄",
    "Apps":      "📱",
    "Archives":  "🗜️",
    "Code":      "💻",
    "Documents": "📝",
    "Security":  "🔐",
    "Other":     "📦",
}

def human_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def scan(path):
    """sdcard සම්පූර්ණයෙන් scan කිරීම"""
    categories = {}
    total_size = 0
    total_files = 0
    skipped_dirs = 0
    largest_files = []

    for root, dirs, files in os.walk(path):
        # System ෆෝල්ඩර skip
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.startswith("."):
                continue
            full_path = os.path.join(root, file)
            try:
                size = os.path.getsize(full_path)
            except (PermissionError, OSError):
                skipped_dirs += 1
                continue

            _, ext = os.path.splitext(file)
            ext = ext.lower()
            category = EXT_MAP.get(ext, "Other")

            if category not in categories:
                categories[category] = {"count": 0, "size": 0, "files": []}

            categories[category]["count"] += 1
            categories[category]["size"]  += size

            # Top 10 largest files ලැයිස්තුව
            rel_path = os.path.relpath(full_path, path)
            largest_files.append((size, file, rel_path, category))

            total_size  += size
            total_files += 1

    largest_files.sort(reverse=True)
    largest_files = largest_files[:10]

    return categories, total_size, total_files, largest_files, skipped_dirs


def build_html(categories, total_size, total_files, largest_files, skipped_dirs):
    """HTML report ගොනුව සෑදීම"""
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Category cards HTML
    sorted_cats = sorted(categories.items(), key=lambda x: x[1]["size"], reverse=True)

    cards_html = ""
    for cat, data in sorted_cats:
        icon = CATEGORY_ICONS.get(cat, "📦")
        pct  = (data["size"] / total_size * 100) if total_size else 0
        cards_html += f"""
        <div class="card">
          <div class="card-icon">{icon}</div>
          <div class="card-name">{cat}</div>
          <div class="card-count">{data['count']:,} ෆයිල්</div>
          <div class="card-size">{human_size(data['size'])}</div>
          <div class="bar-wrap"><div class="bar" style="width:{min(pct,100):.1f}%"></div></div>
          <div class="card-pct">{pct:.1f}%</div>
        </div>"""

    # Largest files table HTML
    rows_html = ""
    for i, (size, name, path, cat) in enumerate(largest_files, 1):
        icon = CATEGORY_ICONS.get(cat, "📦")
        rows_html += f"""
        <tr>
          <td class="rank">#{i}</td>
          <td class="fname">{icon} {name}</td>
          <td class="fpath">{path}</td>
          <td class="fsize">{human_size(size)}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="si">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📱 SDCard Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', sans-serif;
    background: #0f1117;
    color: #e0e0e0;
    min-height: 100vh;
    padding: 20px;
  }}
  header {{
    text-align: center;
    padding: 30px 20px 20px;
    border-bottom: 1px solid #2a2d3a;
    margin-bottom: 30px;
  }}
  header h1 {{ font-size: 1.8rem; color: #7ee8a2; letter-spacing: 1px; }}
  header p  {{ color: #888; font-size: 0.85rem; margin-top: 6px; }}

  .summary {{
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 32px;
  }}
  .stat {{
    background: #1a1d2e;
    border: 1px solid #2a2d3a;
    border-radius: 12px;
    padding: 16px 24px;
    text-align: center;
    flex: 1;
    min-width: 130px;
  }}
  .stat .val {{ font-size: 1.6rem; font-weight: 700; color: #7ee8a2; }}
  .stat .lbl {{ font-size: 0.75rem; color: #888; margin-top: 4px; }}

  h2 {{
    font-size: 1rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
    padding-left: 4px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 14px;
    margin-bottom: 40px;
  }}
  .card {{
    background: #1a1d2e;
    border: 1px solid #2a2d3a;
    border-radius: 14px;
    padding: 16px;
    transition: border-color 0.2s;
  }}
  .card:hover {{ border-color: #7ee8a2; }}
  .card-icon  {{ font-size: 1.8rem; margin-bottom: 8px; }}
  .card-name  {{ font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }}
  .card-count {{ font-size: 0.78rem; color: #888; }}
  .card-size  {{ font-size: 1rem; color: #7ee8a2; font-weight: 700; margin: 6px 0 4px; }}
  .bar-wrap   {{ background: #2a2d3a; border-radius: 4px; height: 5px; margin: 6px 0 3px; }}
  .bar        {{ background: #7ee8a2; height: 5px; border-radius: 4px; }}
  .card-pct   {{ font-size: 0.72rem; color: #555; }}

  .table-wrap {{ overflow-x: auto; margin-bottom: 40px; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }}
  th {{
    background: #1a1d2e;
    color: #7ee8a2;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    letter-spacing: 0.5px;
  }}
  td {{ padding: 9px 14px; border-bottom: 1px solid #1e2030; }}
  tr:hover td {{ background: #1a1d2e; }}
  .rank  {{ color: #555; font-weight: 700; width: 40px; }}
  .fname {{ color: #e0e0e0; font-weight: 500; }}
  .fpath {{ color: #555; font-size: 0.78rem; word-break: break-all; }}
  .fsize {{ color: #7ee8a2; font-weight: 700; white-space: nowrap; }}

  footer {{
    text-align: center;
    color: #333;
    font-size: 0.75rem;
    padding: 20px 0;
    border-top: 1px solid #1e2030;
  }}
</style>
</head>
<body>

<header>
  <h1>📱 SDCard Report</h1>
  <p>Scan කළ දිනය: {scan_time} &nbsp;|&nbsp; Path: /sdcard/</p>
</header>

<div class="summary">
  <div class="stat"><div class="val">{total_files:,}</div><div class="lbl">සම්පූර්ණ ෆයිල්</div></div>
  <div class="stat"><div class="val">{human_size(total_size)}</div><div class="lbl">සම්පූර්ණ ප්‍රමාණය</div></div>
  <div class="stat"><div class="val">{len(categories)}</div><div class="lbl">ෆයිල් වර්ග</div></div>
  <div class="stat"><div class="val">{skipped_dirs}</div><div class="lbl">Skip වූ ගොනු</div></div>
</div>

<h2>📂 ෆයිල් වර්ග අනුව</h2>
<div class="grid">
{cards_html}
</div>

<h2>🏆 විශාලම ෆයිල් Top 10</h2>
<div class="table-wrap">
<table>
  <thead><tr><th>#</th><th>ෆයිල් නම</th><th>ස්ථානය</th><th>ප්‍රමාණය</th></tr></thead>
  <tbody>{rows_html}</tbody>
</table>
</div>

<footer>Generated by SDCard Scanner · {scan_time}</footer>
</body>
</html>"""


if __name__ == "__main__":
    print(f"\n🔍 Scanning {SCAN_PATH} ...\n")
    categories, total_size, total_files, largest_files, skipped = scan(SCAN_PATH)

    print(f"✅ ෆයිල් ගණන   : {total_files:,}")
    print(f"💾 සම්පූර්ණ ප්‍රමාණය: {human_size(total_size)}")
    print(f"⚠️  Skip වූ ගොනු : {skipped}")
    print(f"\n📊 HTML report සාදමින්...")

    html = build_html(categories, total_size, total_files, largest_files, skipped)

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report සාදා ඇත: {OUTPUT_HTML}")
    print("   Browser හෝ HTML viewer app එකෙන් විවෘත කරන්න.\n")

