import unittest
import os
import tempfile
import shutil
from app.models.database import KickDB

class TestKickDB(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory and database for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_kickarr.db")
        self.db = KickDB(self.db_path)

    def tearDown(self):
        """Clean up the temporary directory."""
        self.db.close()
        shutil.rmtree(self.test_dir)

    def test_add_and_get_vod(self):
        """Test adding a VOD and retrieving it."""
        self.db.add_vod("v123", "streamer1", "Title 1", "http://url")
        vods = self.db.get_pending_vods()
        
        self.assertEqual(len(vods), 1)
        self.assertEqual(vods[0]['id'], "v123")
        self.assertEqual(vods[0]['status'], "pending")

    def test_get_next_task_fifo(self):
        """Test that tasks are retrieved in First-In-First-Out order."""
        self.db.add_vod("v1", "s1", "Oldest", "u1")
        self.db.add_vod("v2", "s1", "Newest", "u2")
        
        task = self.db.get_next_task()
        self.assertIsNotNone(task)
        self.assertEqual(task['id'], "v1") # Should be v1 (oldest)

    def test_update_status(self):
        """Test status updates flow."""
        self.db.add_vod("v1", "s1", "t1", "u1")
        
        # Move to downloading
        self.db.update_status("v1", "downloading")
        
        # Should no longer be pending
        pending = self.db.get_pending_vods()
        self.assertEqual(len(pending), 0)
        
        # Verify status in DB
        cursor = self.db.conn.execute("SELECT status FROM vods WHERE id = 'v1'")
        row = cursor.fetchone()
        self.assertEqual(row['status'], "downloading")

if __name__ == "__main__":
    unittest.main()