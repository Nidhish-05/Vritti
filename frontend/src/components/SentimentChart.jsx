import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts'
import { Activity } from 'lucide-react'

function fmtDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false,
  })
}

function SentimentTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border-color)',
      borderRadius: 10,
      padding: '10px 14px',
      fontSize: 12,
      maxWidth: 240,
    }}>
      <div style={{ color: 'var(--text-muted)', marginBottom: 4 }}>
        {fmtDate(d.published_at)}
      </div>
      <div style={{ color: 'var(--signal-buy)', fontWeight: 700 }}>
        Score: {parseFloat(d.sentiment_score).toFixed(3)}
      </div>
      {d.title && (
        <div style={{
          color: 'var(--text-secondary)', marginTop: 6,
          whiteSpace: 'normal', lineHeight: 1.4,
        }}>
          {d.title.slice(0, 80)}{d.title.length > 80 ? '…' : ''}
        </div>
      )}
    </div>
  )
}

/**
 * SentimentChart — Recharts AreaChart for rolling FinBERT sentiment scores.
 *
 * Props:
 *   data {Array} — array of news sentiment records from /sentiment/history
 */
export default function SentimentChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="empty-state" style={{ padding: '32px 0' }}>
        <Activity size={32} className="empty-state-icon" />
        <span className="empty-state-title">No sentiment data</span>
        <span className="empty-state-desc">No classified articles in this window.</span>
      </div>
    )
  }

  const chartData = data
    .filter(d => d.sentiment_score !== null)
    .map(d => ({
      ...d,
      label: fmtDate(d.published_at),
      sentiment_score: parseFloat(d.sentiment_score),
    }))
    // Reverse so oldest is on the left
    .reverse()

  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={180}>
        <AreaChart data={chartData} margin={{ top: 6, right: 8, bottom: 0, left: 0 }}>
          <defs>
            <linearGradient id="sentGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="var(--signal-buy)" stopOpacity={0.35} />
              <stop offset="95%" stopColor="var(--signal-buy)" stopOpacity={0.02} />
            </linearGradient>
          </defs>

          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border-color)"
            vertical={false}
          />
          <XAxis
            dataKey="label"
            tick={{ fill: 'var(--text-muted)', fontSize: 9 }}
            tickLine={false}
            axisLine={false}
            interval="preserveStartEnd"
          />
          <YAxis
            domain={[0, 1]}
            tick={{ fill: 'var(--text-muted)', fontSize: 10 }}
            tickLine={false}
            axisLine={false}
            tickFormatter={v => v.toFixed(1)}
            width={30}
          />
          <Tooltip content={<SentimentTooltip />} />
          <Area
            type="monotone"
            dataKey="sentiment_score"
            stroke="var(--signal-buy)"
            strokeWidth={2}
            fill="url(#sentGrad)"
            dot={false}
            activeDot={{ r: 4, fill: 'var(--signal-buy)', strokeWidth: 0 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
