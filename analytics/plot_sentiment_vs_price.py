import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
from utils.config import DB_URL, NEWS_CANDIDATE_LABELS
from utils.logging import setup_logger

logger = setup_logger(__name__)

def plot_sentiment_vs_price():
    engine = create_engine(DB_URL)
    # Query joined data with relevance label
    sql = text("""
        SELECT 
          n.relevance_label AS label,
          n.finbert_score AS sentiment,
          h.delta_pct AS price_change
        FROM headline_impacts h
        JOIN news_articles n ON n.id = h.article_id
        WHERE n.finbert_score IS NOT NULL
          AND h.delta_pct IS NOT NULL
    """)
    df = pd.read_sql(sql, engine)

    for label in NEWS_CANDIDATE_LABELS: 
      label_df = df[df['label'] == label]
      # Scatter for general
      plt.figure()
      plt.scatter(label_df['sentiment'], label_df['price_change'], alpha=0.6, s=10)
      plt.xlabel('Sentiment Score')
      plt.ylabel('Price Change (%)')
      plt.title('General News: Sentiment vs. Price Change')
      plt.tight_layout()
      plt.savefig(f'data/analytics/{label}_scatter.png')
      plt.close()

      # Histogram for crypto
      plt.figure()
      plt.hist(label_df['price_change'], bins=50, edgecolor='black')
      plt.xlabel('Price Change (%)')
      plt.ylabel('Frequency')
      plt.title('Crypto-related News: Price Change Distribution')
      plt.tight_layout()
      plt.savefig(f'data/analytics/{label}_hist.png')
      plt.close()

      logger.info("Sentiment vs Price Plots are all generated")

# Run the plotting function
if __name__ == "__main__":
    plot_sentiment_vs_price()

