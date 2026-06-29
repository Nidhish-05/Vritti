"""
ticker_mapper.py — Rule-based headline → ticker mapper

TODO (Phase 3): Implement TickerMapper class with:
  - A dictionary mapping company names / aliases → ticker symbols
  - map(headline: str) -> list[str]  (a headline may match multiple tickers)
  - Case-insensitive matching
  - Log when no ticker is matched (useful for debugging coverage)

NOTE: This is intentionally simple (dictionary lookup).
A production system would use Named Entity Recognition (NER).
Document this design decision and tradeoff in the README.

Start with at least these mappings for your watchlist:
  AAPL: apple, iphone, tim cook, mac, macbook, ios, app store
  TSLA: tesla, elon musk, ev, electric vehicle, gigafactory
  MSFT: microsoft, azure, satya nadella, windows, copilot, xbox
  GOOGL: google, alphabet, sundar pichai, youtube, android, bard, gemini
  AMZN: amazon, aws, andy jassy, prime, alexa, whole foods
"""
