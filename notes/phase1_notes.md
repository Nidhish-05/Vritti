# Phase 1 Notes — Data Exploration
# Fill this in BEFORE writing any ingestion code.
# -----------------------------------------------

## NewsAPI Fields

### Fields I will STORE (and why):
<!-- e.g., title — this is what FinBERT scores -->
<!-- e.g., published_at — time dimension for hypertable -->

### Fields I will DISCARD (and why):


## Deduplication Strategy

### News articles — unique key:
### Price ticks — unique key:


## Ticker Matching

### How will I match "Apple announces iPhone 17" → AAPL?
<!-- Describe your approach here before writing code -->


## TimescaleDB Questions

### What is a hypertable and what does it give me over a regular table?

### What is the time dimension column for each of my three tables?

### Why is time-range query performance better in TimescaleDB?


## Schema Draft

### news_sentiment columns:
<!-- draft them here before writing SQL -->

### price_ticks columns:

### signals columns:
