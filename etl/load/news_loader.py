# File: etl/load/news_loader.py
import pandas as pd
from etl.load.base_loader import Loader

class NewsLoader(Loader):
    TABLE_NAME = 'news_articles'
    CONSTRAINT = ['url']         # unique constraint on url
    # no update columns—once an article exists, we don’t re‑write it

    def load(self, df: pd.DataFrame):
        # ensure published_at is a Python datetime
        df['published_at'] = pd.to_datetime(df['published_at'])
        # upsert: skip duplicates
        inserted = self._upsert(
            self.TABLE_NAME,
            df,
            constraint_cols=self.CONSTRAINT,
            update_cols=None
        )
        return inserted
