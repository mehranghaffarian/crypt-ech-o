from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

class SentimentEnricher:
    """
    Takes a DataFrame with 'title' and 'description' columns
    and adds a 'sentiment' column:
      - compound polarity score from VADER, in [-1, +1].
    """
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        # Ensure text fields exist
        df = df.copy()
        df['text_to_score'] = df['title'].fillna('') + '. ' + df['description'].fillna('')
        # Compute sentiment
        df['sentiment_score'] = df['text_to_score'] \
            .apply(lambda txt: self.analyzer.polarity_scores(txt)['compound'])
        # Drop helper col
        df.drop(columns=['text_to_score'], inplace=True)
        return df
