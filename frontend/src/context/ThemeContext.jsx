import { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext(null)

/**
 * ThemeProvider — Wraps the app and provides dark/light theme state.
 * Persists the user's preference to localStorage.
 * Applies `data-theme` attribute on <html> so CSS variables switch automatically.
 */
export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    // Read saved preference, default to dark
    return localStorage.getItem('vritti-theme') || 'dark'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('vritti-theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme(t => (t === 'dark' ? 'light' : 'dark'))

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

/**
 * useTheme — Hook for any component that needs the current theme or toggle.
 * Usage: const { theme, toggleTheme } = useTheme()
 */
export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used inside <ThemeProvider>')
  return ctx
}
