import { useState, useEffect, useCallback } from 'react'
import { fetchAllSignals } from '../api/client'

/**
 * useAllSignals — Fetches and auto-refreshes signals for the entire watchlist.
 * Returns: { signals, loading, error, refetch, lastUpdated }
 */
export function useAllSignals() {
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const load = useCallback(async () => {
    setError(null)
    try {
      const data = await fetchAllSignals()
      if (data && data.length > 0) {
        setSignals(data)
        setLastUpdated(new Date())
      } else if (data && data.length === 0) {
        setSignals([])
      }
    } catch {
      setError('Unable to reach the market data server.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
    // Auto-refresh every 60 seconds
    const interval = setInterval(load, 60_000)
    return () => clearInterval(interval)
  }, [load])

  return { signals, loading, error, refetch: load, lastUpdated }
}
