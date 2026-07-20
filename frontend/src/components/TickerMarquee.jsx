import { useState, useEffect } from 'react'
import { TrendingUp, TrendingDown, Minus, Radio } from 'lucide-react'
import { fetchAllSignals } from '../api/client'

/** Formats a momentum value (e.g. 0.043) as "+4.30%" */
function formatMomentum(val) {
  if (val === null || val === undefined) return '—'
  const pct = (parseFloat(val) * 100).toFixed(2)
  return pct >= 0 ? `+${pct}%` : `${pct}%`
}

/** Returns the CSS class and arrow icon for a given signal */
function signalMeta(signal) {
  switch (signal) {
    case 'BUY':
      return { cls: 'marquee-signal-buy',  Icon: TrendingUp,   label: '▲ BUY' }
    case 'SELL':
      return { cls: 'marquee-signal-sell', Icon: TrendingDown, label: '▼ SELL' }
    case 'HOLD':
      return { cls: 'marquee-signal-hold', Icon: Minus,        label: '— HOLD' }
    default:
      return { cls: 'marquee-signal-none', Icon: null,         label: '—' }
  }
}

/**
 * TickerMarquee — Fixed bottom strip showing live BUY/SELL/HOLD signals for all tickers.
 * - Fetches /signals/all on mount and refreshes every 30 seconds.
 * - Duplicates the item list to create a seamless infinite loop.
 * - Pauses on hover.
 */
export default function TickerMarquee() {
  const [signals, setSignals] = useState([])

  const load = async () => {
    const data = await fetchAllSignals()
    if (data && data.length > 0) setSignals(data)
  }

  useEffect(() => {
    load()
    const interval = setInterval(load, 30_000)
    return () => clearInterval(interval)
  }, [])

  // Need at least one item to render
  if (signals.length === 0) {
    return (
      <div className="marquee-wrapper">
        <span className="marquee-label">
          <Radio size={10} style={{ marginRight: 6 }} />LIVE
        </span>
        <div style={{ padding: '0 20px', fontSize: 12, color: 'var(--text-muted)' }}>
          Connecting to market data…
        </div>
      </div>
    )
  }

  // Duplicate items for seamless loop (CSS animation scrolls -50%)
  const items = [...signals, ...signals]

  return (
    <div className="marquee-wrapper" role="marquee" aria-label="Live market signals">
      <span className="marquee-label">
        <Radio size={10} style={{ marginRight: 6 }} />LIVE
      </span>

      <div className="marquee-track-wrapper">
        <div className="marquee-track">
          {items.map((s, i) => {
            const { cls, Icon, label } = signalMeta(s.signal)
            const momentum = formatMomentum(s.momentum)
            return (
              <span key={i} className="marquee-item" title={`${s.ticker}: ${s.signal}`}>
                <span className="marquee-ticker">{s.ticker}</span>
                <span className={cls}>
                  {Icon && (
                    <Icon
                      size={11}
                      strokeWidth={2.5}
                      style={{ display: 'inline', verticalAlign: 'middle', marginRight: 2 }}
                    />
                  )}
                  {s.signal || '—'}
                </span>
                <span className="marquee-momentum">{momentum}</span>
              </span>
            )
          })}
        </div>
      </div>
    </div>
  )
}
