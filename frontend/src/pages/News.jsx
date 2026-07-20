import { useEffect, useState } from 'react'
import { Newspaper, ExternalLink, RefreshCw, AlertCircle } from 'lucide-react'
import { fetchLatestNews } from '../api/client'
import { sanitizeUrl } from '../utils/security'

/** Sentiment badge for news items */
function SentimentBadge({ label, score }) {
  const cls =
    label === 'positive' ? 'badge badge-positive' :
    label === 'negative' ? 'badge badge-negative' :
    'badge badge-neutral'

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <span className={cls}>{label || 'unscored'}</span>
      {score !== null && score !== undefined && (
        <span style={{ fontSize: 11, fontFamily: 'monospace', color: 'var(--text-muted)' }}>
          {(parseFloat(score) * 100).toFixed(0)}% conf
        </span>
      )}
    </div>
  )
}

/** Formats ISO date as a readable local datetime */
function fmtDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('en-IN', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

export default function News() {
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const loadNews = async () => {
    setLoading(true)
    setError(null)
    const data = await fetchLatestNews(null, 50) // Fetch top 50 latest globally
    if (data) {
      setNews(data)
      setLastUpdated(new Date())
    } else {
      setError('Unable to reach the server to fetch news.')
    }
    setLoading(false)
  }

  useEffect(() => {
    document.title = 'Vritti — Market News'
    loadNews()
  }, [])

  const lastUpdatedStr = lastUpdated
    ? lastUpdated.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })
    : null

  return (
    <main className="main-content page-enter">
      <section style={{ maxWidth: 1000, margin: '0 auto', padding: '40px 24px 60px' }}>
        
        {/* Header */}
        <div style={{ marginBottom: 40, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <Newspaper size={28} color="var(--accent)" />
              <h1 style={{ fontSize: 32, fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.5px' }}>
                Market News Feed
              </h1>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: 15, maxWidth: 500 }}>
              Live FinBERT sentiment analysis of the latest financial articles across all tracked assets.
            </p>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            {lastUpdatedStr && (
              <span style={{ fontSize: 12, color: 'var(--text-muted)', fontFamily: 'monospace' }}>
                Updated {lastUpdatedStr}
              </span>
            )}
            <button className="btn-icon" onClick={loadNews} aria-label="Refresh news feed" disabled={loading}>
              <RefreshCw size={16} className={loading ? "spin" : ""} />
            </button>
          </div>
        </div>

        {/* Loading State */}
        {loading && news.length === 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {[...Array(6)].map((_, i) => (
              <div key={i} className="glass-card" style={{ padding: 20, borderRadius: 12 }}>
                <div className="skeleton" style={{ height: 18, width: '80%', marginBottom: 12 }} />
                <div className="skeleton" style={{ height: 14, width: '40%', marginBottom: 16 }} />
                <div style={{ display: 'flex', gap: 12 }}>
                  <div className="skeleton" style={{ height: 24, width: 70, borderRadius: 12 }} />
                  <div className="skeleton" style={{ height: 24, width: 50, borderRadius: 12 }} />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="empty-state">
            <AlertCircle size={40} className="empty-state-icon" />
            <span className="empty-state-title">Unable to load news</span>
            <span className="empty-state-desc">{error}</span>
            <button className="btn-secondary" onClick={loadNews} style={{ marginTop: 8 }}>
              Try again
            </button>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && news.length === 0 && (
          <div className="empty-state">
            <Newspaper size={40} className="empty-state-icon" />
            <span className="empty-state-title">No news articles found</span>
            <span className="empty-state-desc">The ingestion pipeline hasn't collected any articles yet.</span>
          </div>
        )}

        {/* News Feed */}
        {!loading && news.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {news.map((article, index) => (
              <a
                key={article.id || index}
                href={sanitizeUrl(article.article_url)}
                target="_blank"
                rel="noopener noreferrer"
                className="glass-card news-item-hover"
                style={{
                  display: 'flex', flexDirection: 'column', gap: 12,
                  padding: 24, borderRadius: 16, textDecoration: 'none',
                  transition: 'transform 0.2s, box-shadow 0.2s, border-color 0.2s',
                  animation: `fade-in 0.4s ease both ${index * 30}ms`
                }}
              >
                {/* Top row: Ticker + Sentiment */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{ 
                      fontSize: 14, fontWeight: 800, fontFamily: 'monospace',
                      color: 'var(--text-primary)', background: 'var(--bg-input)',
                      padding: '4px 10px', borderRadius: 6, border: '1px solid var(--border-color)'
                    }}>
                      {article.ticker}
                    </span>
                    <SentimentBadge label={article.sentiment_label} score={article.sentiment_score} />
                  </div>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                    {fmtDate(article.published_at)}
                  </span>
                </div>

                {/* Title */}
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                  <h3 style={{ 
                    fontSize: 16, fontWeight: 600, color: 'var(--text-primary)', 
                    lineHeight: 1.5, margin: 0, flex: 1
                  }}>
                    {article.title || 'Untitled Article'}
                  </h3>
                  <ExternalLink size={16} style={{ color: 'var(--text-muted)', flexShrink: 0, marginTop: 4 }} />
                </div>
                
                {/* Summary (if available) */}
                {article.summary && (
                  <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
                    {article.summary}
                  </p>
                )}
              </a>
            ))}
          </div>
        )}

      </section>
    </main>
  )
}
