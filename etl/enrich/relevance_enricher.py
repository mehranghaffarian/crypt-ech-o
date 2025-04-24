from transformers import pipeline
import pandas as pd
from utils.config import NEWS_CANDIDATE_LABELS

class RelevanceEnricher:
    """
    Zero-shot classifier to score how 'crypto-related' a piece of text is.
    Adds:
      - relevance_label: 'crypto' or 'not_crypto'
      - relevance_score: confidence for the 'crypto' label
    """
    def __init__(self):
        self.cls = pipeline(
            "zero-shot-classification",
            model="valhalla/distilbart-mnli-12-3",
            device=0
        )
        self.hypothesis_template = "This news is related to {}."

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        texts = (df['title'].fillna('') + '. ' + df['description'].fillna('')).tolist()
        out_labels, out_scores = [], []
        for text in texts:
            result = self.cls(
                text,
                candidate_labels=NEWS_CANDIDATE_LABELS,
                hypothesis_template=self.hypothesis_template
            )
            # find the score for 'cryptocurrency'
            label = result['labels'][0]  # the top label
            score = result['scores'][0]
            out_labels.append(label)
            out_scores.append(score)
        df['relevance_label'] = out_labels
        df['relevance_score'] = out_scores
        return df

if __name__ == "__main__": 
    from etl.transform.news_transformer import NewsTransformer
    transformer = NewsTransformer(
        "data/raw/news/crypto/news__2025-04-11_to_2025-04-21.json"
    )
    df = transformer.transform()
    print(RelevanceEnricher().enrich(df))