"""
explore/test_prices.py — Phase 1 exploration script (THROWAWAY — do not import elsewhere)

TASK: Use yfinance to fetch 7 days of TSLA price history and understand the data.

Steps:
  1. pip install yfinance (if not already installed)
  2. Fetch 7 days of TSLA history: yf.Ticker("TSLA").history(period="7d")
  3. Print the resulting DataFrame — study the columns and index
  4. Answer in a comment at the bottom of this file:
     - What columns does yfinance return? (OHLCV + extras)
     - What is the index of the DataFrame? What timezone is it in?
     - How will you flatten this into a dict for DB insertion?
     - What is the unique key for a price tick? (How will you deduplicate?)

DO NOT proceed to Phase 2 until you can answer all four questions.
"""

# YOUR CODE GOES BELOW THIS LINE
# (Remember: you write it, not the AI)
import yfinance as yf
import pandas as pd

dat = yf.Ticker("TSLA")

df1 = pd.DataFrame(dat.history(period="7d"))
print(df1)

"""
Answers of the questions posed in the starting of this document:
1) The columns are: Date, Open, High, Low, Close, Volume, Dividends, Stock Splits.
2) The index of the dataframe is Date along with time. After researching and surfing the internet, I got the answer that the timezone is according to the USA market opening time and closing time and that we can change this.
3) To convert this df into dict, I think we can make key value pairs in which each key will be the column name, and further the values will be list containing the values. It will be like a dictionary of list where the keys are headers and values are lists containing the row values of that column header respectively.
4) I am not sure, but if I had to make a guess, I would say that the open values can be used to check for the duplicacy, since a company stock is supposed to have a unique price. So if 2 stocks are opening at the exact same rate, then they must have been of the same company. 
"""