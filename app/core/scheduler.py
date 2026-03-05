import logging
from typing import Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.scanner import sync_all
from app.downloader import process_queue

logger = logging.getLogger(__name__)

def create_scheduler(config: Dict[str, Any]) -> BackgroundScheduler:
    """
    Creates and configures the background scheduler.
    
    Args:
        config: The loaded configuration dictionary.
        
    Returns:
        BackgroundScheduler: The configured scheduler instance.
    """
    scheduler = BackgroundScheduler()
    
    # Get intervals from config, defaulting to 60 mins for sync
    sync_interval = config.get('archive', {}).get('check_interval_mins', 60)

    # Sync streamers
    scheduler.add_job(sync_all, 'interval', minutes=sync_interval, args=[config.get('streamers', [])])
    
    # Check for downloads every 5 minutes
    scheduler.add_job(process_queue, 'interval', minutes=5, max_instances=1, args=[config])

    return scheduler