from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Extractor(ABC):
    """
    Abstract base class for all data extractors.
    Handles state load/save and defines fetch interface.
    """
    def __init__(self, state_file: str, query: str):
        self.state_file = state_file
        self.query = query
        self.last_timestamp = self.load_state()

    @abstractmethod
    def fetch(self, since: datetime, until: datetime):
        '''Fetch data between since and until.'''
        pass

    def load_state(self) -> datetime:
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    ts = f.read().strip()
                    return datetime.fromisoformat(ts)
        except Exception as e:
            logger.error(f"Failed to load state: {e}, returning 10 days ago")
        return datetime.now(timezone.utc) - timedelta(days=10)

    def save_state(self, timestamp: datetime):
        try:
            os.makedirs(Path(self.state_file).parent, exist_ok=True)
            with open(self.state_file, 'w') as f:
                f.write(timestamp.isoformat())
            logger.debug(f"State saved: {timestamp}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
