"""
generator.py — BUY / HOLD / SELL signal generator

⚠️  DISCLAIMER: This module is for educational and research purposes only.
    Signals produced here are NOT financial advice and should NOT be used
    for real investment decisions.

TODO (Phase 4): Implement SignalGenerator with:
  - generate(ticker: str) -> dict
  - Inputs: aggregated sentiment score (from aggregator.py) +
            price momentum (5-period % change from price_ticks)
  - Output: {"ticker": str, "signal": "BUY"|"HOLD"|"SELL",
             "sentiment_score": float, "momentum": float,
             "generated_at": datetime}

BEFORE implementing, document your thresholds with reasoning:
  - What sentiment_score threshold triggers BUY vs HOLD vs SELL?
  - What momentum threshold do you combine it with?
  - Why those specific numbers? (You MUST be able to defend this in an interview)

HINT: Start simple. Combine:
  sentiment_score ∈ [-1, 1]  (negative=-1, neutral=0, positive=+1)
  momentum = (price_now - price_5_periods_ago) / price_5_periods_ago
"""
