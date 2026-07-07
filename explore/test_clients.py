import os
import logging
from dotenv import load_dotenv
from src.ingestion.news_client import NewsClient
from src.ingestion.price_client import PriceClient

# Configure basic logging to see warnings/errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pipeline_clients():
    # Load secrets from .env file
    load_dotenv()
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        logger.error("NEWS_API_KEY not found in environment. Make sure your .env file is set up!")
        return

    print("=== TESTING PRICE CLIENT ===")
    # TODO Steps:
    # 1. Load the "POLYGON_API_KEY" from the environment using os.getenv().
    #    Check if it exists; if not, print an error and return.
    # 2. Instantiate the PriceClient passing the polygon_api_key.
    # 3. Call fetch_prices for "TSLA" (with days_back=2, multiplier=5, timespan="minute")
    # 4. Print the number of price ticks fetched.
    # 5. Print the first 2 ticks to verify the structure and timezone.
    
    polygon_api_key = os.getenv("MASSIVE_API_KEY")
    if not polygon_api_key:
        logger.error("MASSIVE_API_KEY not found in environment.")
        return
        
    price_client = PriceClient(polygon_api_key)
    
    price_ticks = price_client.fetch_prices("TSLA", days_back=5, multiplier=5, timespan="minute")
    
    print(f"Fetched {len(price_ticks)} price ticks.")
    if len(price_ticks) >= 2:
        print(price_ticks[0])
        print(price_ticks[1])
    elif len(price_ticks) == 1:
        print(price_ticks[0])
    else:
        print("No price ticks retrieved due to rate limiting or error.")

    print("\n=== TESTING NEWS CLIENT ===")
    
    # TODO Steps:
    # 1. Instantiate the NewsClient passing the api_key
    # 2. Call fetch_headlines for TSLA (query="Tesla", ticker="TSLA")
    # 3. Print the number of news articles fetched.
    # 4. Print the first article to verify the keys (especially content and published_at).
    
    news_client = NewsClient(api_key)
    news = news_client.fetch_headlines("Tesla", "TSLA")
    
    print(f"Fetched {len(news)} news articles.")
    if len(news) > 0:
        print(news[0])
    else:
        print("No news articles retrieved due to error.")
if __name__ == "__main__":
    test_pipeline_clients()
