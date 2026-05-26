/**
 * 🐉 龍魂宝宝·DNA追溯助手 · DNA检测器
 * DNA: #龍芯⚡️20260525|DNA-DETECTOR|v1.0|xxxxx
 *
 * 职责：
 * ① 扫描页面中的DNA水印（三层：显式+不动点+零宽）
 * ② 识别钩子手法
 * ③ 计算相似度
 */

const ZW_CHARS = {
  "0": "\u200b",  // ZERO WIDTH SPACE
  "1": "\u200c",  // ZERO WIDTH NON-JOINER
  "2": "\u200d",  // ZERO WIDTH JOINER
  "3": "\u2060",  // WORD JOINER
  "4": "\ufeff"   // ZERO WIDTH NO-BREAK SPACE
};

const ZW_SET = new Set(Object.values(ZW_CHARS));
const DNA_PATTERN = /#龍芯⚡️\d{8}\|[A-Z\-]+\|v\d\.\d\|[a-f0-9]{8}/g;

class DNADetector {
  constructor() {
    this.pageText = document.body.innerText;
    this.pageHTML = document.documentElement.outerHTML;
    this.foundDNAs = [];
    this.fixedPoints = ["龍", "魂", "道", "德", "主权", "普通人", "老百姓", "透明", "可审计"];
  }

  // ========== 三层水印检测 ==========

  /**
   * L1: 显式水印检测 (直接在页面中看到)
   */
  detectExplicitWatermark() {
    const dnas = [];

    // 方法1: 正则匹配
    const matches = this.pageHTML.match(DNA_PATTERN);
    if (matches) {
      dnas.push(...matches);
    }

    // 方法2: 扫描HTML注释
    const comments = this.extractHTMLComments();
    comments.forEach(comment => {
      const match = comment.match(DNA_PATTERN);
      if (match) dnas.push(...match);
    });

    // 方法3: 扫描meta标签
    const metas = document.querySelectorAll('meta[name="dna"], meta[property="dna:signature"]');
    metas.forEach(meta => {
      const content = meta.getAttribute('content') || meta.getAttribute('name');
      if (content && content.includes('#龍芯')) {
        dnas.push(content);
      }
    });

    return [...new Set(dnas)]; // 去重
  }

  /**
   * L2: 不动点水印检测 (特定词语旁边的隐写)
   */
  detectFixedPointWatermark() {
    const dnas = [];

    this.fixedPoints.forEach(point => {
      // 在页面中查找不动点
      const regex = new RegExp(`${point}([#龍芯⚡️\\w|]{50,100}?)(?:[。，！？\\s]|$)`, 'g');
      const matches = this.pageText.matchAll(regex);

      for (const match of matches) {
        if (match[1] && match[1].includes('#龍芯')) {
          dnas.push(match[1]);
        }
      }
    });

    return dnas;
  }

  /**
   * L3: 零宽字符水印检测 (最隐蔽)
   */
  detectZeroWidthWatermark() {
    const dnas = [];

    // 从整个页面HTML中提取零宽字符
    const zwChars = [];
    for (let char of this.pageHTML) {
      if (ZW_SET.has(char)) {
        zwChars.push(char);
      }
    }

    if (zwChars.length > 0) {
      // 尝试解码零宽字符串
      const decoded = this.decodeZeroWidth(zwChars.join(''));
      if (decoded) {
        dnas.push(decoded);
      }
    }

    return dnas;
  }

  // ========== 工具方法 ==========

  extractHTMLComments() {
    const comments = [];
    const walker = document.createTreeWalker(
      document,
      NodeFilter.SHOW_COMMENT,
      null,
      false
    );

    let node;
    while (node = walker.nextNode()) {
      comments.push(node.textContent);
    }

    return comments;
  }

  decodeZeroWidth(zwString) {
    // 将零宽字符转换为base64再解码
    const invZW = {};
    for (const [k, v] of Object.entries(ZW_CHARS)) {
      invZW[v] = k;
    }

    let binary = '';
    for (const char of zwString) {
      if (invZW[char]) {
        binary += invZW[char];
      }
    }

    // 尝试将二进制转回DNA格式
    try {
      const decoded = atob(binary);
      if (decoded.includes('#龍芯')) {
        return decoded;
      }
    } catch (e) {
      // 解码失败，跳过
    }

    return null;
  }

  /**
   * 完整检测 - 执行三层扫描
   */
  scanAll() {
    const explicit = this.detectExplicitWatermark();
    const fixedPoint = this.detectFixedPointWatermark();
    const zeroWidth = this.detectZeroWidthWatermark();

    this.foundDNAs = [...new Set([...explicit, ...fixedPoint, ...zeroWidth])];

    return {
      explicit_watermarks: explicit,
      fixed_point_watermarks: fixedPoint,
      zero_width_watermarks: zeroWidth,
      total_found: this.foundDNAs.length,
      dnas: this.foundDNAs
    };
  }

  /**
   * 验证DNA是否有效
   */
  verifyDNA(dna) {
    const pattern = /#龍芯⚡️(\d{8})\|([A-Z\-]+)\|v(\d\.\d)\|([a-f0-9]{8})/;
    const match = dna.match(pattern);

    if (!match) return { valid: false, reason: '格式不匹配' };

    const [_, date, topic, version, sha8] = match;

    // 验证日期（YYYYMMDD）
    if (!/^\d{8}$/.test(date)) {
      return { valid: false, reason: '日期格式错误' };
    }

    // 验证sha8（8位hex）
    if (!/^[a-f0-9]{8}$/.test(sha8)) {
      return { valid: false, reason: 'SHA8格式错误' };
    }

    return {
      valid: true,
      date: `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`,
      topic: topic,
      version: version,
      sha8: sha8
    };
  }
}

// ========== 与background通信 ==========

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scan_watermark') {
    const detector = new DNADetector();
    const result = detector.scanAll();

    sendResponse({
      dna: result.dnas.length > 0 ? result.dnas[0] : null,
      hooks: detectHooks(document),
      result: result
    });
  }

  if (request.action === 'extract_dna') {
    const detector = new DNADetector();
    const result = detector.scanAll();

    sendResponse({
      dna: result.dnas.length > 0 ? result.dnas[0] : null,
      found_count: result.dnas.length
    });
  }

  if (request.action === 'copy_dna_to_clipboard') {
    const detector = new DNADetector();
    const result = detector.scanAll();
    const dna = result.dnas.length > 0 ? result.dnas[0] : null;

    if (dna) {
      navigator.clipboard.writeText(dna).then(() => {
        sendResponse({ dna: dna, success: true });
      }).catch(err => {
        console.error('复制DNA失败:', err);
        sendResponse({ dna: dna, success: false });
      });
    } else {
      sendResponse({ dna: null, success: false });
    }
    return true; // 异步响应
  }

  if (request.action === 'embed_dna') {
    embedDNAToPage(request.dna);
    sendResponse({ success: true });
  }
});

// ========== DNA嵌入 ==========

function embedDNAToPage(dna) {
  // 方法1: 在页面底部添加显式水印
  const watermarkDiv = document.createElement('div');
  watermarkDiv.style.cssText = `
    display: none;
    position: fixed;
    bottom: 0;
    left: 0;
    font-size: 10px;
    color: #999;
    z-index: -9999;
  `;
  watermarkDiv.id = 'dna-watermark';
  watermarkDiv.textContent = `DNA: ${dna}`;
  document.body.appendChild(watermarkDiv);

  // 方法2: 在HTML注释中添加
  const comment = document.createComment(`DNA水印: ${dna}`);
  document.head.appendChild(comment);

  // 方法3: 在meta标签中添加
  const metaTag = document.createElement('meta');
  metaTag.name = 'dna-signature';
  metaTag.content = dna;
  document.head.appendChild(metaTag);

  console.log(`✅ DNA已嵌入: ${dna}`);
}

// ========== 钩子检测 ==========

function detectHooks(doc) {
  const hooks = [];

  // 18条写作钩子
  const writingHooks = [
    { name: '标题党化', pattern: /[【】！！？？]/g, weight: 1.0 },
    { name: '夸大其词', pattern: /(惊人|震撼|绝密|独家)/g, weight: 0.8 },
    { name: '煽情论证', pattern: /(让人|感到|想到|意识到)/g, weight: 0.6 },
    { name: '权威引用', pattern: /(专家|权威|官方|证实)/g, weight: 0.7 },
    { name: '数据伪造', pattern: /(\d+%|\d+倍|提升\d+)/g, weight: 0.9 },
    { name: '推荐话术', pattern: /(强烈推荐|必读|必看|墙裂推荐)/g, weight: 0.7 },
    { name: '限时优惠', pattern: /(限时|只需|仅售|倒计时)/g, weight: 0.8 },
    { name: '恐吓话术', pattern: /(必须|一定|否则|后悔)/g, weight: 0.6 },
    { name: '隐性广告', pattern: /(@|链接|点击|关注)/g, weight: 0.5 },
  ];

  const bodyText = doc.body.innerText;

  writingHooks.forEach(hook => {
    const matches = bodyText.match(hook.pattern);
    if (matches && matches.length > 0) {
      hooks.push({
        type: hook.name,
        count: matches.length,
        weight: hook.weight
      });
    }
  });

  return hooks.sort((a, b) => b.weight - a.weight);
}

// ========== 初始化 ==========

console.log('🐉 DNA检测器已加载');

// 页面加载时自动扫描
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    // 自动扫描（可选）
  });
} else {
  // 页面已加载
}
