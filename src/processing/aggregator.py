"""
aggregator.py — Rolling window sentiment aggregation

TODO (Phase 4): Implement SentimentAggregator with:
  - compute_rolling(ticker: str, window_hours: int) -> dict
  - Windows: 1h, 6h, 24h
  - Weighting: exponential decay (recent articles weighted higher)
    Use pandas DataFrame.ewm() — read docs before implementing:
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
  - Output per record:
    {ticker, window_hours, weighted_score, article_count, computed_at}

QUESTION TO ANSWER BEFORE IMPLEMENTING:
  Why should recent news be weighted more heavily than older news?
  What real-world scenario demonstrates this matters?
"""
