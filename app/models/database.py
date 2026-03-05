import sqlite3
import os
import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)

class KickDB:
    """Handles SQLite database interactions for KickArr."""

    def __init__(self, db_path: str = "data/kickarr.db") -> None:
        """Initializes the database connection and ensures the schema exists."""
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            # Add timeout to prevent locking errors with threaded scheduler
            self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
            self.conn.row_factory = sqlite3.Row
            self._bootstrap()
        except OSError as e:
            logger.error("Failed to create database directory: %s", e)
            raise
        except sqlite3.Error as e:
            logger.error("Failed to connect to database: %s", e)
            raise

    def _bootstrap(self) -> None:
        """Creates the necessary tables if they do not exist."""
        try:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS vods (
                    id TEXT PRIMARY KEY,
                    streamer TEXT,
                    title TEXT,
                    url TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error("Database bootstrap failed: %s", e)
            raise

    def add_vod(self, v_id: str, streamer: str, title: str, url: str) -> None:
        """Adds a new VOD to the database. Ignores duplicates."""
        try:
            self.conn.execute("""
                INSERT OR IGNORE INTO vods (id, streamer, title, url) 
                VALUES (?, ?, ?, ?)
            """, (v_id, streamer, title, url))
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error("Failed to add VOD %s: %s", v_id, e)

    def get_pending_vods(self) -> List[sqlite3.Row]:
        """Retrieves all VODs with 'pending' status."""
        try:
            cursor = self.conn.execute("SELECT * FROM vods WHERE status = 'pending'")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error("Failed to fetch pending VODs: %s", e)
            return []

    def get_next_task(self) -> Optional[sqlite3.Row]:
        """Retrieves the next pending VOD task (FIFO)."""
        try:
            cursor = self.conn.execute(
                "SELECT * FROM vods WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error("Failed to fetch next task: %s", e)
            return None

    def update_status(self, v_id: str, status: str) -> None:
        """Updates the status of a VOD."""
        try:
            self.conn.execute(
                "UPDATE vods SET status = ? WHERE id = ?", 
                (status, v_id)
            )
            self.conn.commit()
            logger.info("VOD %s updated to %s", v_id, status)
        except sqlite3.Error as e:
            logger.error("Failed to update status for %s: %s", v_id, e)

    def get_history(self, limit: int = 50) -> List[sqlite3.Row]:
        """Retrieves the most recent VODs for the UI."""
        try:
            cursor = self.conn.execute(
                "SELECT * FROM vods ORDER BY created_at DESC LIMIT ?", (limit,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error("Failed to fetch history: %s", e)
            return []

    def close(self) -> None:
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()