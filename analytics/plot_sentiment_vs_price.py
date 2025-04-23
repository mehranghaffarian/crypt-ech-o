import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
from utils.config import DB_URL

def plot_by_relevance():
    engine = create_engine(DB_URL)
    # Query joined data with relevance label
    sql = text("""
        SELECT 
          n.relevance_label AS label,
          n.finbert_score AS sentiment,
          h.delta_pct AS price_change
        FROM headline_impacts h
        JOIN news_articles n ON n.id = h.article_id
        WHERE n.finbert_score IS NOT NULL
          AND h.delta_pct IS NOT NULL
    """)
    df = pd.read_sql(sql, engine)

    # Separate subsets
    df_crypto = df[df['label'] == 'cryptocurrency']
    df_general = df[df['label'] == 'general']

    # Scatter for crypto
    plt.figure()
    plt.scatter(df_crypto['sentiment'], df_crypto['price_change'], alpha=0.6, s=10)
    plt.xlabel('Sentiment Score')
    plt.ylabel('Price Change (%)')
    plt.title('Crypto-related News: Sentiment vs. Price Change')
    plt.tight_layout()
    plt.savefig('data/analytics/crypto_scatter.png')
    plt.close()

    # Scatter for general
    plt.figure()
    plt.scatter(df_general['sentiment'], df_general['price_change'], alpha=0.6, s=10)
    plt.xlabel('Sentiment Score')
    plt.ylabel('Price Change (%)')
    plt.title('General News: Sentiment vs. Price Change')
    plt.tight_layout()
    plt.savefig('data/analytics/general_scatter.png')
    plt.close()

    # Histogram for crypto
    plt.figure()
    plt.hist(df_crypto['price_change'], bins=50, edgecolor='black')
    plt.xlabel('Price Change (%)')
    plt.ylabel('Frequency')
    plt.title('Crypto-related News: Price Change Distribution')
    plt.tight_layout()
    plt.savefig('data/analytics/crypto_hist.png')
    plt.close()

    # Histogram for general
    plt.figure()
    plt.hist(df_general['price_change'], bins=50, edgecolor='black')
    plt.xlabel('Price Change (%)')
    plt.ylabel('Frequency')
    plt.title('General News: Price Change Distribution')
    plt.tight_layout()
    plt.savefig('data/analytics/general_hist.png')
    plt.close()

# Run the plotting function
plot_by_relevance()

