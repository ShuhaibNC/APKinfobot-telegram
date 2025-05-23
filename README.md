# 📦 APKInfoBot

A modular Telegram bot for analyzing Android APK files — focused on malware research and forensic analysis.

## 🚀 Features

- 📥 Accepts APKs via Telegram file uploads  
- 🔍 Extracts detailed APK metadata using `pyaxmlparser`
- 🖼️ Retrieves launcher icon
- 📝 Generates detailed static reports
- 🧮 Calculates MD5 and SHA256 hashes
- 🌐 VirusTotal lookup integration
- 🔁 Asynchronous file processing & cleanup

## 🧠 Tech Stack

- [Pyrogram](https://docs.pyrogram.org/) – Telegram bot API framework  
- [pyaxmlparser](https://github.com/iaml00t/pyaxmlparser) – APK manifest parser  
- `asyncio`, `shutil`, `os` – Efficient async operations  
- Custom helper modules: `func.py`, `Script.py`  

## 📂 Usage

1. Start the bot with `/start`
2. Send an APK file
3. Bot will:
   - Download & scan the file
   - Return basic info + icon + hashes
   - Offer a full analysis report & VirusTotal link

## 🧩 Project Structure

├── bot.py # Main bot logic
├── func.py # Utility functions (hashes, reports, etc.)
├── Script.py # Start/help text
├── requirements.txt # Python dependencies


## 🧪 Requirements

- Python 3.8+
- Dependencies:
  ```bash
  pip install pyrogram tgcrypto pyaxmlparser
  ```
