# File: etl/load/market_loader.py
import pandas as pd
from etl.load.base_loader import Loader

class MarketLoader(Loader):
    TABLE_NAME = 'market_ticks'
    CONSTRAINT = ['coin', 'timestamp']   # unique constraint

    def load(self, df: pd.DataFrame):
        # ensure timestamp is a Python datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # upsert: update price if it changed (optional)
        inserted = self._upsert(
            self.TABLE_NAME,
            df,
            constraint_cols=self.CONSTRAINT,
            update_cols=['price_usd', 'circulating_supply']
        )
        return inserted
