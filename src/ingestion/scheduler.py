import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.ingestion.news_client import NewsClient
from src.ingestion.price_client import PriceClient
from src.db.writer import insert_news_records, insert_price_ticks
from src.processing.classifier import classify_pending_news
from src.processing.aggregator import SentimentAggregator
from src.processing.sentiment import SentimentPipeline
from src.signals.generator import SignalGenerator
from src.db.writer import insert_signal


#Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ── Rate Limit Budget ─────────────────────────────────────────────────────────
# NewsAPI free tier: 100 requests/day.
# This cloud version uses 10 tickers — 1 request per ticker = 10 requests/run.
# Running this script up to 8 times/day stays well under the 100/day limit.
#
# Polygon (Massive) free tier: 5 requests/minute.
# We sleep 12s between each ticker request (= 5 req/min exactly).
# ─────────────────────────────────────────────────────────────────────────────

# ── Watchlist — 10 Representative Tickers ────────────────────────────────────
# One ticker from each major sector. Deliberately trimmed from the 50-ticker
# master-local version to stay within free-tier API limits on the cloud.
# Format: "TICKER": "NewsAPI search query"
# ─────────────────────────────────────────────────────────────────────────────
WATCHLIST = {
    # Big Tech
    "AAPL":  "Apple Inc OR AAPL OR iPhone OR Tim Cook",
    # Semiconductors
    "NVDA":  "NVIDIA OR NVDA OR Jensen Huang OR GPU AI",
    # Finance
    "JPM":   "JPMorgan OR JPM OR Jamie Dimon OR banking earnings",
    # EV & Clean Energy
    "TSLA":  "Tesla OR TSLA OR Elon Musk OR electric vehicle",
    # Consumer & Retail
    "NFLX":  "Netflix OR NFLX OR streaming OR Reed Hastings",
    # Healthcare & Biotech
    "PFE":   "Pfizer OR PFE OR vaccine OR drug pipeline",
    # Cloud & SaaS
    "MSFT":  "Microsoft OR MSFT OR Azure OR Satya Nadella",
    # Crypto & Fintech
    "COIN":  "Coinbase OR COIN OR crypto exchange OR Bitcoin",
    # Aerospace & Industrial
    "BA":    "Boeing OR BA OR aerospace OR airline supply",
    # Emerging / High-growth
    "GOOGL": "Alphabet OR Google OR GOOGL OR Sundar Pichai",
}


async def run_price_ingestion(conn, price_client: PriceClient, generator: SignalGenerator):
    """
    Single-run: fetches price ticks for all 10 WATCHLIST tickers, inserts them
    into the DB, then generates and stores trading signals.

    Sleeps 12s between each Polygon request to respect the 5 req/min free limit.
    """
    logger.info("── Price Ingestion: starting ──")

    for ticker in WATCHLIST:
        try:
            ticks = price_client.fetch_prices(ticker, days_back=2)

            if ticks:
                await insert_price_ticks(conn, ticks)
                logger.info(f"[{ticker}] Inserted {len(ticks)} price ticks.")

            # 12s sleep = 5 requests/minute — exactly at Polygon free-tier limit
            await asyncio.sleep(12)

        except Exception as e:
            logger.error(f"[{ticker}] Price ingestion failed: {e}")

    logger.info("── Price Ingestion: complete ──")

    logger.info("── Signal Generation: starting ──")

    for ticker in WATCHLIST:
        try:
            signal = await generator.generate_signal(conn, ticker, window_hours=24)
            if signal:
                await insert_signal(conn, signal)
                logger.info(f"[{ticker}] Signal: {signal.get('signal')} (sentiment={signal.get('sentiment_score'):.4f}, momentum={signal.get('momentum'):.4f})")

        except Exception as e:
            logger.error(f"[{ticker}] Signal generation failed: {e}")

    logger.info("── Signal Generation: complete ──")


async def run_news_ingestion(conn, news_client: NewsClient, pipeline: SentimentPipeline):
    """
    Single-run: fetches news headlines for all 10 WATCHLIST tickers, inserts
    them into the DB, then runs FinBERT classification on all pending articles.

    Sleeps 1s between each NewsAPI request to avoid burst throttling.
    10 tickers = 10 requests per run, safely within the 100/day free limit.
    """
    logger.info("── News Ingestion: starting ──")

    requests_used = 0

    for ticker in WATCHLIST:
        try:
            news_headlines = news_client.fetch_headlines(WATCHLIST.get(ticker), ticker)
            requests_used += 1

            if news_headlines is None:
                logger.warning(f"[{ticker}] NewsAPI rate limit hit. Stopping news ingestion early.")
                break

            if news_headlines:
                await insert_news_records(conn, news_headlines)
                logger.info(f"[{ticker}] Inserted {len(news_headlines)} news articles.")

            # 1s gap between requests to avoid burst throttling
            await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"[{ticker}] News ingestion failed: {e}")

    logger.info(f"── News Ingestion: complete ({requests_used}/{len(WATCHLIST)} tickers fetched) ──")

    logger.info("── FinBERT Classification: starting ──")

    try:
        count = await classify_pending_news(conn, pipeline)
        logger.info(f"── FinBERT Classification: complete ({count} articles classified) ──")
    except Exception as e:
        logger.error(f"FinBERT classification failed: {e}")


async def main():
    """
    Cloud scheduler entry point — single sequential run.

    Execution order:
      1. Connect to Neon PostgreSQL via ASYNC_DATABASE_URL
      2. Fetch prices for all 10 tickers (12s between each → 5 req/min)
      3. Generate BUY/HOLD/SELL signals and write to DB
      4. Fetch news headlines (1s between each)
      5. Run FinBERT classification on unscored articles
      6. Close the pool and exit

    Designed to be triggered by a cron job or manually — not an infinite loop.
    On Render: deploy as a Background Worker or trigger via external cron.
    Locally against Neon: run `python -m src.ingestion.scheduler` with ASYNC_DATABASE_URL set.
    """
    load_dotenv()

    news_key = os.getenv("NEWS_API_KEY")
    massive_key = os.getenv("MASSIVE_API_KEY")
    db_string = os.getenv("ASYNC_DATABASE_URL")

    if not db_string:
        logger.error("ASYNC_DATABASE_URL is not set. Exiting.")
        return

    if not news_key:
        logger.warning("NEWS_API_KEY is not set. News ingestion will fail.")

    if not massive_key:
        logger.warning("MASSIVE_API_KEY is not set. Price ingestion will fail.")

    #Instantiate clients and pipeline
    news_client = NewsClient(news_key)
    price_client = PriceClient(massive_key)
    pipeline = SentimentPipeline()
    aggregator_instance = SentimentAggregator()
    generator = SignalGenerator(aggregator_instance)

    logger.info("Connecting to Neon PostgreSQL...")

    try:
        pool = await asyncpg.create_pool(dsn=db_string)
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return

    logger.info("Connected. Starting single-run ingestion cycle.")

    try:
        async with pool.acquire() as conn:
            # Step 1: Price ingestion + signal generation
            await run_price_ingestion(conn, price_client, generator)

            # Step 2: News ingestion + FinBERT classification
            await run_news_ingestion(conn, news_client, pipeline)

        logger.info("Ingestion cycle complete. Exiting.")

    except Exception as e:
        logger.error(f"Unexpected error during ingestion cycle: {e}")

    finally:
        await pool.close()
        logger.info("Database pool closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted by user.")
