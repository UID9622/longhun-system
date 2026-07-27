// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from './Constants'

/**
 * DNA本地生成器 v1.0
 *
 * 铁律：本地缓存DNA格式，生成走鲲鹏。
 * 本模块只做格式校验+展示，不做真实的干支计算。
 *
 * DNA格式: #龍芯⚡️{干支}·{卦}-{动作}-v1.0-HM-9622-{序号}
 */
export class DnaGenerator {
  private seqCounter: number = 0

  /**
   * 生成展示用DNA标签（本地格式，不替代鲲鹏DNA）
   * @param action 动作名：代码生成/文案润色/审查/自动路由
   * @param gua 卦名提示（来自响应或默认）
   */
  generateDisplayTag(action: string, gua?: string): string {
    this.seqCounter++
    const now = new Date()
    const yyyymmdd = `${now.getFullYear()}${this.pad(now.getMonth() + 1)}${this.pad(now.getDate())}`
    const hhmm = `${this.pad(now.getHours())}${this.pad(now.getMinutes())}`
    const seq = this.pad3(this.seqCounter)
    const resolvedGua = gua ?? '既济'

    return `${Constants.DNA_PREFIX}${yyyymmdd}·${hhmm}·${resolvedGua}-${action}-${Constants.DNA_VERSION}-HM-${Constants.UID}-${seq}`
  }

  /** 验证DNA格式合法性 */
  validateFormat(dna: string): boolean {
    if (!dna.startsWith(Constants.DNA_PREFIX)) return false
    const parts = dna.substring(Constants.DNA_PREFIX.length).split('-')
    return parts.length >= 4 // 干支·卦-动作-版本-设备-序号
  }

  /** 从完整DNA提取动作标签 */
  extractAction(dna: string): string {
    const parts = dna.substring(Constants.DNA_PREFIX.length).split('-')
    if (parts.length >= 2) return parts[1]  // -动作-...
    return '未知'
  }

  /** 重置序号计数器 */
  resetCounter(): void {
    this.seqCounter = 0
  }

  /** 获取当前序号 */
  getCurrentSeq(): number {
    return this.seqCounter
  }

  /** 获取当前时间的干支四柱占位符（本地不真算，用日期替代） */
  getTimestampGanzhi(): string {
    const now = new Date()
    const y = now.getFullYear().toString()
    const m = this.pad(now.getMonth() + 1)
    const d = this.pad(now.getDate())
    const h = this.pad(now.getHours())
    const min = this.pad(now.getMinutes())
    return `${y}${m}${d}·${h}${min}`
  }

  private pad(n: number): string { return n < 10 ? `0${n}` : `${n}` }
  private pad3(n: number): string {
    if (n < 10) return `00${n}`
    if (n < 100) return `0${n}`
    return `${n}`
  }
}

/** 全局单例 */
export const dnaGen = new DnaGenerator()
