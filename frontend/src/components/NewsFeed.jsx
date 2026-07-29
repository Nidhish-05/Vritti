import { FileText, ExternalLink } from 'lucide-react'

/** Formats ISO timestamp to short date string like "Jul 13, 14:30" */
function formatNewsDate(isoString) {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
}

/** Truncates text longer than max length */
function truncateText(text, max = 90) {
  if (!text) return ''
  return text.length > max ? text.slice(0, max) + '...' : text
}

export default function NewsFeed({ articles }) {
  if (!articles || articles.length === 0) {
    return (
      <div className="glass-card" style={{ padding: 24, textAlign: 'center' }}>
        <FileText size={32} style={{ color: 'var(--text-muted)', margin: '0 auto 12px' }} />
        <h3 style={{ color: 'var(--text-secondary)' }}>No news available</h3>
        <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>News will appear here once ingested.</p>
      </div>
    )
  }

  return (
    <div className="glass-card" style={{ padding: '24px 0' }}>
      <div style={{ padding: '0 24px', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
        <FileText size={20} style={{ color: 'var(--accent)' }} />
        <h3 style={{ margin: 0, fontWeight: 600 }}>Latest News</h3>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {articles.map((article, idx) => {
          // Format sentiment badge
          let badgeCls = 'badge-hold' // default gray
          let score = null
          
          if (article.sentiment_label) {
            const label = article.sentiment_label.toLowerCase()
            if (label === 'positive') badgeCls = 'badge-buy'
            else if (label === 'negative') badgeCls = 'badge-sell'
          }

          if (article.sentiment_score !== null && article.sentiment_score !== undefined) {
            score = (article.sentiment_score * 100).toFixed(0) + '%'
          }

          return (
            <a
              key={article.article_url || idx}
              href={article.article_url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'grid',
                gridTemplateColumns: 'minmax(70px, max-content) 1fr max-content',
                gap: 16,
                padding: '16px 24px',
                borderBottom: '1px solid var(--border-color)',
                textDecoration: 'none',
                color: 'inherit',
                transition: 'background 0.2s'
              }}
              onMouseOver={(e) => e.currentTarget.style.background = 'var(--accent-dim)'}
              onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
            >
              {/* Left Column: Sentiment Badge & Score */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6, alignItems: 'flex-start' }}>
                {article.sentiment_label ? (
                  <span className={`badge ${badgeCls}`} style={{ fontSize: 11 }}>
                    {article.sentiment_label.toUpperCase()}
                  </span>
                ) : (
                  <span className="badge badge-hold" style={{ fontSize: 11 }}>PENDING</span>
                )}
                {score && <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Score: {score}</span>}
              </div>

              {/* Middle Column: Title & Description */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <h4 style={{ margin: 0, fontSize: 15, fontWeight: 500, lineHeight: 1.4, color: 'var(--text-primary)' }}>
                  <span style={{ color: 'var(--accent)', marginRight: 6, fontWeight: 700 }}>[{article.ticker}]</span>
                  {truncateText(article.article_title, 100)}
                </h4>
                {article.article_description && (
                  <p style={{ margin: 0, fontSize: 13, color: 'var(--text-muted)', lineHeight: 1.5 }}>
                    {truncateText(article.article_description, 140)}
                  </p>
                )}
              </div>

              {/* Right Column: Date & Icon */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 12, color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                  {formatNewsDate(article.published_at)}
                </span>
                <ExternalLink size={14} style={{ color: 'var(--text-muted)', opacity: 0.5 }} />
              </div>
            </a>
          )
        })}
      </div>
    </div>
  )
}
