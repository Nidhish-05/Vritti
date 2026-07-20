import { TrendingUp, TrendingDown, Minus, ChevronRight } from 'lucide-react'
import { useTilt } from '../hooks/useTilt'

/** Returns CSS class, color, arrow icon, and display text for a signal */
function getSignalMeta(signal) {
  switch (signal) {
    case 'BUY':
      return {
        cardClass: 'signal-card-buy',
        color: 'var(--signal-buy)',
        Icon: TrendingUp,
        text: 'BUY',
      }
    case 'SELL':
      return {
        cardClass: 'signal-card-sell',
        color: 'var(--signal-sell)',
        Icon: TrendingDown,
        text: 'SELL',
      }
    case 'HOLD':
      return {
        cardClass: 'signal-card-hold',
        color: 'var(--signal-hold)',
        Icon: Minus,
        text: 'HOLD',
      }
    default:
      return {
        cardClass: 'signal-card-none',
        color: 'var(--text-muted)',
        Icon: Minus,
        text: 'N/A',
      }
  }
}

/** Formats momentum as "+4.32%" */
function formatMomentum(val) {
  if (val === null || val === undefined) return '—'
  const pct = (parseFloat(val) * 100).toFixed(2)
  return parseFloat(pct) >= 0 ? `+${pct}%` : `${pct}%`
}

/** Formats a UTC ISO timestamp as a short local time string */
function formatTime(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('en-IN', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

/**
 * SignalCard — Displays the current trading signal for one ticker.
 *
 * Props:
 *   data      {object}   — signal record from /signals/all or /signals/{ticker}
 *   onClick   {function} — called when the card is clicked (opens the drawer)
 */
export default function SignalCard({ data, onClick }) {
  const { ref, onMouseMove, onMouseLeave } = useTilt({ maxRotate: 10, scale: 1.05, perspective: 700 })

  if (!data) return null

  const { cardClass, color, Icon, text } = getSignalMeta(data.signal)
  const momentum = formatMomentum(data.momentum)
  const momentumNum = data.momentum ? parseFloat(data.momentum) : 0
  const momentumColor = momentumNum > 0
    ? 'var(--signal-buy)'
    : momentumNum < 0
      ? 'var(--signal-sell)'
      : 'var(--text-muted)'

  return (
    <div className="signal-card-wrapper">
      <div
        ref={ref}
        className={`signal-card ${cardClass}`}
        onClick={onClick}
        onMouseMove={onMouseMove}
        onMouseLeave={onMouseLeave}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && onClick?.()}
        aria-label={`${data.ticker}: ${text} signal. Click to view details.`}
      >
        {/* Specular shine overlay — follows cursor via CSS vars set in useTilt */}
        <div className="card-shine" aria-hidden="true" />

        {/* Ticker label — pops up 20px */}
        <div className="signal-card-ticker" style={{ transform: 'translateZ(20px)' }}>{data.ticker}</div>

        {/* Signal + icon — pops up 45px (highest) */}
        <div className="signal-card-signal" style={{ transform: 'translateZ(45px)' }}>
          <Icon size={28} color={color} strokeWidth={2.5} style={{ filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.15))' }} />
          <span style={{ color, filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.15))' }}>{text}</span>
        </div>

        {/* Metrics row — pops up 30px */}
        <div className="signal-card-metrics" style={{ transform: 'translateZ(30px)' }}>
          <div className="metric-item">
            <span className="metric-label">Momentum</span>
            <span className="metric-value" style={{ color: momentumColor }}>
              {momentum}
            </span>
          </div>

          {data.sentiment_score !== null && data.sentiment_score !== undefined && (
            <div className="metric-item">
              <span className="metric-label">Sentiment</span>
              <span className="metric-value">
                {parseFloat(data.sentiment_score).toFixed(2)}
              </span>
            </div>
          )}
        </div>

        {/* Footer — stays close to background (10px) */}
        <div className="signal-card-footer" style={{ transform: 'translateZ(10px)' }}>
          <span>{formatTime(data.generated_at)}</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--accent)' }}>
            Details <ChevronRight size={13} />
          </span>
        </div>
      </div>
    </div>
  )
}
