# 📱 SDCard Scanner — Storage Report Generator

ඔබගේ Android දුරකථනයේ **සම්පූර්ණ SDCard** scan කර, ෆයිල් වර්ග, ප්‍රමාණ සහ විශාලම ෆයිල් දැක්වෙන **HTML Report** එකක් ස්වයංක්‍රීයව සාදන Python script එකකි.  
[Termux](https://termux.dev) හරහා Android දුරකථනයේ සෘජුවම ධාවනය කළ හැකිය.

---

## ✨ Features

| Feature | විස්තරය |
|---|---|
| 🔍 Full Scan | `/sdcard/` සම්පූර්ණයෙන් scan කරයි |
| 📊 Category Breakdown | ෆයිල් වර්ග 10ක් අනුව ගණන හා MB දක්වයි |
| 🏆 Top 10 Largest | විශාලම ෆයිල් 10 — නම, ස්ථානය, ප්‍රමාණය |
| 💾 HTML Report | Dark theme සහිත report `/sdcard/Download/` හි සාදයි |
| ⚡ Fast | PermissionError හසුරුවමින් crash නොවී scan කරයි |

---

## 📊 Report එකේ ඇතුළත් දේ

```
┌─────────────────────────────────────────┐
│  📱 SDCard Report                        │
│  Scan කළ දිනය: 2026-06-10 01:11:10      │
├──────────┬──────────┬────────┬──────────┤
│ ෆයිල් ගණන │ සම්පූර්ණ GB │ වර්ග   │ Skip    │
├──────────┴──────────┴────────┴──────────┤
│  📂 ෆයිල් වර්ග Cards (% bar සහිත)       │
│  🏆 Top 10 Largest Files Table           │
└─────────────────────────────────────────┘
```

---

## 📂 හඳුනාගන්නා ෆයිල් වර්ග

| Category | Extensions |
|---|---|
| 🖼️ Images | `.jpg` `.jpeg` `.png` `.gif` `.webp` `.bmp` |
| 🎬 Videos | `.mp4` `.mkv` `.mov` `.avi` `.wmv` |
| 🎵 Music | `.mp3` `.wav` `.aac` `.flac` `.ogg` |
| 📄 PDFs | `.pdf` |
| 📱 Apps | `.apk` `.xapk` |
| 🗜️ Archives | `.zip` `.rar` `.tar` `.gz` `.7z` |
| 💻 Code | `.py` `.js` `.html` `.ts` `.sh` `.json` `.css` |
| 📝 Documents | `.docx` `.txt` `.csv` `.md` `.toml` `.xlsx` |
| 🔐 Security | `.keystore` `.pem` `.key` `.cert` |
| 📦 Other | ඉහත නොවන සෙසු ෆයිල් |

---

## 🚀 ස්ථාපනය (Installation)

### අවශ්‍යතා
- [Termux](https://f-droid.org/packages/com.termux/) (Android)
- Python 3.x

### පියවර

```bash
# 1. Termux හි Python install කිරීම
pkg install python

# 2. Storage permission ලබාගැනීම
termux-setup-storage

# 3. Script ෆෝල්ඩරයක් සෑදීම
mkdir ~/my_script
cd ~/my_script

# 4. sdcard_scanner.py ෆෝල්ඩරයට copy කිරීම
```

---

## ▶️ භාවිතය (Usage)

```bash
cd ~/my_script
python sdcard_scanner.py
```

### Output

```
🔍 Scanning /sdcard/ ...

✅ ෆයිල් ගණන   : 1,243
💾 සම්පූර්ණ ප්‍රමාණය: 4.7 GB
⚠️  Skip වූ ගොනු : 3

📊 HTML report සාදමින්...
✅ Report සාදා ඇත: /sdcard/Download/sdcard_report.html
   Browser හෝ HTML viewer app එකෙන් විවෘත කරන්න.
```

### Report බලන ආකාරය

1. Files app හෝ File Manager හරහා `/sdcard/Download/` වෙත යන්න
2. `sdcard_report.html` ගොනුව tap කරන්න
3. Browser app (Chrome/Firefox) හරහා විවෘත වේ

---

## ⚙️ Path වෙනස් කිරීම

`sdcard_scanner.py` ගොනුවේ මෙම lines සොයාගෙන වෙනස් කරන්න:

```python
# Scan කරන ස්ථානය
SCAN_PATH = "/sdcard/"

# Report save වන ස්ථානය
OUTPUT_HTML = "/sdcard/Download/sdcard_report.html"
```

### විකල්ප

```python
# Termux home folder පමණක් scan
SCAN_PATH = "/data/data/com.termux/files/home/"

# Download folder පමණක් scan
SCAN_PATH = "/sdcard/Download/"
```

---

## ⚠️ වැදගත් සටහන්

- **System folders** (`.` දිය) automatically skip වේ.
- **Permission error** ගොනු count කර skip කරයි — crash නොවේ.
- Report ගොනුව **internet නොමැතිව** browser හි ක්‍රියාකරයි (offline HTML).
- Scan කරන සෑම විටම **report overwrite** වේ — පැරණි report ගොනු නොරැදේ.
- `.keystore` ආදී Security ෆයිල් report හි **🔐 Security** category යටතේ දිස්වේ.

---

## 🗃️ ගොනු විස්තරය

| ගොනුව | විස්තරය |
|---|---|
| `sdcard_scanner.py` | ප්‍රධාන script ගොනුව |
| `sdcard_report.html` | Generate වන HTML report (Downloads හි සාදයි) |

---

## 🛠️ නිර්මාතෘ

Termux + Python project — Android SDCard storage analysis සඳහා.

