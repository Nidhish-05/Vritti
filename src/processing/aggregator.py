import logging
import asyncpg
import pandas as pd
from datetime import UTC, date, datetime, timedelta, timezone

from pandas import cut
from pytz import utc

logger = logging.getLogger(__name__)

class SentimentAggregator:
    """
    Class to calculate rolling weighted sentiment scores for stock tickers
    using Exponentially Weighted Moving Average (EWMA).
    """

    def __init__(self):
        pass

    async def compute_rolling_sentiment(self, conn, ticker: str, window_hours: int) -> dict:
        """
        Fetches recent sentiment records from the database, applies EWMA weighting,
        and calculates the rolling sentiment score.

        Args:
            conn: An active asyncpg Connection or Pool.
            ticker: Stock ticker symbol (e.g. "TSLA").
            window_hours: Rolling window size (e.g. 1, 6, or 24).
        Returns:
            Dictionary containing:
            ['ticker', 'window_hours', 'weighted_score', 'article_count', 'computed_at']
        """
        #Compute the cutoff timestamp
        time_rn = datetime.now(timezone.utc)
        cutoff_timestamp = time_rn - timedelta(hours=window_hours)
        
        #SQL query to select the recent news articles from news_sentiment
        query = '''SELECT * FROM news_sentiment 
                   WHERE ticker =($1) AND published_at >= ($2) AND sentiment_score IS NOT NULL
                   ORDER BY published_at ASC; 
                ''' 
        #Fetch the rows from the database.
        rows = await conn.fetch(query, ticker, cutoff_timestamp)
        
        #Guard Clause: If no articles are found, return a dictionary with:
        #    - ticker
        #    - window_hours
        #    - weighted_score as 0.0
        #    - article_count as 0
        #    - computed_at as the current UTC time.
        if not rows:
            logger.error("Couldn't fetch rows")
            return {'ticker': ticker, 'window_hours': window_hours, 'weighted_score': 0, 'article_count': 0, 'computed_at': datetime.now(timezone=utc)} 
        
        #Extract values and convert the fetched rows to a list of dicts.
        list_of_dicts = []
        for row in rows:
            
            #Convert the sentiment label in numerical terms: 1.0 for positive, 0.0 for neutral, -1.0 for negative
            sentiment_label = row.get('sentiment_label')
            if sentiment_label == 'positive':
                sentiment_label = float(1.0)
            elif sentiment_label == 'negative':
                sentiment_label = float(-1.0)
            else:
                sentiment_label = float(0.0) 

            r_dict = {
                'ticker': ticker,
                'sentiment_score': row.get('sentiment_score'),
                'sentiment_label': sentiment_label,
                'article_title': row.get('article_title'),
                'article_description': row.get('article_description'),
                'content': row.get('content'),
                'published_at': row.get('published_at'),
                'article_url': row.get('article_url')
            }
            list_of_dicts.append(r_dict)

        #Convert the list of dicts into a Pandas DataFrame.
        df = pd.DataFrame(list_of_dicts) 
        
        #Set the DataFrame's index to be the published_at timestamps.
        df = df.set_index('published_at') 
        
        #Apply the Exponential Moving Average (.ewm) calculation on the 
        #    numerical sentiment column.
        ewma_series = df['sentiment_label'].ewm(halflife=0.4*window_hours).mean()

        #Extract the very last value of the calculated EWMA series.
        row_dict = {
                'ticker': ticker,
                'window_hours': window_hours,
                'weighted_score': float(ewma_series.iloc[-1]),
                'article_count': len(list_of_dicts),
                'computed_at': datetime.now(timezone.utc)
            }
        
        #Return a dictionary containing:
        #     - ticker
        #     - window_hours
        #     - weighted_score (the extracted float value)
        #     - article_count (the number of articles in the DataFrame)
        #     - computed_at (current UTC time)
        return row_dict