"""
models.py — SQLAlchemy table definitions

TODO (Phase 1 → Phase 2): Define three tables:
  1. news_sentiment   — stores enriched news records
  2. price_ticks      — stores OHLCV price records
  3. signals          — stores derived BUY/HOLD/SELL signals

BEFORE implementing, answer these questions (write answers in notes/phase1_notes.md):
  - What is the primary time column for each table? (TimescaleDB needs this)
  - What columns need indexes? (Think: what will you query by most often?)
  - How will you enforce deduplication? (UNIQUE constraint? ON CONFLICT?)
  - What data type should `sentiment_score` be? (float4 vs float8 — why?)

Read TimescaleDB hypertables before touching this file:
  https://docs.timescale.com/use-timescale/latest/hypertables/
"""
