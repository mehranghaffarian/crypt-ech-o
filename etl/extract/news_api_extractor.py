import requests
import os
import json
from datetime import datetime
from .base_extractor import Extractor
from utils.config import NEWS_API_KEY

class NewsAPIExtractor(Extractor):
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self, state_file: str = 'state.news_api.txt'):
        super().__init__(state_file)

    def fetch(self, since: datetime, until: datetime):
        params = {
            'apiKey': NEWS_API_KEY,
            'q': 'Apple',
            'from': since.isoformat(),
            'to': until.isoformat(),
            'pageSize': 100,
            # 'sources': 'bbc-news',
            'page': 1,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        all_articles = []
        while params['page'] < 100:
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()
            articles = data.get('articles', [])
            
            if not articles:
                break
            
            all_articles.extend(articles)
            
            if len(articles) < params['pageSize']:
                break
            params['page'] += 1

        # Save raw output
        date_str = until.date().isoformat()
        os.makedirs(f'data/raw/news', exist_ok=True)
        with open(f'data/raw/news/news_{date_str}.json', 'w') as f:
            json.dump(all_articles, f, indent=2)
        
        # Update state
        if all_articles:
            latest = articles[-1]['publishedAt']
            latest_dt = datetime.fromisoformat(latest.replace('Z', '+00:00'))
            self.save_state(latest_dt)
        return all_articles


from datetime import datetime, timedelta, timezone

until = datetime.now(timezone.utc)
since = until - timedelta(days=10)

articles = NewsAPIExtractor().fetch(since, until)
print(articles)