from utils.logging import setup_logger
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from db.models import Base                  # your SQLAlchemy models
from utils.config import DB_URL
from utils.logging import setup_logger
from etl.extract.news_api_extractor import NewsAPIExtractor
from etl.extract.coincap_extractor import CoinCapExtractor
from etl.transform.news_transformer import NewsTransformer
from etl.transform.market_transformer import MarketTransformer
from etl.load.news_loader import NewsLoader
from etl.load.market_loader import MarketLoader

logger = setup_logger(__name__)

def init_db():
    """Create tables if they don't exist yet."""
    logger.info("Initializing database schema…")
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    logger.info("Database schema ready.")

def run_etl():
    """Perform one full ETL cycle."""
    now = datetime.utcnow()
    # — Extract —
    # News
    news_ex = NewsAPIExtractor(state_file="etl/extract/state/news.state", query="crypto regulation OR ETF")
    since_n = news_ex.load_state() or (now - timedelta(hours=6))
    raw_news = news_ex.fetch(since_n, now)

    # Market (for two coins as example)
    coins = ["bitcoin", "ethereum"]
    raw_market = {}
    for coin in coins:
        m_ex = CoinCapExtractor(state_file=f"etl/extract/state/{coin}.state", coin=coin)
        since_m = m_ex.load_state() or (now - timedelta(hours=6))
        raw_market[coin] = m_ex.fetch(since_m, now)

    # — Transform —
    # Note: You could also reuse state to drive which files to transform
    df_news = NewsTransformer("data/raw/news/Apple/news__…json").transform()   # adapt path
    df_mkt  = MarketTransformer("data/raw/market/bitcoin/…json").transform()

    # — Load —
    nl = NewsLoader()
    inserted_news = nl.load(df_news)

    ml = MarketLoader()
    inserted_mkt  = ml.load(df_mkt)

    logger.info(f"ETL done: {inserted_news} news rows, {inserted_mkt} market rows.")

if __name__ == "__main__":
    logger.info("Starting Crypt(Ech)o project...")
    init_db()
    run_etl()

