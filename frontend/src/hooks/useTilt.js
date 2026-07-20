import { useRef, useCallback } from 'react'

/**
 * useTilt — 3D card tilt effect that tracks the mouse cursor.
 *
 * Sets rotateX / rotateY on the element based on cursor position relative
 * to the card center. Uses requestAnimationFrame for smooth 60fps updates.
 * Resets smoothly on mouse leave.
 *
 * Options:
 *   maxRotate  {number} — max rotation in degrees (default 12)
 *   scale      {number} — scale factor on hover (default 1.04)
 *   perspective{number} — CSS perspective in px (default 800)
 *
 * Returns: { ref, onMouseMove, onMouseLeave }
 * Attach ref to the element, spread the event handlers on it.
 */
export function useTilt({
  maxRotate  = 12,
  scale      = 1.04,
  perspective = 800,
} = {}) {
  const ref      = useRef(null)
  const frameRef = useRef(null)

  const handleMouseMove = useCallback((e) => {
    if (!ref.current) return

    // Cancel any pending frame to avoid stale updates
    if (frameRef.current) cancelAnimationFrame(frameRef.current)

    frameRef.current = requestAnimationFrame(() => {
      if (!ref.current) return
      const rect = ref.current.getBoundingClientRect()

      // Normalised cursor offset from card centre: -0.5 → +0.5
      const x = (e.clientX - rect.left)  / rect.width  - 0.5
      const y = (e.clientY - rect.top)   / rect.height - 0.5

      const rotateX = -(y * maxRotate)   // cursor at top → top tilts forward
      const rotateY =   x * maxRotate    // cursor at right → right tilts forward

      ref.current.style.transform = `
        perspective(${perspective}px)
        rotateX(${rotateX.toFixed(2)}deg)
        rotateY(${rotateY.toFixed(2)}deg)
        scale(${scale})
      `
      ref.current.style.transition = 'transform 0.08s linear'

      // Drive the CSS specular highlight position (0%–100%)
      ref.current.style.setProperty('--shine-x', `${((x + 0.5) * 100).toFixed(1)}%`)
      ref.current.style.setProperty('--shine-y', `${((y + 0.5) * 100).toFixed(1)}%`)
    })
  }, [maxRotate, scale, perspective])

  const handleMouseLeave = useCallback(() => {
    if (frameRef.current) cancelAnimationFrame(frameRef.current)
    if (!ref.current) return

    // Smooth spring-back to flat
    ref.current.style.transform = `
      perspective(${perspective}px)
      rotateX(0deg)
      rotateY(0deg)
      scale(1)
    `
    ref.current.style.transition = 'transform 0.45s cubic-bezier(0.4, 0, 0.2, 1)'
  }, [perspective])

  return { ref, onMouseMove: handleMouseMove, onMouseLeave: handleMouseLeave }
}
