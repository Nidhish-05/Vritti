import os
import logging
from contextlib import asynccontextmanager
import asyncpg
from asyncpg import pool
from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import prices, sentiment, signals
from dotenv import load_dotenv

#Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read allowed origins from env var (comma-separated).
# On Render: set ALLOWED_ORIGINS=https://your-app.vercel.app
# Locally:   leave unset or set to * for unrestricted dev access.
def _get_allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "*")
    return [o.strip() for o in raw.split(",") if o.strip()]

#Async context manager function that takes the FastAPI app.
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    
    #Read the database connection variables from the environment.
    load_dotenv()
    db_string = os.getenv("ASYNC_DATABASE_URL")

    #Create an asyncpg connection pool.
    db_pool = await asyncpg.create_pool(dsn=db_string)
        
    #Assign the created pool to the application state.
    app.state.pool = db_pool

    #Log an info message that the database pool was successfully created.
    logger.info("Database Pool Initiated Successfully")

    try:

        #To pass control back to the FastAPI execution flow.
        yield
        
    finally:

        #Close the pool to stop handling requests
        await app.state.pool.close()

        #Log an info message that the database pool has been closed.
        logger.info("Database Pool Has Been Closed.")


#Instantiate the FastAPI app and pass the lifespan context manager.
app = FastAPI(lifespan=lifespan)

#Add CORS middleware to the FastAPI app to allow cross-origin requests.
# Origins are controlled by the ALLOWED_ORIGINS environment variable.
allowed_origins = _get_allowed_origins()
logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include the routers from your routes modules.
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
app.include_router(signals.router, prefix="/signals", tags=["Signals"])

#Define a GET route at the root path "/" that redirects the clientto the "/docs" swagger documentation page
@app.get("/")
async def documentation():
    return RedirectResponse(url="/docs")


#Define a GET route at "/health" that returns a simple status dictionary
@app.get("/health")
async def health():
    return {"status": "healthy"}
