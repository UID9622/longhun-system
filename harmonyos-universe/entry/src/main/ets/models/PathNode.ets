// 龍魂路径宇宙 · 路径节点数据模型
// UID9622 | 龍芯北辰 | 2026-07-18

import { WUXING_COLORS, AUDIT_ALPHA, DR_WUXING, DR_AUDIT } from '../utils/Constants'

export class PathNode {
  d: number       // 数字根 (0-5)
  l: number       // 洛书 (0-8)
  b: number       // 八卦 (0-7)
  g: number       // 64卦 (0-63)
  w: number       // 五行 (0-4)
  tg: number      // 干支 (0-119)
  pathId: number
  x: number
  y: number
  z: number
  wuxing: string
  audit: string
  color: string
  alpha: number
  size: number
  dr: number

  constructor(d: number, l: number, b: number, g: number, w: number, tg: number) {
    this.d = d
    this.l = l
    this.b = b
    this.g = g
    this.w = w
    this.tg = tg

    const drValues = [0, 1, 2, 3, 4, 5]
    this.dr = drValues[d] ?? 0

    this.wuxing = DR_WUXING[this.dr] ?? '土'
    this.audit = DR_AUDIT[this.dr] ?? '🟢'
    this.color = WUXING_COLORS[this.wuxing] ?? '#DAA520'
    this.alpha = AUDIT_ALPHA[this.audit] ?? 1.0

    this.x = d * 9 + l
    this.y = b * 64 + g
    this.z = w * 120 + tg

    this.pathId = d * 9 * 8 * 64 * 5 * 120 +
                  l * 8 * 64 * 5 * 120 +
                  b * 64 * 5 * 120 +
                  g * 5 * 120 +
                  w * 120 +
                  tg

    this.size = 2 + Math.random() * 3
  }
}
