import pandas as pd
from sqlalchemy import create_engine, text
from utils.config import DB_URL
from utils.logging import setup_logger
from scipy.stats import pearsonr, spearmanr

logger = setup_logger(__name__)

def correlate_sentiment_price():
    engine = create_engine(DB_URL)
    # Pull joined data
    sql = text("""
      SELECT
        n.finbert_score    AS sentiment,
        h.delta_pct        AS price_change
      FROM headline_impacts h
      JOIN news_articles n ON n.id = h.article_id
      WHERE n.finbert_score IS NOT NULL
        AND h.delta_pct IS NOT NULL
    """)
    df = pd.read_sql(sql, engine)
    if df.empty:
        logger.warning("No data found for correlation.")
        return

    # Compute correlations
    pearson_corr, pearson_p = pearsonr(df['sentiment'], df['price_change'])
    spearman_corr, spearman_p = spearmanr(df['sentiment'], df['price_change'])

    logger.info(f"Pearson = {pearson_corr:.4f} (p={pearson_p:.3g})")
    logger.info(f"Spearman = {spearman_corr:.4f} (p={spearman_p:.3g})")

    # Optionally save the joined dataset
    df.to_csv("data/analytics/sentiment_vs_price.csv", index=False)
    logger.info("Saved joined data to data/analytics/sentiment_vs_price.csv")

if __name__ == "__main__":
    correlate_sentiment_price()
