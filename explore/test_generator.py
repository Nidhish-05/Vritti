import os
import asyncio
import logging
import asyncpg
from dotenv import load_dotenv
from src.processing import aggregator
from src.processing.aggregator import SentimentAggregator
from src.signals.generator import SignalGenerator
from src.db.writer import insert_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_generator():
    #Load secrets from .env
    load_dotenv()
    
    # 2. Get database credentials
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "vritti_db")
    db_user = os.getenv("DB_USER", "vritti")
    db_password = os.getenv("DB_PASSWORD", "vritti_password")

    #Connect to the database
    try:
        conn = await asyncpg.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    except Exception as e:
        logger.error("Error connecting to database: ", e)
        return
   
    #Instantiate SentimentAggregator.
    aggregator = SentimentAggregator()

    #Instantiate SignalGenerator
    signal_generator = SignalGenerator(aggregator)

    #Calling generate_signal by passing the connection, ticker "TSLA", and window_hours=168.
    generated_signal = await signal_generator.generate_signal(conn, ticker='TSLA',window_hours=168 )
    
    #Print the resulting dictionary containing the generated signal.
    print(generated_signal)

    #Inserting data into the 
    result = await insert_signal(conn, generated_signal)

    if result:
        print("Insertion successful")
    else:
        print("Insertion failed")

    #Close the database connection.
    await conn.close()

if __name__ == "__main__":
    asyncio.run(test_generator())
