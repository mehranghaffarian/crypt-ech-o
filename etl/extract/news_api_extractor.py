import requests
import os
import json
from datetime import datetime
from .base_extractor import Extractor
from utils.config import NEWS_API_KEY
from utils.logging import setup_logger

logger = setup_logger(__name__)

class NewsAPIExtractor(Extractor):
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self, query: str):
        super().__init__(f'etl/extract/state/news/{query}/news_api.state.txt', query)

    def fetch(self, since: datetime, until: datetime):
        if since < self.last_timestamp:
            since = self.last_timestamp

        params = {
            'apiKey': NEWS_API_KEY,
            'q': self.query,
            'from': since.isoformat(),
            'to': until.isoformat(),
            'pageSize': 50,
            # 'sources': 'bbc-news',
            'page': 1,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        logger.info(f"Fetching {self.query} data from {since.isoformat()} to {until.isoformat()}")

        try:
            all_articles = []
            while params['page'] <= 2:
                response = requests.get(self.BASE_URL, params=params)
                logger.info(f"newsAPI returned status {response.status_code}")
                response.raise_for_status()

                data = response.json()
                articles = data.get('articles', [])
                logger.info(f"Received {len(articles)} data points")
                
                if not articles:
                    break
                
                all_articles.extend(articles)
                
                if len(articles) < params['pageSize']:
                    break
                params['page'] += 1

            # Save raw output
            if len(all_articles) > 0:
                since_str = since.date().isoformat()
                until_str = until.date().isoformat()
                raw_dir = f'data/raw/news/{self.query}'
                os.makedirs(raw_dir, exist_ok=True)
                raw_path = os.path.join(raw_dir, f"news__{since_str}_to_{until_str}.json")
                with open(raw_path, 'w') as f:
                    json.dump(all_articles, f, indent=2)
                logger.info(f"Wrote raw data to {raw_path}")

            # Update state
            self.save_state(until)
            return all_articles

        except requests.RequestException as e:
            logger.error(f"Error fetching from CoinCap: {e}")
            return []



from datetime import datetime, timedelta, timezone

until = datetime.now(timezone.utc)
since = until - timedelta(days=12)

articles = NewsAPIExtractor('Apple').fetch(since, until)
