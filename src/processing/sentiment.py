"""
sentiment.py — FinBERT sentiment inference pipeline

TODO (Phase 3): Implement SentimentPipeline class with:
  - __init__: load model ONCE at startup (ProsusAI/finbert)
  - score(headlines: list[str]) -> list[dict[str, Any]]
    Returns: [{"label": "positive"|"negative"|"neutral", "score": float}, ...]
  - Use batching (FINBERT_BATCH_SIZE from env) for efficiency

CRITICAL: Understand what FinBERT was trained on BEFORE implementing.
Read: https://huggingface.co/ProsusAI/finbert
"""
