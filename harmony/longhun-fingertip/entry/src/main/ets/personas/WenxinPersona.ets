// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-文心-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * P00 · 文心 · 意图解析引擎（种子版）
 *
 * 端侧常驻第一人格。所有请求先进文心——判断意图、分配路由、决定处理方式。
 *
 * 核心职责：
 * 1. 意图分类（查状态/对话/审计/部署/设置/帮助）
 * 2. 路由建议（本地处理/调用鲲鹏）
 * 3. 紧急度判定（普通/关注/紧急）
 * 4. 权限预检（是否越权）
 *
 * 端侧限制：
 * - 基于关键词规则匹配，不做语义理解
 * - 不调用鲲鹏即可运行
 * - 不确定时降低信心分，建议走鲲鹏
 */

import { SeedPersona, PersonaResult, PersonaState } from './SeedPersona'
import { AuditColor } from '../cnsh/JsonParser'

/** 意图类型 */
export enum IntentType {
  STATUS = 'STATUS',         // 查询系统状态
  CHAT = 'CHAT',             // AI对话
  AUDIT = 'AUDIT',           // 审计/安全检查
  DEPLOY = 'DEPLOY',         // 部署/运维
  DNA = 'DNA',               // DNA追溯
  SETTINGS = 'SETTINGS',     // 设置/配置
  HELP = 'HELP',             // 帮助/说明
  UNKNOWN = 'UNKNOWN'        // 未识别
}

/** 路由建议 */
export enum RouteSuggestion {
  LOCAL = 'LOCAL',           // 本地处理（断网可用）
  REMOTE = 'REMOTE',         // 走鲲鹏API
  HYBRID = 'HYBRID'          // 本地先尝试，失败走远端
}

/** 紧急度 */
export enum Urgency {
  NORMAL = 'NORMAL',
  ATTENTION = 'ATTENTION',
  URGENT = 'URGENT',
  CRITICAL = 'CRITICAL'
}

/** 文心输出 */
export interface WenxinOutput {
  intent: IntentType
  route: RouteSuggestion
  urgency: Urgency
  target_persona?: string     // 建议路由人格编号
  keywords: string[]
  is_sensitive: boolean       // 是否敏感请求
}

export class WenxinPersona extends SeedPersona {
  readonly PERSONA_CODE: string = 'P00'
  readonly PERSONA_NAME: string = '文心'
  readonly ROLE: string = '元认知统筹·意图解析·总军师'
  readonly MOTTO: string = '万事先过心'

  /** 意图关键词表 */
  private readonly intentPatterns: Record<IntentType, string[]> = {
    STATUS: ['状态', '运行', '健康', 'CPU', '内存', '磁盘', 'uptime', '引擎', '断路器', '检查', '巡检', '体检'],
    CHAT: ['聊天', '对话', '问', '说', '聊', '讲', '回答', '帮我', '解释', '什么是', '怎么', '为什么', '如何', '告诉我'],
    AUDIT: ['审计', '安全', '漏洞', '检查代码', '审查', '扫描', '渗透', '攻击', '风险', '合规', '红线', '底线'],
    DEPLOY: ['部署', '上线', '发布', '回滚', '重启', '同步', '安装', '配置服务', '启动', '停止'],
    DNA: ['DNA', '追溯', '溯源', '签名', '注册表', '哈希', '干支', '卦', '龍芯', '确认码'],
    SETTINGS: ['设置', '配置', '修改', '端口', '地址', '连接', '服务器', '密钥'],
    HELP: ['帮助', '文档', '怎么用', '教程', '新手', '说明', '指南', 'help', 'usage'],
    UNKNOWN: []
  }

  /** 敏感词检测 */
  private readonly sensitivePatterns: RegExp[] = [
    /删除/i,     /绕过/i,     /后门/i,
    /偷偷/i,     /不留记录/i,   /去水印/i,
    /洗来源/i,   /伪造/i,     /冒充/i,
    /转移/i,     /泄露/i,     /越权/i
  ]

  think(input: string, context?: Record<string, string>): PersonaResult {
    const lower = input.toLowerCase().trim()
    const keywords: string[] = []
    const intentScores: Map<IntentType, number> = new Map()

    // 关键词匹配计分
    for (const [intent, patterns] of Object.entries(this.intentPatterns)) {
      let score = 0
      const matched: string[] = []
      for (const p of patterns) {
        if (lower.includes(p)) {
          score += 1
          matched.push(p)
          if (lower.startsWith(p)) score += 0.5  // 开头匹配加权
        }
      }
      if (score > 0) {
        intentScores.set(intent as IntentType, score)
        keywords.push(...matched)
      }
    }

    // 确定最高分意图
    let bestIntent = IntentType.UNKNOWN
    let bestScore = 0
    for (const [intent, score] of intentScores) {
      if (score > bestScore) {
        bestScore = score
        bestIntent = intent
      }
    }

    // 紧急度判定
    const urgency = this.judgeUrgency(lower, bestIntent)

    // 敏感词检测
    const isSensitive = this.sensitivePatterns.some((re: RegExp) => re.test(input))

    // 路由建议
    let route: RouteSuggestion
    let targetPersona: string | undefined

    switch (bestIntent) {
      case IntentType.STATUS:
      case IntentType.HELP:
        route = RouteSuggestion.LOCAL  // 本地可处理
        break
      case IntentType.DNA:
        route = RouteSuggestion.HYBRID // 先查本地缓存，失败调鲲鹏
        targetPersona = 'P03'          // 雯雯归档
        break
      case IntentType.AUDIT:
        route = RouteSuggestion.HYBRID
        targetPersona = 'P05'          // 上帝之眼审计
        break
      case IntentType.DEPLOY:
        route = RouteSuggestion.REMOTE // 部署必须走鲲鹏
        targetPersona = 'P14'          // 吕蒙
        break
      case IntentType.CHAT:
      default:
        route = RouteSuggestion.REMOTE // 对话走鲲鹏21人格
        break
    }

    // 紧急情况强制走远端
    if (urgency >= Urgency.URGENT) {
      route = RouteSuggestion.REMOTE
    }

    // 敏感请求降低信心
    const confidence = isSensitive
      ? Math.min(0.6, bestScore > 0 ? 0.5 : 0.2)
      : bestScore > 0
        ? Math.min(0.9, 0.5 + bestScore * 0.1)
        : 0.3

    const output: WenxinOutput = {
      intent: bestIntent,
      route,
      urgency,
      target_persona: targetPersona,
      keywords,
      is_sensitive: isSensitive
    }

    return this.successResult(
      `ROUTE_TO_${bestIntent}`,
      confidence,
      isSensitive ? '检测到敏感关键词，降低信心分·建议人工复核' : `意图:${bestIntent} 路由:${route}`,
      isSensitive ? '🟡' : '🟢',
      {
        intent: bestIntent,
        route: route,
        urgency: urgency,
        target: targetPersona ?? 'NONE',
        keyword_count: keywords.length,
        sensitive: isSensitive
      }
    )
  }

  /** 紧急度判定 */
  private judgeUrgency(input: string, intent: IntentType): Urgency {
    const lower = input.toLowerCase()

    // 熔断相关 → CRITICAL
    if (/熔断|冻结|入侵|泄露|攻击|数据泄露|紧急/.test(lower)) {
      return Urgency.CRITICAL
    }

    // 安全审计相关 → URGENT
    if (/漏洞|安全风险|红线|渗透|后门/.test(lower)) {
      return Urgency.URGENT
    }

    // 部署相关 → ATTENTION
    if (intent === IntentType.DEPLOY || /上线|发布|重启/.test(lower)) {
      return Urgency.ATTENTION
    }

    return Urgency.NORMAL
  }

  /** 导出意图分析（供其他模块使用） */
  analyzeIntent(input: string): WenxinOutput {
    const result = this.think(input)
    return {
      intent: (result.data?.['intent'] as IntentType) ?? IntentType.UNKNOWN,
      route: (result.data?.['route'] as RouteSuggestion) ?? RouteSuggestion.REMOTE,
      urgency: (result.data?.['urgency'] as Urgency) ?? Urgency.NORMAL,
      target_persona: result.data?.['target'] as string | undefined,
      keywords: [],
      is_sensitive: (result.data?.['sensitive'] as boolean) ?? false
    }
  }
}
