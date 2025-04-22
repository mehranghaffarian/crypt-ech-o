from utils.logging import setup_logger
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from db.models import Base                  # your SQLAlchemy models
from utils.config import DB_URL
from pathlib import Path
from utils.logging import setup_logger
from etl.extract.news_api_extractor import NewsAPIExtractor
from etl.extract.coincap_extractor import CoinCapExtractor
from etl.transform.news_transformer import NewsTransformer
from etl.transform.market_transformer import MarketTransformer
from etl.load.news_loader import NewsLoader
from etl.load.market_loader import MarketLoader

logger = setup_logger(__name__)
NEWS_QUERY = "crypto regulation"
COINS = ["bitcoin","ethereum"]


def init_db():
    """Create tables if they don't exist yet."""
    logger.info("Initializing database schema…")
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    logger.info("Database schema ready.")

def transform_and_load_news():
    news_loader = NewsLoader()
    base = Path("data/raw/news")
    for query_dir in base.iterdir():
        if not query_dir.is_dir():
            continue
        for raw_file in query_dir.glob("*.json"):
            logger.info(f"Transforming news file: {raw_file}")
            df = NewsTransformer(str(raw_file)).transform()
            count = news_loader.load(df)
            logger.info(f"Inserted {count} rows from {raw_file.name}")

def transform_and_load_market():
    market_loader = MarketLoader()
    base = Path("data/raw/market")
    for coin_dir in base.iterdir():
        if not coin_dir.is_dir():
            continue
        for raw_file in coin_dir.glob("*.json"):
            logger.info(f"Transforming market file: {raw_file}")
            df = MarketTransformer(str(raw_file)).transform()
            count = market_loader.load(df)
            logger.info(f"Inserted {count} rows from {raw_file.name}")

def run_etl():
    """Perform one full ETL cycle."""
    now = datetime.utcnow()
    # — Extract —
    # News
    news_ex = NewsAPIExtractor(query=NEWS_QUERY)
    since_n = news_ex.load_state()
    news_ex.fetch(since_n, now)

    # Market (for two coins as example)
    raw_market = {}
    for coin in COINS:
        m_ex = CoinCapExtractor(query=coin)
        since_m = m_ex.load_state()
        raw_market[coin] = m_ex.fetch(since_m, now)

    # — Transform and Load —
    transform_and_load_news()
    transform_and_load_market()
    logger.info("All transform & load steps complete.")

if __name__ == "__main__":
    logger.info("Starting Crypt(Ech)o project...")
    try:
        logger.info("Initializing DB")
        init_db()
        
        logger.info("Running ETL")
        run_etl()
        logger.info("ETL completed successfully.")
    except Exception as e:
        logger.exception(f"ETL failed:{e}")
        exit(1)