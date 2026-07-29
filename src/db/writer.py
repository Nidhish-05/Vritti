import logging
import asyncpg
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

async def insert_news_records(conn, records: list[dict]) -> int:
    """
    Inserts a list of cleaned news dictionaries into the `news_sentiment` table in batch.
    Uses ON CONFLICT DO NOTHING to ignore duplicate articles.

    Args:
        conn: An active asyncpg Connection or Pool object.
        records: A list of dicts from the NewsClient.
    Returns:
        The number of records processed.
    """
    #Guard clause: To check for empty file passed
    if not records:
        logger.debug("insert_news_records called with empty list, skipping.")
        return 0

    #SQL query to insert the values in news_sentiment table
    query = '''INSERT INTO news_sentiment(
        ticker, sentiment_score, sentiment_label, article_url, article_title, article_description, published_at, content
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    ON CONFLICT (published_at, article_url) DO NOTHING;'''

    #Empty tuple which will contain all articles
    news_records_tpl = []

    #Iterating to extract and map articles and storing it in the news_records_tpl tuple
    for record in records:
        try:
            ticker = record.get('ticker')
            sentiment_score = record.get('sentiment_score')
            sentiment_label = record.get('sentiment_label')
            article_url = record.get('article_url')
            article_title = record.get('article_title')
            article_description = record.get('article_description')
            content = record.get('content')

            # Guard: skip articles with a missing or unparseable timestamp
            raw_published_at = record.get('published_at')
            if not raw_published_at:
                logger.warning(f"Skipping article with missing published_at: {article_url}")
                continue
            published_at = datetime.fromisoformat(raw_published_at.replace('Z', '+00:00'))

            record_tpl = (ticker, sentiment_score, sentiment_label, article_url, article_title, article_description, published_at, content)
            news_records_tpl.append(record_tpl)
        except Exception as e:
            logger.warning(f"Skipping malformed news record: {e}")
            continue

    if not news_records_tpl:
        return 0

    #Running SQL query to store the news articles
    try:
        await conn.executemany(query, news_records_tpl)
    except Exception as e:
        logger.error(f"Failed to batch insert news records: {e}")
        return 0

    #Returning the number of articles processed
    return len(news_records_tpl)
    

async def insert_price_ticks(conn, records: list[dict]) -> int:
    """
    Inserts a list of cleaned price tick dictionaries into the `price_ticks` table in batch.
    Uses ON CONFLICT DO NOTHING to ignore duplicate ticks.

    Args:
        conn: An active asyncpg Connection or Pool object.
        records: A list of dicts from the PriceClient.
    Returns:
        The number of records processed.
    """
    #Guard clause: To check for empty file passed
    if not records:
        logger.debug("insert_price_ticks called with empty list, skipping.")
        return 0
    
    #SQL query to insert the values in price_ticks table
    query = ''' INSERT INTO price_ticks(
        ticker, stock_date_time, price_open, price_high, price_low, price_close, stock_volume
    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
    ON CONFLICT (stock_date_time, ticker) DO NOTHING;
'''

    #Empty tuple which will contain all price ticks
    price_records_tpl = [] 

    #Iterating to extract and map ticks and storing it in the price_records_tpl tuple
    for record in records:
        try:
            ticker = record.get('ticker')
            stock_date_time = record.get('stock_date_time')
            price_open = record.get('price_open')
            price_high = record.get('price_high')
            price_low = record.get('price_low')
            price_close = record.get("price_close")
            stock_volume = record.get('stock_volume')

            # Guard: skip ticks with any missing required field
            if any(v is None for v in [ticker, stock_date_time, price_open, price_high, price_low, price_close, stock_volume]):
                logger.warning(f"Skipping malformed price tick for {ticker}: missing required fields")
                continue

            record_tpl = (ticker, stock_date_time, price_open, price_high, price_low, price_close, stock_volume)
            price_records_tpl.append(record_tpl)
        except Exception as e:
            logger.warning(f"Skipping malformed price record: {e}")
            continue

    if not price_records_tpl:
        return 0

    #Running SQL query to store the price ticks
    try:
        await conn.executemany(query, price_records_tpl)
    except Exception as e:
        logger.error(f"Failed to batch insert price ticks: {e}")
        return 0
    
    return len(price_records_tpl)

async def update_news_sentiments(conn, updates: list[tuple]) -> int:
    """
    Updates the sentiment score and label for a list of articles in batch.
    
    Args:
        conn: An active asyncpg Connection or Pool object.
        updates: A list of tuples.
    Returns:
        The number of records updated.
    """
    # 1. Guard clause: If updates is empty
    if not updates:
        logger.info("Received no updates")
        return 0
    
    else:
        
        #SQL query
        query = ''' UPDATE news_sentiment
                    SET sentiment_score = ($1), sentiment_label = ($2)
                    WHERE published_at = ($3) AND article_url = ($4)
                '''
        
    #Running the query in batch.
    await conn.executemany(query, updates)
    
    #Count of records updated
    count = len(updates)

    #Return the total count of records updated.
    return count

async def insert_signal(conn, signal: dict) -> bool:
    """
    Inserts a generated signal dictionary into the `signals` table.

    Args:
        conn: An active asyncpg Connection or Pool object.
        signal: A dictionary containing the generated signal details.
    Returns:
        True if successfully inserted, False otherwise.
    """

    #SQL query to insert values in database
    query = '''INSERT INTO signals(
               generated_at, ticker, signal, sentiment_score, momentum, window_hours) 
               VALUES($1, $2, $3, $4, $5, $6)
               ON CONFLICT (generated_at, ticker, window_hours) DO NOTHING;
            '''
    
    #Extract the corresponding values from the signal dictionary.
    generated_at = signal.get('generated_at')
    ticker = signal.get('ticker')
    stock_signal = signal.get('signal')
    sentiment_score = signal.get('sentiment_score')
    momentum = signal.get('momentum')
    window_hours = signal.get('window_hours')

    #Call execute on the connection to insert the values.
    try:
        await conn.execute(query, generated_at, ticker, stock_signal, sentiment_score, momentum, window_hours)
        return True
    except Exception as e:
        logger.error(f"Error while inserting data: {e}")
        return False


