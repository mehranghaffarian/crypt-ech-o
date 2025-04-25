
# Crypto News Sentiment Impact Analysis

This project analyzes the impact of news sentiment on cryptocurrency price movements. By collecting, transforming, enriching, and visualizing data from news and market sources, the system allows users to explore correlations between public sentiment and crypto price fluctuations.

---

## 🚀 Project Goals

- Collect and analyze financial news data  
- Track crypto market price and volume data  
- Use NLP sentiment analysis to score each news headline  
- Analyze the influence of news on crypto price fluctuations  
- Visualize sentiment trends and price changes over time in an interactive dashboard

---

## 🧱 Project Architecture

The project follows a modular ETL pipeline structure:

1. **Extract**  
   - News from NewsAPI (by search query)  
   - Crypto prices from CoinCap API for specific coins (e.g., Bitcoin, Ethereum)  

2. **Transform**  
   - Parse and clean raw JSON into structured Pandas DataFrames  

3. **Load**  
   - Save structured data to PostgreSQL via SQLAlchemy models  

4. **Enrich**  
   - FinBERT sentiment scoring  
   - Zero‐shot relevance tagging (crypto vs. general)  
   - Matching headlines to before/after market ticks (price deltas, volatility)  

5. **Analyze**  
   - Correlations (Pearson, Spearman) between sentiment and price Δ%  
   - Outlier detection (top positive/negative movers)  
   - Bucketed sentiment analysis (negative/neutral/positive)  

6. **Visualize**  
   - Streamlit dashboard with interactive Plotly charts and tables  

7. **Scripts & Reports**  
   - Standalone analytics scripts under `analytics/`  

---

## 📂 Project Structure

```
.
├── analytics/
│   ├── correlate_by_label.py
│   ├── correlate_sentiment_price.py
│   ├── find_outliers_by_relevance.py
│   ├── interactive_sentiment_plot.py
│   ├── plot_sentiment_vs_price.py
│   ├── sentiment_buckets_analysis.py
│   └── validate_impacts.py
├── db/
│   └── models.py
├── docker-compose.yml
├── dashboard.py           # Streamlit dashboard entrypoint
├── main.py               # ETL orchestrator
├── requirements.txt
└── README.md
```

- **`analytics/`**  
  Contains all standalone analysis scripts:
  - `correlate_by_label.py`  
  - `correlate_sentiment_price.py`  
  - `find_outliers_by_relevance.py`  
  - `interactive_sentiment_plot.py`  
  - `plot_sentiment_vs_price.py`  
  - `sentiment_buckets_analysis.py`  
  - `validate_impacts.py`  

- **`db/models.py`**  
  SQLAlchemy table definitions for `news_articles`, `market_ticks`, and `headline_impacts`.

- **`dashboard.py`**  
  Streamlit app to explore sentiment vs. price change, bucket summaries, and top movers.

- **`main.py`**  
  Bootstraps the database schema, runs ETL extract/transform/load/enrich, and computes headline impacts.

- **`requirements.txt`**  
  All Python dependencies.

- **`docker-compose.yml`**  
  Defines the Postgres database and the Python app (ETL + dashboard) services.

---

## 🐳 Dockerized Deployment

1. **Build and start containers**  
   ```bash
   docker-compose up --build
   ```
2. **ETL & Dashboard**  
   - `app` container runs `main.py` once on startup.  
   - Streamlit dashboard is exposed at `http://localhost:8501/`.

---

## 🧪 Standalone Analysis Scripts

- **`validate_impacts.py`**  
  Summarizes number of impacts, average Δ% and volatility per coin.

- **`correlate_sentiment_price.py`**  
  Computes Pearson & Spearman correlations between sentiment score and price change.

- **`correlate_by_label.py`**  
  Splits correlations by relevance label (`cryptocurrency` vs. `general`).

- **`find_outliers_by_relevance.py`**  
  Exports top positive/negative movers for each relevance group.

- **`interactive_sentiment_plot.py`**  
  Generates an interactive HTML scatter (hoverable headlines).

- **`plot_sentiment_vs_price.py`**  
  Static scatter & histogram of sentiment vs. price change.

- **`sentiment_buckets_analysis.py`**  
  Buckets sentiment into negative/neutral/positive and reports summary stats.

---

## 📈 Streamlit Dashboard Features

1. **Sidebar Filters**  
   - Coin  
   - Relevance (`cryptocurrency` vs. `general`)  
   - Sentiment score range  
   - Price change range  

2. **Interactive Scatter**  
   Sentiment vs. Price Change, colored by relevance & coin, with hover headlines.

3. **Time-Series Scatter**  
   Price change over time for each headline event.

4. **Bucketed Bar Chart**  
   Average Δ% by sentiment bucket (with error bars).

5. **Top Movers Tables**  
   Top 5 positive/negative movers for crypto-related and general news.

---

## 📌 Completed Phase Overview

- **Phase 1**: Extraction of news & market data  
- **Phase 2**: Transformation, loading into Postgres, enrichment, and impact calculation  
- **Phase 3**: Analytics scripts and interactive Streamlit dashboard  

---

## 📖 How to Demo

1. **Run**:  
   ```bash
   docker-compose up --build
   ```  
2. **Browse**:  
   `http://localhost:8501/` to interact with the dashboard.  
3. **Explore**:  
   Use sidebar to slice data, hover scatter to read headlines, view bucket summaries and outlier tables.  

---

## 🔮 Next Steps

- Schedule ETL (cron, Prefect) for continuous updates.  
- Add deeper topic classification or embeddings.  
- Expand data sources (social media, forums).  
- Deploy dashboard to Streamlit Cloud or similar.  

---
