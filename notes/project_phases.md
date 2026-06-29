# Project Vritti — Phases & Roadmap

This document outlines the 8 phases of building **Project Vritti**, a real-time financial news sentiment and stock signal pipeline.

---

## Phase 1 — Foundation & Data Exploration
* **Goal**: Establish the basic setup, explore external APIs, design the database schema, and configure the database.
* **Steps**:
  1. Set up the local workspace structure and requirements.
  2. Write and test `explore/test_news.py` to verify API connection with NewsAPI.
  3. Write and test `explore/test_prices.py` to verify data ingestion using `yfinance`.
  4. Design database schema in `sql/init.sql` using TimescaleDB hypertables.
  5. Initialize TimescaleDB locally via Docker, run the schema, and verify the tables.

---

## Phase 2 — Ingestion Service (Current Phase)
* **Goal**: Build robust, resilient Python clients for fetching news and price data, handle database ingestion with deduplication, and schedule automated runs.
* **Steps**:
  1. **News Client (`src/ingestion/news_client.py`)**: Create a client to fetch news headlines for the watchlist.
  2. **Price Client (`src/ingestion/price_client.py`)**: Create a client to fetch historical and live price ticks using `yfinance`.
  3. **Database Writer (`src/db/writer.py`)**: Write helper functions to insert data using raw queries (`asyncpg`) or SQLAlchemy, implementing deduplication (e.g., `ON CONFLICT DO NOTHING`).
  4. **Scheduler Engine (`src/ingestion/scheduler.py`)**: Implement async worker loops using `asyncio` to run price ingestion every 5 minutes and news ingestion every 15 minutes.

---

## Phase 3 — NLP Processing (FinBERT Integration)
* **Goal**: Integrate the FinBERT sentiment model to analyze fetched headlines and enrich them with sentiment scores and labels.
* **Steps**:
  1. **Model Loader (`src/nlp/classifier.py`)**: Set up a classifier using `transformers` (Hugging Face) to download and run the pre-trained `ProsusAI/finbert` model.
  2. **Batch Classification**: Implement logic to batch classify newly inserted news articles that don't have a sentiment score yet.
  3. **Sentiment Pipeline Worker**: Connect the classifier to the ingestion pipeline, ensuring new articles are enriched before they are stored or updated in `news_sentiment`.

---

## Phase 4 — Aggregation & Signal Logic
* **Goal**: Calculate rolling sentiment metrics and combine them with price momentum to generate BUY/HOLD/SELL signals.
* **Steps**:
  1. **Data Retriever**: Pull recent prices and news sentiment scores from TimescaleDB for the evaluation window (e.g., last 24 hours).
  2. **Calculate Sentiment Metrics**: Use Pandas to calculate the Exponentially Weighted Moving Average (EWMA) of sentiment scores over different windows (1h, 6h, 24h).
  3. **Calculate Price Momentum**: Calculate price rate-of-change (momentum) over the last 5 ticks.
  4. **Signal Engine (`src/analytics/signal_generator.py`)**: Implement conditional logic to combine sentiment and momentum into signals, and store them in the `signals` table.

---

## Phase 5 — FastAPI Backend
* **Goal**: Build a REST API to serve the aggregated database records to the frontend dashboard.
* **Steps**:
  1. Set up a FastAPI server (`src/api/main.py`).
  2. Implement Pydantic schemas for data serialization and validation.
  3. Write API endpoints:
     * `/health`: System status.
     * `/api/v1/news`: Get recent news sentiment for a ticker.
     * `/api/v1/prices`: Get recent price ticks.
     * `/api/v1/signals`: Get latest generated signals.

---

## Phase 6 — Streamlit Dashboard
* **Goal**: Build a highly visual frontend UI to display live stock signals, interactive price charts, and sentiment feeds.
* **Steps**:
  1. Build a Streamlit application (`src/dashboard/app.py`).
  2. Create metrics cards showing current signals (BUY/HOLD/SELL) and sentiment scores.
  3. Build interactive charts (e.g., Plotly line chart showing stock price overlaid with sentiment markers).
  4. Display a searchable news feed showing the most recent articles and their sentiment classification.

---

## Phase 7 — Docker & CI/CD
* **Goal**: Containerize the ingestion, API, and dashboard services, and automate formatting/testing.
* **Steps**:
  1. Write `Dockerfile`s for the ingestion engine, backend API, and Streamlit dashboard.
  2. Create a unified `docker-compose.yml` defining all services (Database, Ingestion, API, Dashboard).
  3. Set up a GitHub Actions workflow to run code linters (`black`, `flake8`) and unit tests on every commit.

---

## Phase 8 — Cloud Deployment & Polish
* **Goal**: Deploy the complete multi-container application to the cloud and add final documentation.
* **Steps**:
  1. Deploy the TimescaleDB instance and services to a platform (e.g., Render, Railway, or AWS/DigitalOcean).
  2. Run production-level tests to ensure websocket/HTTP connections are stable.
  3. Complete the project README with screenshots, architecture diagrams, and a build journal.
