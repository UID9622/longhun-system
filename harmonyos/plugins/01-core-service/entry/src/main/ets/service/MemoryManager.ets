/**
 * 🐉 龍魂·记忆管理器 (Memory Manager)
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-MEMORY-MANAGER-UID9622
 *
 * P0 永恒级 / P1 重要 / P2 普通 / P3 临时 四级存储
 * 使用 @ohos.data.preferences 持久化
 * 关键词检索 + 模糊匹配 + DNA 追溯码生成
 */

import { preferences } from '@kit.ArkData';
import { Context } from '@kit.AbilityKit';

// ─── 记忆优先级枚举 ───
export enum MemoryPriority {
  P0_ETERNAL = 0,  // 永恒级·不可删除
  P1_IMPORTANT = 1, // 重要·年维度
  P2_NORMAL = 2,    // 普通·月维度
  P3_TEMPORARY = 3  // 临时·周维度
}

// ─── 记忆条目定义 ───
export interface MemoryEntry {
  id: string;                    // 唯一ID
  dna: string;                   // DNA 追溯码
  priority: MemoryPriority;      // 优先级
  category: string;              // 分类
  content: string;               // 内容
  keywords: string[];            // 关键词
  timestamp: string;             // ISO 时间戳
  ttl_days: number;              // 存活天数 (-1=永久)
  tricolor: string;              // 三色状态
  source: string;                // 来源
}

// ─── 查询结果 ───
export interface MemoryQueryResult {
  query: string;
  total: number;
  matches: MemoryEntry[];
  elapsed_ms: number;
}

// ─── P0-P3 TTL 配置 ───
const LEVEL_CONFIG: Record<number, { name: string; ttlDays: number }> = {
  [MemoryPriority.P0_ETERNAL]: { name: '永恒级', ttlDays: -1 },
  [MemoryPriority.P1_IMPORTANT]: { name: '重要级', ttlDays: 365 },
  [MemoryPriority.P2_NORMAL]: { name: '普通级', ttlDays: 30 },
  [MemoryPriority.P3_TEMPORARY]: { name: '临时级', ttlDays: 7 },
};

/**
 * 记忆管理器
 */
export class MemoryManager {
  private memories: MemoryEntry[] = [];
  private dataStore?: preferences.Preferences;
  private dnaSeed: string = '';

  /**
   * 初始化
   */
  initialize(context: Context): void {
    this.dnaSeed = `#龍芯⚡️${new Date().toISOString().split('T')[0]}-HARMONYOS-MEMORY`;

    // 加载持久化记忆
    try {
      this.dataStore = preferences.getPreferencesSync(context, { name: 'longhun_memory_store' });
      const raw = this.dataStore.getSync('memories', '[]') as string;
      this.memories = JSON.parse(raw);
      console.info(`[龍魂·记忆] 已加载 ${this.memories.length} 条记忆`);
    } catch (error) {
      console.warn(`[龍魂·记忆] 无已有记忆，从零开始`);
      this.memories = [];
    }

    // 写入P0锚点记忆
    this.ensureP0Anchors();
  }

  /**
   * 确保P0焊死锚点记忆存在
   */
  private ensureP0Anchors(): void {
    const anchors: MemoryEntry[] = [
      {
        id: 'P0-DNA',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-PLUGIN-CORE-SERVICE-UID9622',
        priority: MemoryPriority.P0_ETERNAL,
        category: '身份',
        content: 'UID9622·诸葛鑫·龍芯北辰·唯一主权人',
        keywords: ['UID9622', '主权', '身份', 'DNA'],
        timestamp: new Date().toISOString(),
        ttl_days: -1,
        tricolor: '🟢',
        source: 'system'
      },
      {
        id: 'P0-CONFIRM',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-CONFIRM-UID9622',
        priority: MemoryPriority.P0_ETERNAL,
        category: '协议',
        content: '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z',
        keywords: ['确认码', 'CONFIRM', '9622'],
        timestamp: new Date().toISOString(),
        ttl_days: -1,
        tricolor: '🟢',
        source: 'system'
      },
      {
        id: 'P0-SOVEREIGNTY',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-SOVEREIGNTY-UID9622',
        priority: MemoryPriority.P0_ETERNAL,
        category: '主权',
        content: '#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL',
        keywords: ['主权锚定', '设备绑定', 'SOVEREIGNTY'],
        timestamp: new Date().toISOString(),
        ttl_days: -1,
        tricolor: '🟢',
        source: 'system'
      },
      {
        id: 'P0-369',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-369-UID9622',
        priority: MemoryPriority.P0_ETERNAL,
        category: '底座',
        content: '369不动点: sn=369, log369=5.911, perm369=108',
        keywords: ['369', '洛书', '不动点', '底座'],
        timestamp: new Date().toISOString(),
        ttl_days: -1,
        tricolor: '🟢',
        source: 'system'
      }
    ];

    for (const anchor of anchors) {
      if (!this.memories.find(m => m.id === anchor.id)) {
        this.memories.push(anchor);
      }
    }
  }

  /**
   * 添加记忆
   */
  add(content: string, priority: MemoryPriority = MemoryPriority.P2_NORMAL, category: string = '通用'): MemoryEntry {
    const entry: MemoryEntry = {
      id: `MEM-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      dna: `${this.dnaSeed}-${this.generateDnaShort()}`,
      priority,
      category,
      content,
      keywords: this.extractKeywords(content),
      timestamp: new Date().toISOString(),
      ttl_days: LEVEL_CONFIG[priority]?.ttlDays ?? 30,
      tricolor: '🟢',
      source: 'user'
    };

    this.memories.push(entry);
    this.persist();
    console.info(`[龍魂·记忆] P${priority} 记忆已添加: ${content.substring(0, 50)}...`);
    return entry;
  }

  /**
   * 查询记忆
   */
  query(queryStr: string): string {
    const startTime = Date.now();
    const lowerQuery = queryStr.toLowerCase();
    const terms = lowerQuery.split(/\s+/).filter(t => t.length > 0);

    const matches = this.memories.filter(m => {
      const text = (m.content + ' ' + m.keywords.join(' ') + ' ' + m.category).toLowerCase();
      return terms.every(term => text.includes(term));
    });

    // P0优先 → P1 → P2 → P3 排序
    matches.sort((a, b) => a.priority - b.priority);

    const result: MemoryQueryResult = {
      query: queryStr,
      total: matches.length,
      matches: matches.slice(0, 100), // 限制返回100条
      elapsed_ms: Date.now() - startTime
    };

    return JSON.stringify(result);
  }

  /**
   * 按优先级获取记忆
   */
  getByPriority(priority: MemoryPriority): MemoryEntry[] {
    return this.memories.filter(m => m.priority === priority);
  }

  /**
   * 获取记忆总数
   */
  getTotalCount(): number {
    return this.memories.length;
  }

  /**
   * 获取各级别统计
   */
  getStats(): Record<string, number> {
    return {
      P0: this.memories.filter(m => m.priority === MemoryPriority.P0_ETERNAL).length,
      P1: this.memories.filter(m => m.priority === MemoryPriority.P1_IMPORTANT).length,
      P2: this.memories.filter(m => m.priority === MemoryPriority.P2_NORMAL).length,
      P3: this.memories.filter(m => m.priority === MemoryPriority.P3_TEMPORARY).length,
    };
  }

  /**
   * 清理过期记忆（P0永不清理）
   */
  cleanExpired(): number {
    const now = Date.now();
    const before = this.memories.length;

    this.memories = this.memories.filter(m => {
      if (m.priority === MemoryPriority.P0_ETERNAL) return true;
      if (m.ttl_days <= 0) return true;
      const age = (now - new Date(m.timestamp).getTime()) / (1000 * 60 * 60 * 24);
      return age <= m.ttl_days;
    });

    const removed = before - this.memories.length;
    if (removed > 0) {
      this.persist();
      console.info(`[龍魂·记忆] 清理 ${removed} 条过期记忆`);
    }
    return removed;
  }

  /**
   * 导出全部记忆（用于搬迁）
   */
  exportAll(): MemoryEntry[] {
    return [...this.memories];
  }

  /**
   * 持久化到 Preferences
   */
  persist(): void {
    if (this.dataStore) {
      try {
        this.dataStore.putSync('memories', JSON.stringify(this.memories));
        this.dataStore.flushSync();
      } catch (error) {
        console.error(`[龍魂·记忆] 持久化失败: ${JSON.stringify(error)}`);
      }
    }
  }

  /**
   * 提取关键词（简化版）
   */
  private extractKeywords(text: string): string[] {
    // 去掉标点、按空格/中文分词
    const cleaned = text.replace(/[，。！？、；：""''（）【】《》\n\r\t.,!?;:'"()\[\]{}]/g, ' ');
    const words = cleaned.split(/\s+/).filter(w => w.length >= 2);
    // 简单去重
    return [...new Set(words)].slice(0, 10);
  }

  /**
   * 生成 DNA 短码
   */
  private generateDnaShort(): string {
    const chars = '0123456789abcdef';
    let short = '';
    for (let i = 0; i < 8; i++) {
      short += chars[Math.floor(Math.random() * 16)];
    }
    return short;
  }
}
