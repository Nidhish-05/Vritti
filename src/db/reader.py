import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

async def get_latest_signal(conn, ticker: str) -> dict | None:
    """
    Fetches the single most recently generated signal record for a given ticker.

    Args:
        conn: An active asyncpg Connection or Pool.
        ticker: Stock ticker symbol.
    Returns:
        Dictionary of the row, or None if no signals found.
    """
    
    #SQL query to select columns from the signals table.
    query = ''' SELECT * FROM signals
                WHERE ticker = ($1)
                ORDER BY generated_at DESC
                LIMIT 1;
            '''
    
    #Fetch the single row from the database.
    row = await conn.fetchrow(query, ticker)

    #Return the row as a dict
    return [dict(row) for row in rows]
    

async def get_all_signals(conn) -> list[dict]:
    """
    Fetches the latest signal record for every unique ticker in the database.

    Args:
        conn: An active asyncpg Connection or Pool.
    Returns:
        List of dictionaries containing the latest signal per ticker.
    """
    
    #SQL query to select the latest signal for each distinct ticker.
    query = '''SELECT DISTINCT ON (ticker) * FROM signals
               ORDER BY ticker ASC, generated_at DESC;
            ''' 
    
    #Fetch the rows from the database.
    rows = await conn.fetch(query)

    #Convert and return the fetched rows as a list of dictionaries.
    if rows:
        return [dict(row) for row in rows]

async def get_sentiment_history(conn, ticker: str, hours: int) -> list[dict]:
    """
    Retrieves sentiment score history for a ticker over a rolling window.

    Args:
        conn: An active asyncpg Connection or Pool.
        ticker: Stock ticker symbol.
        hours: How many hours back to retrieve.
    Returns:
        List of dictionaries of news sentiment records.
    """

    #Calculate the cutoff timestamp (Current time minus the hours window).
    current_time = datetime.now(timezone.utc)
    cutoff_timestamp = current_time - timedelta(hours=hours)

    #SQL query to select news sentiment columns.
    query = ''' SELECT * FROM news_sentiment
                WHERE ticker = ($1) AND published_at >= ($2) AND sentiment_score IS NOT NULL
                ORDER BY published_at DESC;
            ''' 
    
    #Fetch the rows from the database.
    rows = await conn.fetch(query, ticker, cutoff_timestamp)

    #Convert and return the rows as a list of dictionaries.
    return [dict(row) for row in rows]

async def get_price_history(conn, ticker: str, hours: int) -> list[dict]:
    """
    Retrieves price history ticks for a ticker over a rolling window.

    Args:
        conn: An active asyncpg Connection or Pool.
        ticker: Stock ticker symbol.
        hours: How many hours back to retrieve.
    Returns:
        List of dictionaries of price ticks.
    """
    #Calculate the cutoff timestamp (Current time minus the hours window).
    current_time = datetime.now(timezone.utc)
    cutoff_timestamp = current_time - timedelta(hours=hours)

    #SQL query to select price columns.
    query = ''' SELECT * FROM price_ticks
                WHERE ticker = ($1) AND stock_date_time >= ($2)
                ORDER BY stock_date_time;
            '''
    
    #Fetch the rows from the database.
    rows = await conn.fetch(query, ticker, cutoff_timestamp)

    #Convert and return the rows as a list of dictionaries.
    
    return [dict(row) for row in rows]

async def get_latest_news(conn, ticker: str, limit: int = 10) -> list[dict]:
    """
    Retrieves the most recent news articles for a ticker.

    Args:
        conn: An active asyncpg Connection or Pool.
        ticker: Stock ticker symbol.
        limit: Max number of articles to return (default 10).
    Returns:
        List of dictionaries of news records.
    """

    #SQL query to select news sentiment columns.
    query = ''' SELECT * FROM news_sentiment
                WHERE ticker = ($1)
                ORDER BY published_at DESC
                LIMIT ($2);
            ''' 
    
    #Fetch the rows from the database.
    rows = await conn.fetch(query, ticker, limit)

    #Convert and return the rows as a list of dictionaries.
    return [dict(row) for row in rows]
