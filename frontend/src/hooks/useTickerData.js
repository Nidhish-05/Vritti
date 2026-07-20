import { useState, useEffect } from 'react'
import {
  fetchSignal,
  fetchPriceHistory,
  fetchSentimentHistory,
  fetchLatestNews,
} from '../api/client'

/**
 * useTickerData — Fetches all data for a single ticker in parallel.
 * Triggers re-fetch whenever ticker or hours changes.
 *
 * Returns: { signal, prices, sentiments, news, loading, error }
 */
export function useTickerData(ticker, hours = 168) {
  const [signal, setSignal] = useState(null)
  const [prices, setPrices] = useState([])
  const [sentiments, setSentiments] = useState([])
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!ticker) {
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)
    // Reset previous data immediately so stale data doesn't flash
    setSignal(null)
    setPrices([])
    setSentiments([])
    setNews([])

    Promise.all([
      fetchSignal(ticker),
      fetchPriceHistory(ticker, hours),
      fetchSentimentHistory(ticker, hours),
      fetchLatestNews(ticker, 10),
    ])
      .then(([sig, prc, sen, nws]) => {
        setSignal(sig)
        setPrices(prc || [])
        setSentiments(sen || [])
        setNews(nws || [])
      })
      .catch(() => {
        setError(`Failed to fetch data for ${ticker}.`)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [ticker, hours])

  return { signal, prices, sentiments, news, loading, error }
}
