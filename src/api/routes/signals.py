import logging
from fastapi import APIRouter, Request, HTTPException
from src.db.reader import get_latest_signal, get_all_signals

#Logger Configuration
logger = logging.getLogger(__name__)

#Creating an instance of APIRouter Class
router = APIRouter()

#Route 1: Getting All Signals
@router.get("/all")
async def get_all_signal_endpoint(req: Request):

    #Getting the database pool from FastAPI app
    db_pool = req.app.state.pool

    #Acquiring a connection from the database pool
    async with db_pool.acquire() as conn:
        try:
        
            #Fetching all the signals for all the tickers
            all_signals = await get_all_signals(conn)

            #Returning all the signals
            return all_signals
        
        except Exception as e:
            
            #Raising exception if all_signals is empty
            raise HTTPException(status_code=500, detail="Error Fetching Data")

#Route 2: Getting Latest Signal For A Ticker
@router.get("/{ticker}")
async def get_latest_signal_endpoint(ticker: str, req: Request):

    #Getting the database pool from FastAPI app
    db_pool = req.app.state.pool

    #Acquiring a connection from the database pool
    async with db_pool.acquire() as conn:
        try:
        
            #Fetching the latest signal for the ticker
            latest_signal = await get_latest_signal(conn, ticker)
            
            #Checking if the signal is empty, we raise error, otherwise return it
            if latest_signal != None:
                return latest_signal
            else:
                raise HTTPException(status_code=404, detail="Error Fetching Data For Ticker")
        
        except Exception as e:
        
            raise HTTPException(status_code=500, detail="Error Fetching Data For Ticker")
    