from utils.logging import setup_logger
from sqlalchemy import create_engine
from db.models import Base             
from utils.config import DB_URL, COINS, NEWS_QUERIES, SINCE, UNTIL
from pathlib import Path
from utils.logging import setup_logger
from etl.extract.news_api_extractor import NewsAPIExtractor
from etl.extract.coincap_extractor import CoinCapExtractor
from etl.transform.news_transformer import NewsTransformer
from etl.transform.market_transformer import MarketTransformer
from etl.load.news_loader import NewsLoader
from etl.load.market_loader import MarketLoader
from etl.enrich.finbert_enricher import FinBERTEnricher
from etl.enrich.impact_calculator import ImpactCalculator
from etl.enrich.relevance_enricher import RelevanceEnricher
from analytics.correlate_by_label import correlate_by_label
from analytics.correlate_sentiment_price import correlate_sentiment_price
from analytics.interactive_sentiment_plot import generate_sentiment_plot
from analytics.find_outliers_by_relevance import find_outliers_by_relevance
from analytics.plot_sentiment_vs_price import plot_sentiment_vs_price
from analytics.sentiment_buckets_analysis import bucket_and_summarize
from analytics.validate_impacts import validate_impacts

logger = setup_logger(__name__)

def init_db():
    """Create tables if they don't exist yet."""
    logger.info("Initializing database schema…")
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    logger.info("Database schema ready.")

def transform_and_load_news():
    news_loader = NewsLoader()
    enricher    = FinBERTEnricher()    
    relevance_cls = RelevanceEnricher()

    base = Path("data/raw/news")
    for query_dir in base.iterdir():
        if not query_dir.is_dir():
            continue
        for raw_file in query_dir.glob("*.json"):
            logger.info(f"Transforming news file: {raw_file}")
            df = NewsTransformer(str(raw_file)).transform()
            df = enricher.enrich(df)     
            df = relevance_cls.enrich(df)
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
    # — Extract —
    # News
    for q in NEWS_QUERIES:
        NewsAPIExtractor(query=q).fetch(SINCE, UNTIL)
        
    # Market 
    for coin in COINS:
        CoinCapExtractor(query=coin).fetch(SINCE, UNTIL)

    # — Transform and Load —
    transform_and_load_news()
    transform_and_load_market()
    logger.info("All transform & load steps complete.")

if __name__ == "__main__":
    logger.info("Starting Crypt(Ech)o project...")
    try:
        logger.info("Initializing DB:")
        init_db()
        
        logger.info("Running ETL:")
        run_etl()
        
        logger.info("Calculating news impacts:")
        ImpactCalculator().compute_all(window_minutes=120)

        logger.info("Analyzing data:")

        logger.info("Caluclating correlate_by_label:")
        correlate_by_label()
        
        logger.info("Calculating correlate_sentiment_price:")
        correlate_sentiment_price()

        logger.info("Finding outliers_by_relevance:")
        find_outliers_by_relevance()

        logger.info("Generating sentiment_plot:")
        generate_sentiment_plot()

        logger.info("plot_by_relevance:")
        plot_sentiment_vs_price()

        logger.info("bucket_and_summarize:")
        bucket_and_summarize()

        logger.info("validate_impacts:")
        validate_impacts()
    except Exception as e:
        logger.exception(f"ETL failed:{e}")
        exit(1)