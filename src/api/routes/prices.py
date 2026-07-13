import logging
from fastapi import APIRouter, Request, HTTPException
from src.db.reader import get_price_history

logger = logging.getLogger(__name__)
router = APIRouter()

#Route 1: Get Prices For Ticker
@router.get("/{ticker}")
async def get_prices(ticker: str, req: Request, hours: int = 24):
    
    #Getting the database pool from FastAPI app
    db_pool = req.app.state.pool
    
    #Acquiring a connection from the database pool
    async with db_pool.acquire() as conn:
        try:
            
            #Fetching the price_history
            price_history = await get_price_history(conn, ticker, hours)
            
            #Returning price_history
            return price_history
      
        except Exception as e:
            
            #logging the error
            logger.error(f"Error Fetching Data: {e}")
            
            #Raising a server side error
            raise HTTPException(status_code=500, detail="Error Fetching Data")