import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from utils.config import DB_URL, NEWS_CANDIDATE_LABELS

# 1. Page configuration
st.set_page_config(
    page_title="Crypt(Ech)o Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📈 Crypt(Ech)o News → Market Dashboard")

# 2. Data loading
@st.cache_data(ttl=600)
def load_impacts():
    engine = create_engine(DB_URL)
    sql = text("""
        SELECT
          n.id            AS article_id,
          n.title         AS headline,
          n.relevance_label,
          n.finbert_score AS sentiment,
          n.published_at AS  published_at,
          h.delta_pct     AS price_change,
          h.coin          AS coin
        FROM headline_impacts h
        JOIN news_articles n ON n.id = h.article_id
        WHERE n.finbert_score IS NOT NULL
          AND h.delta_pct IS NOT NULL
    """)
    df = pd.read_sql(sql, engine)
    return df

@st.cache_data(ttl=600)
def load_bucket_summary():
    path = "data/analytics/sentiment_bucket_summary.csv"
    return pd.read_csv(path)

@st.cache_data(ttl=600)
def load_outliers(label, polarity):
    # label: 'cryptocurrency' or 'general'
    # polarity: 'positive' or 'negative'
    path = f"data/analytics/{label}_top_{polarity}.csv"
    return pd.read_csv(path)

# Load datasets
df_impacts = load_impacts()
bucket_df = load_bucket_summary()

# 3. Sidebar filters
st.sidebar.header("Filters")

# Coin filter
coins = ['all'] + sorted(df_impacts['coin'].unique().tolist())
selected_coin = st.sidebar.selectbox("Coin", coins)
if selected_coin != 'all':
    df_impacts = df_impacts[df_impacts['coin'] == selected_coin]
else:
    df_impacts = load_impacts()

# Relevance filter
relevances = ['all'] + sorted(df_impacts['relevance_label'].unique().tolist())
selected_rel = st.sidebar.selectbox("Relevance", relevances)
if selected_rel != 'all':
    df_impacts = df_impacts[df_impacts['relevance_label'] == selected_rel]
else:
    df_impacts = load_impacts()

# Sentiment range
sent_min, sent_max = st.sidebar.slider(
    "Sentiment Score Range", 0.0, 1.0,
    (float(df_impacts.sentiment.min()), float(df_impacts.sentiment.max())), 0.01
)
df_impacts = df_impacts[df_impacts['sentiment'].between(sent_min, sent_max)]

# Price change range
pc_min, pc_max = st.sidebar.slider(
    "Price Change (%) Range",
    float(df_impacts.price_change.min()), float(df_impacts.price_change.max()),
    (float(df_impacts.price_change.min()), float(df_impacts.price_change.max())), 0.1
)
df_impacts = df_impacts[df_impacts['price_change'].between(pc_min, pc_max)]

# 4. Main visuals
## 4.1 Interactive Scatter
st.subheader("Interactive Sentiment vs. Price Change Scatter")
fig_scatter = px.scatter(
    df_impacts,
    x='sentiment', y='price_change',
    color='relevance_label',
    symbol='coin',
    hover_data=['headline'],
    labels={
        'sentiment': 'Sentiment Score',
        'price_change': 'Price Change (%)'
    },
    title='Sentiment vs. Price Change'
)
st.plotly_chart(fig_scatter, use_container_width=True)

## 4.2 Bucketed Summary Bar Chart
st.subheader("Average Price Change by Sentiment Bucket")
bc = bucket_df
fig, ax = plt.subplots()
ax.bar(bc['bucket'], bc['avg_change'], yerr=bc['std_change'], capsize=5)
ax.set_xlabel('Sentiment Bucket')
ax.set_ylabel('Average Price Change (%)')
ax.set_title('Avg Δ% by Sentiment Bucket')
st.pyplot(fig)

## 4.3 Relevance Labels vs Price change


## 4.4 Top Movers Tables
for relevance_label in NEWS_CANDIDATE_LABELS:
    for movement_direction in ['positive', 'negative']:
        st.markdown(f"**Top 5 {relevance_label}-Related {movement_direction} Movers**")
        st.table(load_outliers(relevance_label, movement_direction)[['delta_pct', 'title']].rename(
            columns={'delta_pct': 'Δ%'}
        ))

## 4.5 Price Change vs. Date Time Series
st.subheader("Price Change Over Time")
# Ensure published_at is datetime
df_impacts['published_at'] = pd.to_datetime(df_impacts['published_at'])
fig_time = px.scatter(
    df_impacts,
    x='published_at', y='price_change',
    color='relevance_label',
    hover_data=['headline', 'relevance_label', 'sentiment'],
    labels={
        'published_at': 'Published At',
        'price_change': 'Price Change (%)'
    },
    title='Price Change vs. Published Date'
)
st.plotly_chart(fig_time, use_container_width=True)

st.markdown("---")
st.write("Built with **Streamlit**, **Plotly**, and **SQLAlchemy**. Use sidebar filters to explore how news sentiment and relevance correlate with market movements.")
