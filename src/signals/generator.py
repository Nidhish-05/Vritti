import logging
from datetime import datetime, timezone
from src.processing import aggregator
from src.processing.aggregator import SentimentAggregator

logger = logging.getLogger(__name__)

class SignalGenerator:
    """
    Class to analyze sentiment and momentum to generate stock trading signals.
    """

    def __init__(self, aggregator: SentimentAggregator):

        #Store the passed aggregator instance.
        self.aggregator = aggregator

    async def calculate_momentum(self, conn, ticker: str) -> float:
        """
        Calculates price momentum over the last 5 price ticks from the database.

        Args:
            conn: An active asyncpg Connection or Pool.
            ticker: Stock ticker symbol.
        Returns:
            The calculated momentum (float).
        """
        
        #SQL query to select the close price of the ticks.
        # - Filter by ticker.
        # - Sort by time in descending order (newest first).
        # - Limit the results to get enough ticks to compute a 5-period change.
        min_ticks_required = 6
        query = ''' SELECT price_close FROM price_ticks
                    WHERE ticker = ($1)
                    ORDER BY stock_date_time DESC
                    LIMIT ($2);
                ''' 

        #Fetch the rows from the database.
        rows = await conn.fetch(query, ticker, min_ticks_required)

        #Guard Clause: If there are not enough ticks to calculate momentum, return 0.0.
        if len(rows)< min_ticks_required:
            momentum = 0.0
            return momentum
        
        #Extract the most recent close price and the oldest close price from the fetched rows.
        latest_cp = rows[0].get('price_close')
        oldest_cp = rows[-1].get('price_close')
        
        #Calculate the percentage change (momentum) as a float.
        momentum = float(((latest_cp - oldest_cp)/oldest_cp) *100)
        
        #Return the calculated momentum
        return momentum

    async def generate_signal(self, conn, ticker: str, window_hours: int = 24) -> dict:
        """
        Combines rolling sentiment and price momentum to generate a BUY/HOLD/SELL signal.

        Args:
            conn: An active asyncpg Connection or Pool.
            ticker: Stock ticker symbol.
            window_hours: The rolling window for sentiment calculation (default 24).
        Returns:
            Dictionary containing the signal details.
        """

        #To compute the rolling sentiment for the ticker.
        rolling_sentiment = await self.aggregator.compute_rolling_sentiment(conn, ticker, window_hours)
        
        #To get the price momentum.
        price_momentum = await self.calculate_momentum(conn, ticker) 
        
        #Threshold limits for both sentiment and momentum.
        if price_momentum>0 and rolling_sentiment['weighted_score']>0:
            value = "positive"
        elif price_momentum<0 and rolling_sentiment['weighted_score']<0:
            value = "negative" 
        else:
            value = "neutral"

        #Logic to determine the signal ("BUY", "HOLD", or "SELL"):
        #    - A BUY signal requires both positive sentiment and positive momentum.
        #    - A SELL signal requires both negative sentiment and negative momentum.
        #    - Otherwise, default the signal to HOLD.
        if value =="positive":
            signal = "BUY"
        elif value =="negative":
            signal = "SELL"
        else:
            signal = "HOLD"

        #Signal Dictionary mapped to the database
        signal_dict = {
            'ticker': ticker,
            'signal': signal,
            'sentiment_score': rolling_sentiment.get('weighted_score'),
            'momentum': price_momentum,
            'window_hours': window_hours,
            'generated_at': datetime.now(timezone.utc)
        }

        #Return the signal Dictionary
        return signal_dict

