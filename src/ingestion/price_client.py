import logging
import yfinance as yf
import pandas as pd

logger = logging.getLogger(__name__)

class PriceClient:
    """
    Client class to interact with yfinance and fetch stock price ticks.
    """

    def __init__(self):
        # NOTE: yfinance doesn't require an API key or client initialization.
        # We don't need to store any credentials here, but having the structure
        # keeps our clients consistent!
        pass

    def fetch_prices(self, ticker: str, period: str = "1d", interval: str = "5m") -> list[dict]:
        """
        Fetches historical price ticks for a given ticker from yfinance, and returns
        a list of dictionaries matching the columns in our `price_ticks` database table.

        Args:
            ticker: Stock ticker symbol (e.g. "TSLA")
            period: The time period of data to retrieve (e.g., "1d", "5d", "7d")
            interval: The frequency of the ticks (e.g., "1m", "5m", "15m", "1h")
        Returns:
            List of cleaned dicts with keys:
            ['ticker', 'stock_date_time', 'price_open', 'price_high',
             'price_low', 'price_close', 'stock_volume']
        """
        # TODO Steps:
        # 1. Wrap in a try-except block to capture any network/API errors.
        #
        # 2. Get the yfinance Ticker object using yf.Ticker(ticker).
        #
        # 3. Call ticker.history(...) passing the period and interval arguments.
        #    This returns a pandas DataFrame.
        #
        # 4. Check if the returned DataFrame is empty. If it is, log a warning and return []
        #
        # 5. Reset the index of the DataFrame using `df.reset_index()` so that the
        #    datetime index becomes a regular column we can access.
        #
        # 6. Initialize an empty list to hold the cleaned price tick dicts.
        #
        # 7. Loop through the rows of the DataFrame.
        #    Tip: You can use `df.iterrows()` or iterate through the DataFrame indices.
        #    For each row, extract and map the fields to match our DB columns:
        #    - 'ticker': ticker (string)
        #    - 'stock_date_time': The datetime value from the index/date column.
        #                         Ensure this is converted to a timezone-aware UTC datetime
        #                         (e.g., using pandas.to_datetime() and converting to UTC).
        #    - 'price_open': Open price (float)
        #    - 'price_high': High price (float)
        #    - 'price_low': Low price (float)
        #    - 'price_close': Close price (float)
        #    - 'stock_volume': Volume (int)
        #
        # 8. Append each mapped dictionary to your list.
        #
        # 9. Return the list of price tick dicts.
        #
        # 10. In the except block: log the exception using logger.error, and return []
        pass
