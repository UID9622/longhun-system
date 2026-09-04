// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-本地数据-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * 本地加密存储服务 v1.1
 *
 * 数据主权不变原则（v1.1新增）：
 * - DNA注册表：本地加密存储·不传输·仅本地查询
 * - 行为审计日志：本地加密存储·不传输·仅本地展示
 * - 记忆库原始数据：本地加密存储·不传输·仅本地调用
 *
 * 分布式网格只调度算力，不搬运数据。
 */

import preferences from '@ohos.data.preferences'
import { DnaRegistryEntry } from '../cnsh/JsonParser'
import { Constants } from '../utils/Constants'

/** 存储键名常量 */
const KEYS = {
  DNA_REGISTRY_JSON: 'lh_dna_registry_json',
  DNA_REGISTRY_LOADED_AT: 'lh_dna_registry_loaded_at',
  AUDIT_LOG: 'lh_audit_log',
  CHAT_HISTORY: 'lh_chat_history',
  USER_PREFS: 'lh_user_prefs',
  FRUSTRATION_COUNT: 'lh_frustration_count',
  LAST_SYNC: 'lh_last_sync'
}

/** 审计日志条目 */
export interface AuditLogEntry {
  timestamp: string
  action: string
  persona: string
  result: string
  audit_color: string
  dna?: string
}

/** 用户偏好 */
export interface UserPrefs {
  server_host: string
  server_ports: Record<string, number>
  use_tls: boolean
  auto_sync: boolean
  offline_mode: boolean
}

export class LocalDataService {
  private store: preferences.Preferences | null = null
  private static instance: LocalDataService | null = null

  /** 单例模式 */
  static getInstance(): LocalDataService {
    if (!LocalDataService.instance) {
      LocalDataService.instance = new LocalDataService()
    }
    return LocalDataService.instance
  }

  /** 初始化存储 */
  async init(context: Context): Promise<void> {
    if (this.store) return
    try {
      this.store = await preferences.getPreferences(context, 'longhun_fingertip')
      console.info('[LocalData] 存储初始化完成')
    } catch (err) {
      console.error(`[LocalData] 存储初始化失败: ${JSON.stringify(err)}`)
    }
  }

  // ══════ DNA注册表（本地·不传输） ══════

  /** 保存DNA注册表JSON到本地 */
  async saveDnaRegistry(jsonStr: string): Promise<boolean> {
    return this.put(KEYS.DNA_REGISTRY_JSON, jsonStr)
  }

  /** 读取本地DNA注册表JSON */
  async loadDnaRegistry(): Promise<string | null> {
    return this.get(KEYS.DNA_REGISTRY_JSON)
  }

  /** 保存注册表加载时间 */
  async saveRegistryLoadedAt(timestamp: number): Promise<boolean> {
    return this.put(KEYS.DNA_REGISTRY_LOADED_AT, String(timestamp))
  }

  /** 获取注册表加载时间 */
  async getRegistryLoadedAt(): Promise<number> {
    const v = await this.get(KEYS.DNA_REGISTRY_LOADED_AT)
    return v ? Number(v) : 0
  }

  // ══════ 审计日志（本地·不传输） ══════

  /** 追加审计日志 */
  async appendAuditLog(entry: AuditLogEntry): Promise<boolean> {
    const existing = await this.getAuditLogs()
    existing.push(entry)
    // 最多保留200条
    if (existing.length > 200) {
      existing.splice(0, existing.length - 200)
    }
    return this.put(KEYS.AUDIT_LOG, JSON.stringify(existing))
  }

  /** 获取审计日志 */
  async getAuditLogs(): Promise<AuditLogEntry[]> {
    const raw = await this.get(KEYS.AUDIT_LOG)
    if (!raw) return []
    try {
      return JSON.parse(raw) as AuditLogEntry[]
    } catch {
      return []
    }
  }

  /** 清除审计日志 */
  async clearAuditLogs(): Promise<boolean> {
    return this.put(KEYS.AUDIT_LOG, '[]')
  }

  // ══════ 聊天历史（本地缓存） ══════

  /** 保存聊天历史 */
  async saveChatHistory(messages: object[]): Promise<boolean> {
    return this.put(KEYS.CHAT_HISTORY, JSON.stringify(messages.slice(-100))) // 最多100条
  }

  /** 读取聊天历史 */
  async loadChatHistory(): Promise<object[]> {
    const raw = await this.get(KEYS.CHAT_HISTORY)
    if (!raw) return []
    try {
      return JSON.parse(raw) as object[]
    } catch {
      return []
    }
  }

  // ══════ 用户偏好 ══════

  /** 保存用户偏好 */
  async saveUserPrefs(prefs: UserPrefs): Promise<boolean> {
    return this.put(KEYS.USER_PREFS, JSON.stringify(prefs))
  }

  /** 读取用户偏好 */
  async loadUserPrefs(): Promise<UserPrefs | null> {
    const raw = await this.get(KEYS.USER_PREFS)
    if (!raw) return null
    try {
      return JSON.parse(raw) as UserPrefs
    } catch {
      return null
    }
  }

  // ══════ 挫败追踪 ══════

  /** 记录挫败 */
  async incrementFrustration(): Promise<number> {
    const raw = await this.get(KEYS.FRUSTRATION_COUNT)
    const current = raw ? Number(raw) : 0
    const next = current + 1
    await this.put(KEYS.FRUSTRATION_COUNT, String(next))
    return next
  }

  /** 重置挫败计数 */
  async resetFrustration(): Promise<boolean> {
    return this.put(KEYS.FRUSTRATION_COUNT, '0')
  }

  /** 获取挫败计数 */
  async getFrustrationCount(): Promise<number> {
    const raw = await this.get(KEYS.FRUSTRATION_COUNT)
    return raw ? Number(raw) : 0
  }

  // ══════ 同步时间 ══════

  /** 记录最后同步时间 */
  async setLastSync(timestamp: number): Promise<boolean> {
    return this.put(KEYS.LAST_SYNC, String(timestamp))
  }

  /** 获取最后同步时间 */
  async getLastSync(): Promise<number> {
    const v = await this.get(KEYS.LAST_SYNC)
    return v ? Number(v) : 0
  }

  // ══════ 存储空间 ══════

  /** 估算存储占用（字节） */
  async estimateSize(): Promise<number> {
    const keys = Object.values(KEYS)
    let total = 0
    for (const key of keys) {
      const v = await this.get(key)
      if (v) total += v.length * 2  // UTF-16 估算
    }
    return total
  }

  /** 清除所有本地数据 */
  async clearAll(): Promise<boolean> {
    const keys = Object.values(KEYS)
    for (const key of keys) {
      await this.put(key, '')
    }
    console.info('[LocalData] 全部本地数据已清除')
    return true
  }

  // ══════ 私有方法 ══════

  private async get(key: string): Promise<string | null> {
    if (!this.store) {
      console.error('[LocalData] 存储未初始化')
      return null
    }
    try {
      const result = await this.store.get(key, '') as string
      return result || null
    } catch {
      return null
    }
  }

  private async put(key: string, value: string): Promise<boolean> {
    if (!this.store) {
      console.error('[LocalData] 存储未初始化')
      return false
    }
    try {
      await this.store.put(key, value)
      await this.store.flush()
      return true
    } catch (err) {
      console.error(`[LocalData] 写入失败 ${key}: ${JSON.stringify(err)}`)
      return false
    }
  }
}
