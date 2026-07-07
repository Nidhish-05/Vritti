import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.ingestion.news_client import NewsClient
from src.ingestion.price_client import PriceClient
from src.db.writer import insert_news_records, insert_price_ticks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_full_pipeline():
    # 1. Load secrets from .env
    load_dotenv()
    
    # 2. Get credentials
    news_key = os.getenv("NEWS_API_KEY")
    massive_key = os.getenv("MASSIVE_API_KEY")
    
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "vritti_db")
    db_user = os.getenv("DB_USER", "vritti")
    db_password = os.getenv("DB_PASSWORD", "vritti_password")

    # TODO Steps:
    # 
    # Step A: Fetch Live Data
    # 1. Instantiate NewsClient and fetch TSLA headlines (query="Tesla", ticker="TSLA").
    news_client = NewsClient(news_key)
    TSLA_headlines = news_client.fetch_headlines(query="Tesla OR TSLA OR Elon Musk", ticker="TSLA")
    
    # 2. Instantiate PriceClient and fetch TSLA prices (days_back=5).
    price_client = PriceClient(massive_key)
    TSLA_stock_prices = price_client.fetch_prices(ticker="TSLA", days_back=5)
    
    # 3. Print the number of items fetched for both.
    print(f"Number of TESLA news articles fetched: {len(TSLA_headlines)}")
    print(f"Number of TESLA stock prices fetched: {len(TSLA_stock_prices)}")
    
    # Step B: Connect to TimescaleDB
    # 4. Connect to the database using:
    #    conn = await asyncpg.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    #    (Wrap in try-except in case Docker container is not running!)
    try:
        conn = await asyncpg.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        return

    # Step C: Write to Database
    # 5. Call insert_price_ticks(conn, price_ticks) and print how many rows were processed.
    await insert_price_ticks(conn, TSLA_stock_prices)
    
    # 6. Call insert_news_records(conn, news) and print how many rows were processed.
    await insert_news_records(conn, TSLA_headlines)

    # Step D: Verify Database Contents
    # 7. Query the DB to check if the records are actually there!
    #    Hint:
    #    price_count = await conn.fetchval("SELECT COUNT(*) FROM price_ticks;")
    #    news_count = await conn.fetchval("SELECT COUNT(*) FROM news_sentiment;")
    #    print(f"Total price ticks now in DB: {price_count}")
    #    print(f"Total news articles now in DB: {news_count}")
    price_count = await conn.fetchval("SELECT COUNT(*) FROM price_ticks;")
    news_count = await conn.fetchval("SELECT COUNT(*) FROM news_sentiment;")
    print(f"Total price ticks now in DB: {price_count}")
    print(f"Total news articles now in DB: {news_count}")

    # Step E: Close Connection
    # 8. Close the connection using `await conn.close()`.
    await conn.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(test_full_pipeline())
