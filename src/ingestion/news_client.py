import logging
from newsapi import NewsApiClient
import json
logger = logging.getLogger(__name__)

class NewsClient:
    """
    Client class to interact with NewsAPI and fetch financial news articles
    for our watchlisted tickers.
    """
    
    def __init__(self, api_key: str):
        #To initialise the news client object
        self.client = NewsApiClient(api_key= api_key)

    def fetch_headlines(self, query: str, ticker: str) -> list[dict]:
        """
        Fetches headlines from NewsAPI based on a query, and returns a list of cleaned
        dictionaries matching the columns in our `news_sentiment` database table.

        Args:
            query: Search query string (e.g. "Tesla OR TSLA OR Elon Musk")
            ticker: Stock ticker symbol (e.g. "TSLA")
        Returns:
            List of cleaned dicts with keys:
            ['ticker', 'sentiment_score', 'sentiment_label', 'article_url',
             'article_title', 'article_description', 'published_at', 'content']
        """
        try:            
            #To call NewsAPI and receive all news
            news = self.client.get_everything(q=query, language='en', sort_by='publishedAt', page_size=50)
            
        # 3. Check the response status from the API. If it is NOT "ok", log an error and return []
            if news['status'] == "ok":
                #Creating a new list which will contain all the news articles
                news_articles = list()
                #To iterate over each article
                news_db = list()
                #To iterate over each article's items
                for article in news['articles']:
                    
                    #Get the details from the article
                    article_title = article.get('title')
                    article_url = article.get('url')
                    published_at = article.get('publishedAt')

                    #checking if vital news atributes are present or not
                    if article_title and article_url and published_at: 
                        
                        #To get the rest of the details
                        article_description = article.get('description') or ""
                        article_content = article.get('content') or ""
                        
                        #To store the obtained details in a clean dictionary according to database schema
                        cleaned_article = {
                            "ticker": ticker,
                            "sentiment_score": None,
                            "sentiment_label": None,
                            "article_url": article_url,
                            "article_title": article_title,
                            "article_description": article_description,
                            "content": article_content,
                            "published_at": published_at
                        } 

                        #To append the cleaned article in a list.
                        news_db.append(cleaned_article)
            
            #Return the list of cleaned articles.
            return news_db
        
        #In the except block: log the exception with logger.error, and return []
        except Exception as e:
            logger.error(e)
            if "rateLimited" in str(e):
                return None
            return []

        








