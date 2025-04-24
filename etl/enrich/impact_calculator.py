from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db.models import NewsArticle, MarketTick, HeadlineImpact
from utils.config import DB_URL, COINS

class ImpactCalculator:
    def __init__(self):
        self.engine = create_engine(DB_URL)

    def compute_all(self, window_minutes: int = 60):
        """
        For each article in news_articles:
          - Find the latest tick <= published_at  (before)
          - Find the earliest tick >= published_at  (after)
          - Compute delta_pct & volatility
          - Insert into headline_impacts
        """
        with Session(self.engine) as session:
            articles = session.scalars(select(NewsArticle)).all()
            for art in articles:
                # Query before/after ticks for each coin
                for coin in COINS:
                    # before tick
                    before = session.scalars(
                        select(MarketTick)
                        .where(MarketTick.coin == coin)
                        .where(MarketTick.timestamp <= art.published_at)
                        .order_by(MarketTick.timestamp.desc())
                        .limit(1)
                    ).first()
                    # after tick
                    after = session.scalars(
                        select(MarketTick)
                        .where(MarketTick.coin == coin)
                        .where(MarketTick.timestamp >= art.published_at)
                        .order_by(MarketTick.timestamp.asc())
                        .limit(1)
                    ).first()

                    if not before or not after:
                        continue

                    # Compute metrics
                    delta_pct = (after.price_usd / before.price_usd - 1) * 100
                    volatility = (before.circulating_supply / after.circulating_supply - 1) * 100
                    # Note: if you prefer high/low, adjust accordingly

                    impact = HeadlineImpact(
                        article_id=art.id,
                        coin=coin,
                        before_id=before.id,
                        after_id=after.id,
                        delta_pct=round(delta_pct, 6),
                        volatility=round(volatility, 6),
                        window_minutes=window_minutes
                    )
                    session.add(impact)
            session.commit()
