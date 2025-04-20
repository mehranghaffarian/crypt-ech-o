from utils.logging import setup_logger
from utils import config

logger = setup_logger()

def main():
    logger.info("Starting Crypt(Ech)o project...")
    logger.debug(f"News API Key: {config.NEWS_API_KEY}")
    logger.debug(f"CoinCap API Key: {config.COINCAP_API_KEY}")
    logger.debug(f"Database URL: {config.DB_URL}")

if __name__ == "__main__":
    main()
