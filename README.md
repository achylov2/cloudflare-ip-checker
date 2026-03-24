# 🚀 Cloudflare IP Checker

Fast multithreaded Cloudflare IP checker with latency measurement.

## ⚡ Features
- Multithreaded scanning
- TCP latency check (port 443)
- Progress bar
- Sorted results (fastest first)
- Saves working and failed IPs

## ▶️ Usage
```bash
python checker.py
```

## 📦 Build EXE
```bash
pyinstaller --onefile --add-data "cloudflare_ipv4.txt;." checker.py
```

## 📁 Output
- working.txt → working IPs with latency
- failed.txt → unreachable IPs

## ⚙️ Requirements
- Python 3.x
- colorama
- tqdm

Install dependencies:
```bash
pip install colorama tqdm
```

## 📜 License
MIT License
