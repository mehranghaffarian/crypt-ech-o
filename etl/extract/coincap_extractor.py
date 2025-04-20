import requests
from datetime import datetime
import os
import json
from etl.extract.base_extractor import Extractor
from utils.config import COINCAP_API_KEY  # if needed

class CoinCapExtractor(Extractor):
    BASE_URL = "https://api.coincap.io/v2/assets"

    def __init__(self, state_file: str = 'state.coincap.txt', coin: str = 'bitcoin'):
        super().__init__(state_file)
        self.coin = coin

    def fetch(self, since: datetime, until: datetime):
        # Example: fetch OHLC data if endpoint available
        resp = requests.get(f"{self.BASE_URL}/{self.coin}/history", params={'interval': 'm1'})
        data = resp.json().get('data', [])
        # Save raw
        date_str = until.date().isoformat()
        os.makedirs(f'data/raw/market/{self.coin}', exist_ok=True)
        with open(f'data/raw/market/{self.coin}/market_{date_str}.json', 'w') as f:
            json.dump(data, f, indent=2)
        # State management placeholder
        self.save_state(until)
        return data
