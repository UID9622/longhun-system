# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂宝宝助手状态管理 v3.0
// DNA:#龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-BAOBAO-STORE-v3.0
// 扩展：计算机引擎（三才决策·易经推演·BraKet·CNSH-64·Lu指令·四柱五行·公式）

import { create } from 'zustand'

export type BaobaoExpression = 'idle' | 'happy' | 'warning' | 'sad' | 'thinking' | 'calculating' | 'revealing'
export type BaobaoAction = 'breathing' | 'waving' | 'talking' | 'resting' | 'pulsing'

interface SkillData {
  type?: string
  // v2.0
  数字根?: number
  五行?: string
  五行颜色?: string
  风险?: string
  风险数字?: number
  DNA码?: string
  河图?: any
  洛书?: any
  数字报告?: { 数字根?: number; 五行?: string; 颜色?: string; 方位?: string }
  // v3.0 三才
  综合得分?: number
  三色?: string
  建议?: string
  输入?: { [key: string]: number }
  // v3.0 易经
  卦象名称?: string
  最终判定?: string
  风险等级?: string
  风险级别?: string
  推理过程?: string
  // v3.0 BraKet
  主力人格?: { 名称: string; 权重: number }
  匹配场景?: string
  权重分布?: Record<string, number>
  // v3.0 计算机诊断
  五维诊断?: any
  总评价?: string
  // v2.0 诊断
  宝宝反应?: string
  宝宝台词?: string
  [key: string]: any
}

interface BaobaoState {
  expression: BaobaoExpression
  action: BaobaoAction
  message: string
  isVisible: boolean
  skillData: SkillData | null
  bubbleColor: string

  setExpression: (expr: BaobaoExpression) => void
  setAction: (action: BaobaoAction) => void
  speak: (message: string, duration?: number) => Promise<void>
  react: (expression: BaobaoExpression) => void
  setVisible: (visible: boolean) => void
  showSkillResult: (data: SkillData) => Promise<void>
  clearSkillData: () => void
}

// 五行→气泡颜色
const 五行气泡色: Record<string, string> = {
  '水': '#1E3A5F', '火': '#D43D1A', '木': '#2D8B2D',
  '金': '#DAA520', '土': '#8B7355',
}

export const useBaobaoStore = create<BaobaoState>((set, get) => ({
  expression: 'idle',
  action: 'breathing',
  message: '我在这里...',
  isVisible: true,
  skillData: null,
  bubbleColor: '#FFE4E1',

  setExpression: (expr) => set({ expression: expr }),
  setAction: (action) => set({ action }),

  speak: async (message, duration = 3000) => {
    set({ message, action: 'talking', skillData: null })
    await new Promise((resolve) => setTimeout(resolve, duration))
    const { skillData } = get()
    if (!skillData) {
      set({ action: 'breathing', message: '我在这里...' })
    }
  },

  react: (expression) => {
    set({ expression, action: 'waving' })
    setTimeout(() => set({ expression: 'idle', action: 'breathing' }), 2000)
  },

  setVisible: (visible) => set({ isVisible: visible }),

  showSkillResult: async (data) => {
    const 五行 = data.五行 || data.数字报告?.五行
    const color = 五行 ? (五行气泡色[五行] || '#FFE4E1') : '#FFE4E1'

    set({
      skillData: data,
      bubbleColor: color,
      action: data.宝宝反应 === 'thinking' ? 'pulsing' : 'talking',
      expression: (data.宝宝反应 as BaobaoExpression) || 'revealing',
    })

    // 6秒后恢复
    await new Promise((resolve) => setTimeout(resolve, 6000))
    set({ action: 'breathing', expression: 'idle', message: '我在这里...' })
  },

  clearSkillData: () => set({ skillData: null, bubbleColor: '#FFE4E1' }),
}))
