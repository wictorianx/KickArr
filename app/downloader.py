import subprocess
import os
import logging
from typing import Dict, Any
from models.database import KickDB

logger = logging.getLogger(__name__)

def process_queue(config: Dict[str, Any]) -> None:
    """Processes the download queue for pending VODs."""
    with KickDB() as db:
        task = db.get_next_task()
        if not task:
            return

        v_id = task['id']
        db.update_status(v_id, 'downloading')
        
        base_path = config.get('archive', {}).get('download_path', 'VODs')
        output_dir = os.path.join(base_path, task['streamer'])
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            logger.error("Failed to create directory %s: %s", output_dir, e)
            db.update_status(v_id, 'failed')
            return
        
        # Best quality 1080p, but remuxing only (no transcoding) to save Pi CPU
        cmd = [
            "yt-dlp", task['url'],
            "-o", f"{output_dir}/%(upload_date)s - %(title)s.%(ext)s",
            "-f", "bestvideo[height<=1080]+bestaudio/best",
            "--hls-use-mpegts",
            "--no-part"
        ]

        try:
            logger.info("Starting download for: %s", task['title'])
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            db.update_status(v_id, 'completed')
            logger.info("Archived: %s", task['title'])
        except FileNotFoundError:
            logger.critical("yt-dlp binary not found! Please install it (e.g., 'sudo apt install yt-dlp').")
            db.update_status(v_id, 'failed')
        except subprocess.CalledProcessError as e:
            logger.error("Download failed for %s. Error: %s", task['title'], e.stderr)
            db.update_status(v_id, 'failed')
        except Exception as e:
            logger.error("Unexpected error during download: %s", e)
            db.update_status(v_id, 'failed')
