import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# TODO Steps:
# 
# Step A: Page Configuration
# 1. Set the Streamlit page title and layout structure.
# 
# Step B: Sidebar Controls
# 2. Add a dropdown selector in the sidebar to choose a stock ticker.
#    Populate it with your watchlist symbols (e.g. AAPL, TSLA, MSFT).
# 
# 3. Add a slider or input box in the sidebar to choose the time window in hours.
#    (e.g., allow selecting 24 hours, 48 hours, 168 hours).
# 
# Step C: Fetching Data from FastAPI
# 4. Write helper functions to call your FastAPI server endpoints using requests:
#    - Fetch latest signals for all tickers.
#    - Fetch price history for the selected ticker and time window.
#    - Fetch sentiment history for the selected ticker and time window.
#    - Fetch the latest news articles for the selected ticker.
#    Wrap all requests in try-except blocks to handle server-offline errors gracefully.
# 
# Step D: Render Signal Metrics
# 5. Display the active signal (BUY, SELL, or HOLD) prominently in the main view.
#    - Color-code the signal (e.g., green for BUY, red for SELL, yellow/gray for HOLD).
#    - Display the raw sentiment score and price momentum metrics alongside the signal.
# 
# Step E: Render Charts
# 6. Plot the stock price history over time.
#    - Convert the fetched price data into a DataFrame.
#    - Render a line chart showing close prices over time.
# 
# 7. Plot the rolling sentiment history over time.
#    - Render a line chart showing the sentiment score over time.
# 
# Step F: Render News Feed Table
# 8. Render a table or list showing the latest 10 news headlines.
#    - Include the article title, description, publication timestamp, and the predicted sentiment label/score.

