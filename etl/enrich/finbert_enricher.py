# etl/enrich/finbert_enricher.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pandas as pd

class FinBERTEnricher:
    def __init__(self):
        model_name = "ProsusAI/finbert"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model     = AutoModelForSequenceClassification.from_pretrained(model_name)
        # Create a pipeline that returns labels+scores
        self.pipe = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer,
            return_all_scores=True
        )

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Combine title + description into one text field
        texts = (df['title'].fillna('') + '. ' + df['description'].fillna('')).tolist()
        # Run in batches (if you have many, chunk them)
        results = self.pipe(texts)
        # Extract scores into new columns
        labels = []
        scores = []
        for item in results:
            # item is a list of dicts: [{'label':'positive','score':0.97}, ...]
            best = max(item, key=lambda x: x['score'])
            labels.append(best['label'])
            scores.append(best['score'])
        df['finbert_label'] = labels
        df['finbert_score'] = scores
        return df

