import json
import pandas as pd
from datetime import datetime
from pathlib import Path

class MarketTransformer:
    def __init__(self, raw_path: str):
        """
        raw_path: path to JSON file, e.g.
          'data/raw/market/bitcoin/market_2025-04-11_to_2025-04-21.json'
        """
        self.raw_path = Path(raw_path)

    def transform(self) -> pd.DataFrame:
        # 1) Load JSON array
        with open(self.raw_path, 'r') as f:
            records = json.load(f)

        # 2) Normalize into DataFrame
        df = pd.json_normalize(records)

        # 3) Extract coin from parent folder name
        coin = self.raw_path.parent.name
        df['coin'] = coin

        # 4) Convert 'time' (ms) → pandas.Timestamp
        df['timestamp'] = pd.to_datetime(df['time'], unit='ms', utc=True)

        # 5) Optionally derive 'date' column (DATE only)
        df['date'] = df['timestamp'].dt.date

        # 6) Cast numeric columns from strings
        df['price_usd'] = df['priceUsd'].astype(float)
        df['circulating_supply'] = df['circulatingSupply'].astype(float)

        # 7) Select/rename only the needed columns
        df = df[['coin', 'timestamp', 'date', 'price_usd', 'circulating_supply']]

        # 8) Drop duplicates just in case
        df = df.drop_duplicates(subset=['coin', 'timestamp'])

        return df


from etl.transform.market_transformer import MarketTransformer

mt = MarketTransformer("data/raw/market/bitcoin/market_2025-04-11_to_2025-04-21.json")
df_mkt = mt.transform()

print(df_mkt.head())
print(df_mkt.dtypes)
print(df_mkt.shape)
