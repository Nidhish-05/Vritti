import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.ingestion.news_client import NewsClient
from src.ingestion.price_client import PriceClient
from src.db.writer import insert_news_records, insert_price_ticks

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# The watchlist: Ticker -> News Search Query
WATCHLIST = {
    "TSLA": "Tesla OR TSLA OR Elon Musk",
    "AAPL": "Apple Inc OR AAPL OR iPhone",
    "MSFT": "Microsoft OR MSFT OR Windows"
}

async def price_polling_loop(pool, price_client: PriceClient):
    """
    Infinite loop that fetches prices for all tickers in WATCHLIST every 5 minutes.
    """
    logger.info("Starting Price Polling Loop...")
    # TODO Steps:
    # 1. Start an infinite loop using `while True:`
    while True:

        # 2. Inside the loop, acquire a connection from the asyncpg Pool:
        #    `async with pool.acquire() as conn:`
        async with pool.acquire() as conn:

            # 3. Iterate through each ticker in the WATCHLIST keys.
            #    - Call `price_client.fetch_prices(ticker, days_back=2)`
            for ticker in WATCHLIST:
                try:
                    ticks = price_client.fetch_prices(ticker, days_back=2)
                
                #    - If ticks are returned, call `await insert_price_ticks(conn, ticks)`
                #    - Wrap this in a try-except to prevent the loop from crashing if one ticker fails.
                    if ticks:
                        await insert_price_ticks(conn, ticks)

                except Exception as e:
                    logger.error(f"Failed to insert tick: {e}")
                
        # 4. Wait for 5 minutes (300 seconds) using `await asyncio.sleep(300)`.
        await asyncio.sleep(300)

async def news_polling_loop(pool, news_client: NewsClient):
    """
    Infinite loop that fetches news headlines for all tickers in WATCHLIST every 15 minutes.
    """
    logger.info("Starting News Polling Loop...")
    # TODO Steps:
    # 1. Start an infinite loop using `while True:`
    while True:

        # 2. Inside the loop, acquire a connection from the pool.
        async with pool.acquire() as conn:
    
        # 3. Iterate through the WATCHLIST keys and queries:
        #    - For each ticker and query, call `news_client.fetch_headlines(query, ticker)`
        #    - If articles are returned, call `await insert_news_records(conn, articles)`
        #    - Wrap in try-except so a single API error doesn't kill the entire loop.
            
            for ticker in WATCHLIST:
            
                try:
                    news_headlines = news_client.fetch_headlines(WATCHLIST.get(ticker), ticker)
                
                    if news_headlines:
                        await insert_news_records(conn, news_headlines)   
                
                except Exception as e:
                    logger.error(f"Failed to insert news article: {e}")
        # 4. Wait for 15 minutes (900 seconds) using `await asyncio.sleep(900)`.
        await asyncio.sleep(900)

async def main():
    # Load secrets
    load_dotenv()
    
    news_key = os.getenv("NEWS_API_KEY")
    massive_key = os.getenv("MASSIVE_API_KEY")
    
    # DB configuration
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "vritti_db")
    db_user = os.getenv("DB_USER", "vritti")
    db_password = os.getenv("DB_PASSWORD", "vritti_password")

    # TODO Steps:
    # 
    # 1. Instantiate the NewsClient and PriceClient.
    news_client = NewsClient(news_key)
    price_client = PriceClient(massive_key)
    # 2. Create the asyncpg connection pool:
    #    `pool = await asyncpg.create_pool(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)`
    pool = await asyncpg.create_pool(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    # 3. Run both loops concurrently. In asyncio, we use `asyncio.gather` to run tasks together:
    #    `await asyncio.gather(price_polling_loop(pool, price_client), news_polling_loop(pool, news_client))`
    try:
        await asyncio.gather(price_polling_loop(pool, price_client), news_polling_loop(pool, news_client))
    except Exception as e:
        logger.error(e)
    # 4. Ensure the pool is closed if the scheduler is stopped.
    finally:
        await pool.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
