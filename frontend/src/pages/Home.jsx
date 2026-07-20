import { useEffect, useState } from 'react'
import { TrendingUp, Cpu, Newspaper, BarChart2, RefreshCw, AlertCircle } from 'lucide-react'
import { useAllSignals } from '../hooks/useAllSignals'
import { fetchSignal } from '../api/client'
import { sanitizeTicker } from '../utils/security'
import SearchBar from '../components/SearchBar'
import SignalCard from '../components/SignalCard'
import CardDrawer from '../components/CardDrawer'

/** Time window options available in the drawer */
const HOUR_OPTIONS = [
  { label: '24h',  value: 24  },
  { label: '48h',  value: 48  },
  { label: '7d',   value: 168 },
]

export default function Home() {
  const { signals, loading, error, refetch, lastUpdated } = useAllSignals()

  // Drawer state
  const [drawerTicker, setDrawerTicker] = useState(null)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [drawerHours, setDrawerHours] = useState(168)

  // Search state
  const [searchResult, setSearchResult] = useState(null)
  const [searchLoading, setSearchLoading] = useState(false)
  const [searchError, setSearchError] = useState(null)

  useEffect(() => {
    document.title = 'Vritti — Market Intelligence'
  }, [])

  // Open drawer for a ticker
  const openDrawer = (ticker) => {
    setDrawerTicker(ticker)
    setDrawerOpen(true)
  }

  const closeDrawer = () => {
    setDrawerOpen(false)
    // Delay clearing ticker so the slide-out animation finishes first
    setTimeout(() => setDrawerTicker(null), 350)
  }

  // Handle ticker search
  const handleSearch = async (rawTicker) => {
    setSearchError(null)
    setSearchResult(null)
    if (!rawTicker) return

    const ticker = sanitizeTicker(rawTicker)
    if (!ticker) return

    // If ticker is already in the watchlist, just open its drawer
    const existing = signals.find(s => s.ticker === ticker)
    if (existing) {
      openDrawer(ticker)
      return
    }

    // Otherwise fetch it from the API
    setSearchLoading(true)
    const data = await fetchSignal(ticker)
    setSearchLoading(false)

    if (data) {
      setSearchResult(data)
    } else {
      setSearchError(`No data found for "${ticker}". This ticker may not be in our watchlist.`)
    }
  }

  const lastUpdatedStr = lastUpdated
    ? lastUpdated.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })
    : null

  return (
    <>
      {/* ── Hero Section ─────────────────────────────────────────────── */}
      <main className="main-content page-enter">
        <section style={{
          minHeight: '72vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '60px 24px 40px',
          position: 'relative',
          overflow: 'hidden',
        }}>
          {/* Background glow orbs */}
          <div style={{
            position: 'absolute', top: '15%', left: '10%',
            width: 500, height: 500, borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(0,198,255,0.06) 0%, transparent 70%)',
            filter: 'blur(60px)', pointerEvents: 'none',
          }} />
          <div style={{
            position: 'absolute', bottom: '10%', right: '10%',
            width: 400, height: 400, borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(0,230,118,0.05) 0%, transparent 70%)',
            filter: 'blur(60px)', pointerEvents: 'none',
          }} />

          {/* Live badge */}
          <span className="badge badge-buy" style={{ marginBottom: 28, fontSize: 10 }}>
            <span style={{
              width: 6, height: 6, borderRadius: '50%',
              background: 'currentColor', display: 'inline-block',
            }} />
            &nbsp; Live Market Intelligence
          </span>

          {/* Headline */}
          <h1 style={{
            fontSize: 'clamp(34px, 5.5vw, 68px)',
            fontWeight: 800, lineHeight: 1.1,
            letterSpacing: '-2px', marginBottom: 22,
            maxWidth: 750, color: 'var(--text-primary)',
          }}>
            Turn Market Noise into{' '}
            <span className="text-gradient">Clear Signals</span>
          </h1>

          <p style={{
            fontSize: 'clamp(15px, 1.8vw, 19px)',
            color: 'var(--text-secondary)',
            maxWidth: 560, lineHeight: 1.7, marginBottom: 40,
          }}>
            Real-time financial news · FinBERT sentiment · price momentum
            → <strong>BUY</strong>, <strong>HOLD</strong>, or{' '}
            <strong>SELL</strong> — no account needed.
          </p>

          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
            <a href="#market" className="btn-primary">
              <TrendingUp size={16} />
              View Market
            </a>
            <a href="/about" className="btn-secondary">
              How it works
            </a>
          </div>

          {/* Feature pills */}
          <div style={{ display: 'flex', gap: 14, marginTop: 52, flexWrap: 'wrap', justifyContent: 'center' }}>
            {[
              { Icon: Newspaper, label: 'Real-time News Ingestion' },
              { Icon: Cpu,       label: 'FinBERT NLP Scoring' },
              { Icon: BarChart2, label: 'Momentum Signal Engine' },
            ].map(({ Icon, label }) => (
              <div key={label} style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '8px 16px',
                borderRadius: 10,
                background: 'var(--bg-card)',
                border: '1px solid var(--border-color)',
                fontSize: 13, color: 'var(--text-secondary)',
              }}>
                <Icon size={15} color="var(--accent)" />
                {label}
              </div>
            ))}
          </div>
        </section>

        {/* ── Market Dashboard ──────────────────────────────────────── */}
        <section id="market" className="market-section">

          {/* Header row: title + search + refresh */}
          <div className="market-header">
            <div>
              <div className="market-title">Market Signals</div>
              <div className="market-subtitle">
                Click any card to view price chart, sentiment history & latest news
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
              {lastUpdatedStr && (
                <span className="last-updated">Updated {lastUpdatedStr}</span>
              )}
              <button
                className="btn-icon"
                onClick={refetch}
                title="Refresh signals"
                aria-label="Refresh signals"
              >
                <RefreshCw size={16} />
              </button>
            </div>
          </div>

          {/* Search bar */}
          <div style={{ marginBottom: 28 }}>
            <SearchBar onSearch={handleSearch} />
            {searchLoading && (
              <div style={{ marginTop: 10, display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-muted)', fontSize: 13 }}>
                <div className="spinner" style={{ width: 14, height: 14 }} />
                Searching…
              </div>
            )}
            {searchError && (
              <div style={{
                marginTop: 10, display: 'flex', alignItems: 'center', gap: 8,
                color: 'var(--signal-sell)', fontSize: 13,
              }}>
                <AlertCircle size={14} />
                {searchError}
              </div>
            )}
          </div>

          {/* Search result card (if ticker not in watchlist) */}
          {searchResult && (
            <div style={{ marginBottom: 28 }}>
              <div style={{ fontSize: 12, color: 'var(--accent)', marginBottom: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                Search Result
              </div>
              <div style={{ maxWidth: 300 }}>
                <SignalCard data={searchResult} onClick={() => openDrawer(searchResult.ticker)} />
              </div>
            </div>
          )}

          {/* Main card grid */}
          {loading && (
            <div className="cards-grid">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="signal-card signal-card-none" style={{ cursor: 'default' }}>
                  <div className="skeleton" style={{ height: 14, width: 60, marginBottom: 16 }} />
                  <div className="skeleton" style={{ height: 32, width: 100, marginBottom: 16 }} />
                  <div className="skeleton" style={{ height: 12, width: '50%', marginBottom: 8 }} />
                  <div className="skeleton" style={{ height: 12, width: '35%' }} />
                </div>
              ))}
            </div>
          )}

          {error && !loading && (
            <div className="empty-state">
              <AlertCircle size={40} className="empty-state-icon" />
              <span className="empty-state-title">Unable to load signals</span>
              <span className="empty-state-desc">{error}</span>
              <button className="btn-secondary" onClick={refetch} style={{ marginTop: 8 }}>
                Try again
              </button>
            </div>
          )}

          {!loading && !error && signals.length === 0 && (
            <div className="empty-state">
              <BarChart2 size={40} className="empty-state-icon" />
              <span className="empty-state-title">No signals yet</span>
              <span className="empty-state-desc">
                The signal pipeline hasn't run yet. Start the ingestion scheduler
                and run the signal generator to populate data.
              </span>
            </div>
          )}

          {!loading && signals.length > 0 && (
            <div className="cards-grid">
              {signals.map(s => (
                <SignalCard
                  key={s.ticker}
                  data={s}
                  onClick={() => openDrawer(s.ticker)}
                />
              ))}
            </div>
          )}

          {/* Hours selector for drawer (shown when a card is selected) */}
          {drawerTicker && (
            <div style={{
              position: 'fixed', bottom: 52, left: '50%', transform: 'translateX(-50%)',
              display: 'flex', gap: 6, background: 'var(--bg-surface)',
              border: '1px solid var(--border-color)', borderRadius: 10,
              padding: '6px 8px', zIndex: 302,
              boxShadow: 'var(--shadow-elevated)',
            }}>
              {HOUR_OPTIONS.map(({ label, value }) => (
                <button
                  key={value}
                  className={`hours-btn${drawerHours === value ? ' active' : ''}`}
                  onClick={() => setDrawerHours(value)}
                >
                  {label}
                </button>
              ))}
            </div>
          )}

        </section>
      </main>

      {/* Card Drawer — rendered outside main so it overlays everything */}
      <CardDrawer
        ticker={drawerTicker}
        hours={drawerHours}
        isOpen={drawerOpen}
        onClose={closeDrawer}
      />
    </>
  )
}
