import yaml
import time
import logging
import sys
from app.core.scheduler import create_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Main entry point for the KickArr service."""
    try:
        with open("config/config.yaml", "r") as f:
            config = yaml.safe_load(f)
    except (IOError, yaml.YAMLError) as e:
        logger.critical("Failed to load configuration: %s", e)
        return
    
    if not config:
        logger.critical("Configuration file is empty or invalid.")
        return

    scheduler = create_scheduler(config)

    logger.info("KickArr Service Started. Monitoring streamers...")
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down service...")
        scheduler.shutdown()

if __name__ == "__main__":
    main()