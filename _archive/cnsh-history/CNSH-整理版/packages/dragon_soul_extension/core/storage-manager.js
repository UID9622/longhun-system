// core/storage-manager.js - IndexedDB 存储管理器
// DNA: #龍芯⚡️2026-03-03-存储管理器-浏览器版

class StorageManager {
  constructor() {
    this.dbName = '龍魂记忆库';
    this.dbVersion = 1;
    this.storeName = '记忆库';
    this.db = null;
  }

  /**
   * 初始化数据库
   * @returns {Promise<void>}
   */
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        console.log('✅ 存储系统初始化完成');
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // 创建记忆库存储
        if (!db.objectStoreNames.contains(this.storeName)) {
          const store = db.createObjectStore(this.storeName, { keyPath: 'DNA' });
          store.createIndex('创建时间', '创建时间', { unique: false });
          store.createIndex('太极变量.情感', '太极变量.情感', { unique: false });
          store.createIndex('太极变量.重要程度', '太极变量.重要程度', { unique: false });
        }

        // 创建压缩库存储
        if (!db.objectStoreNames.contains('压缩库')) {
          const store = db.createObjectStore('压缩库', { keyPath: 'DNA' });
          store.createIndex('压缩级别', '压缩数据.压缩级别', { unique: false });
        }

        // 创建配置库存储
        if (!db.objectStoreNames.contains('配置库')) {
          db.createObjectStore('配置库', { keyPath: 'key' });
        }
      };
    });
  }

  /**
   * 保存记忆
   * @param {object} memory - 记忆对象
   * @returns {Promise<void>}
   */
  async saveMemory(memory) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction([this.storeName], 'readwrite');
      const req = tx.objectStore(this.storeName).put(memory);

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve();
    });
  }

  /**
   * 获取记忆
   * @param {string} dna - DNA 追溯码
   * @returns {Promise<object|null>}
   */
  async getMemory(dna) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction([this.storeName], 'readonly');
      const req = tx.objectStore(this.storeName).get(dna);

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve(req.result || null);
    });
  }

  /**
   * 获取所有记忆
   * @returns {Promise<Array>}
   */
  async getAllMemories() {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction([this.storeName], 'readonly');
      const req = tx.objectStore(this.storeName).getAll();

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve(req.result || []);
    });
  }

  /**
   * 删除记忆
   * @param {string} dna - DNA 追溯码
   * @returns {Promise<void>}
   */
  async deleteMemory(dna) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction([this.storeName], 'readwrite');
      const req = tx.objectStore(this.storeName).delete(dna);

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve();
    });
  }

  /**
   * 批量保存记忆
   * @param {Array} memories - 记忆数组
   * @returns {Promise<void>}
   */
  async batchSaveMemories(memories) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction([this.storeName], 'readwrite');
      const store = tx.objectStore(this.storeName);

      memories.forEach(memory => {
        store.put(memory);
      });

      tx.onerror = () => reject(tx.error);
      tx.oncomplete = () => resolve();
    });
  }

  /**
   * 搜索记忆
   * @param {object} filters - 过滤条件
   * @returns {Promise<Array>}
   */
  async searchMemories(filters = {}) {
    const memories = await this.getAllMemories();

    return memories.filter(memory => {
      // 按关键词过滤
      if (filters.keyword) {
        const keywords = memory.太极变量.关键词.map(k => k.词);
        if (!keywords.some(k => k.includes(filters.keyword))) {
          return false;
        }
      }

      // 按情感过滤
      if (filters.emotion) {
        if (memory.太极变量.情感 !== filters.emotion) {
          return false;
        }
      }

      // 按重要程度过滤
      if (filters.importanceMin !== undefined) {
        if (memory.太极变量.重要程度 < filters.importanceMin) {
          return false;
        }
      }

      // 按日期范围过滤
      if (filters.startDate) {
        const memoryDate = new Date(memory.创建时间);
        if (memoryDate < new Date(filters.startDate)) {
          return false;
        }
      }

      if (filters.endDate) {
        const memoryDate = new Date(memory.创建时间);
        if (memoryDate > new Date(filters.endDate)) {
          return false;
        }
      }

      return true;
    });
  }

  /**
   * 获取存储统计信息
   * @returns {Promise<object>}
   */
  async getStatistics() {
    const memories = await this.getAllMemories();

    const stats = {
      总数: memories.length,
      总大小: 0,
      按情感统计: {},
      按重要程度统计: {},
      按日期统计: {},
      平均压缩率: 0
    };

    let totalCompressionRate = 0;

    memories.forEach(memory => {
      // 计算大小
      stats.总大小 += JSON.stringify(memory).length;

      // 按情感统计
      const emotion = memory.太极变量.情感;
      stats.按情感统计[emotion] = (stats.按情感统计[emotion] || 0) + 1;

      // 按重要程度统计
      const importance = memory.太极变量.重要程度;
      stats.按重要程度统计[importance] = (stats.按重要程度统计[importance] || 0) + 1;

      // 按日期统计
      const date = memory.创建时间.split('T')[0];
      stats.按日期统计[date] = (stats.按日期统计[date] || 0) + 1;

      // 累加压缩率
      if (memory.压缩数据 && memory.压缩数据.压缩率) {
        totalCompressionRate += memory.压缩数据.压缩率;
      }
    });

    // 计算平均压缩率
    if (memories.length > 0) {
      stats.平均压缩率 = Math.round(totalCompressionRate / memories.length);
    }

    // 转换大小为 KB
    stats.总大小KB = Math.round(stats.总大小 / 1024);

    return stats;
  }

  /**
   * 清理过期记忆
   * @param {number} days - 保留天数
   * @returns {Promise<number>} 删除的数量
   */
  async cleanupOldMemories(days = 30) {
    const memories = await this.getAllMemories();
    const cutoffTime = new Date(Date.now() - days * 24 * 60 * 60 * 1000);

    const toDelete = memories.filter(m => new Date(m.创建时间) < cutoffTime);

    for (const memory of toDelete) {
      await this.deleteMemory(memory.DNA);
    }

    return toDelete.length;
  }

  /**
   * 导出所有记忆
   * @returns {Promise<string>} JSON 字符串
   */
  async exportAllMemories() {
    const memories = await this.getAllMemories();

    return JSON.stringify({
      version: 'v2.0',
      exportTime: new Date().toISOString(),
      count: memories.length,
      memories: memories
    }, null, 2);
  }

  /**
   * 导入记忆
   * @param {string} json - JSON 字符串
   * @returns {Promise<number>} 导入的数量
   */
  async importMemories(json) {
    try {
      const data = JSON.parse(json);
      const memories = data.memories || [];

      for (const memory of memories) {
        await this.saveMemory(memory);
      }

      return memories.length;
    } catch (error) {
      console.error('导入失败:', error);
      throw error;
    }
  }

  /**
   * 保存配置
   * @param {string} key - 配置键
   * @param {any} value - 配置值
   * @returns {Promise<void>}
   */
  async saveConfig(key, value) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(['配置库'], 'readwrite');
      const req = tx.objectStore('配置库').put({ key, value });

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve();
    });
  }

  /**
   * 获取配置
   * @param {string} key - 配置键
   * @returns {Promise<any>}
   */
  async getConfig(key) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(['配置库'], 'readonly');
      const req = tx.objectStore('配置库').get(key);

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve(req.result ? req.result.value : null);
    });
  }

  /**
   * 清空所有数据
   * @returns {Promise<void>}
   */
  async clearAll() {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction([this.storeName], 'readwrite');
      const req = tx.objectStore(this.storeName).clear();

      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve();
    });
  }

  /**
   * 关闭数据库连接
   */
  close() {
    if (this.db) {
      this.db.close();
      this.db = null;
    }
  }
}

// 全局单例
window.storageManager = new StorageManager();
