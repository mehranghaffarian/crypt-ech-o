import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from utils.config import DB_URL

def generate_sentiment_plot(output_html="data/analytics/interactive_sentiment.html"):
    engine = create_engine(DB_URL)
    # Load your joined data, including title
    sql = text("""
      SELECT
        n.id            AS article_id,
        n.title         AS headline,
        n.relevance_label AS label,
        n.finbert_score AS sentiment,
        n.relevance_score AS relevance_score,
        h.delta_pct     AS price_change
      FROM headline_impacts h
      JOIN news_articles n ON n.id = h.article_id
      WHERE n.finbert_score IS NOT NULL
        AND h.delta_pct IS NOT NULL
        AND n.relevance_score > 0.6
    """)
    df = pd.read_sql(sql, engine)

    # Build hover text
    df["hover"] = (
        "Headline: " + df["headline"].str.slice(0, 100).fillna("") +
        "<br>Sentiment: " + df["sentiment"].round(3).astype(str) +
        "<br>Relevance Score: " + df["relevance_score"].round(3).astype(str) +
        "<br>Price Δ%: "    + df["price_change"].round(3).astype(str)
    )

    # Create Plotly scatter
    fig = px.scatter(
        df,
        x="relevance_score",
        y="price_change",
        color="label",
        hover_name="headline",
        hover_data={"sentiment": True, "price_change": True},
        labels={"sentiment": "Sentiment Score", "price_change": "Price Change (%)"},
        title="Interactive: Sentiment vs. Price Change"
    )
    # Override hovertemplate to use our custom text
    fig.update_traces(hovertemplate=df["hover"])

    # Save to standalone HTML
    fig.write_html(output_html, include_plotlyjs='cdn')
    print(f"Interactive plot saved to {output_html}")

if __name__ == "__main__":
    generate_sentiment_plot()
