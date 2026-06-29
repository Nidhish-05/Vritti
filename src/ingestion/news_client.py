import logging
from newsapi import NewsApiClient

logger = logging.getLogger(__name__)

class NewsClient:
    """
    Client class to interact with NewsAPI and fetch financial news articles
    for our watchlisted tickers.
    """
    
    def __init__(self, api_key: str):
        # TODO: Initialize the official NewsApiClient using the passed api_key.
        # Store it as an instance attribute (e.g., self.client) so other methods can use it.
        self.client = NewsApiClient(api_key= api_key)
        return self.client

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
        # TODO Steps:
        # 1. Wrap the entire operation in a try-except block to handle network issues or API limits.
        try:
            client = self.__init__(self, my_api_key)
            
        except Exception as e:
            print(f"{e}")

        # 2. Call self.client.get_everything with:
        #    - q=query
        #    - language='en'
        #    - sort_by='publishedAt'
        #    - page_size=50
        #
        # 3. Check the response status from the API. If it is NOT "ok", log an error and return []
        #
        # 4. Extract the 'articles' list from the response.
        #
        # 5. Initialize an empty list to hold the cleaned articles.
        #
        # 6. Loop through each article:
        #    - Skip the article if it lacks vital details: 'title', 'url', or 'publishedAt'.
        #    - Create a dictionary matching the database schema structure.
        #    - For fields like 'sentiment_score' and 'sentiment_label', set them to None for now
        #      (these will be analyzed by FinBERT later in Phase 3).
        #    - Clean fields: Ensure 'description' and 'content' default to empty strings if they are None.
        #    - Append the cleaned dictionary to your list.
        #
        # 7. Return the list of cleaned articles.
        #
        # 8. In the except block: log the exception with logger.error, and return []
        pass








