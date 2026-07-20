import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts'
import { BarChart2 } from 'lucide-react'

/** Formats an ISO timestamp to HH:MM */
function fmtTime(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit', hour12: false,
  })
}

/** Custom Recharts tooltip */
function PriceTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border-color)',
      borderRadius: 10,
      padding: '10px 14px',
      fontSize: 12,
    }}>
      <div style={{ color: 'var(--text-muted)', marginBottom: 6 }}>{label}</div>
      <div style={{ color: 'var(--accent)', fontWeight: 700 }}>
        Close: ${parseFloat(d.price_close || 0).toFixed(2)}
      </div>
      {d.price_open && (
        <div style={{ color: 'var(--text-secondary)', marginTop: 4 }}>
          O: ${parseFloat(d.price_open).toFixed(2)} &nbsp;
          H: ${parseFloat(d.price_high).toFixed(2)} &nbsp;
          L: ${parseFloat(d.price_low).toFixed(2)}
        </div>
      )}
    </div>
  )
}

/**
 * PriceChart — Recharts line chart for OHLCV close prices.
 *
 * Props:
 *   data {Array} — array of price tick objects from /prices/{ticker}
 */
export default function PriceChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="empty-state" style={{ padding: '32px 0' }}>
        <BarChart2 size={32} className="empty-state-icon" />
        <span className="empty-state-title">No price data</span>
        <span className="empty-state-desc">No ticks found in the selected window.</span>
      </div>
    )
  }

  // Prepare: format timestamps and cast price to float
  const chartData = data.map(d => ({
    ...d,
    time: fmtTime(d.stock_date_time),
    price_close: parseFloat(d.price_close),
    price_open: d.price_open ? parseFloat(d.price_open) : undefined,
    price_high: d.price_high ? parseFloat(d.price_high) : undefined,
    price_low:  d.price_low  ? parseFloat(d.price_low)  : undefined,
  }))

  const prices = chartData.map(d => d.price_close)
  const minP = Math.min(...prices) * 0.998
  const maxP = Math.max(...prices) * 1.002

  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData} margin={{ top: 6, right: 8, bottom: 0, left: 0 }}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border-color)"
            vertical={false}
          />
          <XAxis
            dataKey="time"
            tick={{ fill: 'var(--text-muted)', fontSize: 10 }}
            tickLine={false}
            axisLine={false}
            interval="preserveStartEnd"
          />
          <YAxis
            domain={[minP, maxP]}
            tick={{ fill: 'var(--text-muted)', fontSize: 10 }}
            tickLine={false}
            axisLine={false}
            tickFormatter={v => `$${v.toFixed(0)}`}
            width={52}
          />
          <Tooltip content={<PriceTooltip />} />
          <Line
            type="monotone"
            dataKey="price_close"
            stroke="var(--accent)"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: 'var(--accent)', strokeWidth: 0 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
