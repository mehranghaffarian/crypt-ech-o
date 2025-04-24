import requests
import os
import json
from datetime import datetime
from .base_extractor import Extractor
from utils.config import NEWS_API_KEY, SINCE, UNTIL, NEWS_QUERIES
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
            'pageSize': 100,
            # 'sources': ','.join([
            #                 "bbc-news",
            #                 "cnn",
            #                 "bloomberg",
            #                 "reuters",
            #                 "the-new-york-times",
            #                 "the-wall-street-journal",
            #                 "forbes",
            #                 "financial-times",
            #                 "cnbc",
            #                 "al-jazeera-english",
            #                 "associated-press"
            #             ]),
            # 'domains': "bbc.co.uk,cnn.com,reuters.com,bloomberg.com,forbes.com,wsj.com,nytimes.com,cnbc.com,ft.com,theguardian.com,economist.com,techcrunch.com,thenextweb.com,wired.com,venturebeat.com,crypto.news,decrypt.co,coindesk.com,cointelegraph.com",
            'excludeDomains': "medium.com,blogspot.com,wordpress.com,substack.com,tumblr.com,ghost.io,dev.to,hashnode.com,steemit.com,hackernews.com,engadget.com",
            'page': 1,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        logger.info(f"Fetching {self.query} data from {since.isoformat()} to {until.isoformat()}")

        try:
            all_articles = []
            while params['page'] <= 1: # due to free API-KEY limits
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



# articles = []
# articles.extend(NewsAPIExtractor(NEWS_QUERIES[5]).fetch(SINCE, UNTIL))
# articles.extend(NewsAPIExtractor(NEWS_QUERIES[10]).fetch(SINCE, UNTIL))
# articles.extend(NewsAPIExtractor(NEWS_QUERIES[20]).fetch(SINCE, UNTIL))
# print(len(NEWS_QUERIES))
# print("number of news: " + str(len(articles)))