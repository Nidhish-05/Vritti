import { useEffect } from 'react'
import { X, TrendingUp, TrendingDown, Minus, ExternalLink } from 'lucide-react'
import { useTickerData } from '../hooks/useTickerData'
import { sanitizeUrl } from '../utils/security'
import PriceChart from './PriceChart'
import SentimentChart from './SentimentChart'

/** Signal color helper */
function signalColor(signal) {
  if (signal === 'BUY')  return 'var(--signal-buy)'
  if (signal === 'SELL') return 'var(--signal-sell)'
  if (signal === 'HOLD') return 'var(--signal-hold)'
  return 'var(--text-muted)'
}

function SignalIcon({ signal, size = 20 }) {
  if (signal === 'BUY')  return <TrendingUp  size={size} color="var(--signal-buy)"  strokeWidth={2.5} />
  if (signal === 'SELL') return <TrendingDown size={size} color="var(--signal-sell)" strokeWidth={2.5} />
  return <Minus size={size} color="var(--signal-hold)" strokeWidth={2.5} />
}

/** Formats momentum as "+4.32%" */
function fmtMomentum(v) {
  if (v === null || v === undefined) return '—'
  const p = (parseFloat(v) * 100).toFixed(2)
  return parseFloat(p) >= 0 ? `+${p}%` : `${p}%`
}

/** Formats ISO date as short local datetime */
function fmtDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('en-IN', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

/** Sentiment badge for news items */
function SentimentBadge({ label }) {
  const cls =
    label === 'positive' ? 'badge badge-positive' :
    label === 'negative' ? 'badge badge-negative' :
    'badge badge-neutral'
  return <span className={cls}>{label || 'unscored'}</span>
}

/**
 * CardDrawer — Slide-in right panel showing full ticker details.
 *
 * Props:
 *   ticker    {string}   — the selected ticker
 *   hours     {number}   — time window in hours
 *   onClose   {function} — called when the drawer is closed
 *   isOpen    {boolean}  — controls the slide-in animation
 */
export default function CardDrawer({ ticker, hours = 168, onClose, isOpen }) {
  const { signal, prices, sentiments, news, loading } = useTickerData(ticker, hours)
  const [selectedArticle, setSelectedArticle] = useState(null)

  // Lock body scroll when drawer is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => { document.body.style.overflow = '' }
  }, [isOpen])

  // Escape key closes drawer
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div className="drawer-overlay" onClick={onClose} aria-hidden="true" />
      )}

      {/* Panel */}
      <div
        className={`drawer-panel${isOpen ? ' open' : ''}`}
        role="dialog"
        aria-modal="true"
        aria-label={`${ticker} details`}
      >
        {/* Sticky header */}
        <div className="drawer-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span className="drawer-ticker">{ticker}</span>
            {signal && (
              <span style={{
                display: 'flex', alignItems: 'center', gap: 6,
                color: signalColor(signal.signal),
                fontWeight: 700, fontSize: 15,
              }}>
                <SignalIcon signal={signal.signal} size={18} />
                {signal.signal}
              </span>
            )}
          </div>
          <button className="btn-icon" onClick={onClose} aria-label="Close">
            <X size={18} />
          </button>
        </div>

        <div className="drawer-body">

          {loading && (
            <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
              <div className="spinner" />
            </div>
          )}

          {!loading && (
            <>
              {/* Signal Metrics */}
              {signal && (
                <div>
                  <div className="drawer-section-title">Signal Overview</div>
                  <div style={{
                    display: 'grid', gridTemplateColumns: '1fr 1fr 1fr',
                    gap: 12,
                  }}>
                    {[
                      { label: 'Signal',    value: signal.signal || '—',       color: signalColor(signal.signal) },
                      { label: 'Momentum',  value: fmtMomentum(signal.momentum), color: parseFloat(signal.momentum || 0) >= 0 ? 'var(--signal-buy)' : 'var(--signal-sell)' },
                      { label: 'Sentiment', value: signal.sentiment_score !== null ? parseFloat(signal.sentiment_score).toFixed(3) : '—', color: 'var(--text-primary)' },
                    ].map(({ label, value, color }) => (
                      <div key={label} style={{
                        background: 'var(--bg-card)',
                        border: '1px solid var(--border-color)',
                        borderRadius: 12,
                        padding: '14px 16px',
                      }}>
                        <div className="metric-label" style={{ marginBottom: 6 }}>{label}</div>
                        <div style={{ fontSize: 16, fontWeight: 800, color, fontFamily: "'JetBrains Mono', monospace" }}>
                          {value}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 8, fontFamily: 'monospace' }}>
                    Generated: {fmtDate(signal.generated_at)} · Window: {hours}h
                  </div>
                </div>
              )}

              {/* Price Chart */}
              <div>
                <div className="drawer-section-title">Price History</div>
                <PriceChart data={prices} />
              </div>

              {/* Sentiment Chart */}
              <div>
                <div className="drawer-section-title">Sentiment Trend</div>
                <SentimentChart data={sentiments} />
              </div>

              {/* News */}
              <div>
                <div className="drawer-section-title">Latest News ({news.length})</div>
                {news.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No news articles found.</p>
                ) : (
                  <div className="news-list">
                    {news.map((article, i) => (
                      <div key={i} className="news-item">
                        <div className="news-item-top">
                          <SentimentBadge label={article.sentiment_label} />
                          <div
                            onClick={() => setSelectedArticle(article)}
                            className="news-item-title"
                            style={{ cursor: 'pointer' }}
                          >
                            {article.article_title
                              ? (article.article_title.length > 90
                                  ? article.article_title.slice(0, 90) + '…'
                                  : article.article_title)
                              : 'Untitled article'
                            }
                          </div>
                          <ExternalLink size={12} style={{ flexShrink: 0, color: 'var(--text-muted)' }} />
                        </div>
                        <div className="news-item-meta">
                          <span>{fmtDate(article.published_at)}</span>
                          {article.sentiment_score !== null && article.sentiment_score !== undefined && (
                            <span style={{ fontFamily: 'monospace' }}>
                              {(parseFloat(article.sentiment_score) * 100).toFixed(0)}% confidence
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}

        </div>
      </div>

      {/* BIG CARD MODAL */}
      {selectedArticle && (
        <div 
          style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            backdropFilter: 'blur(8px)',
            zIndex: 10000, // Higher than the drawer (which is typically ~300)
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            padding: 24
          }}
          onClick={() => setSelectedArticle(null)}
        >
          <div 
            className="glass-card"
            style={{
              width: '100%', maxWidth: 700, maxHeight: '90vh',
              overflowY: 'auto',
              padding: 32, borderRadius: 20,
              display: 'flex', flexDirection: 'column', gap: 24,
              backgroundColor: 'var(--bg-surface)',
              position: 'relative'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              className="btn-icon" 
              onClick={() => setSelectedArticle(null)}
              style={{ position: 'absolute', top: 24, right: 24 }}
            >
              <X size={24} />
            </button>

            {/* Header info */}
            <div style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap', paddingRight: 40 }}>
              <span style={{ 
                fontSize: 16, fontWeight: 800, fontFamily: 'monospace',
                color: 'var(--accent)', background: 'var(--accent-dim)',
                padding: '6px 12px', borderRadius: 8, border: '1px solid var(--border-color)'
              }}>
                {ticker}
              </span>
              <SentimentBadge label={selectedArticle.sentiment_label} />
              <span style={{ fontSize: 14, color: 'var(--text-muted)' }}>
                {fmtDate(selectedArticle.published_at)}
              </span>
            </div>

            {/* Title */}
            <h2 style={{ fontSize: 24, fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.4, margin: 0 }}>
              {selectedArticle.article_title || 'Untitled Article'}
            </h2>

            {/* Description & Content */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {selectedArticle.article_description && (
                <p style={{ fontSize: 16, color: 'var(--text-primary)', lineHeight: 1.7, margin: 0, fontWeight: 500 }}>
                  {selectedArticle.article_description}
                </p>
              )}
              {selectedArticle.content && (
                <div style={{ 
                  padding: 20, background: 'var(--bg-card)', 
                  borderRadius: 12, border: '1px solid var(--border-color)' 
                }}>
                  <p style={{ fontSize: 15, color: 'var(--text-secondary)', lineHeight: 1.7, margin: 0 }}>
                    {selectedArticle.content}
                  </p>
                  <p style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 16, fontStyle: 'italic' }}>
                    Note: Content is truncated by the News API.
                  </p>
                </div>
              )}
            </div>

            {/* Footer action */}
            <div style={{ marginTop: 8, paddingTop: 24, borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'flex-end' }}>
              <a 
                href={sanitizeUrl(selectedArticle.article_url)} 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn-primary"
                style={{ padding: '12px 24px', fontSize: 15 }}
              >
                Read Full Article on Source <ExternalLink size={16} style={{ marginLeft: 8, display: 'inline' }} />
              </a>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
