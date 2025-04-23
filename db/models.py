from sqlalchemy import (
    Column, BigInteger, Text, DateTime, Date, Numeric,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MarketTick(Base):
    __tablename__ = "market_ticks"
    id = Column(BigInteger, primary_key=True)
    coin = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    date = Column(Date, nullable=False)
    price_usd = Column(Numeric(20,6), nullable=False)
    circulating_supply = Column(Numeric(24,6), nullable=False)
    __table_args__ = (
        UniqueConstraint('coin', 'timestamp', name='uq_coin_timestamp'),
        Index('idx_market_coin_time', 'coin', 'timestamp'),
    )

class NewsArticle(Base):
    __tablename__ = "news_articles"
    id = Column(BigInteger, primary_key=True)
    source_id = Column(Text)
    source_name = Column(Text, nullable=False)
    author = Column(Text)
    title = Column(Text, nullable=False)
    description = Column(Text)
    url = Column(Text, nullable=False, unique=True)
    url_to_image = Column(Text)
    published_at = Column(DateTime(timezone=True), nullable=False)
    content = Column(Text) 
    query = Column(Text)
         = Column(Text)
    finbert_score = Column(Numeric(9,6))
    relevance_label = Column(Text)            # 'cryptocurrency' or 'general'
    relevance_score = Column(Numeric(9,6))    # [0–1] confidence    
    __table_args__ = (
        Index('idx_news_published', 'published_at'),
    )

class HeadlineImpact(Base):
    __tablename__ = "headline_impacts"
    id = Column(BigInteger, primary_key=True)
    article_id = Column(BigInteger, ForeignKey("news_articles.id"), nullable=False)
    coin = Column(Text, nullable=False)
    before_id = Column(BigInteger, ForeignKey("market_ticks.id"), nullable=False)
    after_id = Column(BigInteger, ForeignKey("market_ticks.id"), nullable=False)
    delta_pct = Column(Numeric(10,6))
    volatility = Column(Numeric(10,6))
    window_minutes = Column(BigInteger)
    __table_args__ = (
        Index('idx_impacts_article', 'article_id'),
        Index('idx_impacts_coin', 'coin'),
    )
