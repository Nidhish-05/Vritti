"""
dashboard/app.py — Streamlit dashboard

TODO (Phase 6): Build four views:
  1. Signal Cards    — per-ticker BUY/HOLD/SELL with color coding
  2. Sentiment Timeline — rolling sentiment score over 24h (Plotly line chart)
  3. Price Overlay   — price + sentiment on dual Y-axis (the money visual)
  4. News Feed       — latest 10 headlines with sentiment label + score

IMPORTANT: Connect to FastAPI endpoints, NOT directly to the DB.
  Use API_BASE_URL from environment variable.

Auto-refresh pattern:
  https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun
"""
