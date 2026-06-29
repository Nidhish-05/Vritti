-- =============================================================================
-- Vritti — Database Schema
-- PostgreSQL + TimescaleDB
-- =============================================================================
-- BEFORE running this script, answer:
--   1. Why do we call create_hypertable() instead of just CREATE TABLE?
--   2. What does the second argument to create_hypertable() specify?
--   3. Why is `published_at` the time dimension for news_sentiment
--      rather than `inserted_at`?
-- =============================================================================
-- ANSWERS:
-- 1) We use create_hypertable() because it directly converts a postgreSQL relational table into a hypertable, which is a table partitioning done on the basis of time.
-- 2) The second arguement of the create_hypertable() specify the column in the table on which the partitioning is to be done. In other words it is the column which represents the timestamp column on the basis of which, hypertable will function.
-- 3) The time published_at is the time dimension because it is unique for each news, and more importantly, it forms the basis of the news' timeline as it specifies how old the news is. This will come in handy when analysing the relation between the news and the stock price.
-- =============================================================================
-- Enable TimescaleDB extension

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- =============================================================================
-- TODO (Phase 1): Define your three tables below.
-- Think carefully about:
--   - Column names and types
--   - NOT NULL constraints
--   - UNIQUE constraints for deduplication
--   - Which column is the time dimension for TimescaleDB
-- =============================================================================

-- Table 1: news_sentiment
-- Stores: one row per news article, enriched with FinBERT sentiment
-- TODO: Define columns and constraints here

CREATE TABLE news_sentiment(

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
-- Stores: OHLCV data per ticker per timestamp
-- TODO: Define columns and constraints here

CREATE TABLE price_ticks(

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
-- Stores: derived BUY/HOLD/SELL signals per ticker
-- TODO: Define columns and constraints here

CREATE TABLE signals(
    
    generated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ticker TEXT NOT NULL,
    signal TEXT NOT NULL,
    sentiment_score NUMERIC(5,4) NULL,
    momentum NUMERIC(8,4) NOT NULL,
    window_hours INTEGER NOT NULL,
    PRIMARY KEY(generated_at, ticker, window_hours)

);

-- =============================================================================
-- Convert tables to TimescaleDB hypertables
-- TODO: Call select create_hypertable(...) for each of the three tables above
-- Read: https://docs.timescale.com/api/latest/hypertable/create_hypertable/
-- =============================================================================

SELECT create_hypertable('news_sentiment', by_range('published_at'));
SELECT create_hypertable('price_ticks', by_range('stock_date_time'));
SELECT create_hypertable('signals', by_range('generated_at'));

-- =============================================================================
-- Indexes
-- TODO: Create indexes on columns you will filter by most frequently
-- Hint: What columns appear in WHERE clauses in your API routes?
-- =============================================================================

CREATE INDEX ON news_sentiment (ticker);
CREATE INDEX ON news_sentiment (published_at DESC);
CREATE INDEX ON price_ticks (ticker);
CREATE INDEX ON price_ticks (stock_date_time DESC);
CREATE INDEX ON signals (ticker);