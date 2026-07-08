import logging
from aiohttp.pytest_plugin import loop
import asyncpg
from datetime import datetime, timezone

from numpy.ma import count

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
        logger.error("Empty Record File")
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
        ticker = record.get('ticker')
        sentiment_score = record.get('sentiment_score')
        sentiment_label = record.get('sentiment_label')
        article_url = record.get('article_url')
        article_title = record.get('article_title')
        article_description = record.get('article_description')
        published_at = record.get('published_at')
        published_at = datetime.fromisoformat(record.get('published_at').replace('Z', '+00:00'))
        content = record.get('content')
        record_tpl = (ticker, sentiment_score, sentiment_label, article_url, article_title, article_description, published_at, content)
        news_records_tpl.append(record_tpl)


    #Running SQL query to store the news articles
    await conn.executemany(query, news_records_tpl)

    #Logging the number of articles processed
    number_of_articles = len(news_records_tpl)
    
    #Returning the number of articles processed
    return number_of_articles
    

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
        logger.error("Empty record file")
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
        ticker = record.get('ticker')
        stock_date_time = record.get('stock_date_time')
        price_open = record.get('price_open')
        price_high = record.get('price_high')
        price_low = record.get('price_low')
        price_close = record.get("price_close")
        stock_volume = record.get('stock_volume')
        record_tpl = (ticker, stock_date_time, price_open, price_high, price_low, price_close, stock_volume)
        price_records_tpl.append(record_tpl)

    #Running SQL query to store the price ticks
    await conn.executemany(query, price_records_tpl)
    
    #Log the number of ticks processed.
    number_of_stock_data = len(price_records_tpl)
    
    #Return the count of processed ticks.
    return number_of_stock_data

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

