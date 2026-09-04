// WebSocket 客户端服务
// DNA:#龍芯⚡️丙午·癸巳·己酉·庚午·䷨损-WS-CLIENT-v1.0

import { useRef, useState, useCallback } from 'react'
import { useOverlayStore } from '../store/overlay'
import { useBaobaoStore } from '../store/baobao'

interface WSMessage {
  type: 'overlay' | 'baobao' | 'chat'
  payload: any
}

export function useWSClient() {
  const ws = useRef<WebSocket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [reconnectAttempts, setReconnectAttempts] = useState(0)

  const overlayStore = useOverlayStore()
  const baobaoStore = useBaobaoStore()

  const handleMessage = useCallback((message: WSMessage) => {
    switch (message.type) {
      case 'overlay':
        overlayStore.setLevel(message.payload.level)
        break
      case 'baobao':
        baobaoStore.speak(message.payload.message, message.payload.duration)
        if (message.payload.expression) {
          baobaoStore.setExpression(message.payload.expression)
        }
        break
      case 'chat':
        baobaoStore.react(message.payload.emotion || 'happy')
        break
    }
  }, [overlayStore, baobaoStore])

  const connect = useCallback((url: string) => {
    try {
      ws.current = new WebSocket(url)

      ws.current.onopen = () => {
        console.log('[WS] Connected')
        setIsConnected(true)
        setReconnectAttempts(0)
      }

      ws.current.onmessage = (event) => {
        try {
          const message: WSMessage = JSON.parse(event.data)
          handleMessage(message)
        } catch (error) {
          console.error('[WS] Parse error:', error)
        }
      }

      ws.current.onerror = (error) => {
        console.error('[WS] Error:', error)
        setIsConnected(false)
      }

      ws.current.onclose = () => {
        console.log('[WS] Disconnected')
        setIsConnected(false)

        // 自动重连 (指数退避)
        if (reconnectAttempts < 5) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000)
          setTimeout(() => {
            console.log(`[WS] Reconnecting... (attempt ${reconnectAttempts + 1})`)
            setReconnectAttempts(reconnectAttempts + 1)
            connect(url)
          }, delay)
        }
      }
    } catch (error) {
      console.error('[WS] Connection error:', error)
    }
  }, [reconnectAttempts, handleMessage])

  const send = useCallback((message: WSMessage) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message))
    } else {
      console.warn('[WS] Not connected, message dropped:', message)
    }
  }, [])

  return {
    connect,
    send,
    isConnected,
  }
}
