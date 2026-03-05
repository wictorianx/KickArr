# 🟢 KickArr

**KickArr is an automated tool to track and archive streamer VODs from Kick.com.**

KickArr is a lightweight background service designed to monitor your favorite streamers and automatically archive their VODs. It is optimized for Raspberry Pi and Home Lab users who want a "set it and forget it" solution to preserve content before it's deleted.

---

## ✨ Features

- **Automated Sync:** Checks for new VODs every hour (configurable).
- **Persistent Archive:** Uses SQLite to ensure VODs are only downloaded once, even if the file is moved.
- **Pi-Ready:** Resource-constrained design with single-instance downloading to prevent CPU/RAM spikes on low-end hardware.
- **State Management:** Robustly tracks `pending`, `downloading`, and `completed` tasks.

---

## 🚀 Installation

### 1. Prerequisites

Ensure you have `ffmpeg` and `python3` installed on your system.

```bash
# Arch Linux
sudo pacman -S ffmpeg python yt-dlp

# Debian/Ubuntu (Raspberry Pi OS)
sudo apt update && sudo apt install ffmpeg python3 python3-pip yt-dlp
```

### 2. Clone & Install

```bash
git clone https://github.com/wictorianx/kickarr.git
cd kickarr
pip install -r requirements.txt
```

### 3. Configuration

KickArr uses a YAML configuration. Copy the example and add your streamers:

```bash
cp config/config.example.yaml config/config.yaml
nano config/config.yaml
```

> **Note:** Ensure `config/config.yaml` is in your `.gitignore` to protect your local settings.

---

## 🛠️ Usage

To start the service manually:

```bash
python3 main.py
```

---

## 📦 Systemd Setup (Linux)

To run KickArr as a background service that starts automatically on boot:

1. Edit `kickarr.service` and update the `WorkingDirectory` and `ExecStart` paths to match your local installation.

2. Copy the file to the system directory:

```bash
sudo cp kickarr.service /etc/systemd/system/
```

3. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kickarr
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
