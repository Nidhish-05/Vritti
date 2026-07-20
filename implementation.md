# Vritti — Implementation Notes & Decisions

> *A record of key technical decisions, architectural choices, and the deployment pathways considered for V1 and beyond. Committed alongside the codebase for future reference.*

---

## Architecture Decisions

### Why TimescaleDB?
Hypertables partition `news_sentiment`, `price_ticks`, and `signals` on their time columns. At scale (months of 50-ticker data), this reduces range queries from O(full scan) to O(partition). Schema uses standard SQL otherwise — TimescaleDB is a pure performance layer.

### Why asyncpg over SQLAlchemy?
Raw async PostgreSQL driver. Lower overhead for the high-frequency batch insert workload (hundreds of rows per poll cycle). All DB functions are plain async Python taking a connection parameter — simple, testable, no ORM magic.

### Why FastAPI?
Native async, auto-generated Swagger docs, Pydantic validation. Industry standard for ML serving APIs. Matches the async nature of the ingestion and DB layers.

### Why FinBERT over general sentiment models?
`ProsusAI/finbert` is trained on financial corpora. General models (VADER, TextBlob) misclassify finance-specific language. *"Apple beats earnings estimates"* scores ambiguous in VADER, strongly positive in FinBERT. Domain specificity is the value.

### Why React + Vite over Streamlit?
Streamlit cannot produce the 3D physics-based card effects, glassmorphic design, or live ticker marquee that make this project visually distinctive. React + Vite produces a real SPA deployable to Vercel. Vanilla CSS was chosen over Tailwind for full control over the custom design system.

---

## Notable Bugs Found & Fixed

| Bug | Root Cause | Fix |
|---|---|---|
| 500 on `/signals/{ticker}` | `reader.py` dereferenced `rows` (list) instead of `rows[0]` (first record) | Corrected indexing |
| React white screen on load | `useTilt()` hook called after early return — violates Rules of Hooks | Moved hook call to top of component |
| React white screen on load | `Github` / `Linkedin` not exported by `lucide-react v1.x` | Replaced with inline SVG paths |
| PostCSS CSS `@import` error | Google Fonts `@import url()` placed after `@import "tailwindcss"` | Moved Google Fonts import to line 1 in `index.css` |
| Network Error / CORS on all API calls | Vite proxy only watched `/api` prefix; Axios baseURL was `localhost:8000` directly | Fixed proxy to intercept `/signals`, `/prices`, `/sentiment` prefixes; set Axios baseURL to `''` |

---

## Watchlist (50 Tickers)

Expanded from 3 → 50 in `src/ingestion/scheduler.py`.

**NewsAPI Rate Limit Note:** Free tier = 100 req/day. At 50 tickers × 1 req × 96 polls/day = 4,800 req — far over limit. Mitigation: throttle to 2 batched queries per 15-min cycle using compound `OR` queries. Each query covers ~25 tickers semantically.

---

## Deployment Pathways

Three options were evaluated. Choose based on your goal at the time.

### Option 1 — Full Local (Current State)
Everything runs on your machine. Docker + uvicorn + scheduler + FinBERT + Vite dev server. Zero cost, zero setup, best for development. No public URL.

### Option 2 — Hybrid Free Cloud
- **Frontend:** Vercel (free, auto-deploys from GitHub push)
- **API:** Render (free 512MB Web Service)
- **Database:** Neon.tech (free 500MB serverless PostgreSQL)
- **Ingestion + FinBERT:** Still runs locally, writes to Neon DB

**Schema change required:** Remove `CREATE EXTENSION IF NOT EXISTS timescaledb` and the three `SELECT create_hypertable(...)` calls from `sql/init.sql`. Tables are standard PostgreSQL — no functional change.

**Result:** Live public URL at zero cost. Data freshness depends on running the local pipeline periodically.

### Option 3 — Full Production (Maximum Resume Value)
- **Frontend:** Vercel (CDN, auto-deploy)
- **API:** Railway.app (always-on FastAPI)
- **Database:** Neon.tech (serverless PostgreSQL)
- **FinBERT Inference:** Modal.com (serverless GPU functions — free $30/month credit, enough for this workload)
- **Scheduler/CI:** GitHub Actions cron (runs ingestion + FinBERT every 6h automatically, free 2000 min/month)

**Why Modal.com is the right call for FinBERT:** FinBERT needs ~1.5–2GB RAM. Free cloud tiers cap at 512MB. Modal spins up a serverless container with sufficient memory on demand, runs inference, and scales to zero. You pay ~$0.002/day at this volume.

**LinkedIn talking point:** *"Deployed a serverless ML inference pipeline for financial NLP using Modal, automated via GitHub Actions, serving a React SPA from Vercel with a FastAPI backend."*

**Cost:** Effectively $0/month across all services on free tiers.

---

## Long-Term Versioning Roadmap

| Version | Core Feature | Tech Addition |
|---|---|---|
| V1 (current) | FinBERT news sentiment → BUY/HOLD/SELL | FastAPI + React + TimescaleDB |
| V2 | LSTM price-trend model + IPO watchlist + Risk calculator | PyTorch, SEC EDGAR API |
| V3 | Education platform + GenAI report generator (SaaS) | LLM API, Auth, Stripe |

---

## Current Status at Last Commit

**Complete:** Phases 1–6 (backend pipeline + React frontend)  
**Pending:** Phase 7 (CI/CD + Docker Compose), Phase 8 (Cloud deployment)  
**Watchlist:** 50 tickers across 8 sectors  
**Frontend:** Builds clean, Vite proxy correctly routing to FastAPI, all pages functional
