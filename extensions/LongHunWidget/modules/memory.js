##龍芯⚡️2026-06-21-ENGINE-MEMORY-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 龍魂记忆管理器 v2.0
 * IndexedDB 本地存储 · DNA追溯 · 太极算法
 */

const DB_NAME = 'LongHunDB';
const DB_VERSION = 1;
const STORE_MEMORIES = 'memories';

class MemoryManager {
  constructor() {
    this.db = null;
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => { this.db = request.result; resolve(this.db); };
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(STORE_MEMORIES)) {
          const store = db.createObjectStore(STORE_MEMORIES, { keyPath: 'id', autoIncrement: true });
          store.createIndex('dna', 'dna', { unique: false });
          store.createIndex('timestamp', 'timestamp', { unique: false });
          store.createIndex('tags', 'tags', { unique: false, multiEntry: true });
        }
      };
    });
  }

  async save(memory) {
    if (!this.db) await this.init();
    const record = {
      dna: memory.dna || generateDNA('MEMORY', 'v1.0'),
      title: memory.title || '未命名记忆',
      content: memory.content || '',
      summary: memory.summary || '',
      compressed: memory.compressed || false,
      compressionRate: memory.compressionRate || 0,
      tags: memory.tags || [],
      emotion: memory.emotion || 'neutral',
      importance: memory.importance || 5,
      url: memory.url || '',
      timestamp: Date.now(),
      syncStatus: 'local'
    };
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(STORE_MEMORIES, 'readwrite');
      const store = tx.objectStore(STORE_MEMORIES);
      const req = store.add(record);
      req.onsuccess = () => resolve({ id: req.result, ...record });
      req.onerror = () => reject(req.error);
    });
  }

  async getAll(limit = 100) {
    if (!this.db) await this.init();
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(STORE_MEMORIES, 'readonly');
      const store = tx.objectStore(STORE_MEMORIES);
      const idx = store.index('timestamp');
      const req = idx.openCursor(null, 'prev');
      const results = [];
      req.onsuccess = (e) => {
        const cursor = e.target.result;
        if (cursor && results.length < limit) {
          results.push(cursor.value);
          cursor.continue();
        } else {
          resolve(results);
        }
      };
      req.onerror = () => reject(req.error);
    });
  }

  async delete(id) {
    if (!this.db) await this.init();
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(STORE_MEMORIES, 'readwrite');
      const store = tx.objectStore(STORE_MEMORIES);
      const req = store.delete(id);
      req.onsuccess = () => resolve(true);
      req.onerror = () => reject(req.error);
    });
  }

  async getStats() {
    const all = await this.getAll(9999);
    const totalSize = all.reduce((sum, m) => sum + (m.content?.length || 0), 0);
    const compressed = all.filter(m => m.compressed).length;
    return {
      count: all.length,
      totalSize,
      compressed,
      lastUpdate: all.length > 0 ? all[0].timestamp : null
    };
  }
}

// 太极算法简化版：提取文本特征
function taijiExtract(text) {
  const chars = text.length;
  const lines = text.split(/\n/).length;
  const words = text.match(/[\u4e00-\u9fa5]+/g) || [];
  const keywords = extractKeywords(text);
  const emotion = detectEmotion(text);
  const importance = Math.min(10, Math.max(1, Math.floor(chars / 100) + keywords.length));
  return { chars, lines, words: words.length, keywords, emotion, importance };
}

function extractKeywords(text, topN = 5) {
  // 简单关键词提取：找高频实词
  const stops = new Set(['的','了','是','在','我','有','和','就','不','人','都','一','一个','上','也','很','到','说','要','去','你','会','着','没有','看','好','自己','这','那','我们','咱们','这个','那个','什么','怎么','为什么','如何','可以','现在','今天','还是','但是','因为','所以','如果','就','让','把','被','给','对','将','还','又','而','却','么','之','与','及','等','或','但','而','因','于','即','则','乃','若','虽','亦','且','乃']);
  const freq = {};
  const matches = text.match(/[\u4e00-\u9fa5]{2,8}/g) || [];
  for (const w of matches) {
    if (!stops.has(w) && w.length >= 2) freq[w] = (freq[w] || 0) + 1;
  }
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word, count]) => ({ word, count }));
}

function detectEmotion(text) {
  const pos = /开心|快乐|幸福|喜欢|爱|棒|好|赞|成功|赢|顺利|舒服|轻松|温暖|感动|惊喜|希望|期待|兴奋|满足|安心/;
  const neg = /难过|痛苦|悲伤|恨|糟糕|坏|失败|输|困难|累|烦|怒|气|失望|担心|焦虑|恐惧|绝望|后悔|遗憾/;
  const p = (text.match(pos) || []).length;
  const n = (text.match(neg) || []).length;
  if (p > n) return 'positive';
  if (n > p) return 'negative';
  return 'neutral';
}

function compressMemory(text, ratio = 0.5) {
  const lines = text.split(/\n/).filter(l => l.trim());
  if (lines.length <= 3) return { summary: text, compressed: text, rate: 0 };
  const keep = Math.max(1, Math.floor(lines.length * ratio));
  const summary = lines.slice(0, keep).join('\n') + (lines.length > keep ? '\n...' : '');
  const compressed = summary;
  const rate = Math.floor((1 - compressed.length / text.length) * 100);
  return { summary, compressed, rate: Math.max(0, rate) };
}

// 全局可用
if (typeof window !== 'undefined') {
  window.MemoryManager = MemoryManager;
  window.taijiExtract = taijiExtract;
  window.compressMemory = compressMemory;
  window.generateDNA = generateDNA;
  window.verifyDNA = verifyDNA;
}
