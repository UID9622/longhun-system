// ===== 龍魂太极算法变量提取器 =====

window.taijiExtractor = (function() {

  // 中文停用词
  const STOP_WORDS = new Set([
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
    '自己', '这', '他', '她', '它', '们', '那', '些', '什么', '怎么', '如何', '为什么',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
    'and', 'but', 'or', 'nor', 'not', 'so', 'yet', 'both', 'either',
    'this', 'that', 'these', 'those', 'it', 'its'
  ]);

  // 情感词典
  const POSITIVE_WORDS = ['好', '优秀', '棒', '成功', '开心', '快乐', '美', '强', '赞', '完美', '胜利', '希望', '爱', '幸福', '进步', 'good', 'great', 'excellent', 'happy', 'success', 'love', 'perfect', 'win', 'best', 'awesome'];
  const NEGATIVE_WORDS = ['坏', '差', '失败', '难过', '痛苦', '丑', '弱', '错', '问题', '危险', '恨', '悲', '困难', 'bad', 'fail', 'sad', 'pain', 'ugly', 'wrong', 'problem', 'danger', 'hate', 'difficult'];

  // 分词（简易版）
  function tokenize(text) {
    // 中文按字/词分割，英文按空格分割
    const tokens = [];
    // 提取中文词组（2-4字）
    const zhMatches = text.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
    tokens.push(...zhMatches);
    // 提取英文单词
    const enMatches = text.match(/[a-zA-Z]+/g) || [];
    tokens.push(...enMatches.map(w => w.toLowerCase()));
    return tokens;
  }

  // 提取关键词
  function extractKeywords(text, topN = 8) {
    const tokens = tokenize(text);
    const freq = {};

    tokens.forEach(token => {
      if (token.length < 2 || STOP_WORDS.has(token)) return;
      freq[token] = (freq[token] || 0) + 1;
    });

    return Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, topN)
      .map(([word, count]) => ({ 词: word, 频率: count }));
  }

  // 情感分析
  function analyzeSentiment(text) {
    const lower = text.toLowerCase();
    let positive = 0, negative = 0;

    POSITIVE_WORDS.forEach(w => {
      const regex = new RegExp(w, 'gi');
      const matches = lower.match(regex);
      if (matches) positive += matches.length;
    });

    NEGATIVE_WORDS.forEach(w => {
      const regex = new RegExp(w, 'gi');
      const matches = lower.match(regex);
      if (matches) negative += matches.length;
    });

    if (positive > negative * 1.5) return '积极 ✨';
    if (negative > positive * 1.5) return '消极 ⚡';
    if (positive > 0 && negative > 0) return '混合 ☯️';
    return '中性 ⚖️';
  }

  // 计算重要程度
  function calculateImportance(text, keywords) {
    let score = 5; // 基础分

    // 长度加分
    if (text.length > 500) score += 1;
    if (text.length > 1000) score += 1;

    // 关键词密度加分
    const totalKeyFreq = keywords.reduce((sum, k) => sum + k.频率, 0);
    if (totalKeyFreq > 10) score += 1;

    // 结构化加分（包含标点、段落）
    const paragraphs = text.split(/\n\n+/).length;
    if (paragraphs > 3) score += 1;

    // 特殊标记加分
    if (text.includes('重要') || text.includes('关键') || text.includes('核心')) score += 1;

    return Math.min(score, 10);
  }

  // 主提取函数
  function extract(text) {
    const lines = text.split('\n').filter(l => l.trim());
    const keywords = extractKeywords(text);
    const sentiment = analyzeSentiment(text);
    const importance = calculateImportance(text, keywords);

    return {
      字数: text.length,
      行数: lines.length,
      段落数: text.split(/\n\n+/).filter(p => p.trim()).length,
      关键词: keywords,
      情感: sentiment,
      重要程度: importance,
      语言: detectLanguage(text),
      提取时间: new Date().toISOString()
    };
  }

  // 语言检测
  function detectLanguage(text) {
    const zhCount = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const enCount = (text.match(/[a-zA-Z]/g) || []).length;
    if (zhCount > enCount * 2) return '中文';
    if (enCount > zhCount * 2) return 'English';
    return '中英混合';
  }

  return { extract, extractKeywords, analyzeSentiment, tokenize };
})();
