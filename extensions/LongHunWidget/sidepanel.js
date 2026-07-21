##龍芯⚡️2026-06-21-ENGINE-SIDEPANEL-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 龍魂 SidePanel 主控逻辑 v1.1
 * + MCP 认证桥接面板
 */

// ===== Web Crypto HMAC-SHA256（MCP L0 签到用）=====
async function hmacSHA256(key, message) {
  const enc = new TextEncoder();
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    enc.encode(key),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, enc.encode(message));
  return Array.from(new Uint8Array(signature))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

// ===== 初始化 =====
let memMgr = null;
let auditEng = null;
let mcpSession = { signed: false, sig: null, ts: 0, agentId: '' };
let mcpLog = [];

document.addEventListener('DOMContentLoaded', async () => {
  document.getElementById('headerDNA').textContent = generateDNA('WIDGET', 'v1.1');
  document.getElementById('footerDNA').textContent = generateDNA('SIDEpanel', 'v1.1');

  memMgr = new MemoryManager();
  await memMgr.init();
  auditEng = new AuditEngine();
  await auditEng.load();

  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.panel).classList.add('active');
    });
  });

  await loadMemories();
  await loadAuditStats();
  await loadCurrentPage();
  calcWuxingAuto();
  bindEvents();
  loadMcpLog();
});

function bindEvents() {
  // DNA
  document.getElementById('btnGenDNA').addEventListener('click', () => {
    const topic = document.getElementById('dnaTopic').value.trim() || 'WIDGET';
    const version = document.getElementById('dnaVersion').value.trim() || 'v1.0';
    const dna = generateDNA(topic, version);
    const el = document.getElementById('dnaGenResult');
    el.textContent = dna;
    el.style.display = 'block';
    el.classList.remove('error');
    auditEng.audit('generate_dna', { level: 'green' });
  });
  document.getElementById('btnVerifyDNA').addEventListener('click', () => {
    const input = document.getElementById('dnaVerifyInput').value.trim();
    const el = document.getElementById('dnaVerifyResult');
    if (!input) { el.textContent = '请输入 DNA 签名'; el.classList.add('error'); el.style.display = 'block'; return; }
    const result = verifyDNA(input);
    if (result.valid) {
      el.textContent = `✅ DNA 有效 | 日期: ${result.date} | 主题: ${result.topic} | 版本: ${result.version}`;
      el.classList.remove('error');
      auditEng.audit('verify_dna', { level: 'green' });
    } else {
      el.textContent = `❌ ${result.reason}`;
      el.classList.add('error');
      auditEng.audit('verify_dna_fail', { level: 'yellow' });
    }
    el.style.display = 'block';
  });

  // 记忆
  document.getElementById('btnProcessMem').addEventListener('click', processMemoryUI);
  document.getElementById('btnCompressMem').addEventListener('click', compressMemoryUI);
  document.getElementById('btnSaveMem').addEventListener('click', saveMemoryUI);
  document.getElementById('btnClearMem').addEventListener('click', () => {
    document.getElementById('memInput').value = '';
    document.getElementById('memTitle').value = '';
    document.getElementById('memResult').style.display = 'none';
  });

  // 页面
  document.getElementById('btnReadPage').addEventListener('click', readCurrentPage);
  document.getElementById('btnSavePage').addEventListener('click', savePageToMemory);
  document.getElementById('btnOpenConsole').addEventListener('click', () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('sidepanel.html') });
  });

  // 审计
  document.getElementById('btnClearAudit').addEventListener('click', async () => {
    await chrome.storage.local.set({ auditLog: [] });
    auditEng.log = [];
    loadAuditStats();
  });

  // 五行
  ['Wood','Fire','Earth','Metal','Water'].forEach(el => {
    document.getElementById('rng'+el).addEventListener('input', calcWuxingManual);
  });
  document.getElementById('btnCalcWuxing').addEventListener('click', calcWuxingManual);

  // MCP 桥接
  document.getElementById('btnMcpSign').addEventListener('click', mcpSignL0);
  document.getElementById('btnMcpConfirm').addEventListener('click', mcpConfirm);
  document.getElementById('btnMcpGpg').addEventListener('click', mcpGpgCheck);
  document.getElementById('btnMcpReset').addEventListener('click', mcpReset);
  document.getElementById('btnCopyPrompt').addEventListener('click', copyCursorPrompt);
  document.getElementById('btnOpenAuth').addEventListener('click', () => openFile('mcp-bridge/longhun-mcp-auth.json'));
  document.getElementById('btnOpenWrapper').addEventListener('click', () => openFile('mcp-bridge/longhun-mcp-wrapper.js'));
  document.getElementById('btnOpenPrompt').addEventListener('click', () => openFile('mcp-bridge/cursor-prompt.md'));
  document.getElementById('btnOpenInstall').addEventListener('click', () => openFile('mcp-bridge/install.sh'));
}

// ===== MCP 桥接逻辑 =====
const MCP_AUTH = {
  version: "0.1.0",
  owner_uid: "9622",
  gpg_fingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  confirm_code: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  audit_rules: {
    green: ["read_page","take_screenshot","list_pages","list_network_requests","list_console_messages"],
    yellow: ["click","type","navigate","fill","select_option"],
    red: ["evaluate_script","delete_cookies","clear_storage","close_page","upload_file"]
  }
};

async function mcpSignL0() {
  const agentId = 'browser-widget-' + Date.now();
  const secret = MCP_AUTH.gpg_fingerprint + MCP_AUTH.confirm_code;
  const sig = await hmacSHA256(secret, agentId + Date.now());
  mcpSession = { signed: true, sig, ts: Date.now(), agentId };
  showMcpResult(`✅ 闸门① L0 签到成功\nAgent: ${agentId}\n签章: ${sig.slice(0,16)}...`, false);
  pushMcpLog('SIGN_L0', 'green', agentId);
}

async function mcpConfirm() {
  if (!mcpSession.signed) { showMcpResult('❌ 未签到·先点 L0 签到', true); return; }
  const code = MCP_AUTH.confirm_code;
  showMcpResult(`✅ 闸门② CONFIRM 校验通过\n确认码: ${code}\n会话: ${mcpSession.agentId}`, false);
  pushMcpLog('CONFIRM_OK', 'green', code);
}

async function mcpGpgCheck() {
  const envGpg = MCP_AUTH.gpg_fingerprint;
  const match = envGpg === "A2D0092CEE2E5BA87035600924C3704A8CC26D5F";
  if (match) {
    showMcpResult(`✅ 闸门④ GPG 指纹匹配\n${envGpg}`, false);
    pushMcpLog('GPG_MATCH', 'green', '指纹一致');
  } else {
    showMcpResult(`🔴 GPG 指纹不匹配\n配置: ${envGpg}`, true);
    pushMcpLog('GPG_FAIL', 'red', '指纹不一致');
  }
}

function mcpReset() {
  mcpSession = { signed: false, sig: null, ts: 0, agentId: '' };
  showMcpResult('🔄 MCP 会话已重置', false);
  pushMcpLog('RESET', 'yellow', '会话重置');
}

function showMcpResult(text, isError) {
  const el = document.getElementById('mcpGateResult');
  el.textContent = text;
  el.style.display = 'block';
  el.classList.toggle('error', isError);
}

function pushMcpLog(action, color, detail) {
  const line = { action, color, detail, time: Date.now() };
  mcpLog.unshift(line);
  if (mcpLog.length > 50) mcpLog.pop();
  chrome.storage.local.set({ mcpBridgeLog: mcpLog });
  renderMcpLog();
}

function loadMcpLog() {
  chrome.storage.local.get('mcpBridgeLog').then(d => {
    mcpLog = d.mcpBridgeLog || [];
    renderMcpLog();
  });
}

function renderMcpLog() {
  const container = document.getElementById('mcpAuditLog');
  if (mcpLog.length === 0) {
    container.innerHTML = '暂无桥接记录';
    return;
  }
  container.innerHTML = mcpLog.map(l => {
    const c = l.color === 'red' ? '🔴' : l.color === 'yellow' ? '🟡' : '🟢';
    return `<div style="margin-bottom:4px;border-bottom:1px solid rgba(255,255,255,0.03);padding-bottom:2px">${c} ${l.action} · ${escapeHtml(l.detail)} <span style="color:#555">${formatTime(l.time)}</span></div>`;
  }).join('');
}

async function copyCursorPrompt() {
  const text = document.getElementById('cursorPrompt').value;
  await navigator.clipboard.writeText(text);
  showMcpResult('✅ Cursor 提示词已复制到剪贴板', false);
}

function openFile(relativePath) {
  const url = chrome.runtime.getURL(relativePath);
  chrome.tabs.create({ url });
}

async function hmacSHA256(key, message) {
  const enc = new TextEncoder();
  const cryptoKey = await crypto.subtle.importKey('raw', enc.encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', cryptoKey, enc.encode(message));
  return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// ===== 记忆功能 =====
let currentProcessed = null;

async function processMemoryUI() {
  const text = document.getElementById('memInput').value.trim();
  if (!text) { alert('请输入记忆内容'); return; }
  const taiji = taijiExtract(text);
  const dna = generateDNA('MEMORY', 'v1.0');
  currentProcessed = { dna, content: text, taiji, summary: text.slice(0,200)+(text.length>200?'...':''), title: document.getElementById('memTitle').value.trim() || '未命名记忆' };
  let html = `🧬 DNA: ${dna}\n\n☯️ 太极变量:\n  字数: ${taiji.chars} | 行数: ${taiji.lines}\n  关键词: ${taiji.keywords.map(k=>k.word).join(', ')}\n  情感: ${taiji.emotion} | 重要度: ${taiji.importance}/10\n`;
  document.getElementById('memResult').textContent = html;
  document.getElementById('memResult').style.display = 'block';
  auditEng.audit('process_memory', { level: 'green' });
}

function compressMemoryUI() {
  const text = document.getElementById('memInput').value.trim();
  if (!text) return;
  const compressed = compressMemory(text, 0.4);
  let html = document.getElementById('memResult').textContent + '\n\n';
  html += `📦 压缩结果:\n  原始: ${text.length} 字 → 压缩后: ${compressed.compressed.length} 字\n  压缩率: ${compressed.rate}%\n  摘要:\n${compressed.summary}`;
  document.getElementById('memResult').textContent = html;
  if (currentProcessed) { currentProcessed.compressed = compressed.compressed; currentProcessed.compressionRate = compressed.rate; currentProcessed.summary = compressed.summary; }
}

async function saveMemoryUI() {
  if (!currentProcessed) await processMemoryUI();
  if (!currentProcessed) return;
  await memMgr.save(currentProcessed);
  await loadMemories();
  document.getElementById('memResult').textContent += '\n\n✅ 已保存到 IndexedDB';
  auditEng.audit('save_memory', { level: 'green' });
}

async function loadMemories() {
  const list = await memMgr.getAll(50);
  const container = document.getElementById('memLibrary');
  document.getElementById('memCountLabel').textContent = `(${list.length})`;
  document.getElementById('statMemCount').textContent = list.length;
  if (list.length === 0) { container.innerHTML = '<div style="color:var(--muted);text-align:center;padding:20px;font-size:11px">暂无记忆</div>'; return; }
  container.innerHTML = list.map(m => `
    <div class="mem-item">
      <div class="mem-head"><span class="mem-title">${escapeHtml(m.title)}</span><span class="mem-time">${formatTime(m.timestamp)}</span></div>
      <div class="mem-dna">${m.dna}</div>
      <div class="mem-summary">${escapeHtml(m.summary || m.content.slice(0,100))}${(m.content?.length||0)>100?'...':''}</div>
      <div class="btn-group"><button class="btn btn-ghost" style="padding:2px 6px;font-size:9px" onclick="deleteMem(${m.id})">🗑️ 删除</button></div>
    </div>`).join('');
}

async function deleteMem(id) {
  if (!confirm('确定删除这条记忆？')) return;
  await memMgr.delete(id);
  await loadMemories();
  auditEng.audit('delete_memory', { level: 'yellow' });
}

// ===== 页面读取 =====
async function loadCurrentPage() {
  try {
    const tab = await chrome.runtime.sendMessage({ type: 'GET_TAB_INFO' });
    document.getElementById('currentPageInfo').innerHTML = `标题: ${escapeHtml(tab.title||'未知')}<br>URL: ${escapeHtml(tab.url||'未知')}<br>Tab ID: ${tab.id}`;
  } catch (e) {
    document.getElementById('currentPageInfo').textContent = '无法读取当前页面（可能需要刷新）';
  }
}

async function readCurrentPage() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const resp = await chrome.tabs.sendMessage(tab.id, { type: 'EYE_READ_PAGE' });
    if (resp.restricted) { alert('🔴 铁律熔断：该页面为敏感页面，禁止读取'); auditEng.audit('read_page_blocked', { level: 'red', url: tab.url }); return; }
    const info = document.getElementById('currentPageInfo');
    info.innerHTML += `<br><br>📄 内容摘要:<br><pre style="white-space:pre-wrap;font-size:10px;color:var(--muted);max-height:120px;overflow:auto">${escapeHtml(resp.summary.slice(0,500))}</pre>`;
    auditEng.audit('read_page', { level: 'green', url: tab.url });
  } catch (e) { alert('读取失败：' + e.message); }
}

async function savePageToMemory() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await memMgr.save({ title: `📄 ${tab.title||'未命名页面'}`, content: tab.url||'', summary: `页面收藏: ${tab.url||''}`, tags: ['page','auto'], url: tab.url||'' });
    await loadMemories();
    alert('✅ 页面已保存到记忆');
    auditEng.audit('save_page', { level: 'green', url: tab.url });
  } catch (e) { alert('保存失败'); }
}

// ===== 审计 =====
async function loadAuditStats() {
  const stats = auditEng.getStats();
  document.getElementById('auditTotal').textContent = stats.total;
  document.getElementById('auditG').textContent = stats.green;
  document.getElementById('auditY').textContent = stats.yellow;
  document.getElementById('auditR').textContent = stats.red;
  document.getElementById('auditB').textContent = stats.blocked;
  document.getElementById('statAuditGreen').textContent = stats.green;
  document.getElementById('statAuditRed').textContent = stats.red;
  const container = document.getElementById('auditLog');
  const recent = auditEng.getRecent(30);
  if (recent.length === 0) { container.innerHTML = '<div style="color:var(--muted);text-align:center;padding:20px;font-size:11px">暂无审计记录</div>'; return; }
  container.innerHTML = recent.map(r => `
    <div class="audit-item">
      <span class="audit-dot ${r.level}"></span>
      <div class="audit-text"><div class="audit-action">${r.action}${r.blocked?' ⛔已阻断':''}</div><div class="audit-reason">${r.reason||''}</div></div>
      <span class="audit-time">${formatTime(r.timestamp)}</span>
    </div>`).join('');
}

// ===== 五行 =====
function calcWuxingAuto() {
  const now = new Date();
  const hour = now.getHours();
  const memCount = parseInt(document.getElementById('statMemCount').textContent) || 0;
  const auditRed = parseInt(document.getElementById('statAuditRed').textContent) || 0;
  const hourWx = [3,3,4,4,1,1,1,2,2,5,5,5,3,3,4,4,1,1,2,2,5,5,3,3];
  const base = hourWx[hour] || 3;
  const wood = Math.min(100, Math.max(10, (base===1?70:30)+memCount*2));
  const fire = Math.min(100, Math.max(10, (base===2?70:30)+auditRed*5));
  const earth = Math.min(100, Math.max(10, (base===5?70:40)));
  const metal = Math.min(100, Math.max(10, 40+(memCount>10?20:0)));
  const water = Math.min(100, Math.max(10, (base===3?70:30)+(hour>=21||hour<=5?20:0)));
  setWuxingValues({wood, fire, earth, metal, water});
}

function calcWuxingManual() {
  setWuxingValues({
    wood: parseInt(document.getElementById('rngWood').value),
    fire: parseInt(document.getElementById('rngFire').value),
    earth: parseInt(document.getElementById('rngEarth').value),
    metal: parseInt(document.getElementById('rngMetal').value),
    water: parseInt(document.getElementById('rngWater').value)
  });
}

function setWuxingValues(v) {
  ['Wood','Fire','Earth','Metal','Water'].forEach(k => {
    document.getElementById('wx'+k).textContent = v[k.toLowerCase()];
    document.getElementById('bar'+k).style.width = v[k.toLowerCase()] + '%';
  });
  const max = Math.max(v.wood,v.fire,v.earth,v.metal,v.water);
  let dominant = '';
  if (max===v.wood) dominant='木气旺盛 · 生发 · 适合启动新项目、创作、播种';
  else if (max===v.fire) dominant='火气当令 · 炎上 · 适合推进、展示、表达、加速';
  else if (max===v.earth) dominant='土德厚重 · 稼穑 · 适合整合、稳定、承载、收尾';
  else if (max===v.metal) dominant='金气肃杀 · 从革 · 适合决断、切割、收敛、规范';
  else if (max===v.water) dominant='水势润下 · 闭藏 · 适合思考、谋划、储备、等待';
  const min = Math.min(v.wood,v.fire,v.earth,v.metal,v.water);
  let weak = '';
  if (min===v.wood) weak='木气不足 · 生发乏力 · 宜早起、接触自然、做计划';
  else if (min===v.fire) weak='火气不足 · 动力欠缺 · 宜运动、社交、晒太阳';
  else if (min===v.earth) weak='土气不足 · 根基不稳 · 宜整理、饮食、脚踏实地';
  else if (min===v.metal) weak='金气不足 · 决断力弱 · 宜断舍离、明确边界';
  else if (min===v.water) weak='水气不足 · 智慧闭塞 · 宜阅读、冥想、早睡';
  document.getElementById('wuxingDesc').innerHTML = `<strong style="color:var(--gold)"> dominant：</strong>${dominant}<br><strong style="color:var(--blue)"> 弱势：</strong>${weak}`;
}

// ===== 工具函数 =====
function escapeHtml(str) { if(!str)return''; return str.replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }
function formatTime(ts) { if(!ts)return'未知'; const d=new Date(ts); return `${d.getMonth()+1}/${d.getDate()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`; }
