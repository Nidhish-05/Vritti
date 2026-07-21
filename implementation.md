# Vritti — Implementation Notes & Decisions

> *A record of key technical decisions, architectural choices, and the deployment pathways considered for V1 and beyond. Committed alongside the codebase for future reference.*

---

## Branch Strategy

```
vritti/
├── master            → original working branch (all Phase 1-6 history)
├── master-local      → full local version (source of truth, 50 tickers, TimescaleDB)
└── master-cloud      → stripped demo version (10 tickers, Neon PostgreSQL, Vercel + Render)
```

### Branch Creation (Run Once)

```bash
git checkout -b master-local
git push origin master-local

git checkout master
git checkout -b master-cloud
git push origin master-cloud

git checkout master-local   # return here for all development work
```

### What Differs Between Branches

| File | master-local | master-cloud |
|---|---|---|
| `sql/init.sql` | TimescaleDB extension + 3× `create_hypertable()` | Those lines removed (standard PostgreSQL for Neon) |
| `src/ingestion/scheduler.py` | 50 tickers | 10 tickers |
| Database | Local TimescaleDB Docker | Neon.tech serverless PostgreSQL |
| API | Local uvicorn | Render Web Service |
| Frontend | Vite dev server | Vercel (auto-deploy) |

---

## Architecture Decisions

### Why TimescaleDB?
Hypertables partition `news_sentiment`, `price_ticks`, `signals` on their time columns. At scale, this reduces range queries from O(full scan) to O(partition). Standard SQL otherwise. Not available on Neon → hence the branch split.

### Why asyncpg over SQLAlchemy?
Raw async PostgreSQL driver. Lower overhead for high-frequency batch inserts. All DB functions are plain async Python — no ORM magic.

### Why FastAPI?
Native async, auto-generated Swagger docs, Pydantic validation. Industry standard for ML serving APIs.

### Why FinBERT (`ProsusAI/finbert`) over general sentiment models?
Trained on financial corpora. General models misclassify finance language. Needs ~1.5–2GB RAM — free cloud tiers cap at 512MB. Manual local schedule → push to cloud DB is the V1 workaround.

### Why React + Vite over Streamlit?
Cannot produce 3D physics card effects, glassmorphism, or live ticker marquee. Vanilla CSS over Tailwind for full control of the custom design system.

### NewsAPI Rate Limit Strategy
Free tier = 100 req/day. `master-cloud` reduces to 10 tickers. `master-local` uses compound OR queries to cover 50 tickers across fewer requests.

---

## Notable Bugs Fixed

| Bug | Root Cause | Fix |
|---|---|---|
| 500 on `/signals/{ticker}` | `reader.py` dereferenced `rows` (list) instead of `rows[0]` | Corrected indexing |
| React white screen | `useTilt()` hook called after early return — violates Rules of Hooks | Moved hook to top of component |
| React white screen | `Github`/`Linkedin` not exported by `lucide-react v1.x` | Replaced with inline SVGs |
| PostCSS `@import` error | Google Fonts `@import url()` after `@import "tailwindcss"` | Moved Google Fonts to line 1 |
| Network Error / CORS | Vite proxy watched `/api`; Axios baseURL was `localhost:8000` | Fixed proxy prefixes; Axios baseURL set to `''` |

---

## Deployment Pathways

### Option 1 — Full Local (`master-local`)
Everything on your machine. Zero cost, full FinBERT capacity, TimescaleDB. No public URL.

### Option 2 — Hybrid Free Cloud (`master-cloud`)
- Frontend: Vercel (auto-deploy from master-cloud)
- API: Render (512MB free, sleeps after 15min)
- DB: Neon.tech (500MB free PostgreSQL)
- FinBERT: Runs locally on manual schedule, writes to Neon DB
- **Schema change required:** Remove `CREATE EXTENSION IF NOT EXISTS timescaledb` and the three `create_hypertable()` calls from `sql/init.sql`

### Option 3 — Full Production (V2 target)
- Frontend: Vercel
- API: Railway
- DB: Neon
- FinBERT: Modal.com (serverless GPU, $30/month free credit)
- CI/CD: GitHub Actions cron (runs ingestion + FinBERT every 6h automatically)

Do not introduce Modal.com until V2.

---

## Long-Term Versioning Roadmap

| Version | Core Feature | Tech Addition |
|---|---|---|
| V1 (current) | FinBERT news sentiment → BUY/HOLD/SELL | FastAPI + React + TimescaleDB |
| V2 | LSTM price-trend model + IPO watchlist + Risk calculator | PyTorch, SEC EDGAR API, Modal.com |
| V3 | Education platform + GenAI report generator (SaaS) | LLM API, Auth, Stripe |

---

## Current Status at Last Commit

**Complete:** Phases 1–6 (backend pipeline + React frontend)
**Pending:** Phase 7 (CI/CD + Docker Compose on master-local), Phase 8 (cloud deployment on master-cloud)
**Watchlist:** 50 tickers on master-local, 10 tickers on master-cloud
**Frontend:** Builds clean, Vite proxy routing correctly, all pages functional
