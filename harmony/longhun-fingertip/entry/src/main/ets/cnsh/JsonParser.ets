// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-CNSH-Lite-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * CNSH-Lite JSON解析器 v1.1
 *
 * 第二步起步——不是完整运行时，只是JSON解析器。
 * 能读DNA注册表、审计标签，不做本地生成。
 * 生成仍走鲲鹏API，端侧只负责展示和查询。
 *
 * 限制（v1.1降级）：
 * - ❌ 不本地生成DNA（走鲲鹏API）
 * - ❌ 不本地计算审计标签（走鲲鹏API）
 * - ✅ 本地读取DNA注册表JSON
 * - ✅ 本地展示审计标签
 * - ✅ DNA条目查询·过滤·排序
 */

/** DNA注册表顶层结构 */
export interface DnaRegistryHeader {
  generated: string
  root: string
  mode: string
  since_ts: number
  dna_valid: number
  dna_invalid: number
  no_dna: number
  total_registered: number
  alignment_rate: number
  diff: DnaDiff
  by_layer: Record<string, number>
  by_status: Record<string, number>
}

export interface DnaDiff {
  added: number
  updated: number
  unchanged: number
  removed: number
}

/** DNA注册表单条目 */
export interface DnaRegistryEntry {
  file: string
  dna: string
  date: string
  module: string
  version: string
  valid: boolean
  layer: LayerLevel
  status: AuditColor
  priority: number
  weight: number
  mtime: number
}

/** 五层架构 */
export type LayerLevel = 'L0_ETERNAL' | 'L1_SEASONAL' | 'L2_DECISION' | 'L3_GENERATIONAL' | 'L4_INSTANT'

/** 三色审计 */
export type AuditColor = '🟢' | '🟡' | '🔴'

/** DNA注册表完整数据 */
export interface DnaRegistry {
  header: DnaRegistryHeader
  entries: DnaRegistryEntry[]
}

/** DNA查询过滤条件 */
export interface DnaQueryFilter {
  layer?: LayerLevel
  status?: AuditColor
  module?: string
  keyword?: string
  dateFrom?: string
  dateTo?: string
  minWeight?: number
}

/** DNA查询结果 */
export interface DnaQueryResult {
  total: number
  matched: number
  entries: DnaRegistryEntry[]
  filter: DnaQueryFilter
}

/** 审计标签 */
export interface AuditLabel {
  color: AuditColor
  label: string
  description: string
  requires_action: boolean
}

/** 层名中文映射 */
const LAYER_NAMES: Record<LayerLevel, string> = {
  L0_ETERNAL: '永恒层',
  L1_SEASONAL: '季候层',
  L2_DECISION: '决策层',
  L3_GENERATIONAL: '代际层',
  L4_INSTANT: '瞬时层'
}

/** 审计标签映射 */
const AUDIT_LABELS: Record<AuditColor, AuditLabel> = {
  '🟢': { color: '🟢', label: '通过', description: '全检查点通过·放行', requires_action: false },
  '🟡': { color: '🟡', label: '待核', description: '推演/待实测/待用户数据·标记+通知', requires_action: true },
  '🔴': { color: '🔴', label: '红线', description: '安全风险·立即停止+锁定+DNA追溯', requires_action: true }
}

export class CnsHJsonParser {
  private registry: DnaRegistry | null = null
  private loadedAt: number = 0

  /**
   * 加载DNA注册表JSON字符串
   * @param jsonStr DNA注册表JSON原始字符串
   * @returns 解析后的注册表，失败返回null
   */
  loadRegistry(jsonStr: string): DnaRegistry | null {
    try {
      const raw = JSON.parse(jsonStr) as Record<string, Object>
      const header = this.parseHeader(raw)
      const entries = this.parseEntries(raw)
      this.registry = { header, entries }
      this.loadedAt = Date.now()
      console.info(`[CNSH-Lite] DNA注册表加载完成: ${entries.length}条目, 对齐率${header.alignment_rate}%`)
      return this.registry
    } catch (err) {
      console.error(`[CNSH-Lite] DNA注册表解析失败: ${JSON.stringify(err)}`)
      return null
    }
  }

  /** 解析注册表头部 */
  private parseHeader(raw: Record<string, Object>): DnaRegistryHeader {
    return {
      generated: raw['generated'] as string ?? '',
      root: raw['root'] as string ?? '',
      mode: raw['mode'] as string ?? 'full',
      since_ts: raw['since_ts'] as number ?? 0,
      dna_valid: raw['dna_valid'] as number ?? 0,
      dna_invalid: raw['dna_invalid'] as number ?? 0,
      no_dna: raw['no_dna'] as number ?? 0,
      total_registered: raw['total_registered'] as number ?? 0,
      alignment_rate: raw['alignment_rate'] as number ?? 0,
      diff: this.parseDiff(raw['diff']),
      by_layer: this.toRecord(raw['by_layer']),
      by_status: this.toRecord(raw['by_status'])
    }
  }

  /** 解析差异数据 */
  private parseDiff(raw: unknown): DnaDiff {
    if (typeof raw !== 'object' || raw === null) {
      return { added: 0, updated: 0, unchanged: 0, removed: 0 }
    }
    const d = raw as Record<string, unknown>
    return {
      added: d['added'] as number ?? 0,
      updated: d['updated'] as number ?? 0,
      unchanged: d['unchanged'] as number ?? 0,
      removed: d['removed'] as number ?? 0
    }
  }

  /** 通用对象转Record<string,number> */
  private toRecord(raw: unknown): Record<string, number> {
    if (typeof raw !== 'object' || raw === null) return {}
    const result: Record<string, number> = {}
    const obj = raw as Record<string, unknown>
    for (const key of Object.keys(obj)) {
      result[key] = Number(obj[key]) || 0
    }
    return result
  }

  /** 解析条目数组 */
  private parseEntries(raw: Record<string, Object>): DnaRegistryEntry[] {
    const entriesRaw = raw['entries']
    if (!Array.isArray(entriesRaw)) return []

    return entriesRaw.map((e: Record<string, unknown>, i: number): DnaRegistryEntry => {
      return {
        file: e['file'] as string ?? `unknown-${i}`,
        dna: e['dna'] as string ?? '',
        date: e['date'] as string ?? '',
        module: e['module'] as string ?? 'UNKNOWN',
        version: e['version'] as string ?? '0.0',
        valid: e['valid'] as boolean ?? true,
        layer: (e['layer'] as LayerLevel) ?? 'L3_GENERATIONAL',
        status: (e['status'] as AuditColor) ?? '🟢',
        priority: e['priority'] as number ?? 0,
        weight: e['weight'] as number ?? 1.0,
        mtime: e['mtime'] as number ?? 0
      }
    })
  }

  /**
   * 查询DNA条目
   * @param filter 查询过滤条件
   * @returns 查询结果
   */
  query(filter: DnaQueryFilter = {}): DnaQueryResult {
    if (!this.registry) {
      return { total: 0, matched: 0, entries: [], filter }
    }

    let matched = this.registry.entries.filter((entry: DnaRegistryEntry) => {
      if (filter.layer && entry.layer !== filter.layer) return false
      if (filter.status && entry.status !== filter.status) return false
      if (filter.module && !entry.module.toUpperCase().includes(filter.module.toUpperCase())) return false
      if (filter.keyword) {
        const kw = filter.keyword.toLowerCase()
        const inFile = entry.file.toLowerCase().includes(kw)
        const inDna = entry.dna.toLowerCase().includes(kw)
        const inModule = entry.module.toLowerCase().includes(kw)
        if (!inFile && !inDna && !inModule) return false
      }
      if (filter.dateFrom && entry.date < filter.dateFrom) return false
      if (filter.dateTo && entry.date > filter.dateTo) return false
      if (filter.minWeight !== undefined && entry.weight < filter.minWeight) return false
      return true
    })

    // 按权重降序排列
    matched.sort((a: DnaRegistryEntry, b: DnaRegistryEntry) => b.weight - a.weight)

    return {
      total: this.registry.entries.length,
      matched: matched.length,
      entries: matched,
      filter
    }
  }

  /**
   * 按文件路径精确查找DNA条目
   */
  findByFile(filePath: string): DnaRegistryEntry | null {
    if (!this.registry) return null
    return this.registry.entries.find((e: DnaRegistryEntry) => e.file === filePath) ?? null
  }

  /**
   * 按模块名查找
   */
  findByModule(moduleName: string): DnaRegistryEntry[] {
    if (!this.registry) return []
    return this.registry.entries.filter((e: DnaRegistryEntry) =>
      e.module.toUpperCase() === moduleName.toUpperCase()
    )
  }

  /**
   * 获取统计摘要
   */
  getSummary(): DnaRegistryHeader | null {
    return this.registry?.header ?? null
  }

  /**
   * 获取层名中文
   */
  getLayerName(layer: LayerLevel): string {
    return LAYER_NAMES[layer] ?? layer
  }

  /**
   * 解析审计标签
   */
  getAuditLabel(color: AuditColor): AuditLabel {
    return AUDIT_LABELS[color] ?? {
      color: color,
      label: '未知',
      description: '未知审计状态',
      requires_action: true
    }
  }

  /**
   * 获取所有审计标签定义
   */
  getAllAuditLabels(): AuditLabel[] {
    return Object.values(AUDIT_LABELS)
  }

  /**
   * 检查是否需要行动（🟡或🔴）
   */
  needsAction(color: AuditColor): boolean {
    return color === '🟡' || color === '🔴'
  }

  /**
   * 获取各层统计
   */
  getLayerStats(): { layer: LayerLevel; name: string; count: number }[] {
    if (!this.registry) return []
    return Object.entries(this.registry.header.by_layer).map(([layer, count]) => ({
      layer: layer as LayerLevel,
      name: this.getLayerName(layer as LayerLevel),
      count
    }))
  }

  /**
   * 获取状态统计
   */
  getStatusStats(): { status: AuditColor; label: string; count: number }[] {
    if (!this.registry) return []
    return Object.entries(this.registry.header.by_status).map(([status, count]) => ({
      status: status as AuditColor,
      label: this.getAuditLabel(status as AuditColor).label,
      count
    }))
  }

  /**
   * 注册表是否已加载
   */
  isLoaded(): boolean {
    return this.registry !== null
  }

  /**
   * 加载时间
   */
  getLoadedAt(): number {
    return this.loadedAt
  }
}
