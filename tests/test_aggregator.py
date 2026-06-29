"""
tests/test_aggregator.py — Unit tests for rolling sentiment aggregator

TODO (Phase 4): Write tests that verify:
  1. Rolling window returns correct time range of records
  2. Exponential decay weights sum correctly
  3. Article count in output matches input record count
  4. Empty ticker (no articles) returns a neutral/zero score, not an error
"""

import pytest

# TODO: Import SentimentAggregator when implemented
# from src.processing.aggregator import SentimentAggregator
