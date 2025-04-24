import requests
from datetime import datetime
import os
import json
from etl.extract.base_extractor import Extractor
from utils.config import COINCAP_API_KEY, SINCE, UNTIL
from utils.logging import setup_logger

logger = setup_logger(__name__)

class CoinCapExtractor(Extractor):
    BASE_URL = "https://rest.coincap.io/v3/assets"

    def __init__(self, query: str):
        super().__init__(f'etl/extract/state/market/{query}/coincap.state.txt', query)

    def fetch(self, since: datetime, until: datetime):
        if since < self.last_timestamp:
            since = self.last_timestamp

        start = int(since.timestamp() * 1000)
        end = int(until.timestamp() * 1000)

        logger.info(f"Fetching {self.query} data from {since.isoformat()} to {until.isoformat()}")

        
        try:
            resp = requests.get(
                f"{self.BASE_URL}/{self.query}/history",
                params={"interval": "h2", "start": start, "end": end},
                headers={"Authorization": f"Bearer {COINCAP_API_KEY}"}
            )
            logger.info(f"CoinCap returned status {resp.status_code}")
            resp.raise_for_status()

            data = resp.json().get("data", [])
            logger.info(f"Received {len(data)} data points")

            # Save raw JSON
            if len(data) > 0:
                since_str = since.date().isoformat()
                until_str = until.date().isoformat()
                raw_dir = f"data/raw/market/{self.query}"
                os.makedirs(raw_dir, exist_ok=True)
                raw_path = os.path.join(raw_dir, f"market_{since_str}_to_{until_str}.json")
                with open(raw_path, "w") as f:
                    json.dump(data, f, indent=2)
                logger.info(f"Wrote raw data to {raw_path}")

            # Update state
            self.save_state(until)
            logger.debug(f"State file updated to {until.isoformat()}")

            return data

        except requests.RequestException as e:
            logger.error(f"Error fetching from CoinCap: {e}")
            return []



# from datetime import datetime, timedelta, timezone

# until = datetime.now(timezone.utc)
# since = until - timedelta(days=12)

# articles = CoinCapExtractor('bitcoin').fetch(SINCE, UNTIL)
