// 龍魂宝宝助手组件
// DNA: #龍芯⚡️2026-06-04-BAOBAO-COMPONENT-v1.0

import React, { useMemo } from 'react'
import { useBaobaoStore } from '../store/baobao'
import '../styles/animations.css'

export const Baobao: React.FC = () => {
  const { expression, action, message, isVisible } = useBaobaoStore()

  const containerStyle = useMemo(
    () => ({
      position: 'fixed' as const,
      bottom: '30px',
      right: '30px',
      zIndex: 999998,
      opacity: isVisible ? 1 : 0,
      transition: 'opacity 0.3s',
      pointerEvents: 'none' as const,
    }),
    [isVisible]
  )

  const baobaoStyle = useMemo(
    () => ({
      width: '80px',
      height: '80px',
      borderRadius: '50%',
      background: 'radial-gradient(circle at 30% 30%, #FFE4E1, #FFB6C1)',
      boxShadow: '0 4px 20px rgba(255, 182, 193, 0.4), 0 0 40px rgba(255, 20, 147, 0.2)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      animation:
        action === 'talking'
          ? 'baobao-talk 0.4s infinite'
          : action === 'waving'
            ? 'baobao-wave 0.6s ease-in-out'
            : 'baobao-breathing 3s ease-in-out infinite',
      cursor: 'pointer',
      position: 'relative' as const,
    }),
    [action]
  )

  const eyeStyle = {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#333',
    position: 'absolute' as const,
  }

  const leftEyeStyle = { ...eyeStyle, left: '20px', top: '25px' }
  const rightEyeStyle = { ...eyeStyle, right: '20px', top: '25px' }

  const bubbleStyle = useMemo(
    () => ({
      position: 'absolute' as const,
      bottom: '-80px',
      left: '50%',
      transform: 'translateX(-50%)',
      background: '#FFE4E1',
      color: '#333',
      padding: '8px 12px',
      borderRadius: '12px',
      fontSize: '12px',
      whiteSpace: 'nowrap' as const,
      border: '2px solid #FFB6C1',
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
      animation: 'bubble-pop 0.3s ease-out',
      maxWidth: '150px',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
    }),
    []
  )

  const tailStyle = {
    position: 'absolute' as const,
    width: '30px',
    height: '30px',
    background: '#FFB6C1',
    borderRadius: '50%',
    bottom: '-20px',
    left: '60%',
    animation: 'baobao-tail 1.5s ease-in-out infinite',
  }

  return (
    <div style={containerStyle} className="baobao-container">
      <div style={baobaoStyle} className={`baobao baobao-${expression}`}>
        {/* 眼睛 */}
        <div style={leftEyeStyle} />
        <div style={rightEyeStyle} />

        {/* 嘴巴 */}
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
            width: '20px',
            height: '10px',
            borderBottom: '2px solid #333',
            borderRadius: '0 0 20px 20px',
          }}
        />

        {/* 尾巴 */}
        <div style={tailStyle} />
      </div>

      {/* 语音气泡 */}
      {message && <div style={bubbleStyle}>{message}</div>}
    </div>
  )
}
