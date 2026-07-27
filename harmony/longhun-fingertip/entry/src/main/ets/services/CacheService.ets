// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { DnaEntry } from '../models/Types'

/**
 * DNA离线缓存服务
 * 本地DNA记忆存储·离线时仍可追溯·7天自动过期
 */
export class CacheService {
  private cache: Map<string, { data: string, expireAt: number }> = new Map()

  /** 保存DNA条目 */
  saveDna(entry: DnaEntry): void {
    const key = Constants.CACHE_PREFIX_DNA + entry.dna
    this.cache.set(key, {
      data: JSON.stringify(entry),
      expireAt: Date.now() + Constants.CACHE_TTL_MS
    })
    this.evict()
  }

  /** 批量保存DNA条目 */
  saveDnaBatch(entries: DnaEntry[]): void {
    entries.forEach(e => this.saveDna(e))
  }

  /** 获取DNA条目 */
  getDna(dna: string): DnaEntry | null {
    const key = Constants.CACHE_PREFIX_DNA + dna
    const cached = this.cache.get(key)
    if (!cached) return null
    if (Date.now() > cached.expireAt) {
      this.cache.delete(key)
      return null
    }
    try {
      return JSON.parse(cached.data) as DnaEntry
    } catch {
      return null
    }
  }

  /** 获取所有DNA缓存条目 */
  getAllDna(): DnaEntry[] {
    const entries: DnaEntry[] = []
    const now = Date.now()
    this.cache.forEach((v, k) => {
      if (k.startsWith(Constants.CACHE_PREFIX_DNA) && now <= v.expireAt) {
        try {
          const entry = JSON.parse(v.data) as DnaEntry
          entry.cached = true
          entries.push(entry)
        } catch {}
      }
    })
    return entries.sort((a, b) => b.timestamp.localeCompare(a.timestamp))
  }

  /** 保存聊天消息 */
  saveChat(id: string, messages: object[]): void {
    const key = Constants.CACHE_PREFIX_CHAT + id
    this.cache.set(key, {
      data: JSON.stringify(messages),
      expireAt: Date.now() + Constants.CACHE_TTL_MS
    })
  }

  /** 获取聊天历史 */
  getChat(id: string): object[] | null {
    const key = Constants.CACHE_PREFIX_CHAT + id
    const cached = this.cache.get(key)
    if (!cached || Date.now() > cached.expireAt) return null
    try {
      return JSON.parse(cached.data) as object[]
    } catch {
      return null
    }
  }

  /** 保存系统状态快照 */
  saveStatus(status: object): void {
    const key = Constants.CACHE_PREFIX_STATUS + 'latest'
    this.cache.set(key, {
      data: JSON.stringify(status),
      expireAt: Date.now() + 5 * 60 * 1000  // 5分钟过期
    })
  }

  /** 获取缓存状态快照 */
  getStatus(): object | null {
    const key = Constants.CACHE_PREFIX_STATUS + 'latest'
    const cached = this.cache.get(key)
    if (!cached || Date.now() > cached.expireAt) return null
    try { return JSON.parse(cached.data) } catch { return null }
  }

  /** 缓存总数 */
  count(): number {
    return this.cache.size
  }

  /** 清空缓存 */
  clear(): void {
    this.cache.clear()
  }

  /** 过期淘汰 */
  private evict(): void {
    if (this.cache.size <= Constants.MAX_CACHE_ITEMS) return
    const now = Date.now()
    // 先删过期的
    this.cache.forEach((v, k) => {
      if (now > v.expireAt) this.cache.delete(k)
    })
    // 如果还是超了，删最老的
    if (this.cache.size > Constants.MAX_CACHE_ITEMS) {
      const entries = Array.from(this.cache.entries())
        .sort((a, b) => a[1].expireAt - b[1].expireAt)
      const toDelete = entries.slice(0, this.cache.size - Constants.MAX_CACHE_ITEMS)
      toDelete.forEach(([k]) => this.cache.delete(k))
    }
  }
}
