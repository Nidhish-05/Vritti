import logging
from unittest import result
import asyncpg
from src.processing.sentiment import SentimentPipeline
from src.db.writer import update_news_sentiments

logger = logging.getLogger(__name__)

async def fetch_unclassified_news(conn) -> list[dict]:
    """
    Queries the database for all news articles that do not have a sentiment score yet.
    
    Args:
        conn: An active asyncpg Connection.
    Returns:
        List of dicts representing the raw database rows.
    """
    # TODO Steps:
    # 1. Write the SQL query:
    #    SELECT published_at, article_url, article_title, article_description
    #    FROM news_sentiment
    #    WHERE sentiment_score IS NULL;
    query = '''SELECT published_at, article_url, article_title, article_description, content
               FROM news_sentiment
               WHERE sentiment_score IS NULL;
            '''
    # 
    # 2. Use `rows = await conn.fetch(query)` to get results.
    rows = await conn.fetch(query)
    # 3. Convert the rows to a list of standard dictionaries:
    #    `return [dict(row) for row in rows]`
    return [dict(row) for row in rows]

async def classify_pending_news(conn, pipeline: SentimentPipeline) -> int:
    """
    Fetches unclassified news, runs them through the FinBERT pipeline,
    and updates their sentiment scores/labels in the database.

    Args:
        conn: An active asyncpg Connection.
        pipeline: An initialized SentimentPipeline.
    Returns:
        The number of articles classified.
    """

    #Fetch articles without sentiment analysis
    pending_articles = await fetch_unclassified_news(conn)

    # 2. Guard clause: To check if there are no pending articles
    if not pending_articles:
        logger.info("No pending articles")
        return 0
    
    else:

        #Prepare the text inputs for FinBERT:
        pending_articles_list = []
        for article in pending_articles:
            
            text = f"{article.get('article_title')}. {article.get('article_description')}. {article.get('content')}"
            pending_articles_list.append(text)

    #Generating results for FinBERT
    results = pipeline.score(pending_articles_list)
    
    #Empty list which will contain the updated articles 
    updates=[]

    #Iterating and combining the updated articles
    for article, result in zip(pending_articles, results):

        article_tpl = (
            result.get('score'),
            result.get('label'),
            article.get('published_at'),
            article.get('article_url')
        )

        updates.append(article_tpl)
    
    #Making updates in database records
    await update_news_sentiments(conn, updates)

    #Log how many articles were successfully classified.
    count = len(updates)

    #Return the count.
    return count
