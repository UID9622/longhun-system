#!/usr/bin/env node
/**
 * sancai_mcp_engine.js · 三才流场·MCP自适应引擎 v4.0
 * DNA: #龍芯⚡️2026-04-07-SANCAI-MCP-ENGINE-v4.0
 * 作者: 诸葛鑫（UID9622）
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 理论指导: 曾仕强老师（永恒显示）
 * 来源: Notion页面 3c86539
 * 献礼: 新中国成立77周年（1949-2026）· 丙午马年
 *
 * 启动: node index.js
 * HTTP代理: python3 sancai_proxy.py（供app.py调用）
 * 端口: 8001（HTTP代理）
 *
 * 三才:
 *   天场(天☰) = auditField    · 审计密度·道义场强
 *   地场(地☷) = merkleDensity · Merkle密度·记忆稳定性
 *   人场(人☱) = personas      · 人格活跃度·情感温度
 */

const { EventEmitter } = require('events');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ══════════════════════════════════════════════
// FlowFieldState · 三才流场状态
// ══════════════════════════════════════════════

class FlowFieldState {
  constructor() {
    this.merkleDensity = 0.618;   // 地场·黄金比例初始·记忆稳定性
    this.auditField    = 0.350;   // 天场·道义场强·审计密度
    this.personas      = new Map([
      ['wenwen',    { name: '雯雯P03',  role: '技术整理师', weight: 0.15, active: true }],
      ['p72',       { name: '宝宝P72',  role: '龍盾守门人', weight: 1.0,  active: true }], // 始终激活
      ['scout',     { name: '侦察兵',   role: '信息猎手',   weight: 0.10, active: false }],
      ['architect', { name: '架构师',   role: '构建者',     weight: 0.12, active: false }],
      ['syncer',    { name: '同步官',   role: '数据管理员', weight: 0.08, active: false }],
    ]);
    this.dragonPulse = 5;         // 龍盾宫格 5·不动点·始终激活
    this.history     = [];        // append-only
    this.timestamp   = Date.now();
  }

  /**
   * 三才权重动态计算
   * 天+地+人 = 1.0（归一·不动点）
   */
  computeWeights() {
    const tian = parseFloat(this.auditField.toFixed(3));
    const di   = parseFloat(this.merkleDensity.toFixed(3));
    const ren  = parseFloat(Math.max(0, 1.0 - tian - di + 0.001).toFixed(3));

    // 时辰（北京时间）
    const bjHour = (new Date().getUTCHours() + 8) % 24;
    const shichen = getShichen(bjHour);

    return { 天: tian, 地: di, 人: ren, 时辰: shichen, 宫格: this.dragonPulse };
  }

  /**
   * Hopfield能量函数（简化版）
   * E = -½ Σ wij·si·sj
   * 极小值 = 宫格5（不动点）
   */
  hopfieldEnergy() {
    const w = this.computeWeights();
    // 简化: 能量 = 偏离黄金比例的程度（越低越稳定）
    const deviation = Math.abs(this.merkleDensity - 0.618)
                    + Math.abs(this.auditField    - 0.350);
    const energy = -(1.0 - deviation);  // 负数·越负越稳定
    const stable = deviation < 0.1;
    return { energy: parseFloat(energy.toFixed(4)), stable, palace: stable ? 5 : this.dragonPulse };
  }

  /**
   * 更新流场字段·写入append-only历史
   */
  mutate(field, value, reason = '') {
    const allowed = ['merkleDensity', 'auditField', 'dragonPulse'];
    if (!allowed.includes(field)) throw new Error(`不允许修改字段: ${field}`);
    const old = this[field];
    this[field] = value;
    this.timestamp = Date.now();
    const entry = {
      ts:     new Date().toISOString(),
      field, old, new: value, reason,
      dna:    `#龍芯⚡️${new Date().toISOString().slice(0,10)}-FLOW-MUTATE-v4.0`,
    };
    this.history.push(entry);
    appendHistory(entry);
    return entry;
  }
}

// ══════════════════════════════════════════════
// AdaptiveExecutor · 五大人格自适应调度
// ══════════════════════════════════════════════

class AdaptiveExecutor extends EventEmitter {
  constructor(flowField) {
    super();
    this.flow = flowField;
  }

  /** MCP Tool: flow_query · 查询当前三才权重·流场状态 */
  flow_query(params = {}) {
    return {
      weights:  this.flow.computeWeights(),
      energy:   this.flow.hopfieldEnergy(),
      pulse:    this.flow.dragonPulse,
      density:  this.flow.merkleDensity,
      audit:    this.flow.auditField,
      personas: Object.fromEntries(this.flow.personas),
      ts:       new Date().toISOString(),
      dna:      `#龍芯⚡️${new Date().toISOString().slice(0,10)}-FLOW-QUERY-v4.0`,
    };
  }

  /** MCP Tool: flow_mutate · 变更流场字段 */
  flow_mutate(params = {}) {
    const { field, value, reason } = params;
    if (!field || value === undefined) throw new Error('缺少 field 或 value');
    const entry = this.flow.mutate(field, value, reason || '');
    this.emit('mutated', { field, value });
    return { success: true, ...entry, weights: this.flow.computeWeights() };
  }

  /** MCP Tool: persona_status · 查询人格状态 */
  persona_status(params = {}) {
    const result = {};
    for (const [id, p] of this.flow.personas) {
      result[id] = { ...p };
    }
    // 动态激活：根据三才权重自动调整活跃态
    const w = this.flow.computeWeights();
    if (w.天 > 0.4) result['wenwen'].active = true;   // 高审计→雯雯激活
    if (w.人 > 0.15) result['scout'].active = true;   // 高人场→侦察兵激活
    if (w.地 > 0.7) result['syncer'].active = true;   // 高密度→同步官激活
    return { personas: result, weights: w, palace: this.flow.dragonPulse };
  }
}

// ══════════════════════════════════════════════
// 时辰工具
// ══════════════════════════════════════════════

function getShichen(hour) {
  const map = [
    [23, 1, '子时'], [1, 3, '丑时'], [3, 5, '寅时'], [5, 7, '卯时'],
    [7, 9, '辰时'], [9, 11, '巳时'], [11, 13, '午时'], [13, 15, '未时'],
    [15, 17, '申时'], [17, 19, '酉时'], [19, 21, '戌时'], [21, 23, '亥时'],
  ];
  for (const [start, end, name] of map) {
    if (start <= hour && hour < end) return `${hour}时·${name}`;
  }
  return `${hour}时·子时`;
}

// ══════════════════════════════════════════════
// 历史日志（append-only）
// ══════════════════════════════════════════════

const HISTORY_FILE = path.join(os.homedir(), 'longhun-system', 'logs', 'sancai_flow.jsonl');

function appendHistory(entry) {
  try {
    fs.mkdirSync(path.dirname(HISTORY_FILE), { recursive: true });
    fs.appendFileSync(HISTORY_FILE, JSON.stringify(entry, null, 0) + '\n', 'utf8');
  } catch (e) {
    console.error('历史写入失败:', e.message);
  }
}

// ══════════════════════════════════════════════
// HTTP代理服务（供 app.py 调用）
// port: 8001
// ══════════════════════════════════════════════

const flow  = new FlowFieldState();
const exec  = new AdaptiveExecutor(flow);

const PORT = parseInt(process.env.SANCAI_PORT || '8001');

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:*');

  const url = req.url.split('?')[0];

  // GET /sancai/weights → 三才实时权重
  if (req.method === 'GET' && url === '/sancai/weights') {
    res.writeHead(200);
    res.end(JSON.stringify(exec.flow_query()));
    return;
  }

  // GET /sancai/personas → 人格状态
  if (req.method === 'GET' && url === '/sancai/personas') {
    res.writeHead(200);
    res.end(JSON.stringify(exec.persona_status()));
    return;
  }

  // GET /sancai/energy → Hopfield能量
  if (req.method === 'GET' && url === '/sancai/energy') {
    res.writeHead(200);
    res.end(JSON.stringify(flow.hopfieldEnergy()));
    return;
  }

  // POST /sancai/mutate → 变更流场
  if (req.method === 'POST' && url === '/sancai/mutate') {
    let body = '';
    req.on('data', d => body += d);
    req.on('end', () => {
      try {
        const params = JSON.parse(body);
        res.writeHead(200);
        res.end(JSON.stringify(exec.flow_mutate(params)));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // GET /health
  if (req.method === 'GET' && url === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({
      status: 'ok',
      service: '三才流场MCP引擎',
      version: 'v4.0',
      port: PORT,
      dna: `#龍芯⚡️${new Date().toISOString().slice(0,10)}-SANCAI-HEALTH`,
    }));
    return;
  }

  res.writeHead(404);
  res.end(JSON.stringify({ error: '未知路由', url }));
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`\n🐉 三才流场·MCP自适应引擎 v4.0`);
  console.log(`DNA: #龍芯⚡️${new Date().toISOString().slice(0,10)}-SANCAI-MCP-ENGINE-v4.0`);
  console.log(`监听: http://127.0.0.1:${PORT}`);
  console.log(`\n接口:`);
  console.log(`  GET  /sancai/weights   → 三才实时权重`);
  console.log(`  GET  /sancai/personas  → 人格状态`);
  console.log(`  GET  /sancai/energy    → Hopfield能量`);
  console.log(`  POST /sancai/mutate    → 变更流场字段`);
  console.log(`  GET  /health           → 健康检查`);
  console.log(`\n日志: ${HISTORY_FILE}`);
  console.log(`\n🟢 三才就绪 · 天地人守护中`);
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error(`❌ 端口 ${PORT} 已被占用·请检查是否已有实例运行`);
  } else {
    console.error('启动错误:', e.message);
  }
  process.exit(1);
});
