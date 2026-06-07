// 龍魂宝宝守护助手 · 主应用
// DNA: #龍芯⚡️2026-06-04-BAOBAO-APP-v1.0

import React, { useEffect } from 'react'
import { Overlay } from './components/Overlay'
import { Baobao } from './components/Baobao'
import { ParticleContainer } from './components/ParticleContainer'
import { useWSClient } from './services/wsClient'
import './styles/index.css'

export default function App() {
  const { connect, isConnected } = useWSClient()

  useEffect(() => {
    // 连接 WebSocket
    connect('ws://localhost:8000/ws/overlay')
  }, [])

  return (
    <div className="app-container">
      {/* 全屏 Overlay 层 */}
      <Overlay />

      {/* 粒子系统背景 */}
      <ParticleContainer />

      {/* 宝宝助手 */}
      <Baobao />

      {/* 状态指示器 */}
      <div className="status-indicator">
        <div className={`status-dot ${isConnected ? 'online' : 'offline'}`}></div>
        <span>{isConnected ? '已连接' : '离线'}</span>
      </div>
    </div>
  )
}
