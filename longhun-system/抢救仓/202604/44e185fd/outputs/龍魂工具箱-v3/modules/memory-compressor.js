// ===== 龍魂记忆压缩器 =====

window.memoryCompressor = (function() {

  // 简易哈希
  function quickHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).toUpperCase().padStart(8, '0');
  }

  // 生成摘要
  function generateSummary(text, keywords, level) {
    const sentences = text.split(/[。！？\.\!\?]+/).filter(s => s.trim().length > 5);
    let maxSentences;

    switch (level) {
      case 'high': maxSentences = 1; break;
      case 'medium': maxSentences = 3; break;
      case 'low': maxSentences = 5; break;
      default: maxSentences = 3;
    }

    if (sentences.length <= maxSentences) {
      return sentences.join('。') + '。';
    }

    // 用关键词给句子打分
    const keywordSet = new Set(keywords.map(k => k.词));
    const scored = sentences.map(sentence => {
      let score = 0;
      keywordSet.forEach(kw => {
        if (sentence.includes(kw)) score += 2;
      });
      // 首句加分
      if (sentence === sentences[0]) score += 3;
      return { sentence, score };
    });

    scored.sort((a, b) => b.score - a.score);
    const selected = scored.slice(0, maxSentences).map(s => s.sentence.trim());
    return selected.join('。') + '。';
  }

  // 压缩记忆
  function compress(text, taijiVars, level = 'medium') {
    const keywords = taijiVars ? taijiVars.关键词 : [];
    const summary = generateSummary(text, keywords, level);
    const fullHash = quickHash(text);

    const originalLen = text.length;
    const compressedLen = summary.length;
    const ratio = originalLen > 0 ? Math.round((1 - compressedLen / originalLen) * 100) : 0;

    return {
      摘要: summary,
      原始长度: originalLen,
      压缩后长度: compressedLen,
      压缩率: Math.max(ratio, 0),
      完整哈希: fullHash,
      压缩级别: level,
      关键词保留: keywords.map(k => k.词),
      压缩时间: new Date().toISOString()
    };
  }

  // 批量压缩
  function batchCompress(items, level = 'medium') {
    return items.map(item => {
      const taijiVars = window.taijiExtractor ? window.taijiExtractor.extract(item.content) : null;
      return {
        id: item.id,
        compressed: compress(item.content, taijiVars, level)
      };
    });
  }

  return { compress, batchCompress, generateSummary };
})();
