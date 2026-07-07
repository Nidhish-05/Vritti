import logging
from aiohttp.pytest_plugin import loop
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
    # TODO Steps:
    # 1. Guard clause: If the records list is empty, return 0.
    if not records:
        logger.error("Empty Record File")
        return 0

    # 2. Write the SQL query. The format for asyncpg placeholders is $1, $2, $3...
    #    Hint:
    #    INSERT INTO news_sentiment (
    #        ticker, sentiment_score, sentiment_label, article_url,
    #        article_title, article_description, published_at, content
    #    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    #    ON CONFLICT (published_at, article_url) DO NOTHING;
    query = '''INSERT INTO news_sentiment(
        ticker, sentiment_score, sentiment_label, article_url, article_title, article_description, published_at, content
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    ON CONFLICT (published_at, article_url) DO NOTHING;'''

    # 3. Prepare the data:
    #    - Loop through each record dictionary.
    #    - Convert the `published_at` date string (e.g. "2026-06-29T02:32:07Z") into a 
    #      timezone-aware Python datetime object. 
    #      Tip: You can use `datetime.fromisoformat(r['published_at'].replace('Z', '+00:00'))`
    #    - Create a tuple of values matching the order of placeholders ($1 to $8).
    #    - Append the tuple to a list of tuples.
    news_records_tpl = []

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


    # 4. Use `await conn.executemany(query, list_of_tuples)` to batch insert all records.
    await conn.executemany(query, news_records_tpl)

    # 5. Log the number of articles processed.
    number_of_articles = len(news_records_tpl)
    
    # 6. Return the count of processed articles.
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
    # TODO Steps:
    # 1. Guard clause: If the records list is empty, return 0.
    if not records:
        logger.error("Empty record file")
        return 0
    
    # 2. Write the SQL query using placeholders ($1 to $7).
    #    Hint:
    #    INSERT INTO price_ticks (
    #        ticker, stock_date_time, price_open, price_high, price_low, price_close, stock_volume
    #    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
    #    ON CONFLICT (stock_date_time, ticker) DO NOTHING;
    query = ''' INSERT INTO price_ticks(
        ticker, stock_date_time, price_open, price_high, price_low, price_close, stock_volume
    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
    ON CONFLICT (stock_date_time, ticker) DO NOTHING;
'''

    # 3. Prepare the data:
    #    - Loop through each record dictionary.
    #    - Make sure `stock_date_time` is a datetime object (our PriceClient already does this!).
    #    - Create a tuple of values matching the order of placeholders ($1 to $7).
    #    - Append the tuple to a list of tuples.
    price_records_tpl = [] 

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

    # 4. Use `await conn.executemany(query, list_of_tuples)` to batch insert all records.
    await conn.executemany(query, price_records_tpl)
    
    # 5. Log the number of ticks processed.
    number_of_stock_data = len(price_records_tpl)
    
    # 6. Return the count of processed ticks.
    return number_of_stock_data
