// core/memory-restorer.js - 记忆还原模块
// DNA: #龍芯⚡️2026-03-03-记忆还原-浏览器版

class MemoryRestorer {
  constructor() {
    this.uid = "9622";
    this.dnaPrefix = "#龍芯⚡️";
  }

  /**
   * 从 DNA 追溯码恢复记忆
   * @param {string} dna - DNA 追溯码
   * @param {object} compressedData - 压缩数据
   * @param {object} options - 还原选项
   * @returns {Promise<object>} 还原结果
   */
  async restore(dna, compressedData, options = {}) {
    const result = {
      success: false,
      dna: dna,
      原始内容: null,
      摘要: compressedData.摘要,
      关键词: compressedData.关键词,
      完整哈希: compressedData.完整哈希,
      还原方式: 'partial',
      还原质量: 0,
      错误: null
    };

    try {
      // 验证 DNA 格式
      const dnaValid = this.validateDNA(dna);
      if (!dnaValid.valid) {
        result.错误 = 'DNA 格式无效';
        return result;
      }

      // 检查是否需要完整还原
      if (options.requireFull && !compressedData.可还原) {
        result.错误 = '该记忆不可完整还原';
        return result;
      }

      // 尝试从存储中获取完整内容
      if (options.useStorage) {
        const fullContent = await this.restoreFromStorage(dna);
        if (fullContent) {
          result.原始内容 = fullContent;
          result.还原方式 = 'full';
          result.还原质量 = 100;
          result.success = true;
          return result;
        }
      }

      // 如果没有完整内容，生成摘要版本
      if (!result.原始内容) {
        result.原始内容 = this.generatePartialContent(compressedData);
        result.还原方式 = 'partial';
        result.还原质量 = this.calculateRestoreQuality(compressedData);
        result.success = true;
      }

      // 验证哈希（如果有完整内容）
      if (result.还原方式 === 'full') {
        const hash = this.generateHash(result.原始内容);
        if (hash !== compressedData.完整哈希) {
          result.警告 = '哈希验证失败，内容可能已损坏';
        }
      }

    } catch (error) {
      result.错误 = error.message;
      console.error('记忆还原失败:', error);
    }

    return result;
  }

  /**
   * 从存储中恢复记忆
   * @param {string} dna - DNA 追溯码
   * @returns {Promise<string|null>} 原始内容
   */
  async restoreFromStorage(dna) {
    try {
      if (window.storageManager) {
        const memory = await window.storageManager.getMemory(dna);
        return memory ? memory.原始内容 : null;
      }
      return null;
    } catch (error) {
      console.error('从存储恢复失败:', error);
      return null;
    }
  }

  /**
   * 生成部分内容（基于摘要和关键词）
   * @param {object} compressedData - 压缩数据
   * @returns {string} 部分内容
   */
  generatePartialContent(compressedData) {
    let content = '';

    // 添加摘要
    content += compressedData.摘要 + '\n\n';

    // 添加关键词
    if (compressedData.关键词 && compressedData.关键词.length > 0) {
      content += '【关键词】\n';
      if (Array.isArray(compressedData.关键词)) {
        content += compressedData.关键词.map(k => {
          if (typeof k === 'string') {
            return k;
          } else if (k.词) {
            return `${k.词} (${k.频次}次)`;
          } else {
            return JSON.stringify(k);
          }
        }).join('、');
      }
      content += '\n\n';
    }

    // 添加提示
    content += '【提示】\n';
    content += '这是压缩后的摘要版本。如需完整内容，请确保原始内容已保存到存储中。';

    return content;
  }

  /**
   * 计算还原质量
   * @param {object} compressedData - 压缩数据
   * @returns {number} 还原质量 (0-100)
   */
  calculateRestoreQuality(compressedData) {
    if (!compressedData) return 0;

    const summaryLength = compressedData.摘要 ? compressedData.摘要.length : 0;
    const originalLength = compressedData.原始长度 || 1;

    // 基于摘要长度与原长度的比例计算质量
    let quality = Math.round((summaryLength / originalLength) * 100);

    // 如果有关键词，加分
    if (compressedData.关键词 && compressedData.关键词.length > 0) {
      quality += 10;
    }

    // 限制在 0-100 之间
    return Math.min(100, Math.max(0, quality));
  }

  /**
   * 验证 DNA 格式
   * @param {string} dna - DNA 追溯码
   * @returns {object} 验证结果
   */
  validateDNA(dna) {
    if (!dna) {
      return { valid: false, error: 'DNA 为空' };
    }

    if (!dna.startsWith(this.dnaPrefix)) {
      return { valid: false, error: 'DNA 前缀不匹配' };
    }

    const pattern = new RegExp(`${this.dnaPrefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\d{4}-\\d{2}-\\d{2}-[\\w\\-]+-UID\\d+`);
    if (!pattern.test(dna)) {
      return { valid: false, error: 'DNA 格式不正确' };
    }

    return { valid: true };
  }

  /**
   * 生成哈希值
   * @param {string} content - 内容
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
   * 批量还原记忆
   * @param {Array} items - 记忆项数组
   * @param {object} options - 还原选项
   * @returns {Promise<Array>} 还原结果数组
   */
  async batchRestore(items, options = {}) {
    const results = [];

    for (const item of items) {
      const result = await this.restore(item.DNA, item.压缩数据, options);
      results.push(result);
    }

    return results;
  }

  /**
   * 验证还原完整性
   * @param {object} restoreResult - 还原结果
   * @returns {object} 验证结果
   */
  verifyRestore(restoreResult) {
    const verification = {
      完整: false,
      哈希匹配: false,
      内容完整: false,
      建议: []
    };

    if (!restoreResult.success) {
      verification.建议.push('还原失败，请检查 DNA 和压缩数据');
      return verification;
    }

    // 检查还原方式
    if (restoreResult.还原方式 === 'full') {
      verification.完整 = true;
      verification.内容完整 = true;
    } else {
      verification.建议.push('这是摘要版本，如需完整内容请确保原始内容已保存');
    }

    // 检查哈希
    if (restoreResult.原始内容) {
      const hash = this.generateHash(restoreResult.原始内容);
      verification.哈希匹配 = hash === restoreResult.完整哈希;

      if (!verification.哈希匹配) {
        verification.建议.push('哈希验证失败，内容可能已损坏');
      }
    }

    // 检查还原质量
    if (restoreResult.还原质量 < 50) {
      verification.建议.push('还原质量较低，建议从备份中恢复完整内容');
    }

    return verification;
  }

  /**
   * 生成还原报告
   * @param {Array} restoreResults - 还原结果数组
   * @returns {string} 报告文本
   */
  generateRestoreReport(restoreResults) {
    let report = '🧬 记忆还原报告\n\n';

    const total = restoreResults.length;
    const successful = restoreResults.filter(r => r.success).length;
    const fullRestore = restoreResults.filter(r => r.还原方式 === 'full').length;
    const partialRestore = restoreResults.filter(r => r.还原方式 === 'partial').length;
    const failed = restoreResults.filter(r => !r.success).length;

    report += `总计: ${total} 条\n`;
    report += `成功: ${successful} 条\n`;
    report += `完整还原: ${fullRestore} 条\n`;
    report += `部分还原: ${partialRestore} 条\n`;
    report += `失败: ${failed} 条\n\n`;

    const avgQuality = restoreResults.reduce((sum, r) => sum + (r.还原质量 || 0), 0) / total;
    report += `平均还原质量: ${Math.round(avgQuality)}%\n\n`;

    // 列出失败的项目
    if (failed > 0) {
      report += '❌ 失败项目:\n';
      restoreResults.filter(r => !r.success).forEach(r => {
        report += `  - ${r.DNA}: ${r.错误}\n`;
      });
      report += '\n';
    }

    // 列出警告
    const warnings = restoreResults.filter(r => r.警告);
    if (warnings.length > 0) {
      report += '⚠️ 警告:\n';
      warnings.forEach(r => {
        report += `  - ${r.DNA}: ${r.警告}\n`;
      });
    }

    return report;
  }

  /**
   * 导出还原结果为 JSON
   * @param {Array} restoreResults - 还原结果数组
   * @returns {string} JSON 字符串
   */
  exportToJSON(restoreResults) {
    return JSON.stringify({
      version: 'v2.0',
      exportTime: new Date().toISOString(),
      total: restoreResults.length,
      successful: restoreResults.filter(r => r.success).length,
      results: restoreResults
    }, null, 2);
  }
}

// 全局单例
window.memoryRestorer = new MemoryRestorer();
