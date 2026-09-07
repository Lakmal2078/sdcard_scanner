# 📱 SDCard Scanner — Advanced Storage Report Generator

ඔබගේ Android දුරකථනයේ SDCard scan කර, ෆයිල් වර්ග, ප්‍රමාණය, ඩුප්ලිකේට් සහ
පැරණි ෆයිල් දැක්වෙන HTML/CSV/JSON Report එකක් ස්වයංක්‍රීයව සාදන Python script පද්ධතියකි.

## ✨ විශේෂාංග

| විශේෂාංගය | විස්තරය |
|---|---|
| 🔍 **වේගවත් Scan** | `os.scandir()` භාවිතා කරමින් 2-3x වේගවත් scanning |
| 📊 **ප්‍රවර්ගීකරණය** | ෆයිල් වර්ග 10ක් අනුව ගණන හා MB දක්වයි |
| 🏆 **Top Files** | විශාලතම ගොනු (අභිරුචි ගණනක්) — නම, ස්ථානය, ප්‍රමාණය |
| 🔁 **ඩුප්ලිකේට්** | MD5 hash මගින් සැබෑ ඩුප්ලිකේට් හඳුනාගැනීම |
| 🕰️ **පැරණි ගොනු** | නියමිත දින ගණනකට වඩා පැරණි ගොනු වෙන් කිරීම |
| 💾 **බහු-ආකෘති** | HTML, CSV, JSON ආකෘති එකවර ලබා ගැනීම |
| ⚡ **සමාන්තර** | `ThreadPoolExecutor` මගින් වේගවත් hash ගණනය |
| 📊 **Progress Bar** | `tqdm` සමඟ real-time progress feedback |
| 🎨 **Dark Theme UI** | කියවීමට පහසු HTML වාර්තාව |
| 🔕 **Exclusions** | පද්ධති බහාලුම් ස්වයංක්‍රීයව මග හැරීම |

## 🚀 ස්ථාපනය

### අවශ්‍යතා
- Termux (Android) හෝ Python 3.8+
- Storage permissions

### පියවර

```bash
# 1. Termux හි Python install කිරීම
pkg install python

# 2. Storage permission ලබාගැනීම
termux-setup-storage

# 3. tqdm install කිරීම (නිර්දේශිත)
pip install tqdm

# 4. ව්‍යාපෘති ගොනු copy කිරීම
mkdir ~/sdcard_scanner
cd ~/sdcard_scanner
# ගොනු සියල්ල මෙම බහාලුමට copy කරන්න
```

## ▶️ භාවිතය

### මූලික භාවිතය
```bash
python main.py
```

### නිශ්චිත බහාලුමක් scan කිරීම
```bash
python main.py --path /sdcard/DCIM
python main.py --path /sdcard/WhatsApp
```

### බහු-ආකෘති වාර්තා
```bash
python main.py --format html csv json
```

### විශාලතම ගොනු 50ක් පෙන්වීම
```bash
python main.py --top 50
```

### වෙනත් ස්ථානයක සේව් කිරීම
```bash
python main.py --output /sdcard/Documents/Reports/
```

### ඩුප්ලිකේට් පරීක්ෂාව අක්‍රිය කිරීම
```bash
python main.py --no-duplicates
```

### අභිරුචි බහාලුම් මග හැරීම
```bash
python main.py --exclude ".cache,temp,backup,old_photos"
```

### සම්පූර්ණ විධානය
```bash
python main.py --path /sdcard/ \
               --format html csv json \
               --output /sdcard/Download/ \
               --top 50 \
               --old-days 180 \
               --workers 8 \
               --exclude ".cache,temp"
```

### සියලුම විකල්ප බැලීම
```bash
python main.py --help
```

## 📁 ව්‍යාපෘති ව්‍යුහය

sdcard_scanner/
├── main.py                  # ප්‍රධාන entry point
├── cli.py                   # Command Line Argument handling
├── scanner.py               # Directory scanning logic
├── duplicates.py            # Duplicate file detection
├── report_generator.py      # HTML/CSV/JSON report generation
├── utils.py                 # Helper functions
├── constants.py             # නියතයන් සහ සැකසුම්
├── requirements.txt         # යැපීම්
└── README.md                # මෙම ගොනුව

## 📊 Output උදාහරණ

### Console Output

=================================================================
📱 SDCard Scanner v3.0.0 — Advanced Storage Report
සාදන ලද්දේ Lakmal විසින්
📂 Scan මාර්ගය   : /sdcard/
💾 Output මාර්ගය  : /sdcard/Download/
📋 ආකෘතිය       : html
🏆 Top ගොනු       : 20
🕰️  පැරණි දින සීමාව: 365
⚡ Workers        : 4
🚫 ඩුප්ලිකේට්     : සක්‍රිය
🔍 Scanning: 15,243 files
✅ සාර්ථකව scan කරන ලදී:
ෆයිල් ගණන     : 15,243
සම්පූර්ණ ප්‍රමාණය : 12.45 GB
මග හැරි ගොනු  : 23
🔎 ඩුප්ලිකේට් ගොනු පරීක්ෂා කරමින්...
📦 Hash කළ යුතු ගොනු: 1,245
🔐 Hashing: 100%|████████| 1245/1245 [00:15<00:00, 82.3file/s]
🔁 ඩුප්ලිකේට් කාණ්ඩ 45ක් හමුවිය.
අපතේ යන මුළු ඉඩ: 1.23 GB
📊 වාර්තා සාදමින්...
✅ HTML වාර්තාව: /sdcard/Download/sdcard_report.html
=================================================================

