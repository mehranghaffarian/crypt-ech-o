import json
import pandas as pd
from etl.transform.base_transform import Transformer
from pathlib import Path

class NewsTransformer:
    def __init__(self, raw_path: str):
        super.__init__(raw_path)

    def transform(self) -> pd.DataFrame:
        # 1) Load JSON
        with open(self.raw_path, 'r') as f:
            articles = json.load(f)

        # 2) Normalize into DataFrame
        df = pd.json_normalize(articles)

        # 3) Extract the query name from the folder (if you want to keep it)
        #    parent folder name is your query, e.g. 'Apple'
        query_name = self.raw_path.parent.name
        df['query'] = query_name

        # 4) Rename & select only the columns matching your schema
        df = df.rename(columns={
            'source.id': 'source_id',
            'source.name': 'source_name',
            'publishedAt': 'published_at',
            'urlToImage': 'url_to_image',
        })
        df = df[[
            'query',
            'source_id', 'source_name', 'author', 'title', 'description',
            'url', 'url_to_image', 'published_at', 'content'
        ]]

        # 5) Parse timestamps
        df['published_at'] = pd.to_datetime(df['published_at'], utc=True)

        # 6) Deduplicate by URL
        df = df.drop_duplicates(subset=['url'])

        return df


# point at your real file
transformer = NewsTransformer(
    "data/raw/news/crypto/news__2025-04-11_to_2025-04-21.json"
)
df = transformer.transform()
print(df.head())
print(df.dtypes)
print(df.columns.tolist())
