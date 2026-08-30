// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-870989e5
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · 路径追踪引擎
// UID9622 | 龍芯北辰 | 2026-07-18

import { TraceResult } from '../models/TraceResult'

export class PathTracer {
  trace(text: string): TraceResult {
    // 计算数字根
    const digits = text.split('').filter(c => /\d/.test(c)).map(Number)
    let dr = 0
    if (digits.length > 0) {
      let n = digits.reduce((a, b) => a + b, 0)
      while (n >= 10) {
        n = String(n).split('').map(Number).reduce((a, b) => a + b, 0)
      }
      dr = n
    }

    const d = Math.min(dr, 5)
    const l = this.hashCode(text) % 9
    const b = this.hashCode(text + 'bagua') % 8
    const g = this.hashCode(text + '64gua') % 64
    const w = Math.min(dr, 4)
    const tg = this.hashCode(text + 'tiangan') % 120

    return new TraceResult(text, dr, d, l, b, g, w, tg)
  }

  private hashCode(str: string): number {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash
    }
    return Math.abs(hash)
  }

  /**
   * 确定性随机数生成器 (Mulberry32)
   */
  static mulberry32(a: number): () => number {
    return () => {
      let t = a += 0x6D2B79F5
      t = Math.imul(t ^ (t >>> 15), t | 1) as number
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61) as number
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296
    }
  }
}
