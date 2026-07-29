-- =============================================================================
-- Vritti — Database Schema (master-cloud)
-- Standard PostgreSQL — compatible with Neon.tech
-- TimescaleDB extension and hypertable calls intentionally omitted.
-- =============================================================================

-- Table 1: news_sentiment
-- Stores one row per news article, enriched with FinBERT sentiment.

CREATE TABLE IF NOT EXISTS news_sentiment(

    ticker TEXT NOT NULL,
    sentiment_score NUMERIC(5,4) NULL,
    sentiment_label TEXT NULL,
    article_url TEXT NOT NULL,
    article_title TEXT NOT NULL,
    article_description TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    content TEXT NOT NULL,
    PRIMARY KEY (published_at, article_url)

);

-- Table 2: price_ticks
-- Stores OHLCV data per ticker per timestamp.

CREATE TABLE IF NOT EXISTS price_ticks(

    ticker TEXT NOT NULL,
    stock_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    price_open DECIMAL(10, 6) NOT NULL,
    price_high DECIMAL(10, 6) NOT NULL,
    price_low DECIMAL(10, 6) NOT NULL,
    price_close DECIMAL(10, 6) NOT NULL,
    stock_volume BIGINT NOT NULL,
    PRIMARY KEY(stock_date_time, ticker)

);

-- Table 3: signals
-- Stores derived BUY/HOLD/SELL signals per ticker.

CREATE TABLE IF NOT EXISTS signals(

    generated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ticker TEXT NOT NULL,
    signal TEXT NOT NULL,
    sentiment_score NUMERIC(5,4) NULL,
    momentum NUMERIC(8,4) NOT NULL,
    window_hours INTEGER NOT NULL,
    PRIMARY KEY(generated_at, ticker, window_hours)

);

-- =============================================================================
-- Indexes — same as master-local, standard PostgreSQL B-tree indexes.
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_news_sentiment_ticker      ON news_sentiment (ticker);
CREATE INDEX IF NOT EXISTS idx_news_sentiment_published   ON news_sentiment (published_at DESC);
CREATE INDEX IF NOT EXISTS idx_price_ticks_ticker         ON price_ticks (ticker);
CREATE INDEX IF NOT EXISTS idx_price_ticks_datetime       ON price_ticks (stock_date_time DESC);
CREATE INDEX IF NOT EXISTS idx_signals_ticker             ON signals (ticker);