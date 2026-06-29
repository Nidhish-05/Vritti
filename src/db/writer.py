"""
writer.py — DB insert helpers

TODO (Phase 2): Implement insert functions with deduplication:
  - insert_news_record(record: dict) -> None
  - insert_price_tick(record: dict) -> None
  - Both must use INSERT ... ON CONFLICT DO NOTHING (or equivalent)
    to prevent duplicate rows across polling cycles

IMPORTANT: Use proper logging, not print() statements.
  Log: how many records inserted, how many skipped as duplicates.
"""
