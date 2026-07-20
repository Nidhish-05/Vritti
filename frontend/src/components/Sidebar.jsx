/**
 * Sidebar.jsx — Left navigation panel with ticker search and time window selector.
 *
 * Props:
 *   selectedTicker  {string}    — currently selected ticker (e.g. "TSLA")
 *   onTickerChange  {function}  — callback called with the new ticker string when user selects one
 *   selectedHours   {number}    — currently selected time window in hours
 *   onHoursChange   {function}  — callback called with the new hours value
 *   allSignals      {Array}     — array of signal objects for all watchlist tickers
 *
 * TODO Steps:
 *
 * 1. Render a vertical sidebar container with a dark background.
 *    Give it a fixed width, full height, and a right border.
 *
 * 2. At the top, render the app name "Vritti" as a logo/title
 *    with an optional small subtitle like "Market Intelligence".
 *
 * 3. Below the logo, render a text input for ticker search.
 *    - When the user types and hits Enter (or clicks a search button),
 *      call onTickerChange with the uppercased input value.
 *    - Clear the input after selecting.
 *
 * 4. Below the search, render three time window quick-select buttons:
 *    - "24h"  → calls onHoursChange(24)
 *    - "48h"  → calls onHoursChange(48)
 *    - "7d"   → calls onHoursChange(168)
 *    Highlight the currently selected button using a different background color.
 *
 * 5. Below the buttons, render a "Watchlist" heading.
 *
 * 6. For each item in the allSignals array, render a mini row showing:
 *    - The ticker symbol in bold
 *    - A small colored dot indicating the signal:
 *      green for BUY, red for SELL, yellow for HOLD, gray for unknown
 *    - Clicking the row calls onTickerChange with that ticker's symbol.
 *    - Highlight the row that matches the selectedTicker.
 */
export default function Sidebar({
  selectedTicker,
  onTickerChange,
  selectedHours,
  onHoursChange,
  allSignals,
}) {
  // Write your component here
}
