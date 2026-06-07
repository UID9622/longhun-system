// 龍魂 Overlay 状态管理
// DNA: #龍芯⚡️2026-06-04-OVERLAY-STORE-v1.0

import { create } from 'zustand'

export type OverlayLevel = 'safe' | 'warning' | 'danger'

interface OverlayState {
  color: string
  intensity: number
  isVisible: boolean
  level: OverlayLevel

  // 动作
  setLevel: (level: OverlayLevel) => void
  updateColor: (color: string, intensity: number) => void
  setVisible: (visible: boolean) => void
  reset: () => void
}

const colorMap = {
  safe: '#00FF00',
  warning: '#FFA500',
  danger: '#FF0000',
}

const intensityMap = {
  safe: 0.05,
  warning: 0.15,
  danger: 0.3,
}

export const useOverlayStore = create<OverlayState>((set) => ({
  color: colorMap.safe,
  intensity: intensityMap.safe,
  isVisible: true,
  level: 'safe',

  setLevel: (level) =>
    set({
      level,
      color: colorMap[level],
      intensity: intensityMap[level],
    }),

  updateColor: (color, intensity) =>
    set({ color, intensity }),

  setVisible: (visible) =>
    set({ isVisible: visible }),

  reset: () =>
    set({
      color: colorMap.safe,
      intensity: intensityMap.safe,
      isVisible: true,
      level: 'safe',
    }),
}))
