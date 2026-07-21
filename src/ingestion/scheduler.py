import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.ingestion.news_client import NewsClient
from src.ingestion.price_client import PriceClient
from src.db.writer import insert_news_records, insert_price_ticks
from src.processing import aggregator
from src.processing.classifier import classify_pending_news
from src.processing.aggregator import SentimentAggregator
from src.processing.sentiment import SentimentPipeline
from src.signals.generator import SignalGenerator
from src.db.writer import insert_signal


#Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ── Watchlist ──────────────────────────────────────────────────────────────────
# Format: "TICKER": "NewsAPI search query"
#
# NEWS BATCHING STRATEGY (important for free tier):
#   NewsAPI free plan = 100 requests/day.
#   Rather than 1 request per ticker, several tickers share one query using OR.
#   The news_polling_loop fetches 50 articles per query — enough to cover all
#   tickers in a batch. Articles are tagged with the ticker key, not filtered by
#   the query result, so we get broad market coverage within the rate limit.
#
# PRICE POLLING:
#   Polygon.io free tier has no ticker-count limit — all 50 tickers are fetched
#   independently with a small sleep between requests to avoid throttling.
# ──────────────────────────────────────────────────────────────────────────────

WATCHLIST = {
    # ── Big Tech ──────────────────────────────────────────────────────────────
    "AAPL":  "Apple Inc OR AAPL OR iPhone OR Tim Cook",
    "MSFT":  "Microsoft OR MSFT OR Azure OR Satya Nadella",
    "GOOGL": "Alphabet OR Google OR GOOGL OR Sundar Pichai",
    "META":  "Meta Platforms OR META OR Facebook OR Mark Zuckerberg",
    "AMZN":  "Amazon OR AMZN OR AWS OR Andy Jassy",
    "NVDA":  "NVIDIA OR NVDA OR Jensen Huang OR GPU AI",
    "TSLA":  "Tesla OR TSLA OR Elon Musk OR electric vehicle",
    "ORCL":  "Oracle OR ORCL OR Larry Ellison OR cloud database",
    "CRM":   "Salesforce OR CRM OR Marc Benioff OR SaaS",
    "ADBE":  "Adobe OR ADBE OR Creative Cloud OR Firefly AI",

    # ── Semiconductors ────────────────────────────────────────────────────────
    "AMD":   "AMD OR Advanced Micro Devices OR Lisa Su OR Ryzen",
    "INTC":  "Intel OR INTC OR Pat Gelsinger OR semiconductor",
    "QCOM":  "Qualcomm OR QCOM OR Snapdragon OR 5G chip",
    "AVGO":  "Broadcom OR AVGO OR semiconductor OR networking chip",
    "TSM":   "TSMC OR TSM OR Taiwan Semiconductor OR chip foundry",

    # ── Finance & Banking ─────────────────────────────────────────────────────
    "JPM":   "JPMorgan OR JPM OR Jamie Dimon OR banking earnings",
    "GS":    "Goldman Sachs OR GS OR investment banking",
    "MS":    "Morgan Stanley OR MS OR wealth management",
    "BAC":   "Bank of America OR BAC OR consumer banking",
    "V":     "Visa OR payment network OR fintech earnings",

    # ── EV & Clean Energy ─────────────────────────────────────────────────────
    "RIVN":  "Rivian OR RIVN OR electric truck OR EV startup",
    "LCID":  "Lucid Motors OR LCID OR luxury EV OR electric car",
    "NIO":   "NIO OR Chinese EV OR electric vehicle China",
    "ENPH":  "Enphase Energy OR ENPH OR solar microinverter",
    "FSLR":  "First Solar OR FSLR OR solar panel OR clean energy",

    # ── Consumer & Retail ─────────────────────────────────────────────────────
    "NFLX":  "Netflix OR NFLX OR streaming OR Reed Hastings",
    "DIS":   "Disney OR DIS OR Disney+ OR Bob Iger OR streaming",
    "SBUX":  "Starbucks OR SBUX OR coffee OR Brian Niccol",
    "NKE":   "Nike OR NKE OR athletic OR John Donahoe",
    "MCD":   "McDonald's OR MCD OR fast food OR Chris Kempczinski",

    # ── Healthcare & Biotech ──────────────────────────────────────────────────
    "JNJ":   "Johnson and Johnson OR JNJ OR pharma OR medical device",
    "PFE":   "Pfizer OR PFE OR vaccine OR drug pipeline",
    "MRNA":  "Moderna OR MRNA OR mRNA OR vaccine biotech",
    "UNH":   "UnitedHealth OR UNH OR health insurance",
    "ABBV":  "AbbVie OR ABBV OR Humira OR immunology drug",

    # ── Cloud & Enterprise SaaS ───────────────────────────────────────────────
    "NOW":   "ServiceNow OR NOW OR enterprise software OR workflow AI",
    "SNOW":  "Snowflake OR SNOW OR data cloud OR data warehouse",
    "DDOG":  "Datadog OR DDOG OR cloud monitoring OR observability",
    "TEAM":  "Atlassian OR TEAM OR Jira OR developer tools",
    "ZS":    "Zscaler OR ZS OR cybersecurity OR zero trust",

    # ── Crypto-adjacent & Fintech ─────────────────────────────────────────────
    "COIN":  "Coinbase OR COIN OR crypto exchange OR Bitcoin",
    "PYPL":  "PayPal OR PYPL OR digital payments OR fintech",
    "SQ":    "Block OR Square OR SQ OR Jack Dorsey OR fintech",
    "HOOD":  "Robinhood OR HOOD OR retail investing OR commission-free",
    "MSTR":  "MicroStrategy OR MSTR OR Bitcoin treasury OR Michael Saylor",

    # ── Aerospace & Industrial ────────────────────────────────────────────────
    "BA":    "Boeing OR BA OR aerospace OR airline supply",
    "LMT":   "Lockheed Martin OR LMT OR defense contract OR fighter jet",
    "UBER":  "Uber OR UBER OR ride-hailing OR Dara Khosrowshahi",
    "LYFT":  "Lyft OR LYFT OR ride-sharing OR gig economy",
    "ABNB":  "Airbnb OR ABNB OR short-term rental OR travel platform",
}


async def price_polling_loop(pool, price_client: PriceClient, generator: SignalGenerator):
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
                        
                    # Sleep 12s to respect Polygon's 5 requests/minute free limit
                    await asyncio.sleep(12)

                except Exception as e:
                    logger.error(f"Failed to insert tick: {e}")
            
            for ticker in WATCHLIST:
                try:

                    #Generating signals for the ticks
                    signals = await generator.generate_signal(conn, ticker, window_hours=24)
                
                    if signals:

                        #Inserting signals in database
                        await insert_signal(conn, signals)

                except Exception as e:
                    logger.error(f"Failed to insert tick: {e}")

        #Wait for 5 min before next API request
        await asyncio.sleep(900)

async def news_polling_loop(pool, news_client: NewsClient, pipeline: SentimentPipeline):
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
                
                    if news_headlines is None:
                        logger.warning("NewsAPI rate limit reached. Skipping remaining tickers for this cycle.")
                        break

                    if news_headlines:

                        #Running query to insert news records in database
                        await insert_news_records(conn, news_headlines)   
                
                except Exception as e:
                    logger.error(f"Failed to insert news article: {e}")

            try:

                #Classifying the pending news
                count = await classify_pending_news(conn, pipeline)
                logger.info(f"Ran Classification for {count} Pending Articles")

            except Exception as e:
                logger.info(f"Error In Classification Of Pending News: {e}")
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
    pipeline = SentimentPipeline()
    aggregator = SentimentAggregator()
    generator = SignalGenerator(aggregator)

    #Create the asyncpg connection pool:
    pool = await asyncpg.create_pool(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    
    #Run both loops concurrently.
    try:
        await asyncio.gather(price_polling_loop(pool, price_client, generator), news_polling_loop(pool, news_client, pipeline))
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
