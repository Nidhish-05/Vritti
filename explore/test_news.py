"""
explore/test_news.py — Phase 1 exploration script (THROWAWAY — do not import elsewhere)

TASK: Hit the NewsAPI /everything endpoint with a keyword and print the raw response.
      Study the JSON structure carefully — you will decide which fields to keep.

Steps:
  1. Load your NEWS_API_KEY from .env using python-dotenv
  2. Make a request to: https://newsapi.org/v2/everything
     with params: q="Tesla earnings", language="en", pageSize=5
  3. Print the full JSON response with json.dumps(..., indent=2)
  4. Answer in a comment at the bottom of this file:
     - Which fields will you store in your DB? Which will you discard? Why?
     - What is the unique identifier for each article? (How will you deduplicate?)
     - What timezone is publishedAt in? Does that matter for TimescaleDB?

DO NOT proceed to Phase 2 until you can answer all three questions.
"""

# YOUR CODE GOES BELOW THIS LINE
# (Remember: you write it, not the AI)
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import json

load_dotenv()

my_api_key = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key=my_api_key)

all_news = newsapi.get_everything(q="Tesla earnings", language="en", page_size=5)
news_string_all = json.dumps(all_news)
print(news_string_all)

"""
The answers to your questions are:
1) In my database, I will only be storing the parameter q as it contains the keywords of the headline which I searched for. In the JSON string I got, I will be storing the following things: Title, Description, Content, urlToImage, publishedAt. I will discard the author, url as they serve no use to the sentiment analysis.
2) The duplicacy in articles can be sorted using the urlToImage as it will be different for each of them, we can also check for the cosine similarity between the descriptions to match the similarity between the 2 articles and then take the revelant non duplicate sentiments.
3) The timezone used in publishedAt is UTC (z for zullu time). I am not sure why it must be important for the timescaleddb but if I had to guess, I would probably say it's because we need to check how old is the news and predict if it would have been changed as per the news headline or not.
"""