/**
 * NewsFeed.jsx — Renders a scrollable list of recent news articles
 *                with their FinBERT sentiment labels and scores.
 *
 * Props:
 *   articles {Array} — array of news objects from the API.
 *                      Each object has: title, description, article_url,
 *                      published_at, sentiment_label, sentiment_score.
 *
 * TODO Steps:
 *
 * 1. If the articles prop is empty or null, render a placeholder div
 *    saying "No news available".
 *
 * 2. Render a section with a heading "Latest News".
 *
 * 3. For each article in the array, render a card row containing:
 *
 *    a. A colored sentiment badge on the left:
 *       - "positive" → green background
 *       - "negative" → red background
 *       - "neutral"  → gray background
 *       The badge text should be the sentiment_label capitalized.
 *
 *    b. The article title as a clickable link that opens article_url
 *       in a new browser tab. Truncate titles longer than 90 characters
 *       by slicing and appending "...".
 *
 *    c. The sentiment score as a percentage (e.g. "87%") in muted text.
 *
 *    d. The published_at timestamp formatted as a short date string
 *       (e.g. "Jul 13, 14:30") in muted text on the right.
 *
 * 4. Add a unique 'key' prop to each rendered article row using the
 *    article's index in the array (or article_url if available).
 */
export default function NewsFeed({ articles }) {
  // Write your component here
}
