import logging
from typing import List
from kickapi import KickAPI
from app.models.database import KickDB

logger = logging.getLogger(__name__)

def sync_all(streamer_slugs: List[str]) -> None:
    """Syncs VODs for a list of streamers using KickAPI."""
    kick_api = KickAPI()
    
    with KickDB() as db:
        for slug in streamer_slugs:
            try:
                channel = kick_api.channel(slug)

                if channel is None or not hasattr(channel, 'id'):
                    logger.warning("Could not find streamer: %s", slug)
                    continue

                logger.info("Found %s. Syncing VODs...", slug)

                for video in channel.videos:
                    if not hasattr(video, 'id') or not getattr(video, 'stream', None):
                        continue
                    
                    db.add_vod(
                        v_id=str(video.id),
                        streamer=slug,
                        title=video.title,
                        url=video.stream 
                    )
            except Exception as e:
                logger.critical("Critical error scanning %s: %s", slug, e)