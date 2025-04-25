import pandas as pd
from sqlalchemy import create_engine, text
from utils.config import DB_URL
from utils.logging import setup_logger
import matplotlib.pyplot as plt

logger = setup_logger(__name__)

def bucket_and_summarize():
    engine = create_engine(DB_URL)
    # Pull required columns
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

    # Define buckets
    bins   = [0.0, 0.33, 0.66, 1.0]
    labels = ["negative", "neutral", "positive"]
    df["bucket"] = pd.cut(df["sentiment"], bins=bins, labels=labels, include_lowest=True)

    # Aggregate stats
    summary = (
        df.groupby("bucket")["price_change"]
          .agg(
            count=("count"),
            avg_change=("mean"),
            std_change=("std"),
            min_change=("min"),
            max_change=("max")
          )
          .reset_index()
    )

    # Log and save
    logger.info("Sentiment Bucket Summary:")
    logger.info(summary.to_string(index=False))

    summary.to_csv("data/analytics/sentiment_bucket_summary.csv", index=False)
    logger.info("Saved bucket summary to data/analytics/sentiment_bucket_summary.csv")

    df = pd.read_csv("data/analytics/sentiment_bucket_summary.csv")

    plt.figure()
    plt.bar(df['bucket'], df['avg_change'], yerr=df['std_change'], capsize=5)
    plt.xlabel('Sentiment Bucket')
    plt.ylabel('Average Price Change (%)')
    plt.title('Avg Crypto Price Move by Sentiment Bucket')
    plt.tight_layout()
    plt.savefig('data/analytics/bucket_bar_chart.png')
    logger.info("Saved bucket bar chart to data/analytics/bucket_bar_chart.png")


if __name__ == "__main__":
    bucket_and_summarize()
