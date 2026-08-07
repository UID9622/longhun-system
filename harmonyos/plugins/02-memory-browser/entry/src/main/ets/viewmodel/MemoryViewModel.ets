/**
 * 🐉 龍魂·MemoryViewModel — 记忆状态管理
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-MEMORY-VIEWMODEL-UID9622
 */

import { MemoryEntry, MemoryPriority } from '../../01-core-service/entry/src/main/ets/service/MemoryManager';
import { CoreServiceClient } from '../service/CoreServiceClient';

// 本地模拟数据结构（离线模式）
interface LocalMemoryEntry {
  id: string;
  dna: string;
  priority: number;
  category: string;
  content: string;
  keywords: string[];
  timestamp: string;
  tricolor: string;
}

@Observed
export class MemoryViewModel {
  memories: LocalMemoryEntry[] = [];
  loading: boolean = false;
  error: string = '';
  searchResults: LocalMemoryEntry[] = [];
  searchQuery: string = '';

  // 优先级颜色映射
  static readonly PRIORITY_COLORS: Record<number, string> = {
    0: '#E63946', // P0 永恒·红
    1: '#F4A261', // P1 重要·橙
    2: '#457B9D', // P2 普通·蓝
    3: '#A8DADC', // P3 临时·灰
  };

  static readonly PRIORITY_LABELS: Record<number, string> = {
    0: 'P0·永恒',
    1: 'P1·重要',
    2: 'P2·普通',
    3: 'P3·临时',
  };

  /**
   * 从核心服务加载记忆
   */
  async loadMemories(query: string = ''): Promise<void> {
    this.loading = true;
    this.error = '';

    try {
      const result = await CoreServiceClient.queryMemory(query || '*');
      const parsed = JSON.parse(result);
      this.memories = parsed.matches || [];
      if (parsed.total === 0) {
        this.error = '暂无记忆';
      }
    } catch (e) {
      // 离线模式：加载本地模拟数据
      this.memories = this.getLocalMockData();
      this.error = '（离线模式·本地数据）';
    } finally {
      this.loading = false;
    }
  }

  /**
   * 搜索记忆
   */
  async search(query: string): Promise<void> {
    this.searchQuery = query;
    await this.loadMemories(query);
  }

  /**
   * 按优先级过滤
   */
  filterByPriority(priority: number): LocalMemoryEntry[] {
    return this.memories.filter(m => m.priority === priority);
  }

  /**
   * 获取优先级统计
   */
  getStats(): Record<string, number> {
    return {
      'P0·永恒': this.memories.filter(m => m.priority === 0).length,
      'P1·重要': this.memories.filter(m => m.priority === 1).length,
      'P2·普通': this.memories.filter(m => m.priority === 2).length,
      'P3·临时': this.memories.filter(m => m.priority === 3).length,
    };
  }

  /**
   * 本地模拟数据（离线降级）
   */
  private getLocalMockData(): LocalMemoryEntry[] {
    return [
      {
        id: 'MEM-P0-001',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-UID9622',
        priority: 0,
        category: '身份',
        content: 'UID9622 = 诸葛鑫·Lucky·龍芯北辰·唯一主权人',
        keywords: ['UID9622', '主权', '身份', 'DNA'],
        timestamp: '2026-08-06T00:00:00+08:00',
        tricolor: '🟢'
      },
      {
        id: 'MEM-P1-001',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-DEPLOY-UID9622',
        priority: 1,
        category: '部署',
        content: '鲲鹏服务器 119.13.90.27·SSH key优先·华为云新加坡',
        keywords: ['鲲鹏', '部署', '服务器'],
        timestamp: '2026-08-05T12:00:00+08:00',
        tricolor: '🟢'
      },
      {
        id: 'MEM-P2-001',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-BUILD-UID9622',
        priority: 2,
        category: '构建',
        content: '鸿蒙插件生态10颗插件·分批构建·Rust核心库编译中',
        keywords: ['鸿蒙', '插件', '构建'],
        timestamp: '2026-08-06T01:00:00+08:00',
        tricolor: '🟢'
      },
      {
        id: 'MEM-P3-001',
        dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-TEMP-UID9622',
        priority: 3,
        category: '临时',
        content: '测试IPC连接·验证跨插件通信',
        keywords: ['测试', 'IPC', '通信'],
        timestamp: '2026-08-06T00:30:00+08:00',
        tricolor: '🟡'
      }
    ];
  }
}
