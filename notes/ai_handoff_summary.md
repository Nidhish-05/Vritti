# Project Vritti — AI Handoff & Comprehensive Build Summary

> **Purpose:** This document is a complete handoff record of all conversations, decisions, code, configurations, and next steps for Project Vritti. It is written for another AI assistant to continue this project with no access to the original conversation.

---

## 1. Project Overview

**Project Name:** Vritti (वृत्ति — meaning "movement" or "fluctuation" in Sanskrit)

**Full Description:** A real-time financial news sentiment and stock signal pipeline. It ingests live financial news headlines and stock market prices, processes sentiment using FinBERT (a finance-specialized transformer model), aggregates sentiment over rolling time windows, and generates actionable BUY/HOLD/SELL trading signals presented via a REST API and Streamlit dashboard.

**Developer:** Nidhish — B.Tech CSE student, MAIT Delhi (2023–27)

**Repository:** `D:\Projects\Vritti\` on a Windows machine

**Disclaimer:** Educational/research project only. Signals must NOT be used for real investment decisions.

---

## 2. Mentorship Rules (CRITICAL — Read Before Proceeding)

These rules govern how the AI assistant must behave with Nidhish. They are **non-negotiable**:

1. **NEVER write production code for Nidhish** unless asked for a tiny syntax clarification. He must write every line himself.
2. **NEVER paste a full working implementation** into the chat — this happened once and Nidhish explicitly called it out.
3. **Always test Nidhish's understanding first** before explaining a concept. Ask him questions, wait for his answer, then build on what he knows.
4. **Always explain the "why" before the "how"** — Nidhish must be able to defend every architectural decision in a job interview.
5. **Use comments and TODO instructions** in stub files to guide him on what to build. He then fills in the code himself.
6. **Minimal tool usage** — don't run unnecessary commands or generate files he didn't ask for.
7. **Ask before assuming** — if his intent is ambiguous, ask a clarifying question.
8. Nidhish is new to most of this stack (Docker, TimescaleDB, FastAPI, asyncio, NLP). Explain from first principles.
9. He sometimes uses ChatGPT for minor syntax lookups — this is acceptable for config/syntax only, not for architecture.

---

## 3. Technology Stack

| Layer | Technology | Reason |
|---|---|---|
| News Data | NewsAPI (Free Tier) | Clean JSON, keyword filtering, free tier with 100 req/day |
| Price Data | `yfinance` | Free, no API key required, returns clean OHLCV DataFrames |
| NLP Model | FinBERT (`ProsusAI/finbert`) | Pre-trained on Financial PhraseBank — outperforms VADER/TextBlob for finance |
| Ingestion Engine | Python `asyncio` + `aiohttp` | Non-blocking I/O for parallel news + price polling loops |
| Storage | PostgreSQL + TimescaleDB | SQL-compatible time-series storage with hypertable partitioning |
| Analytics | Pandas + NumPy | Rolling windows, EWMA (Exponentially Weighted Moving Average) |
| Backend API | FastAPI | Async-native, Pydantic validation, auto OpenAPI docs |
| Visualization | Streamlit | Rapid dashboard generation with native Plotly integration |
| DevOps | Docker + Docker Compose | Containerized reproducibility |
| CI/CD | GitHub Actions | Auto linting (`black`, `flake8`) and tests on commit |
| Cloud (Phase 8) | Render / Railway / AWS | Decision deferred to Phase 8 |

---

## 4. Project Directory Structure

```
D:\Projects\Vritti\
├── .env                         # Real secrets (not committed to git)
├── .env.example                 # Template for secrets
├── .gitignore
├── README.md                    # Project README with build journal table
├── docker-compose.yml           # TimescaleDB service config
├── requirements.txt             # All Python dependencies
│
├── explore/                     # One-off exploration scripts (not production code)
│   ├── test_news.py             # DONE: fetches Tesla headlines from NewsAPI
│   └── test_prices.py          # DONE: fetches 7-day TSLA OHLCV via yfinance
│
├── notes/                       # Developer notes and planning docs
│   ├── project_phases.md        # Phase-by-phase roadmap (created by AI)
│   └── ai_handoff_summary.md   # THIS FILE
│
├── sql/
│   └── init.sql                 # DONE: Full schema — 3 hypertables + 5 indexes
│
├── src/
│   ├── __init__.py
│   ├── api/                     # Phase 5 — FastAPI backend
│   ├── dashboard/               # Phase 6 — Streamlit UI
│   ├── db/                      # DB connection + writer helpers
│   ├── ingestion/               # Phase 2 — News and price ingestion
│   │   ├── news_client.py       # IN PROGRESS: NewsClient class skeleton
│   │   └── price_client.py      # TODO
│   ├── processing/              # Phase 3 — FinBERT NLP processing
│   └── signals/                 # Phase 4 — Signal generation logic
│
├── tests/                       # Unit tests (stubbed)
└── .github/
    └── workflows/               # GitHub Actions CI/CD YAML
```

---

## 5. Environment Configuration

### `.env` file (real values, already set up)
```env
NEWS_API_KEY=36b9ef6444c84d9ebc9fb6460d22e9fb
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vritti_db
DB_USER=vritti
DB_PASSWORD=vritti_password
```

### `docker-compose.yml` (final working version)
```yaml
services:
  timescaledb:
    image: timescale/timescaledb-ha:pg16     # IMPORTANT: NOT timescale/timescaledb:latest-pg16
    container_name: vritti-timescaledb
    environment:
      POSTGRES_DB: vritti_db
      POSTGRES_USER: vritti
      POSTGRES_PASSWORD: vritti_password
    ports:
      - "5432:5432"
    volumes:
      - timescaledb_data:/var/lib/postgresql/data

volumes:
  timescaledb_data:
```

> **CRITICAL NOTE:** The image `timescale/timescaledb:latest-pg16` and `timescale/timescaledb:latest-pg17` both FAIL to pull on Nidhish's machine (EOF network errors on large layers, possibly due to Docker Desktop Resource Saver mode). The working image is **`timescale/timescaledb-ha:pg16`** — use this always.

### Key Docker Commands
```powershell
# Start the database
docker-compose up -d

# Stop and DELETE volumes (needed when switching PostgreSQL major versions)
docker-compose down -v

# Run init.sql against the live database (PowerShell — NOT bash syntax)
Get-Content sql/init.sql -Raw | docker exec -i vritti-timescaledb psql -U vritti -d vritti_db

# Verify tables were created
docker exec -it vritti-timescaledb psql -U vritti -d vritti_db -c "\dt"

# Drop all tables (to re-run init cleanly)
docker exec -it vritti-timescaledb psql -U vritti -d vritti_db -c "DROP TABLE IF EXISTS news_sentiment, price_ticks, signals CASCADE;"
```

> **PowerShell Gotcha:** PowerShell does NOT support `<` stdin redirection (e.g., `psql ... < sql/init.sql`). Always use `Get-Content ... | docker exec -i ...` instead.

---

## 6. Database Schema (Final — Verified Working)

File: [`sql/init.sql`](file:///D:/Projects/Vritti/sql/init.sql)

### `news_sentiment` (TimescaleDB Hypertable)
```sql
CREATE TABLE news_sentiment(
    ticker              TEXT NOT NULL,
    sentiment_score     NUMERIC(5,4) NULL,       -- Filled by FinBERT in Phase 3
    sentiment_label     TEXT NULL,               -- "positive" / "negative" / "neutral" — filled by FinBERT
    article_url         TEXT NOT NULL,
    article_title       TEXT NOT NULL,
    article_description TEXT NOT NULL,
    published_at        TIMESTAMP WITH TIME ZONE NOT NULL,
    content             TEXT NOT NULL,
    PRIMARY KEY (published_at, article_url)      -- Composite PK — required for hypertable uniqueness
);
SELECT create_hypertable('news_sentiment', by_range('published_at'));
```

**Key Design Decisions:**
- `sentiment_score` and `sentiment_label` are **NULL at insert time** — FinBERT fills them later in Phase 3.
- `article_url` is the **deduplication key** (not `urlToImage` as Nidhish initially suggested).
- The composite `PRIMARY KEY (published_at, article_url)` is **required** by TimescaleDB — any unique constraint on a hypertable MUST include the time partitioning column.
- All `VARCHAR` fields changed to `TEXT` (no performance difference in PostgreSQL; TEXT is recommended).

### `price_ticks` (TimescaleDB Hypertable)
```sql
CREATE TABLE price_ticks(
    ticker          TEXT NOT NULL,
    stock_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    price_open      DECIMAL(10, 6) NOT NULL,
    price_high      DECIMAL(10, 6) NOT NULL,
    price_low       DECIMAL(10, 6) NOT NULL,
    price_close     DECIMAL(10, 6) NOT NULL,
    stock_volume    BIGINT NOT NULL,             -- NOT INTEGER — Tesla trades ~50M shares/day
    PRIMARY KEY(stock_date_time, ticker)
);
SELECT create_hypertable('price_ticks', by_range('stock_date_time'));
```

**Key Design Decisions:**
- Volume is `BIGINT` because TSLA daily volume (~50M) overflows `INTEGER` (max ~2.1B, but daily intraday tick volumes also need to be safe).
- Composite `PRIMARY KEY(stock_date_time, ticker)` for deduplication.

### `signals` (TimescaleDB Hypertable)
```sql
CREATE TABLE signals(
    generated_at    TIMESTAMP WITH TIME ZONE NOT NULL,
    ticker          TEXT NOT NULL,
    signal          TEXT NOT NULL,               -- "BUY" / "HOLD" / "SELL"
    sentiment_score NUMERIC(5,4) NULL,           -- Recency-weighted EWMA sentiment
    momentum        NUMERIC(8,4) NOT NULL,       -- Price rate-of-change
    window_hours    INTEGER NOT NULL,            -- Rolling window: 1, 6, or 24 hours
    PRIMARY KEY(generated_at, ticker, window_hours)
);
SELECT create_hypertable('signals', by_range('generated_at'));
```

### Indexes
```sql
CREATE INDEX ON news_sentiment (ticker);
CREATE INDEX ON news_sentiment (published_at DESC);
CREATE INDEX ON price_ticks (ticker);
CREATE INDEX ON price_ticks (stock_date_time DESC);
CREATE INDEX ON signals (ticker);
```

**Why indexes?** Indexes pre-build lookup data structures so that `WHERE ticker = 'TSLA'` and `ORDER BY published_at DESC` queries avoid full table scans as the data grows. Without indexes on a hypertable with millions of rows, each query would scan every chunk sequentially.

---

## 7. Key Concepts Nidhish Has Learned (For Interview Defense)

### Why TimescaleDB hypertables instead of regular PostgreSQL tables?
TimescaleDB transparently partitions a regular PostgreSQL table into time-based **chunks** (e.g., one chunk per week). Benefits:
- Indexes stay small (per-chunk, not global) → inserts and range queries stay fast as data grows.
- You still use standard SQL — no new query language to learn.
- Automated data retention policies (future use).

### Why FinBERT over VADER or TextBlob?
- VADER was trained on social media text. It misclassifies financial language (e.g., "bullish outlook" may score neutral; "shares dropped" may be rated highly negative without understanding context).
- FinBERT was specifically trained on the **Financial PhraseBank** dataset — it understands domain-specific financial terminology.
- Nidhish will use FinBERT for **inference only** (NOT training/fine-tuning).

### Why `asyncio` for the scheduler?
- `asyncio` is single-threaded but non-blocking. Perfect for I/O-bound workloads (waiting for HTTP API responses).
- Allows parallel polling loops (news every 15min, prices every 5min) without spinning up multiple OS threads.

### Why EWMA for sentiment aggregation?
- EWMA (Exponentially Weighted Moving Average) gives higher weight to more recent articles.
- A news article from 15 minutes ago carries much more market impact signal than an article from 18 hours ago.
- Implemented via `pandas.Series.ewm()`.

### Always store UTC in the DB, convert for display
All timestamps stored as `TIMESTAMP WITH TIME ZONE` in UTC. Display-layer converts to user's local timezone.

---

## 8. Phase 2 — Current Progress & Next Steps

### Watchlist Map Pattern (Answer to Nidhish's Q3)
Each ticker maps to a search query string for NewsAPI:
```python
WATCHLIST_QUERIES = {
    "TSLA": "Tesla OR TSLA OR Elon Musk",
    "AAPL": "Apple Inc OR AAPL OR iPhone",
    "MSFT": "Microsoft OR MSFT OR Windows"
}
```
The scheduler loops through each ticker, calls `fetch_headlines(query, ticker)`, and tags every returned article with that ticker symbol.

### `src/ingestion/news_client.py` — Current State
The file currently has imports and a class skeleton. **Nidhish must write the implementation.** The file structure is:

```python
import logging
import os
from newsapi import NewsApiClient

logger = logging.getLogger(__name__)

class NewsClient:
    """
    Client class to interact with NewsAPI and fetch financial news articles
    for our watchlisted tickers.
    """
    
    def __init__(self, api_key: str):
        # TODO: Initialize the official NewsApiClient using the passed api_key.
        # Store it as self.client
        pass

    def fetch_headlines(self, query: str, ticker: str) -> list[dict]:
        """
        Args:
            query: Search query string (e.g. "Tesla OR TSLA OR Elon Musk")
            ticker: Stock ticker symbol (e.g. "TSLA")
        Returns:
            List of cleaned dicts with keys matching DB schema.
        """
        # TODO:
        # 1. Wrap in try-except for network errors / rate limits
        # 2. Call self.client.get_everything(q=query, language='en', sort_by='publishedAt', page_size=50)
        # 3. Check response status — if not "ok", log error and return []
        # 4. Loop articles:
        #    - Skip if title, url, or publishedAt is None/empty
        #    - Extract: ticker, title, description, url, published_at, content
        #    - Return description/content as "" if None
        # 5. Return list of cleaned dicts
        # 6. In except block: log exception, return []
        pass
```

**Important:** The `newsapi` Python library handles HTTP → JSON → dict conversion automatically. No manual JSON parsing needed.

### Rate Limit Architecture
- NewsAPI free tier: 100 requests/day
- Polling frequency: every 15 minutes = 96 requests/day (fits within limit)
- Rate limit handling: wrap calls in `try-except`, catch exceptions, log them, return `[]` so the pipeline doesn't crash.

### Files Still To Build (Phase 2)

| File | Status | Description |
|---|---|---|
| `src/ingestion/news_client.py` | 🔄 In Progress — Nidhish writing | `NewsClient` class with `fetch_headlines()` |
| `src/ingestion/price_client.py` | ⏳ TODO | `PriceClient` class with `fetch_prices(ticker)` using `yfinance` |
| `src/db/writer.py` | ⏳ TODO | DB insert functions with `ON CONFLICT DO NOTHING` deduplication |
| `src/ingestion/scheduler.py` | ⏳ TODO | `asyncio` polling loops — 5min prices, 15min news |

---

## 9. Full Phase Roadmap

### Phase 1 — Foundation & Data Exploration ✅ COMPLETE
- Docker + TimescaleDB running locally.
- `explore/test_news.py` — fetches Tesla articles from NewsAPI, prints JSON.
- `explore/test_prices.py` — fetches 7-day TSLA OHLCV via yfinance, prints DataFrame.
- `sql/init.sql` — 3 hypertables + 5 indexes — successfully executed against live DB.

### Phase 2 — Ingestion Service 🔄 IN PROGRESS
Build `NewsClient`, `PriceClient`, DB writer with deduplication, and `asyncio` scheduler.

### Phase 3 — NLP Processing (FinBERT)
- `src/processing/classifier.py`: Load `ProsusAI/finbert` via Hugging Face `transformers`.
- Batch classify newly inserted articles with NULL sentiment.
- Update `news_sentiment` rows with `sentiment_score` and `sentiment_label`.

### Phase 4 — Aggregation & Signal Logic
- Pull recent prices + sentiment from TimescaleDB.
- Compute EWMA sentiment scores for 1h, 6h, 24h windows using `pandas.ewm()`.
- Compute price momentum (rate-of-change over last 5 ticks).
- Combine sentiment + momentum → BUY/HOLD/SELL signal → insert into `signals` table.

### Phase 5 — FastAPI Backend
- `src/api/main.py`: FastAPI server.
- Pydantic schemas for serialization.
- Endpoints: `/health`, `/api/v1/news`, `/api/v1/prices`, `/api/v1/signals`.

### Phase 6 — Streamlit Dashboard
- `src/dashboard/app.py`: Live signal cards, Plotly price chart with sentiment overlay, news feed.

### Phase 7 — Docker & CI/CD
- `Dockerfile`s for ingestion, API, dashboard services.
- Unified `docker-compose.yml` for all services.
- GitHub Actions workflow for `black` + `flake8` linting + unit tests.

### Phase 8 — Cloud Deployment & Polish
- Deploy to Render / Railway / AWS.
- Complete README with architecture diagram and build journal.
- Add live demo URL.

---

## 10. Explore Scripts (Already Written & Tested)

### `explore/test_news.py`
Fetches Tesla articles from NewsAPI and prints the full JSON response. Confirmed working — returned 301 results including real articles from Gizmodo, Business Insider, etc.

Key pattern used:
```python
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
response = newsapi.get_everything(q="Tesla")
print(json.dumps(response, indent=2))
```

### `explore/test_prices.py`
Fetches 7-day TSLA OHLCV data via yfinance and prints as DataFrame. Confirmed working.

Sample output structure:
```
                                 Open        High         Low       Close    Volume  Dividends  Stock Splits
Date
2026-06-08 00:00:00-04:00  396.329987  412.940002  394.720001  408.950012  50328800        0.0           0.0
```

Key pattern used:
```python
import yfinance as yf
ticker = yf.Ticker("TSLA")
df = ticker.history(period="7d")
print(df)
```

---

## 11. Decisions Made & Alternatives Rejected

| Decision | Choice Made | Alternative Rejected | Reason |
|---|---|---|---|
| TimescaleDB image | `timescale/timescaledb-ha:pg16` | `timescale/timescaledb:latest-pg16` | Latest image fails to pull (EOF network errors) |
| TimescaleDB vs. Supabase | TimescaleDB | Supabase | TimescaleDB is free via Docker locally |
| PostgreSQL version | pg16 | pg17 | pg17 caused volume incompatibility; pg16 works |
| Deduplication key for news | `article_url` (as part of composite PK) | `urlToImage` (Nidhish's initial suggestion) | URL uniquely identifies articles; images can be shared |
| Deduplication key for prices | Composite `(stock_date_time, ticker)` | `price_open` (Nidhish's initial suggestion) | Open price is not unique; time+ticker pair is |
| String types | `TEXT` | `VARCHAR(N)` | No performance difference in PostgreSQL; TEXT preferred |
| Volume column type | `BIGINT` | `INTEGER` | TSLA trades ~50M shares/day; INTEGER max is ~2.1B but safer to use BIGINT |
| Timestamp storage | `TIMESTAMP WITH TIME ZONE` (UTC) | Local time | Always store UTC; convert at display layer |

---

## 12. Common Errors Encountered & Solutions

| Error | Cause | Solution |
|---|---|---|
| `The '<' operator is reserved for future use` | PowerShell doesn't support `<` stdin redirection | Use `Get-Content sql/init.sql -Raw \| docker exec -i ...` |
| `multiple primary keys for table "news_sentiment" are not allowed` | Two PRIMARY KEY definitions in `news_sentiment` | Remove `PRIMARY KEY` inline on `article_url`; keep only composite PK at bottom |
| `cannot create a unique index without the column "published_at"` | TimescaleDB requires time partition column in any unique constraint | Use composite `PRIMARY KEY(published_at, article_url)` |
| Docker HTTP 500 / container crash | Docker Desktop bug | Run `wsl --shutdown` then restart Docker Desktop |
| `timescale/timescaledb:latest-pg16` EOF pull failure | Network/resource issue with large image layers | Use `timescale/timescaledb-ha:pg16` instead |
| pg16 container fails to start after pg17 was running | Data volume incompatibility between PostgreSQL major versions | Run `docker-compose down -v` (with `-v` to delete volumes) before switching |

---

## 13. Open Questions / TODOs for Future AI

1. **`news_client.py`**: Nidhish is currently implementing the `NewsClient` class. Guide him through the `fetch_headlines` method step by step using the TODO comments already placed in the file. Do NOT write the code for him.

2. **WATCHLIST_QUERIES**: Where should this live? Options: a config file (`config/watchlist.py`), hardcoded in `scheduler.py`, or in `.env`. Discuss with Nidhish before deciding.

3. **DB Connection**: How will the ingestion scripts connect to TimescaleDB? Options: `asyncpg` (async, raw SQL), `SQLAlchemy` (ORM). Discuss with Nidhish in Phase 2 Step 3 (writer.py).

4. **`price_client.py`**: Once `news_client.py` is done, guide Nidhish to build this. Key question: how does yfinance handle real-time vs. historical data? What interval should we use for polling?

5. **Scheduler design**: The `asyncio` scheduler pattern is new to Nidhish. He will need conceptual explanation of `asyncio.sleep()` and async loops before implementing `scheduler.py`.

6. **FinBERT model download**: In Phase 3, the model will be downloaded on first run via Hugging Face `transformers`. Nidhish should understand this is a one-time ~400MB download cached locally.

---

## 14. Nidhish's Understanding Checkpoints

These are concepts Nidhish has demonstrated understanding of:

- ✅ Why `create_hypertable()` vs. plain `CREATE TABLE`
- ✅ What the second argument of `create_hypertable()` does (time partition column)
- ✅ Why `published_at` is the time dimension for `news_sentiment`
- ✅ Why `article_url` is the deduplication key for news
- ✅ Why volume needs `BIGINT`
- ✅ The difference between `__init__` (setup/constructor) and an API handler
- ✅ What `news_client.py` is doing at a high level (fetching, filtering, cleaning)
- ✅ The decoupled architecture: news_client → DB → FinBERT (not direct pipeline)
- ✅ Rate limiting strategy (100 req/day, 15-min poll interval = 96 req/day)
- ✅ What fields to extract from NewsAPI response (matches DB schema columns)
- ⏳ Ticker-to-query mapping pattern (explained but not yet implemented)
- ⏳ `asyncio` concurrency model (not yet explained in depth)
- ⏳ `ON CONFLICT DO NOTHING` deduplication in SQL
