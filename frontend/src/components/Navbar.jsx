import { useState } from 'react'
import { NavLink, Link } from 'react-router-dom'
import { Sun, Moon, Menu, X, TrendingUp } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

/**
 * Navbar — Fixed top navigation bar with glassmorphism effect.
 * Features: logo, nav links with active highlighting, theme toggle, mobile hamburger.
 */
export default function Navbar() {
  const { theme, toggleTheme } = useTheme()
  const [menuOpen, setMenuOpen] = useState(false)

  const closeMenu = () => setMenuOpen(false)

  const navLinks = [
    { to: '/',      label: 'Market' },
    { to: '/news',  label: 'News' },
    { to: '/about', label: 'About' },
  ]

  return (
    <>
      <nav className="navbar">
        <div className="navbar-inner">

          {/* Logo */}
          <Link to="/" className="navbar-logo" onClick={closeMenu}>
            <img src="/logo1.jpg" alt="Vritti Logo" />
            <span className="navbar-logo-text">
              V<span>ritti</span>
            </span>
          </Link>

          {/* Desktop Nav Links */}
          <div className="navbar-links">
            {navLinks.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `nav-link${isActive ? ' active' : ''}`
                }
              >
                {label}
              </NavLink>
            ))}
          </div>

          {/* Actions */}
          <div className="navbar-actions">
            {/* Theme Toggle */}
            <button
              className="btn-icon"
              onClick={toggleTheme}
              title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              aria-label="Toggle theme"
            >
              {theme === 'dark'
                ? <Sun size={18} strokeWidth={2} />
                : <Moon size={18} strokeWidth={2} />
              }
            </button>

            {/* Hamburger (mobile only) */}
            <button
              className="btn-icon hamburger"
              onClick={() => setMenuOpen(o => !o)}
              aria-label="Toggle menu"
            >
              {menuOpen
                ? <X size={20} strokeWidth={2} />
                : <Menu size={20} strokeWidth={2} />
              }
            </button>
          </div>

        </div>
      </nav>

      {/* Mobile Dropdown Menu */}
      <div className={`mobile-menu${menuOpen ? ' open' : ''}`}>
        {navLinks.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `mobile-nav-link${isActive ? ' active' : ''}`
            }
            onClick={closeMenu}
          >
            {label}
          </NavLink>
        ))}
      </div>
    </>
  )
}
