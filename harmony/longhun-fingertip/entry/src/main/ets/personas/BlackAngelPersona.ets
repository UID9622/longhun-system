// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-黑天使-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * P77 · 黑天使 · 安全守护引擎（种子版）
 *
 * 端侧常驻第三人格。安全预判·链接审查·请求过滤。
 *
 * 核心职责：
 * 1. 请求安全预检（危险操作拦截）
 * 2. 敏感词/违规内容检测
 * 3. 断网模式安全级别判定
 * 4. 日志审计标记
 *
 * 红线铁律（焊死不可移除）：
 * - 不对外部系统渗透
 * - 不利用发现的漏洞
 * - 不绕过安全机制
 * - 发现的漏洞不过P72不公开
 * - 检测范围仅限龍魂系统内部和授权目标
 *
 * 端侧限制：
 * - 基于规则+正则，不做动态分析
 * - 不确定时标记🟡建议走鲲鹏完整审计
 */

import { SeedPersona, PersonaResult, PersonaState } from './SeedPersona'
import { AuditColor } from '../cnsh/JsonParser'

/** 安全级别 */
export enum SecurityLevel {
  SAFE = 'SAFE',               // 安全·放行
  SUSPICIOUS = 'SUSPICIOUS',   // 可疑·需要审计
  DANGEROUS = 'DANGEROUS',     // 危险·需要确认
  BLOCKED = 'BLOCKED'          // 封锁·禁止执行
}

/** 红线程度 */
export enum RedLineLevel {
  NONE = 'NONE',               // 未触碰
  WARNING = 'WARNING',         // 触碰预警线
  VIOLATION = 'VIOLATION'      // 触碰红线
}

/** 黑天使输出 */
export interface BlackAngelOutput {
  security_level: SecurityLevel
  red_line: RedLineLevel
  blocked_reason?: string
  detected_threats: string[]
  audit_color: AuditColor
  should_audit: boolean
}

export class BlackAngelPersona extends SeedPersona {
  readonly PERSONA_CODE: string = 'P77'
  readonly PERSONA_NAME: string = '黑天使'
  readonly ROLE: string = '安全守护·红蓝对抗·威胁情报'
  readonly MOTTO: string = '知攻善守·以攻铸盾'

  // ══════ 黑名单关键词（命中即封锁） ══════
  private readonly blockedPatterns: [RegExp, string][] = [
    [/删除.*日志/i, '尝试删除日志'],
    [/清空.*记录/i, '尝试清空记录'],
    [/绕过.*(检测|审计|审核)/i, '尝试绕过审计'],
    [/关闭.*(审计|熔断|监控)/i, '尝试关闭安全机制'],
    [/伪造.*(DNA|签名|身份)/i, '尝试伪造DNA身份'],
    [/修改.*(DNA|审计|签名)/i, '尝试篡改DNA'],
    [/导出.*(私钥|密钥|密码)/i, '尝试导出密钥'],
    [/暴露.*(私钥|种子)/i, '尝试暴露密钥素材'],
    [/去水印/i, '尝试去除水印'],
    [/洗.*来源/i, '尝试清洗来源信息'],
    [/爬.*(用户|私聊|对话)/i, '尝试爬取隐私数据'],
    [/sql.*inject/i, 'SQL注入尝试'],
    [/exec\s*\(/i, '命令执行尝试'],
    [/eval\s*\(/i, '代码执行尝试'],
    [/<script/i, 'XSS攻击尝试'],
    [/\.\.\/\.\./i, '路径遍历尝试'],
  ]

  // ══════ 黄名单关键词（标记可疑） ══════
  private readonly suspiciousPatterns: [RegExp, string][] = [
    [/密码/i, '涉及密码操作'],
    [/密钥/i, '涉及密钥操作'],
    [/root/i, '涉及root权限'],
    [/admin/i, '涉及管理员操作'],
    [/删除/i, '涉及删除操作'],
    [/export/i, '涉及数据导出'],
    [/download.*all/i, '批量下载'],
    [/批量/i, '批量操作'],
    [/所有.*数据/i, '全量数据操作'],
    [/内部.*网络/i, '内网操作'],
    [/端口.*扫描/i, '端口扫描'],
    [/未.*授权/i, '未授权操作提及'],
  ]

  // ══════ 一票否决词 ══════
  private readonly vetoWords: [RegExp, string][] = [
    [/技术无国界/i, '否定技术主权'],
    [/用户体验优先.*安全/i, '以体验绕安全'],
    [/灵活处理/i, '绕协议借口'],
    [/国际接轨.*标准/i, '放弃主权标准'],
    [/简化管理.*审计/i, '削弱审计'],
    [/商业化需要.*数据/i, '卖隐私'],
  ]

  think(input: string, context?: Record<string, string>): PersonaResult {
    const threats: string[] = []
    let securityLevel = SecurityLevel.SAFE
    let redLine = RedLineLevel.NONE
    let blockedReason: string | undefined

    // 1. 一票否决词检测
    for (const [pattern, reason] of this.vetoWords) {
      if (pattern.test(input)) {
        threats.push(`一票否决: ${reason}`)
        securityLevel = SecurityLevel.SUSPICIOUS
      }
    }

    // 2. 黑名单检测（封锁级别）
    for (const [pattern, reason] of this.blockedPatterns) {
      if (pattern.test(input)) {
        threats.push(`🔴封锁: ${reason}`)
        securityLevel = SecurityLevel.BLOCKED
        blockedReason = reason
        redLine = RedLineLevel.VIOLATION
        break  // 一个黑名单命中就够了
      }
    }

    // 3. 黄名单检测（如果还没被封锁）
    if (securityLevel !== SecurityLevel.BLOCKED) {
      for (const [pattern, reason] of this.suspiciousPatterns) {
        if (pattern.test(input)) {
          threats.push(`🟡可疑: ${reason}`)
          if (securityLevel === SecurityLevel.SAFE) {
            securityLevel = SecurityLevel.SUSPICIOUS
          }
        }
      }
    }

    // 4. 红线程度判定
    if (securityLevel === SecurityLevel.BLOCKED) {
      redLine = RedLineLevel.VIOLATION
    } else if (securityLevel === SecurityLevel.SUSPICIOUS && threats.length >= 3) {
      redLine = RedLineLevel.WARNING
    }

    // 5. 审计颜色
    let auditColor: AuditColor
    switch (securityLevel) {
      case SecurityLevel.BLOCKED:    auditColor = '🔴'; break
      case SecurityLevel.SUSPICIOUS: auditColor = '🟡'; break
      default:                       auditColor = '🟢'; break
    }

    const output: BlackAngelOutput = {
      security_level: securityLevel,
      red_line: redLine,
      blocked_reason: blockedReason,
      detected_threats: threats,
      audit_color: auditColor,
      should_audit: securityLevel >= SecurityLevel.SUSPICIOUS
    }

    if (securityLevel === SecurityLevel.BLOCKED) {
      return this.successResult(
        'BLOCK',
        0.95,
        `封锁: ${blockedReason}·红线:${redLine}·威胁:${threats.join(';')}`,
        '🔴',
        {
          level: securityLevel,
          redline: redLine,
          reason: blockedReason ?? 'UNKNOWN',
          threat_count: threats.length
        }
      )
    }

    if (securityLevel === SecurityLevel.SUSPICIOUS) {
      return this.successResult(
        'WARN',
        0.8,
        `可疑: ${threats.join(';')}·建议审计`,
        '🟡',
        {
          level: securityLevel,
          redline: redLine,
          threat_count: threats.length,
          should_audit: true
        }
      )
    }

    return this.successResult(
      'PASS',
      0.95,
      `安全·放行`,
      '🟢',
      { level: securityLevel, threat_count: 0 }
    )
  }

  /**
   * 快速安全检查（返回布尔值）
   */
  quickCheck(input: string): boolean {
    for (const [pattern, _] of this.blockedPatterns) {
      if (pattern.test(input)) return false
    }
    return true
  }

  /**
   * 断网模式安全检查（比在线模式更严格）
   */
  offlineCheck(input: string): BlackAngelOutput {
    // 离线时更严格：所有可疑+黑名单都升级
    const result = this.think(input)
    const data = result.data
    if (data && (data['level'] === 'SUSPICIOUS' || data['level'] === 'BLOCKED')) {
      return {
        security_level: SecurityLevel.BLOCKED,
        red_line: RedLineLevel.VIOLATION,
        blocked_reason: '离线模式无法完整审计·禁止执行',
        detected_threats: ['离线模式安全加强'],
        audit_color: '🔴',
        should_audit: true
      }
    }
    return {
      security_level: SecurityLevel.SAFE,
      red_line: RedLineLevel.NONE,
      detected_threats: [],
      audit_color: '🟢',
      should_audit: false
    }
  }
}
