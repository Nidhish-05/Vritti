/**
 * security.js — Client-side input sanitization utilities.
 * Prevents XSS and injection attacks on all user-controlled inputs.
 */

/**
 * Sanitizes a stock ticker input.
 * - Strips all non-alphabetic characters
 * - Converts to uppercase
 * - Truncates to 5 characters max (longest valid US ticker)
 *
 * @param {string} raw - Raw user input
 * @returns {string} Sanitized ticker string
 */
export function sanitizeTicker(raw) {
  if (typeof raw !== 'string') return ''
  return raw
    .replace(/[^a-zA-Z]/g, '')  // only letters
    .toUpperCase()
    .slice(0, 5)
}

/**
 * Sanitizes generic display text.
 * - Strips HTML tags to prevent XSS when displaying user content
 * - Trims whitespace
 * - Truncates to a safe max length
 *
 * @param {string} raw - Raw string
 * @param {number} maxLength - Maximum length (default 500)
 * @returns {string} Safe display string
 */
export function sanitizeText(raw, maxLength = 500) {
  if (typeof raw !== 'string') return ''
  return raw
    .replace(/<[^>]*>/g, '')   // strip HTML tags
    .trim()
    .slice(0, maxLength)
}

/**
 * Validates that a URL is safe to use in an anchor href.
 * Blocks javascript: protocol and data: URLs.
 *
 * @param {string} url - URL string to validate
 * @returns {string} The URL if safe, or '#' fallback
 */
export function sanitizeUrl(url) {
  if (typeof url !== 'string') return '#'
  const lower = url.trim().toLowerCase()
  if (lower.startsWith('javascript:') || lower.startsWith('data:')) return '#'
  return url.trim()
}
