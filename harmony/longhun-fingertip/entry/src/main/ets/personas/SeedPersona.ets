// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-种子人格-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * 种子人格基类 v1.1
 *
 * 第二步：3种子人格常驻内存（文心/宝宝/黑天使），其余按需云端加载。
 * 端侧轻量引擎——不做完整推理，只做意图识别·情感温度·安全预判。
 *
 * 设计原则：
 * - 不调鲲鹏API即可运行（断网能力核心）
 * - 基于关键词+规则匹配，不依赖大模型
 * - 输出JSON结构，与鲲鹏人格集群格式对齐
 */

import { AuditColor } from '../cnsh/JsonParser'

/** 人格执行结果 */
export interface PersonaResult {
  persona_code: string
  persona_name: string
  action: string
  confidence: number     // 0-1
  reasoning: string
  dna: string
  audit: AuditColor
  data?: Record<string, string | number | boolean>
}

/** 种子人格状态 */
export enum PersonaState {
  IDLE = 'IDLE',
  THINKING = 'THINKING',
  DONE = 'DONE',
  ERROR = 'ERROR'
}

/**
 * 种子人格抽象基类
 */
export abstract class SeedPersona {
  abstract readonly PERSONA_CODE: string
  abstract readonly PERSONA_NAME: string
  abstract readonly ROLE: string
  abstract readonly MOTTO: string

  protected state: PersonaState = PersonaState.IDLE
  protected lastResult: PersonaResult | null = null

  /**
   * 执行推理（子类必须实现）
   * @param input 用户输入或上下文
   */
  abstract think(input: string, context?: Record<string, string>): PersonaResult

  /**
   * 完整执行循环：重置→思考→记录
   */
  run(input: string, context?: Record<string, string>): PersonaResult {
    this.state = PersonaState.THINKING
    try {
      this.lastResult = this.think(input, context)
      this.state = PersonaState.DONE
      return this.lastResult
    } catch (err) {
      this.state = PersonaState.ERROR
      console.error(`[${this.PERSONA_CODE}] 执行异常: ${JSON.stringify(err)}`)
      return this.errorResult(String(err))
    }
  }

  /** 获取当前状态 */
  getState(): PersonaState {
    return this.state
  }

  /** 获取上次结果 */
  getLastResult(): PersonaResult | null {
    return this.lastResult
  }

  /** 重置状态 */
  reset(): void {
    this.state = PersonaState.IDLE
    this.lastResult = null
  }

  /** 生成DNA标识 */
  protected genDna(action: string): string {
    const now = new Date()
    const dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
    return `#龍芯⚡️${dateStr}-${this.PERSONA_CODE}-${action}-v1.1-HM-SEED`
  }

  /** 生成错误结果 */
  protected errorResult(reason: string): PersonaResult {
    return {
      persona_code: this.PERSONA_CODE,
      persona_name: this.PERSONA_NAME,
      action: 'ERROR',
      confidence: 0,
      reasoning: reason,
      dna: this.genDna('ERROR'),
      audit: '🔴'
    }
  }

  /** 生成成功结果 */
  protected successResult(
    action: string,
    confidence: number,
    reasoning: string,
    audit: AuditColor = '🟢',
    data?: Record<string, string | number | boolean>
  ): PersonaResult {
    return {
      persona_code: this.PERSONA_CODE,
      persona_name: this.PERSONA_NAME,
      action,
      confidence: Math.min(1, Math.max(0, confidence)),
      reasoning,
      dna: this.genDna(action),
      audit,
      data
    }
  }
}
