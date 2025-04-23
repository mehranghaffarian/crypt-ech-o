from sqlalchemy import create_engine, text
from utils.config import DB_URL
from utils.logging import setup_logger

logger = setup_logger(__name__)

def validate_impacts():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        # Summarize counts and averages per coin
        sql = text("""
            SELECT
              coin,
              COUNT(*)       AS num_impacts,
              AVG(delta_pct) AS avg_delta_pct,
              AVG(volatility) AS avg_volatility
            FROM headline_impacts
            GROUP BY coin
            ORDER BY coin;
        """)
        result = conn.execute(sql)
        rows = result.fetchall()

        logger.info("Summary of Headline Impacts:")
        logger.info(f"{'COIN':<10} {'#IMPACTS':>8} {'AVG_DELTA%':>12} {'AVG_VOL%':>10}")
        for coin, num, avg_d, avg_v in rows:
            logger.info(f"{coin:<10} {num:>8} {avg_d:12.4f} {avg_v:10.4f}")

    
if __name__ == "__main__":
    validate_impacts()
