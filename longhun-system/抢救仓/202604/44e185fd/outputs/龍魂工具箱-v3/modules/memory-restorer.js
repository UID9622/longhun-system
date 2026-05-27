// ===== 龍魂记忆还原器 =====

window.memoryRestorer = (function() {

  // 还原记忆
  async function restore(dna, compressedData, options = {}) {
    const { useStorage = true, requireFull = false } = options;

    try {
      // 尝试从存储中获取完整记忆
      if (useStorage && window.storageManager) {
        const stored = await window.storageManager.getMemory(dna);
        if (stored && stored.原始内容) {
          return {
            success: true,
            DNA: dna,
            原始内容: stored.原始内容,
            还原方式: 'full',
            还原质量: 100,
            来源: 'IndexedDB'
          };
        }
      }

      // 完整还原不可用，使用摘要还原
      if (requireFull) {
        return {
          success: false,
          DNA: dna,
          错误: '完整记忆不可用，且要求完整还原'
        };
      }

      // 摘要还原
      if (compressedData && compressedData.摘要) {
        let restoredContent = compressedData.摘要;

        // 尝试用关键词扩展
        if (compressedData.关键词保留 && compressedData.关键词保留.length > 0) {
          restoredContent += '\n\n[关键词]: ' + compressedData.关键词保留.join(', ');
        }

        const quality = Math.round(
          (compressedData.压缩后长度 / Math.max(compressedData.原始长度, 1)) * 100
        );

        return {
          success: true,
          DNA: dna,
          原始内容: restoredContent,
          还原方式: 'summary',
          还原质量: Math.min(quality + 20, 95),
          警告: '此为摘要还原，非完整原文。完整度约 ' + Math.min(quality + 20, 95) + '%',
          来源: '压缩数据'
        };
      }

      return {
        success: false,
        DNA: dna,
        错误: '无可用数据进行还原'
      };
    } catch (error) {
      return {
        success: false,
        DNA: dna,
        错误: error.message
      };
    }
  }

  // 批量还原
  async function batchRestore(items) {
    const results = [];
    for (const item of items) {
      const result = await restore(item.dna, item.compressedData, item.options || {});
      results.push(result);
    }
    return results;
  }

  return { restore, batchRestore };
})();
