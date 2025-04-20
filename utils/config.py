from dotenv import load_dotenv
import os

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")
DB_URL = os.getenv("DB_URL")
