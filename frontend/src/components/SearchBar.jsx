import { useState, useRef, useEffect } from 'react'
import { Search, X } from 'lucide-react'
import { sanitizeTicker } from '../utils/security'

/**
 * SearchBar — Ticker search input with sanitization and keyboard support.
 *
 * Props:
 *   onSearch    {function} — called with the sanitized ticker string on submit
 *   placeholder {string}  — input placeholder text
 */
export default function SearchBar({ onSearch, placeholder = 'Search ticker… e.g. AAPL' }) {
  const [value, setValue] = useState('')
  const inputRef = useRef(null)

  // Keyboard shortcut: "/" focuses the search bar
  useEffect(() => {
    const handler = (e) => {
      if (e.key === '/' && document.activeElement !== inputRef.current) {
        e.preventDefault()
        inputRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [])

  const handleChange = (e) => {
    const sanitized = sanitizeTicker(e.target.value)
    setValue(sanitized)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const ticker = value.trim()
    if (ticker.length > 0) {
      onSearch(ticker)
    }
  }

  const handleClear = () => {
    setValue('')
    inputRef.current?.focus()
    onSearch('')
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 10 }}>
      <div className="search-wrapper">
        {/* Icon inside input */}
        <Search size={17} className="search-icon" />

        <input
          ref={inputRef}
          type="text"
          className="search-input"
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          maxLength={5}
          autoComplete="off"
          spellCheck={false}
          aria-label="Search for a stock ticker"
        />

        {/* Clear button */}
        {value && (
          <button
            type="button"
            className="search-clear"
            onClick={handleClear}
            aria-label="Clear search"
          >
            <X size={14} />
          </button>
        )}
      </div>

      <button type="submit" className="btn-primary" style={{ flexShrink: 0, height: 48 }}>
        Search
      </button>
    </form>
  )
}
