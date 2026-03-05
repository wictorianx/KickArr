# 🟢 KickArr

**KickArr** is an automated tool to track and archive streamer VODs from Kick.com.

Designed as a lightweight background service, it monitors your favorite streamers and automatically archives their VODs. It is optimized for **Raspberry Pi** and **Home Lab** users who want a "set it and forget it" solution to preserve content.

## ✨ Features

*   **Automated Sync**: Checks for new VODs periodically (default: every hour).
*   **Web Dashboard**: Includes a lightweight web interface to monitor download status and history.
*   **Persistent Archive**: Uses SQLite to ensure VODs are tracked and only downloaded once.
*   **Pi-Ready**: Resource-constrained design with single-instance downloading to prevent CPU/RAM spikes.
*   **State Management**: Robustly tracks pending, downloading, completed, and failed tasks.

## 🚀 Installation

### 1. Prerequisites

Ensure you have `ffmpeg`, `python3`, and `yt-dlp` installed on your system.

**Arch Linux**
```bash
sudo pacman -S ffmpeg python yt-dlp
```

**Debian/Ubuntu (Raspberry Pi OS)**
```bash
sudo apt update && sudo apt install ffmpeg python3 python3-pip yt-dlp
```

### 2. Clone & Install

```bash
git clone https://github.com/wictorianx/kickarr.git
cd kickarr
pip install -r requirements.txt
```

### 3. Configuration

KickArr uses a YAML configuration file. Create one based on your needs:

```bash
# Create the config directory if it doesn't exist
mkdir -p config
# Create/Edit config.yaml
nano config/config.yaml
```

Example `config/config.yaml`:
```yaml
streamers:
  - jahrein
  - nymn

archive:
  download_path: "VODs"
  check_interval_mins: 60
```

## 🛠️ Usage

KickArr comes with a helper script to start both the background scheduler and the web dashboard.

1.  Make the script executable:
    ```bash
    chmod +x run.sh
    ```

2.  Start the service:
    ```bash
    ./run.sh
    ```

3.  **Access the Dashboard**: Open your browser and navigate to `http://localhost:5000`.

## 📦 Systemd Setup (Linux)

To run KickArr as a background service that starts automatically on boot, point your systemd service file to the `run.sh` script.

1.  Update `ExecStart` in your service file:
    ```ini
    ExecStart=/path/to/kickarr/run.sh
    ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
