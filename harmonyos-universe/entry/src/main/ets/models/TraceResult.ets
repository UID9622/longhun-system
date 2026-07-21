// 龍魂路径宇宙 · 追踪结果数据模型
// UID9622 | 龍芯北辰 | 2026-07-18

import { DR_WUXING, DR_AUDIT } from '../utils/Constants'

export class TraceResult {
  text: string
  pathId: number
  x: number
  y: number
  z: number
  dr: number
  wuxing: string
  audit: string
  d: number
  l: number
  b: number
  g: number
  w: number
  tg: number

  constructor(text: string, dr: number, d: number, l: number, b: number,
              g: number, w: number, tg: number) {
    this.text = text
    this.dr = dr
    this.d = d
    this.l = l
    this.b = b
    this.g = g
    this.w = w
    this.tg = tg

    this.wuxing = DR_WUXING[dr] ?? '土'
    this.audit = DR_AUDIT[dr] ?? '🟢'

    this.x = d * 9 + l
    this.y = b * 64 + g
    this.z = w * 120 + tg

    this.pathId = d * 9 * 8 * 64 * 5 * 120 +
                  l * 8 * 64 * 5 * 120 +
                  b * 64 * 5 * 120 +
                  g * 5 * 120 +
                  w * 120 + tg
  }
}
