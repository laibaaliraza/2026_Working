import logging
import json
from datetime import datetime

logger=logging.getLogger("scraper")
logging.basicConfig(level=logging.INFO, format="%(message)s")

async def log_events(event,data=None):
    log_data={"timestamp":datetime.utcnow().isoformat(),"event": event}
    if data:
        log_data.update(data)
    logger.info(json.dumps(log_data))