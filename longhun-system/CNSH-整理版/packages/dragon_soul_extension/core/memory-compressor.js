// core/memory-compressor.js - 记忆压缩核心模块
// DNA: #龍芯⚡️2026-03-03-记忆压缩-浏览器版

class MemoryCompressor {
  constructor() {
    this.uid = "9622";
    this.dnaPrefix = "#龍芯⚡️";
    this.compressionLevels = {
      'light': { summaryLength: 200, keywordCount: 3 },
      'medium': { summaryLength: 100, keywordCount: 5 },
      'heavy': { summaryLength: 50, keywordCount: 7 }
    };
  }

  /**
   * 压缩记忆内容
   * @param {string} content - 原始内容
   * @param {object} taijiVars - 太极算法变量
   * @param {string} level - 压缩级别 (light/medium/heavy)
   * @returns {object} 压缩结果
   */
  compress(content, taijiVars, level = 'medium') {
    const config = this.compressionLevels[level] || this.compressionLevels['medium'];

    const compressed = {
      原始长度: content.length,
      压缩后长度: 0,
      压缩率: 0,
      摘要: '',
      关键词: taijiVars.关键词.slice(0, config.keywordCount),
      完整哈希: this.simpleHash(content),
      可还原: true,
      压缩级别: level,
      时间戳: new Date().toISOString()
    };

    // 生成智能摘要
    compressed.摘要 = this.generateSmartSummary(content, config.summaryLength);

    // 计算压缩后长度（摘要 + 关键词 + 哈希）
    compressed.压缩后长度 = compressed.摘要.length +
      JSON.stringify(compressed.关键词).length +
      compressed.完整哈希.length;

    // 计算压缩率
    compressed.压缩率 = Math.round((1 - compressed.压缩后长度 / compressed.原始长度) * 100);

    return compressed;
  }

  /**
   * 生成智能摘要
   * @param {string} content - 原始内容
   * @param {number} maxLength - 最大长度
   * @returns {string} 摘要
   */
  generateSmartSummary(content, maxLength) {
    if (content.length <= maxLength) {
      return content;
    }

    // 尝试在句子边界截断
    const sentences = content.split(/[。！？.!?]/);
    let summary = '';

    for (const sentence of sentences) {
      if (summary.length + sentence.length > maxLength) {
        break;
      }
      if (sentence.trim()) {
        summary += sentence.trim() + '。';
      }
    }

    // 如果摘要太短，直接截断
    if (summary.length < maxLength * 0.5) {
      summary = content.substring(0, maxLength - 3) + '...';
    } else if (summary.length > maxLength) {
      summary = summary.substring(0, maxLength - 3) + '...';
    }

    return summary;
  }

  /**
   * 简单哈希函数
   * @param {string} str - 输入字符串
   * @returns {string} 哈希值
   */
  simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).padStart(8, '0');
  }

  /**
   * 批量压缩记忆
   * @param {Array} memories - 记忆数组
   * @param {string} level - 压缩级别
   * @returns {Array} 压缩后的记忆数组
   */
  batchCompress(memories, level = 'medium') {
    return memories.map(memory => {
      const taijiVars = memory.太极变量 || this.extractTaijiVars(memory.原始内容);
      const compressed = this.compress(memory.原始内容, taijiVars, level);
      return {
        ...memory,
        压缩数据: compressed
      };
    });
  }

  /**
   * 估算压缩效果
   * @param {string} content - 原始内容
   * @returns {object} 压缩估算
   */
  estimateCompression(content) {
    const estimates = {};
    for (const [level, config] of Object.entries(this.compressionLevels)) {
      const taijiVars = this.extractTaijiVars(content);
      const compressed = this.compress(content, taijiVars, level);
      estimates[level] = {
        压缩率: compressed.压缩率,
        节省空间: compressed.原始长度 - compressed.压缩后长度,
        摘要长度: compressed.摘要.length,
        关键词数量: compressed.关键词.length
      };
    }
    return estimates;
  }

  /**
   * 提取太极算法变量（内部方法）
   * @param {string} content - 原始内容
   * @returns {object} 太极变量
   */
  extractTaijiVars(content) {
    const lines = content.split('\n');
    const wordCount = content.length;
    const keywords = this.extractKeywords(content);
    const emotion = this.analyzeEmotion(content);
    const importance = Math.min(10, Math.ceil(wordCount / 100) + keywords.length);

    return {
      字数: wordCount,
      行数: lines.length,
      关键词: keywords,
      情感: emotion,
      重要程度: importance,
      时间戳: new Date().toISOString(),
      创建者: this.uid
    };
  }

  /**
   * 提取关键词（内部方法）
   * @param {string} text - 文本
   * @returns {Array} 关键词数组
   */
  extractKeywords(text) {
    const stopWords = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'];
    const words = text.split(/[，。！？；：、\s]+/).filter(w => w.length > 1);
    const filtered = words.filter(w => !stopWords.includes(w));
    const freq = {};
    filtered.forEach(w => { freq[w] = (freq[w] || 0) + 1; });
    return Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([w]) => w);
  }

  /**
   * 分析情感（内部方法）
   * @param {string} text - 文本
   * @returns {string} 情感类型
   */
  analyzeEmotion(text) {
    const positive = ['开心', '快乐', '高兴', '幸福', '美好', '喜欢', '爱', '棒', '好', '成功'];
    const negative = ['难过', '悲伤', '痛苦', '失败', '糟糕', '讨厌', '恨', '差', '错误'];
    let pos = 0, neg = 0;
    positive.forEach(w => { if (text.includes(w)) pos++; });
    negative.forEach(w => { if (text.includes(w)) neg++; });
    if (pos > neg) return '积极';
    if (neg > pos) return '消极';
    return '平静';
  }
}

// 全局单例
window.memoryCompressor = new MemoryCompressor();
