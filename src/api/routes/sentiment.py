import logging
from fastapi import APIRouter, Request, HTTPException
from src.db.reader import get_sentiment_history, get_latest_news

logger = logging.getLogger(__name__)
router = APIRouter()

#Route 1: Sentiment History
@router.get("/history")
async def get_sentiment_history_endpoint(ticker: str, req: Request, hours: int = 24):
    
    #Getting the database pool from FastAPI app
    db_pool = req.app.state.pool
    
    #Acquiring a connection from the database pool
    async with db_pool.acquire() as conn:
        try:
            
            #Fetching the sentiment_history
            sentiment_history = await get_sentiment_history(conn, ticker, hours)
            
            #Returning sentiment_history
            return sentiment_history
      
        except Exception as e:
            
            #logging the error
            logger.error(f"Error Fetching Data: {e}")
            
            #Raising a server side error
            raise HTTPException(status_code=500, detail="Error Fetching Data")

#Route 2: Latest News
@router.get("/news/latest")
async def get_latest_news_endpoint(ticker: str, req: Request, limit: int = 10):
    
    #Getting the database pool from FastAPI app
    db_pool = req.app.state.pool
    
    #Acquiring a connection from the database pool
    async with db_pool.acquire() as conn:
        try:
            
            #Fetching the latest_news
            latest_news = await get_latest_news(conn, ticker, limit)
            
            #Returning latest_news
            return latest_news
      
        except Exception as e:
            
            #logging the error
            logger.error(f"Error Fetching Data: {e}")
            
            #Raising a server side error
            raise HTTPException(status_code=500, detail="Error Fetching Data")