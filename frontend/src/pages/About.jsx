import { useEffect } from 'react'
import {
  Database, Server, Layout, Cpu,
  ArrowRight, ShieldCheck, Zap, Activity
} from 'lucide-react'

/* Inline SVGs for social icons (lucide-react v1.x removed brand icons) */
const GithubIcon = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
  </svg>
)

const LinkedinIcon = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
  </svg>
)

export default function About() {
  useEffect(() => {
    document.title = 'Vritti — About & Architecture'
  }, [])

  return (
    <main className="main-content page-enter">
      <section style={{ maxWidth: 1000, margin: '0 auto', padding: '40px 24px 80px' }}>
        
        {/* ── Author Profile ────────────────────────────────────────────── */}
        <div className="glass-card" style={{ 
          padding: '40px 48px', 
          borderRadius: 24, 
          marginBottom: 60,
          position: 'relative',
          overflow: 'hidden'
        }}>
          {/* Decorative glow */}
          <div style={{
            position: 'absolute', top: '-50%', right: '-10%',
            width: 300, height: 300, borderRadius: '50%',
            background: 'radial-gradient(circle, var(--accent-dim) 0%, transparent 70%)',
            filter: 'blur(40px)', pointerEvents: 'none',
          }} />

          <div style={{ display: 'flex', gap: 40, flexWrap: 'wrap', alignItems: 'center' }}>
            {/* Profile Picture */}
            <div style={{
              width: 140, height: 140, borderRadius: '50%',
              padding: 4, background: 'var(--bg-surface)',
              border: '1px solid var(--border-color)',
              boxShadow: 'var(--shadow-elevated)',
              flexShrink: 0
            }}>
              <img 
                src="/pfp.png" 
                alt="Nidhish Bansal" 
                style={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E";
                  e.target.style.padding = '20px';
                  e.target.style.opacity = '0.5';
                }}
              />
            </div>

            {/* Details */}
            <div style={{ flex: 1, minWidth: 280 }}>
              <h1 style={{ fontSize: 32, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 8, letterSpacing: '-0.5px' }}>
                Nidhish Bansal
              </h1>
              <p style={{ fontSize: 16, color: 'var(--accent)', fontWeight: 600, marginBottom: 12 }}>
                Data Science & ML Enthusiast
              </p>
              <p style={{ fontSize: 15, color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: 24, maxWidth: 500 }}>
                4th-year Computer Science and Technology student at Maharaja Agrasen Institute of Technology (2023-2027). Building things that turn raw data into decisions.
              </p>
              
              <div style={{ display: 'flex', gap: 16 }}>
                <a
                  href="https://www.github.com/Nidhish-05"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary"
                  style={{ padding: '10px 20px', borderRadius: 12, gap: 8 }}
                >
                  <GithubIcon size={18} />
                  GitHub
                </a>
                <a
                  href="https://www.linkedin.com/in/nidhish-bansal-906a83298/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary"
                  style={{ padding: '10px 20px', borderRadius: 12, gap: 8 }}
                >
                  <LinkedinIcon size={18} />
                  LinkedIn
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* ── Project Architecture ──────────────────────────────────────── */}
        <div style={{ marginBottom: 40 }}>
          <h2 style={{ fontSize: 28, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 12, letterSpacing: '-0.5px' }}>
            System Architecture
          </h2>
          <p style={{ fontSize: 16, color: 'var(--text-secondary)', maxWidth: 600, lineHeight: 1.6 }}>
            Vritti is a flagship end-to-end data pipeline combining real-time financial news ingestion, natural language processing, and technical momentum indicators.
          </p>
        </div>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 24,
          marginBottom: 60 
        }}>
          {/* Frontend */}
          <div className="glass-card" style={{ padding: 32, borderRadius: 20 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
              <div style={{ padding: 10, background: 'var(--bg-input)', borderRadius: 12, border: '1px solid var(--border-color)' }}>
                <Layout size={24} color="var(--accent)" />
              </div>
              <h3 style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)' }}>Client Layer</h3>
            </div>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 12 }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <ShieldCheck size={16} color="var(--signal-buy)" /> React + Vite SPA
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <ShieldCheck size={16} color="var(--signal-buy)" /> Vanilla CSS Design System
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <ShieldCheck size={16} color="var(--signal-buy)" /> 3D Floating UI Mechanics
              </li>
            </ul>
          </div>

          {/* Backend */}
          <div className="glass-card" style={{ padding: 32, borderRadius: 20 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
              <div style={{ padding: 10, background: 'var(--bg-input)', borderRadius: 12, border: '1px solid var(--border-color)' }}>
                <Server size={24} color="var(--accent)" />
              </div>
              <h3 style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)' }}>API & Logic Layer</h3>
            </div>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 12 }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <Zap size={16} color="var(--signal-hold)" /> FastAPI (Python 3.11)
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <Zap size={16} color="var(--signal-hold)" /> Asyncpg connection pooling
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <Zap size={16} color="var(--signal-hold)" /> RESTful JSON Endpoints
              </li>
            </ul>
          </div>

          {/* ML & DB */}
          <div className="glass-card" style={{ padding: 32, borderRadius: 20 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
              <div style={{ padding: 10, background: 'var(--bg-input)', borderRadius: 12, border: '1px solid var(--border-color)' }}>
                <Database size={24} color="var(--accent)" />
              </div>
              <h3 style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)' }}>Data & ML Pipeline</h3>
            </div>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 12 }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <Activity size={16} color="var(--signal-sell)" /> PostgreSQL via Docker
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <Activity size={16} color="var(--signal-sell)" /> FinBERT Sentiment Scoring
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, color: 'var(--text-secondary)' }}>
                <Activity size={16} color="var(--signal-sell)" /> Price Momentum Engine
              </li>
            </ul>
          </div>
        </div>

        {/* ── Data Flow Diagram ─────────────────────────────────────────── */}
        <div className="glass-card" style={{ padding: '40px', borderRadius: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
            <Cpu size={24} color="var(--text-primary)" />
            <h3 style={{ fontSize: 20, fontWeight: 700, color: 'var(--text-primary)' }}>Pipeline Flow</h3>
          </div>
          
          <div style={{ 
            display: 'flex', flexDirection: 'column', gap: 16,
            background: 'var(--bg-input)', border: '1px solid var(--border-color)', 
            padding: 24, borderRadius: 16 
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, color: 'var(--text-secondary)', fontSize: 14 }}>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)', width: 80 }}>Step 1</div>
              <ArrowRight size={16} style={{ opacity: 0.5 }} />
              <div>Data Ingestion scripts pull financial news and price ticks from APIs into Postgres.</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, color: 'var(--text-secondary)', fontSize: 14 }}>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)', width: 80 }}>Step 2</div>
              <ArrowRight size={16} style={{ opacity: 0.5 }} />
              <div>FinBERT processes raw text. NLP model assigns positive/negative/neutral labels with confidence scores.</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, color: 'var(--text-secondary)', fontSize: 14 }}>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)', width: 80 }}>Step 3</div>
              <ArrowRight size={16} style={{ opacity: 0.5 }} />
              <div>Signal Generator calculates technical momentum and combines it with sentiment for a unified BUY/HOLD/SELL verdict.</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, color: 'var(--text-secondary)', fontSize: 14 }}>
              <div style={{ fontWeight: 600, color: 'var(--accent)', width: 80 }}>Step 4</div>
              <ArrowRight size={16} color="var(--accent)" />
              <div style={{ color: 'var(--text-primary)', fontWeight: 500 }}>FastAPI serves the synthesized records to the React dashboard in real-time.</div>
            </div>
          </div>
        </div>

      </section>
    </main>
  )
}
