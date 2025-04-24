import pandas as pd
from sqlalchemy import create_engine, select, text
from utils.config import DB_URL, NEWS_CANDIDATE_LABELS
from utils.logging import setup_logger

logger = setup_logger(__name__)

def find_outliers_by_relevance(n=5):
    engine = create_engine(DB_URL)
    for label in NEWS_CANDIDATE_LABELS:
        # Positive movers
        pos_sql = text(f"""
          SELECT h.delta_pct, n.title, n.relevance_score
          FROM headline_impacts h
          JOIN news_articles n ON n.id = h.article_id
          WHERE n.relevance_label = :label
          ORDER BY h.delta_pct DESC
          LIMIT :n;
        """)
        df_pos = pd.read_sql(pos_sql, engine, params={"label": label, "n": n})
        df_pos.to_csv(f"data/analytics/{label}_top_positive.csv", index=False)
        logger.info(f"Top positive movers for {label} saved to data/analytics/{label}_top_positive.csv")

        # Negative movers
        neg_sql = text(f"""
          SELECT h.delta_pct, n.title, n.relevance_score
          FROM headline_impacts h
          JOIN news_articles n ON n.id = h.article_id
          WHERE n.relevance_label = :label
          ORDER BY h.delta_pct ASC
          LIMIT :n;
        """)
        df_neg = pd.read_sql(neg_sql, engine, params={"label": label, "n": n})
        df_neg.to_csv(f"data/analytics/{label}_top_negative.csv", index=False)
        logger.info(f"Top negative movers for {label} saved to data/analytics/{label}_top_negative.csv")

if __name__ == "__main__":
    find_outliers_by_relevance()
