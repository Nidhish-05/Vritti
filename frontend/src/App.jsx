import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Navbar from './components/Navbar'
import TickerMarquee from './components/TickerMarquee'
import Home from './pages/Home'
import News from './pages/News'
import About from './pages/About'

/**
 * App — Root component.
 * Wraps the entire tree with ThemeProvider (dark/light mode context)
 * and BrowserRouter (client-side routing).
 *
 * Layout:
 *   <Navbar />        — fixed top (64px)
 *   <Routes>          — page content fills the middle
 *   <TickerMarquee /> — fixed bottom (36px)
 */
export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Navbar />

        <Routes>
          <Route path="/"      element={<Home />}  />
          <Route path="/news"  element={<News />}  />
          <Route path="/about" element={<About />} />
          {/* Catch-all: redirect unknown routes to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        <TickerMarquee />
      </BrowserRouter>
    </ThemeProvider>
  )
}
