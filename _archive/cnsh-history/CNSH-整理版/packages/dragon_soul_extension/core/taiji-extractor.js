// core/taiji-extractor.js - 太极算法变量提取器
// DNA: #龍芯⚡️2026-03-03-太极提取器-浏览器版

class TaijiExtractor {
  constructor() {
    this.uid = "9622";
    this.stopWords = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'];
    this.positiveWords = ['开心', '快乐', '高兴', '幸福', '美好', '喜欢', '爱', '棒', '好', '成功', '优秀', '完美', '精彩', '期待', '希望'];
    this.negativeWords = ['难过', '悲伤', '痛苦', '失败', '糟糕', '讨厌', '恨', '差', '错误', '失望', '担心', '焦虑', '害怕', '恐惧', '愤怒'];
  }

  /**
   * 提取太极算法变量
   * @param {string} content - 原始内容
   * @returns {object} 太极变量
   */
  extract(content) {
    const lines = content.split('\n');
    const wordCount = content.length;
    const keywords = this.extractKeywords(content);
    const emotion = this.analyzeEmotion(content);
    const importance = this.calculateImportance(content, keywords);
    const sentimentScore = this.calculateSentimentScore(content);

    return {
      字数: wordCount,
      行数: lines.length,
      关键词: keywords,
      情感: emotion,
      重要程度: importance,
      情感分数: sentimentScore,
      时间戳: new Date().toISOString(),
      创建者: this.uid,
      版本: 'v2.0'
    };
  }

  /**
   * 提取关键词
   * @param {string} text - 文本
   * @param {number} maxCount - 最大关键词数量
   * @returns {Array} 关键词数组
   */
  extractKeywords(text, maxCount = 5) {
    // 分词
    const words = text.split(/[，。！？；：、\s]+/).filter(w => w.length > 1);

    // 去除停用词
    const filtered = words.filter(w => !this.stopWords.includes(w));

    // 统计词频
    const freq = {};
    filtered.forEach(w => {
      freq[w] = (freq[w] || 0) + 1;
    });

    // 按词频排序
    const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]);

    // 返回前 N 个关键词
    return sorted.slice(0, maxCount).map(([w, count]) => ({
      词: w,
      频次: count
    }));
  }

  /**
   * 分析情感
   * @param {string} text - 文本
   * @returns {string} 情感类型
   */
  analyzeEmotion(text) {
    const sentimentScore = this.calculateSentimentScore(text);

    if (sentimentScore > 0.3) return '积极';
    if (sentimentScore < -0.3) return '消极';
    return '平静';
  }

  /**
   * 计算情感分数
   * @param {string} text - 文本
   * @returns {number} 情感分数 (-1 到 1)
   */
  calculateSentimentScore(text) {
    let pos = 0, neg = 0;

    this.positiveWords.forEach(w => {
      const regex = new RegExp(w, 'g');
      const matches = text.match(regex);
      if (matches) pos += matches.length;
    });

    this.negativeWords.forEach(w => {
      const regex = new RegExp(w, 'g');
      const matches = text.match(regex);
      if (matches) neg += matches.length;
    });

    const total = pos + neg;
    if (total === 0) return 0;

    return (pos - neg) / total;
  }

  /**
   * 计算重要程度
   * @param {string} content - 内容
   * @param {Array} keywords - 关键词
   * @returns {number} 重要程度 (1-10)
   */
  calculateImportance(content, keywords) {
    const wordCount = content.length;
    const keywordScore = keywords.reduce((sum, k) => sum + k.频次, 0);
    const sentenceCount = content.split(/[。！？.!?]/).length;

    // 基础分数：字数
    let score = Math.min(5, Math.ceil(wordCount / 200));

    // 关键词加分
    score += Math.min(3, Math.ceil(keywordScore / 2));

    // 句子数加分
    score += Math.min(2, Math.ceil(sentenceCount / 5));

    // 限制在 1-10 之间
    return Math.max(1, Math.min(10, score));
  }

  /**
   * 批量提取太极变量
   * @param {Array} contents - 内容数组
   * @returns {Array} 太极变量数组
   */
  batchExtract(contents) {
    return contents.map(content => this.extract(content));
  }

  /**
   * 比较两个太极变量
   * @param {object} vars1 - 太极变量1
   * @param {object} vars2 - 太极变量2
   * @returns {object} 比较结果
   */
  compare(vars1, vars2) {
    return {
      字数差异: vars2.字数 - vars1.字数,
      行数差异: vars2.行数 - vars1.行数,
      情感变化: vars1.情感 !== vars2.情感 ? `${vars1.情感} → ${vars2.情感}` : '无变化',
      重要程度变化: vars2.重要程度 - vars1.重要程度,
      关键词重叠: this.calculateKeywordOverlap(vars1.关键词, vars2.关键词)
    };
  }

  /**
   * 计算关键词重叠度
   * @param {Array} keywords1 - 关键词1
   * @param {Array} keywords2 - 关键词2
   * @returns {object} 重叠度信息
   */
  calculateKeywordOverlap(keywords1, keywords2) {
    const words1 = new Set(keywords1.map(k => k.词));
    const words2 = new Set(keywords2.map(k => k.词));

    const intersection = [...words1].filter(w => words2.has(w));
    const union = new Set([...words1, ...words2]);

    const overlap = intersection.length / union.length;

    return {
      重叠关键词: intersection,
      重叠度: Math.round(overlap * 100) + '%'
    };
  }

  /**
   * 生成太极变量摘要
   * @param {object} taijiVars - 太极变量
   * @returns {string} 摘要
   */
  generateSummary(taijiVars) {
    const summary = [];

    summary.push(`字数：${taijiVars.字数}`);
    summary.push(`行数：${taijiVars.行数}`);
    summary.push(`关键词：${taijiVars.关键词.map(k => k.词).join(', ')}`);
    summary.push(`情感：${taijiVars.情感}`);
    summary.push(`重要程度：${taijiVars.重要程度}/10`);

    return summary.join('\n');
  }

  /**
   * 更新停用词列表
   * @param {Array} words - 新的停用词
   */
  updateStopWords(words) {
    this.stopWords = [...this.stopWords, ...words];
  }

  /**
   * 更新积极词列表
   * @param {Array} words - 新的积极词
   */
  updatePositiveWords(words) {
    this.positiveWords = [...this.positiveWords, ...words];
  }

  /**
   * 更新消极词列表
   * @param {Array} words - 新的消极词
   */
  updateNegativeWords(words) {
    this.negativeWords = [...this.negativeWords, ...words];
  }

  /**
   * 导出太极变量为 JSON
   * @param {object} taijiVars - 太极变量
   * @returns {string} JSON 字符串
   */
  exportToJSON(taijiVars) {
    return JSON.stringify(taijiVars, null, 2);
  }

  /**
   * 从 JSON 导入太极变量
   * @param {string} json - JSON 字符串
   * @returns {object} 太极变量
   */
  importFromJSON(json) {
    try {
      return JSON.parse(json);
    } catch (error) {
      console.error('导入失败:', error);
      return null;
    }
  }
}

// 全局单例
window.taijiExtractor = new TaijiExtractor();
