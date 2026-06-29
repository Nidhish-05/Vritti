"""
reader.py — DB query helpers for FastAPI routes

TODO (Phase 5): Implement async query functions:
  - get_latest_signal(ticker: str) -> dict | None
  - get_all_signals() -> list[dict]
  - get_sentiment_history(ticker: str, hours: int) -> list[dict]
  - get_price_history(ticker: str, hours: int) -> list[dict]
  - get_latest_news(ticker: str, limit: int = 10) -> list[dict]

Use asyncpg for async DB access (required by FastAPI's async routes).
"""
