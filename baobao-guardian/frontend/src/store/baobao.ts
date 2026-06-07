// 龍魂宝宝助手状态管理
// DNA: #龍芯⚡️2026-06-04-BAOBAO-STORE-v1.0

import { create } from 'zustand'

export type BaobaoExpression = 'idle' | 'happy' | 'warning' | 'sad' | 'thinking'
export type BaobaoAction = 'breathing' | 'waving' | 'talking' | 'resting'

interface BaobaoState {
  expression: BaobaoExpression
  action: BaobaoAction
  message: string
  isVisible: boolean

  // 动作
  setExpression: (expr: BaobaoExpression) => void
  setAction: (action: BaobaoAction) => void
  speak: (message: string, duration?: number) => Promise<void>
  react: (expression: BaobaoExpression) => void
  setVisible: (visible: boolean) => void
}

export const useBaobaoStore = create<BaobaoState>((set, get) => ({
  expression: 'idle',
  action: 'breathing',
  message: '我在这里...',
  isVisible: true,

  setExpression: (expr) => set({ expression: expr }),

  setAction: (action) => set({ action }),

  speak: async (message, duration = 3000) => {
    set({ message, action: 'talking' })
    await new Promise((resolve) => setTimeout(resolve, duration))
    set({ action: 'breathing' })
  },

  react: (expression) => {
    set({ expression, action: 'waving' })
    setTimeout(() => {
      set({ expression: 'idle', action: 'breathing' })
    }, 2000)
  },

  setVisible: (visible) => set({ isVisible: visible }),
}))
