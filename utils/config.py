from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")
DB_URL = os.getenv("DB_URL")

NEWS_QUERIES = ["crypto regulation", "crypto legislation", "bitcoin ban", "SEC crypto enforcement", "crypto tax policy", "CBDC launch", "BlackRock bitcoin ETF", "institutional crypto adoption", "crypto investment bank", "bitcoin holdings", "Tesla", "Trump", "Musk", "MicroStrategy", "Fed interest rate crypto", "inflation bitcoin", "dollar strength crypto", "crypto safe haven", "crypto payment integration", "bitcoin accepted", "NFT marketplace", "layer 2 scaling ethereum", "bitcoin lightning network", "bitcoin crashing", "altcoin surge", "crypto market panic", "whale buying bitcoin", "Ethereum to the moon", "quantum computing", "natural disaster", "energy grid blackout", "major wildfire spreads", "amazon layoffs", "black friday record", "new virus outbreak", "drug approval stock surge", "celebrity scandal", "Kanye West", "Russia sanctions", "How to cook", "onion", "orage", "dark web leak", "Jerome Powell", "Christine Lagarde", "Andrew Bailey"]
COINS = ["bitcoin"]

SINCE = datetime(2025, 3, 25,  0, 0, 0, tzinfo=timezone.utc)
UNTIL = datetime(2025, 4, 22,  0, 0, 0, tzinfo=timezone.utc)

NEWS_CANDIDATE_LABELS = ["cryptocurrency", "stock market", "politics", "technology", "entertainment", "general"]