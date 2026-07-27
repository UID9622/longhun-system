// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-宝宝-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * P02 · 宝宝 · 情感温度引擎（种子版）
 *
 * 端侧常驻第二人格。30%情感隔离——观察情绪但不被情绪绑架。
 *
 * 核心职责：
 * 1. 情感温度检测（积极/中性/消极/愤怒/焦虑）
 * 2. 回应策略建议（安抚/讲理/沉默/升级）
 * 3. 挫败保护（连续3次失败→自动降速·建议休息）
 * 4. 教学场景温度调节
 *
 * 端侧限制：
 * - 基于关键词+标点+长度特征，不做NLP
 * - 温度值 0-100（0=冰山 50=中性 100=沸点）
 */

import { SeedPersona, PersonaResult, PersonaState } from './SeedPersona'
import { AuditColor } from '../cnsh/JsonParser'

/** 情感状态 */
export enum EmotionState {
  POSITIVE = 'POSITIVE',       // 积极·开心·满意
  NEUTRAL = 'NEUTRAL',         // 中性·平淡
  NEGATIVE = 'NEGATIVE',       // 消极·低落·不满
  ANGRY = 'ANGRY',             // 愤怒·暴躁
  ANXIOUS = 'ANXIOUS',         // 焦虑·不安
  FRUSTRATED = 'FRUSTRATED'    // 挫败·想放弃
}

/** 回应策略 */
export enum ResponseTone {
  ENCOURAGE = 'ENCOURAGE',     // 鼓励·正向
  CALM = 'CALM',               // 冷静·讲理
  SOOTHE = 'SOOTHE',           // 安抚·情绪先被接住
  SILENT = 'SILENT',           // 少说·等情绪过
  ESCALATE = 'ESCALATE',       // 升级·建议转人工
  DIRECT = 'DIRECT'            // 直接·不绕
}

/** 宝宝输出 */
export interface BaobaoOutput {
  temperature: number          // 0-100 情感温度
  emotion: EmotionState
  tone: ResponseTone
  should_slow_down: boolean    // 是否建议降速
  frustration_count: number    // 连续挫败次数
  suggestion: string           // 行动建议
}

export class BaobaoPersona extends SeedPersona {
  readonly PERSONA_CODE: string = 'P02'
  readonly PERSONA_NAME: string = '宝宝'
  readonly ROLE: string = '情感温度引擎·30%情感隔离·挫败保护'
  readonly MOTTO: string = '先接住情绪，再解决问题'

  private frustrationHistory: number[] = []  // 挫败时间戳记录
  private readonly FRUSTRATION_WINDOW = 10 * 60 * 1000  // 10分钟窗口
  private readonly FRUSTRATION_THRESHOLD = 3

  /** 积极关键词 */
  private readonly positiveWords: string[] = [
    '好', '棒', '厉害', '牛', '赞', '谢谢', '感谢', '开心', '满意',
    '完成', '成功', '通了', '可以', 'OK', 'ok', '不错', '完美', '漂亮', '帅'
  ]

  /** 消极关键词 */
  private readonly negativeWords: string[] = [
    '烦', '累', '难', '不行', '失败', '报错', '错误', '不通', '卡',
    '慢', '等太久', '不好', '差', '烂', '垃圾', '无语', '算了', '不做了'
  ]

  /** 愤怒关键词 */
  private readonly angryWords: string[] = [
    '操', '妈的', '草', 'fuck', 'shit', '靠', '日', '滚',
    '傻逼', 'sb', '脑子有病', '坑爹', '骗', '忽悠'
  ]

  /** 焦虑关键词 */
  private readonly anxiousWords: string[] = [
    '怎么办', '会不会', '万一', '担心', '害怕', '紧张', '不确定',
    '能不能行', '来得及吗', '有问题', '稳不稳', '靠谱吗', '保险吗'
  ]

  /** 挫败关键词 */
  private readonly frustrationWords: string[] = [
    '又失败了', '还是不行', '放弃', '不搞了', '算了', '没救了', '学不会',
    '太难了', '搞不定', '白费', '浪费时间', '没意义'
  ]

  think(input: string, context?: Record<string, string>): PersonaResult {
    const lower = input.toLowerCase()

    // 标点特征
    const exclamationCount = (input.match(/[！!]/g) ?? []).length
    const questionCount = (input.match(/[？?]/g) ?? []).length
    const upperRatio = (input.match(/[A-Z]/g) ?? []).length / Math.max(1, input.length)

    // 各情感分数
    let positiveScore = this.countMatches(lower, this.positiveWords)
    let negativeScore = this.countMatches(lower, this.negativeWords)
    let angryScore = this.countMatches(lower, this.angryWords)
    let anxiousScore = this.countMatches(lower, this.anxiousWords)
    let frustrationScore = this.countMatches(lower, this.frustrationWords)

    // 标点加权
    if (exclamationCount >= 3) angryScore += 1
    if (questionCount >= 3) anxiousScore += 1
    if (upperRatio > 0.3) angryScore += 0.5  // 大量大写=在吼

    // 消息长度特征
    if (input.length < 5 && angryScore > 0) angryScore += 0.5  // 短消息+愤怒词=暴怒
    if (input.length > 100) anxiousScore += 0.5  // 长消息=焦虑倾诉

    // 上下文感知
    if (context?.['is_teaching']) {
      frustrationScore += 0.5  // 教学场景更容易挫败
    }

    // 确定主导情感
    let emotion = EmotionState.NEUTRAL
    let maxScore = 0
    const scores: [EmotionState, number][] = [
      [EmotionState.ANGRY, angryScore],
      [EmotionState.FRUSTRATED, frustrationScore],
      [EmotionState.ANXIOUS, anxiousScore],
      [EmotionState.NEGATIVE, negativeScore],
      [EmotionState.POSITIVE, positiveScore]
    ]
    for (const [e, s] of scores) {
      if (s > maxScore) {
        maxScore = s
        emotion = e
      }
    }

    // 如果没检测到任何情感，保持中性
    if (maxScore === 0) emotion = EmotionState.NEUTRAL

    // 计算温度 (0-100)
    let temperature = 50  // 中性基准
    switch (emotion) {
      case EmotionState.POSITIVE:    temperature = 50 + Math.min(40, positiveScore * 15); break
      case EmotionState.ANGRY:       temperature = 50 + angryScore * 20; break    // 愤怒=高温
      case EmotionState.FRUSTRATED:  temperature = 50 - frustratedScore * 10; break // 挫败=降温
      case EmotionState.ANXIOUS:     temperature = 50 + anxiousScore * 8; break
      case EmotionState.NEGATIVE:    temperature = 50 - negativeScore * 8; break
    }
    temperature = Math.min(100, Math.max(0, temperature))

    // 挫败追踪
    const now = Date.now()
    if (emotion === EmotionState.FRUSTRATED) {
      this.frustrationHistory.push(now)
    }
    // 清理过期记录
    this.frustrationHistory = this.frustrationHistory.filter((t: number) => now - t < this.FRUSTRATION_WINDOW)
    const frustrationCount = this.frustrationHistory.length
    const shouldSlowDown = frustrationCount >= this.FRUSTRATION_THRESHOLD

    // 回应策略
    let tone: ResponseTone
    if (shouldSlowDown) {
      tone = ResponseTone.SOOTHE
    } else {
      switch (emotion) {
        case EmotionState.POSITIVE:  tone = ResponseTone.ENCOURAGE; break
        case EmotionState.ANGRY:     tone = ResponseTone.SILENT; break   // 不劝·不反驳·等过去
        case EmotionState.ANXIOUS:   tone = ResponseTone.CALM; break
        case EmotionState.FRUSTRATED:tone = ResponseTone.SOOTHE; break
        case EmotionState.NEGATIVE:  tone = ResponseTone.DIRECT; break
        default:                     tone = ResponseTone.DIRECT; break
      }
    }

    // 生成建议
    let suggestion: string
    switch (tone) {
      case ResponseTone.ENCOURAGE:
        suggestion = '继续保持正向节奏·肯定对方努力'
        break
      case ResponseTone.SOOTHE:
        suggestion = frustrationCount >= this.FRUSTRATION_THRESHOLD
          ? `连续${frustrationCount}次挫败·建议暂停·换思路或休息后再来`
          : '情绪有挫败迹象·先接住情绪·不要急着给方案'
        break
      case ResponseTone.SILENT:
        suggestion = '对方情绪激烈·不劝不反驳·等情绪回落再沟通'
        break
      case ResponseTone.CALM:
        suggestion = '对方焦虑·需要稳定感·用确定的事实回复·不要说"可能""也许"'
        break
      default:
        suggestion = '正常节奏·直接回应'
    }

    const output: BaobaoOutput = {
      temperature,
      emotion,
      tone,
      should_slow_down: shouldSlowDown,
      frustration_count: frustrationCount,
      suggestion
    }

    return this.successResult(
      `EMOTION_${emotion}`,
      0.7,
      `温度${temperature}·${emotion}·策略:${tone}${shouldSlowDown ? '·⚠️建议降速' : ''}`,
      shouldSlowDown ? '🟡' : '🟢',
      {
        temperature: temperature,
        emotion: emotion,
        tone: tone,
        slowdown: shouldSlowDown,
        frustration: frustrationCount
      }
    )
  }

  /** 关键词计数 */
  private countMatches(text: string, words: string[]): number {
    let count = 0
    for (const w of words) {
      if (text.includes(w)) count += 1
    }
    return count
  }

  /** 获取当前挫败状态 */
  getFrustrationCount(): number {
    const now = Date.now()
    this.frustrationHistory = this.frustrationHistory.filter((t: number) => now - t < this.FRUSTRATION_WINDOW)
    return this.frustrationHistory.length
  }

  /** 重置挫败计数（比如成功完成任务后） */
  clearFrustration(): void {
    this.frustrationHistory = []
  }
}
