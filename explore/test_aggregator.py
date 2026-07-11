import datetime
import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.processing.aggregator import SentimentAggregator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_aggregator():
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
        logger.error("Error in establishing connection: ", e)
        return []
    # Step B: Initialize the Sentiment Aggregator
    # 2. Instantiate your SentimentAggregator class.
    aggregator = SentimentAggregator()
    # Step C: Compute and Print Rolling Sentiments
    # 3. Define the windows to test (e.g. 1 hour, 6 hours, 24 hours).
    window_test = 168 #hours
    # 4. Iterate through each window.
    #    - Call compute_rolling_sentiment passing the connection, ticker "TSLA", and the window.
    #    - Print the resulting dictionary to see the weighted score.
    result_dict = await aggregator.compute_rolling_sentiment(conn, 'TSLA', window_test)
    print(result_dict)
    # Step D: Clean Up
    # 5. Close the database connection.
    await conn.close()

if __name__ == "__main__":
    asyncio.run(test_aggregator())
