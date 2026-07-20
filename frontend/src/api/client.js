import axios from 'axios'

// Base Axios instance pointing to the FastAPI server.
// During development, Vite's proxy rewrites /api → http://localhost:8000
// In production, VITE_API_BASE_URL points to the deployed API.
const api = axios.create({
  // Use relative base URL so requests go through the Vite dev proxy.
  // Set VITE_API_BASE_URL in .env for production deployments.
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 10000,
})

// ── API helper functions ───────────────────────────────────────────
// Each function wraps an axios call in try-catch.
// On success it returns the response data.
// On error it logs the error and returns null.

/**
 * Fetch the latest BUY/HOLD/SELL signal for every ticker in the watchlist.
 * Calls: GET /signals/all
 */
export async function fetchAllSignals() {
  try {
    const response = await api.get('/signals/all')
    return response.data
  } catch (error) {
    console.error('fetchAllSignals error:', error)
    return null
  }
}

/**
 * Fetch the latest signal for a single ticker.
 * Calls: GET /signals/{ticker}
 * @param {string} ticker - e.g. "TSLA"
 */
export async function fetchSignal(ticker) {
  try {
    const response = await api.get(`/signals/${ticker}`)
    return response.data
  } catch (error) {
    console.error(`fetchSignal(${ticker}) error:`, error)
    return null
  }
}

/**
 * Fetch OHLCV price ticks for a ticker over a rolling time window.
 * Calls: GET /prices/{ticker}?hours=N
 * @param {string} ticker
 * @param {number} hours - rolling window in hours (default 24)
 */
export async function fetchPriceHistory(ticker, hours = 24) {
  try {
    const response = await api.get(`/prices/${ticker}`, { params: { hours } })
    return response.data
  } catch (error) {
    console.error(`fetchPriceHistory(${ticker}, ${hours}h) error:`, error)
    return null
  }
}

/**
 * Fetch rolling FinBERT sentiment scores for a ticker.
 * Calls: GET /sentiment/history?ticker=X&hours=N
 * @param {string} ticker
 * @param {number} hours
 */
export async function fetchSentimentHistory(ticker, hours = 24) {
  try {
    const response = await api.get('/sentiment/history', { params: { ticker, hours } })
    return response.data
  } catch (error) {
    console.error(`fetchSentimentHistory(${ticker}, ${hours}h) error:`, error)
    return null
  }
}

/**
 * Fetch the most recent classified news articles.
 * Calls: GET /sentiment/news/latest
 * @param {string} [ticker] - Optional ticker. If omitted, fetches globally.
 * @param {number} limit - number of articles (default 10)
 */
export async function fetchLatestNews(ticker = null, limit = 10) {
  try {
    const params = { limit }
    if (ticker && ticker !== 'all') params.ticker = ticker
    
    const response = await api.get('/sentiment/news/latest', { params })
    return response.data
  } catch (error) {
    console.error(`fetchLatestNews(${ticker}) error:`, error)
    return null
  }
}
