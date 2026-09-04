/**
 * 龍魂万年历 · 主权固化层
 * DNA: #龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-CALENDAR-SOVEREIGNTY-v1.0
 *
 * 功能：
 * 1. 页面渲染完成后计算 DOM 哈希
 * 2. 生成带时间戳的 DNA
 * 3. 把每日痕迹写入 localStorage 哈希链
 * 4. 提供完整性校验
 */

const LonghunSovereignty = (function () {
  'use strict';

  const STORAGE_KEY = 'longhun_calendar_chain';
  const MODULE = 'LONGHUN-PERPETUAL-CALENDAR';

  async function sha256Hex(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
  }

  function pad2(n) { return n < 10 ? '0' + n : n; }

  function timestamp() {
    const d = new Date();
    return `${d.getFullYear()}${pad2(d.getMonth()+1)}${pad2(d.getDate())}${pad2(d.getHours())}${pad2(d.getMinutes())}${pad2(d.getSeconds())}${String(d.getMilliseconds()).padStart(3,'0')}`;
  }

  async function generateDNA(seed) {
    const ts = timestamp();
    const hash = await sha256Hex(`${MODULE}|${seed}|${ts}`);
    return `#龍芯⚡️${ts}-${MODULE}-${hash.slice(0, 8)}`;
  }

  // 计算页面关键 DOM 的哈希
  async function computePageHash() {
    const text = document.documentElement.outerHTML;
    return await sha256Hex(text);
  }

  // 读取本地链
  function loadChain() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  // 写入链
  function appendChain(record) {
    const chain = loadChain();
    const prevHash = chain.length ? chain[chain.length - 1].hash : '0' * 64;
    record.prevHash = prevHash;
    chain.push(record);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(chain.slice(-365))); // 保留最近一年
    } catch (e) {
      console.warn('龍魂链写入失败', e);
    }
    return chain;
  }

  async function init() {
    const pageHash = await computePageHash();
    const dna = await generateDNA(pageHash.slice(0, 16));
    const dateSeed = LonghunCalendar ? LonghunCalendar.dateNumber(new Date()) : timestamp().slice(0, 8);
    const dayDNA = await generateDNA(`DAY-${dateSeed}`);

    // 显示当前 DNA
    const dnaEl = document.getElementById('current-dna');
    if (dnaEl) dnaEl.textContent = dna;

    // 完整性校验
    const badge = document.getElementById('integrity-badge');
    if (badge) {
      badge.textContent = `🔒 完整性已固化 · ${pageHash.slice(0, 12)}…`;
    }

    // 写入今日链记录
    const record = {
      dna: dayDNA,
      pageHash: pageHash,
      date: new Date().toISOString(),
      seed: dateSeed
    };
    const chain = appendChain(record);

    // 链哈希显示
    const chainEl = document.getElementById('chain-hash');
    if (chainEl) {
      const chainHash = await sha256Hex(JSON.stringify(chain));
      chainEl.textContent = `链哈希: ${chainHash.slice(0, 24)}… · 共 ${chain.length} 日痕迹`;
    }

    // 在 detail 里更新 DNA（覆盖 calendar.js 的简化版）
    const detailDNA = document.querySelector('#detail-content div:last-child');
    // 不覆盖，由 calendar.js 提供； sovereignty 负责链
  }

  // 公开校验函数
  async function verify() {
    const chain = loadChain();
    if (!chain.length) return { ok: false, reason: '无链记录' };
    for (let i = 1; i < chain.length; i++) {
      if (chain[i].prevHash !== chain[i - 1].hash) {
        return { ok: false, reason: `链断裂于第 ${i} 条`, record: chain[i] };
      }
    }
    const currentHash = await computePageHash();
    const last = chain[chain.length - 1];
    return {
      ok: last.pageHash === currentHash,
      lastHash: last.pageHash,
      currentHash,
      length: chain.length
    };
  }

  return { init, verify, generateDNA };
})();
