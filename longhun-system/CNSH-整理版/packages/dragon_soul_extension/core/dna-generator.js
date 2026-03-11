// core/dna-generator.js - DNA追溯码生成器
// DNA: #龍芯⚡️2026-03-03-DNA生成器-浏览器版

class DNAGenerator {
  constructor() {
    this.uid = "9622";
    this.dnaPrefix = "#龍芯⚡️";
    this.version = "v2.0";
    this.gpgFingerprint = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F";
    this.confirmCode = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";
  }

  /**
   * 生成 DNA 追溯码
   * @param {string} content - 原始内容
   * @param {string} type - 类型 (MEMORY, EDITOR, SYSTEM等)
   * @returns {string} DNA 追溯码
   */
  generate(content, type = 'MEMORY') {
    const timestamp = new Date().toISOString().split('T')[0];
    const hash = this.generateHash(content);
    const random = this.generateRandomCode();

    return `${this.dnaPrefix}${timestamp}-${type}-${hash}-${random}-UID${this.uid}`;
  }

  /**
   * 生成哈希值
   * @param {string} content - 原始内容
   * @returns {string} 哈希值
   */
  generateHash(content) {
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).padStart(8, '0');
  }

  /**
   * 生成随机代码
   * @returns {string} 随机代码
   */
  generateRandomCode() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 4; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * 解析 DNA 追溯码
   * @param {string} dna - DNA 追溯码
   * @returns {object} 解析结果
   */
  parse(dna) {
    const pattern = new RegExp(`${this.dnaPrefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(\\d{4}-\\d{2}-\\d{2})-(\\w+)-([a-f0-9]{8})-([A-Z0-9]{4})-UID(\\d+)`);
    const match = dna.match(pattern);

    if (!match) {
      return {
        valid: false,
        error: 'DNA 格式无效'
      };
    }

    return {
      valid: true,
      prefix: this.dnaPrefix,
      date: match[1],
      type: match[2],
      hash: match[3],
      random: match[4],
      uid: match[5],
      original: dna
    };
  }

  /**
   * 验证 DNA 追溯码
   * @param {string} dna - DNA 追溯码
   * @param {string} content - 原始内容（可选，用于验证哈希）
   * @returns {object} 验证结果
   */
  validate(dna, content = null) {
    const parsed = this.parse(dna);

    if (!parsed.valid) {
      return {
        valid: false,
        error: parsed.error
      };
    }

    // 验证 UID
    if (parsed.uid !== this.uid) {
      return {
        valid: false,
        error: 'UID 不匹配',
        expected: this.uid,
        actual: parsed.uid
      };
    }

    // 如果提供了内容，验证哈希
    if (content) {
      const expectedHash = this.generateHash(content);
      if (parsed.hash !== expectedHash) {
        return {
          valid: false,
          error: '哈希不匹配',
          expected: expectedHash,
          actual: parsed.hash
        };
      }
    }

    return {
      valid: true,
      parsed: parsed
    };
  }

  /**
   * 生成确认码
   * @returns {string} 确认码
   */
  generateConfirmCode() {
    return this.confirmCode;
  }

  /**
   * 批量生成 DNA 追溯码
   * @param {Array} contents - 内容数组
   * @param {string} type - 类型
   * @returns {Array} DNA 追溯码数组
   */
  batchGenerate(contents, type = 'MEMORY') {
    return contents.map(content => this.generate(content, type));
  }

  /**
   * 搜索 DNA 追溯码
   * @param {string} query - 搜索查询
   * @param {Array} dnas - DNA 追溯码数组
   * @returns {Array} 匹配的 DNA 追溯码
   */
  search(query, dnas) {
    const lowerQuery = query.toLowerCase();
    return dnas.filter(dna => {
      const parsed = this.parse(dna);
      if (!parsed.valid) return false;

      return (
        dna.toLowerCase().includes(lowerQuery) ||
        parsed.date.includes(query) ||
        parsed.type.toLowerCase().includes(lowerQuery)
      );
    });
  }

  /**
   * 获取 DNA 统计信息
   * @param {Array} dnas - DNA 追溯码数组
   * @returns {object} 统计信息
   */
  getStatistics(dnas) {
    const stats = {
      total: dnas.length,
      byType: {},
      byDate: {},
      valid: 0,
      invalid: 0
    };

    dnas.forEach(dna => {
      const parsed = this.parse(dna);
      if (parsed.valid) {
        stats.valid++;
        stats.byType[parsed.type] = (stats.byType[parsed.type] || 0) + 1;
        stats.byDate[parsed.date] = (stats.byDate[parsed.date] || 0) + 1;
      } else {
        stats.invalid++;
      }
    });

    return stats;
  }

  /**
   * 导出 DNA 追溯码为 JSON
   * @param {Array} dnas - DNA 追溯码数组
   * @returns {string} JSON 字符串
   */
  exportToJSON(dnas) {
    const data = dnas.map(dna => {
      const parsed = this.parse(dna);
      return {
        dna: dna,
        parsed: parsed,
        valid: parsed.valid
      };
    });

    return JSON.stringify({
      version: this.version,
      uid: this.uid,
      gpgFingerprint: this.gpgFingerprint,
      timestamp: new Date().toISOString(),
      count: dnas.length,
      dnas: data
    }, null, 2);
  }

  /**
   * 从 JSON 导入 DNA 追溯码
   * @param {string} json - JSON 字符串
   * @returns {Array} DNA 追溯码数组
   */
  importFromJSON(json) {
    try {
      const data = JSON.parse(json);
      return data.dnas.map(item => item.dna);
    } catch (error) {
      console.error('导入失败:', error);
      return [];
    }
  }
}

// 全局单例
window.dnaGenerator = new DNAGenerator();
