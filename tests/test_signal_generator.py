"""
tests/test_signal_generator.py — Unit tests for signal generator

TODO (Phase 4): Write tests that verify:
  1. High positive sentiment + positive momentum → BUY
  2. High negative sentiment + negative momentum → SELL
  3. Mixed signals → HOLD
  4. Output dict always contains required keys: ticker, signal, sentiment_score, momentum, generated_at
  5. Signal is always one of: "BUY", "HOLD", "SELL"
"""

import pytest

# TODO: Import SignalGenerator when implemented
# from src.signals.generator import SignalGenerator
