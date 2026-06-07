// 龍魂全屏 Overlay 层
// DNA: #龍芯⚡️2026-06-04-OVERLAY-COMPONENT-v1.0

import React, { useMemo } from 'react'
import { useOverlayStore } from '../store/overlay'
import '../styles/animations.css'

export const Overlay: React.FC = () => {
  const { color, intensity, isVisible, level } = useOverlayStore()

  const overlayStyle = useMemo(
    () => ({
      position: 'fixed' as const,
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      pointerEvents: 'none' as const,
      zIndex: 999999,
      backgroundColor: `${color}${Math.round(intensity * 255)
        .toString(16)
        .padStart(2, '0')
        .toUpperCase()}`,
      border: `3px solid ${color}`,
      boxShadow: `0 0 ${Math.round(40 * intensity)}px ${color}, inset 0 0 ${Math.round(
        20 * intensity
      )}px ${color}33`,
      opacity: isVisible ? 1 : 0,
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      animation:
        level === 'danger'
          ? 'pulse-danger 0.5s infinite'
          : level === 'warning'
            ? 'pulse-warning 1s infinite'
            : 'pulse-safe 2s infinite',
    }),
    [color, intensity, isVisible, level]
  )

  return <div style={overlayStyle} className={`overlay overlay-${level}`} />
}
