import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.ingestion.news_client import NewsClient
from src.ingestion.price_client import PriceClient
from src.db.writer import insert_news_records, insert_price_ticks

#Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

#The watchlist: Ticker -> News Search Query
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
    
    #Start an infinite loop
    while True:

        #Starting the connection
        async with pool.acquire() as conn:

            #Iterating through the WATCHLIST
            for ticker in WATCHLIST:
                try:

                    #Fetching prices for the ticker
                    ticks = price_client.fetch_prices(ticker, days_back=2)
                
                    if ticks:

                        #Inserting tick in database
                        await insert_price_ticks(conn, ticks)

                except Exception as e:
                    logger.error(f"Failed to insert tick: {e}")
                
        #Wait for 5 min before next API request
        await asyncio.sleep(300)

async def news_polling_loop(pool, news_client: NewsClient):
    """
    Infinite loop that fetches news headlines for all tickers in WATCHLIST every 15 minutes.
    """
    logger.info("Starting News Polling Loop...")

    #Start an infinite loop
    while True:

        #Acquire a connection from the pool
        async with pool.acquire() as conn:
    
            #Iterating for every ticker in WATCHLIST
            for ticker in WATCHLIST:
            
                try:

                    #Fetching headlines
                    news_headlines = news_client.fetch_headlines(WATCHLIST.get(ticker), ticker)
                
                    if news_headlines:

                        #Running query to insert news records in database
                        await insert_news_records(conn, news_headlines)   
                
                except Exception as e:
                    logger.error(f"Failed to insert news article: {e}")
        
        #Wait for 15 minutes before next API request
        await asyncio.sleep(900)

async def main():
    
    #Load secrets
    load_dotenv()
    
    news_key = os.getenv("NEWS_API_KEY")
    massive_key = os.getenv("MASSIVE_API_KEY")
    
    # DB configuration
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "vritti_db")
    db_user = os.getenv("DB_USER", "vritti")
    db_password = os.getenv("DB_PASSWORD", "vritti_password")

    #Instantiate the NewsClient and PriceClient.
    news_client = NewsClient(news_key)
    price_client = PriceClient(massive_key)
    
    #Create the asyncpg connection pool:
    pool = await asyncpg.create_pool(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    
    #Run both loops concurrently.
    try:
        await asyncio.gather(price_polling_loop(pool, price_client), news_polling_loop(pool, news_client))
    except Exception as e:
        logger.error(e)
    
    #Ensure the pool is closed if the scheduler is stopped.
    finally:
        await pool.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
