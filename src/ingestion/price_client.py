from csv import excel_tab
import logging
import requests
from datetime import date, datetime, timedelta, timezone
import json

logger = logging.getLogger(__name__)

class PriceClient:
    """
    Client class to interact with Polygon.io and fetch stock price ticks.
    """

    def __init__(self, api_key: str):
        # TODO: Store the passed api_key as an instance attribute (e.g., self.api_key)
        # so other methods can access it.
        self.api_key = api_key

    def fetch_prices(self, ticker: str, days_back: int = 2, multiplier: int = 5, timespan: str = "minute") -> list[dict]:
        """
        Fetches historical price ticks for a given ticker from Polygon.io, and returns
        a list of dictionaries matching the columns in our `price_ticks` database table.

        Args:
            ticker: Stock ticker symbol (e.g. "TSLA")
            days_back: How many days of history to fetch (default: 2, to handle weekends safely)
            multiplier: The size of the timespan (e.g., 5 for 5-minute ticks)
            timespan: The size of the interval (e.g., "minute", "hour", "day")
        Returns:
            List of cleaned dicts with keys:
            ['ticker', 'stock_date_time', 'price_open', 'price_high',
             'price_low', 'price_close', 'stock_volume']
        """
        #To check if api_key is present or not (Guard Clause)
        try:
            if not self.api_key:
                logger.error("No API key detected; Try again!")
                
                return []

            #Set the timestamps
            now = datetime.now(timezone.utc)
            to_date = now.strftime("%Y-%m-%d")
            from_date = (now - timedelta(days=days_back)).strftime("%Y-%m-%d")

            #Creating the URL for API requests        
            massive_url = f"https://api.massive.com/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}?apiKey={self.api_key}"
            
       
            #Make a request to the API
            response = requests.get(url=massive_url)

            if response.status_code !=200:
                logger.error(f"Status Code: {response.status_code}")
                return []                    
                
            #To parse the response
            data = response.json()

            #To get the list "results"  
            results = data.get("results")  

            #Check if the "results" key is present in the response dictionary.
            if not results:

                #If not, or if the list is empty, log a debug message and return [].
                logger.debug(f"[{ticker}] No price data received (market may be closed).")
                return []
            else:
        
                #Initialize an empty list to hold your cleaned price ticks.
                cleaned_price_ticks = list()
                       
                #Loop through the items in the "results" list. Each item is a dictionary representing one tick.
                for result in results:
                    stock_date_time_ms = result['t']
                    stock_date_time =  datetime.fromtimestamp(stock_date_time_ms/1000, tz=timezone.utc)
                    price_open = float(result['o'])
                    price_high = float(result['h'])
                    price_low = float(result['l'])
                    price_close = float(result['c'])
                    stock_volume = int(result['v'])

                    tick={
                        'ticker': ticker,
                        'stock_date_time': stock_date_time,
                        'price_open': price_open,
                        'price_high': price_high,
                        'price_low': price_low,
                        'price_close': price_close,
                        'stock_volume': stock_volume
                        }
                            
                    #Append each mapped dictionary to your list.
                    cleaned_price_ticks.append(tick)
                    
                #Return the list of price ticks.
                return cleaned_price_ticks
        
        #log the exception, and return []
        except Exception as e:
            logger.error(e)
            return []

        

