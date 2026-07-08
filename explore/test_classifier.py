import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.processing.sentiment import SentimentPipeline
from src.processing.classifier import classify_pending_news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_classifier():
    # 1. Load secrets from .env
    load_dotenv()
    
    # 2. Get database credentials
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "vritti_db")
    db_user = os.getenv("DB_USER", "vritti")
    db_password = os.getenv("DB_PASSWORD", "vritti_password")

    # TODO Steps:
    # 
    # Step A: Connect to TimescaleDB
    # 1. Connect to the database using asyncpg.connect.
    #    Wrap in try-except and return early on failure.
    try:
    
        conn = await asyncpg.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    except Exception as e:
        logger.error(e)
        return 0
    # Step B: Initialize the Sentiment Pipeline
    # 2. Instantiate your SentimentPipeline class.
    pipeline = SentimentPipeline()
    
    # Step C: Classify News
    # 3. Call classify_pending_news passing the connection and the pipeline.
    #    Save and print the count of classified articles.
    classified_news = await classify_pending_news(conn, pipeline)

    # Step D: Verify Database Results
    # 4. Run a query using conn.fetch to select the ticker, published_at,
    #    sentiment_score, and sentiment_label for a few articles from the
    #    news_sentiment table where the sentiment_score is NOT NULL.
    # 5. Loop through and print those articles to verify the data was written.
    print("=======FETCHING UPDATED COLUMNS========")
    rows = await conn.fetch("SELECT ticker, published_at, sentiment_score, sentiment_label FROM news_sentiment WHERE sentiment_score IS NOT NULL LIMIT 5")
    for row in rows:
        print(row)
    # Step E: Clean Up
    # 6. Close the database connection.
    await conn.close()

if __name__ == "__main__":
    asyncio.run(test_classifier())
