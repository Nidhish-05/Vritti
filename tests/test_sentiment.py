"""
tests/test_sentiment.py — Unit tests for FinBERT sentiment pipeline

TODO (Phase 3/5): Write tests that verify:
  1. SentimentPipeline returns correct output shape for a list of headlines
  2. Output labels are always one of: "positive", "negative", "neutral"
  3. Output scores are in range [0, 1]
  4. Empty list input is handled gracefully (no crash)
  5. Batching produces the same results as single-item processing

DO NOT skip tests. Write them alongside the implementation, not after.
"""

import pytest

# TODO: Import SentimentPipeline when implemented
# from src.processing.sentiment import SentimentPipeline
