import pandas as pd
from sqlalchemy import create_engine, text
from utils.config import DB_URL, NEWS_CANDIDATE_LABELS
from utils.logging import setup_logger
from scipy.stats import pearsonr, spearmanr

logger = setup_logger(__name__)

def correlate_by_label():
    engine = create_engine(DB_URL)
    for label in NEWS_CANDIDATE_LABELS:
        sql = text("""
          SELECT n.finbert_score AS sentiment, h.delta_pct AS price_change
          FROM headline_impacts h
          JOIN news_articles n ON n.id = h.article_id
          WHERE n.relevance_label = :label
            AND n.finbert_score IS NOT NULL
            AND h.delta_pct IS NOT NULL
        """)
        df = pd.read_sql(sql, engine, params={"label": label})
        if len(df) < 2:
            logger.info(f"No enough data for label {label}, data len: {len(df)}")
            continue
        pr, pp = pearsonr(df['sentiment'], df['price_change'])
        sr, sp = spearmanr(df['sentiment'], df['price_change'])
        logger.info(f"[{label}] Pearson r = {pr:.4f} (p={pp:.3g}), Spearman ρ = {sr:.4f} (p={sp:.3g})")

if __name__ == "__main__":
    correlate_by_label()
