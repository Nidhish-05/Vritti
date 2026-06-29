"""
tests/test_api.py — Integration tests for FastAPI endpoints

TODO (Phase 5): Write tests using httpx.AsyncClient that verify:
  1. GET /health → 200 OK
  2. GET /signals/AAPL → 200 with correct schema
  3. GET /signals/INVALID_TICKER → 404 (ticker not in watchlist)
  4. GET /sentiment/history?ticker=AAPL&hours=24 → 200 with list
  5. GET /prices/AAPL?hours=24 → 200 with list
  6. GET /news/latest?ticker=AAPL → 200 with max 10 items

Use pytest-asyncio for async test functions.
Read: https://fastapi.tiangolo.com/tutorial/testing/
"""

import pytest
import pytest_asyncio

# TODO: Import FastAPI app when implemented
# from src.api.main import app
