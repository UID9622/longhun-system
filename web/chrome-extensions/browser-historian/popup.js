/**
 * 龍魂 · 浏览器史官 — Popup 界面逻辑
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 初始化
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
document.addEventListener('DOMContentLoaded', async () => {
  const status = await chrome.runtime.sendMessage({ type: 'GET_STATUS' });
  const data = await chrome.runtime.sendMessage({ type: 'GET_STORED_DATA' });

  if (data && data.totalUnique > 0) {
    showDashboard(data);
  }

  if (status.status === 'scanning') {
    showScanning();
  }

  bindEvents(data);
});

function bindEvents(data) {
  document.getElementById('btn-scan').addEventListener('click', startScan);
  document.getElementById('btn-export').addEventListener('click', prepareExport);
  document.getElementById('filter-input').addEventListener('input', (e) => filterItems(e.target.value));
  document.getElementById('filter-cat').addEventListener('change', (e) => filterByCategory(e.target.value));

  // Tab切换
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 扫描历史
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async function startScan() {
  const daysBack = parseInt(document.getElementById('scan-days').value) || 0;

  document.getElementById('scanning-section').style.display = 'block';
  document.getElementById('btn-scan').disabled = true;
  document.getElementById('progress-bar').style.width = '0%';
  document.getElementById('progress-text').textContent = '正在连接历史数据库...';

  try {
    const result = await chrome.runtime.sendMessage({
      type: 'SCAN_HISTORY',
      daysBack: daysBack,
    });

    if (result.success) {
      document.getElementById('scanning-section').style.display = 'none';
      document.getElementById('btn-scan').disabled = false;

      const data = await chrome.runtime.sendMessage({ type: 'GET_STORED_DATA' });
      showDashboard(data);
    } else {
      document.getElementById('progress-text').textContent = '扫描出错: ' + result.error;
    }
  } catch (err) {
    document.getElementById('progress-text').textContent = '扫描出错: ' + err.message;
    document.getElementById('btn-scan').disabled = false;
  }
}

function showScanning() {
  document.getElementById('scanning-section').style.display = 'block';
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 仪表盘渲染
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function showDashboard(data) {
  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('dashboard').style.display = 'block';
  document.getElementById('btn-export').style.display = 'block';

  // 总体统计
  document.getElementById('stat-total').textContent = data.totalUnique.toLocaleString();
  document.getElementById('stat-raw').textContent = data.totalRaw.toLocaleString();
  document.getElementById('stat-cats').textContent =
    Object.keys(data.stats).filter(k => data.stats[k].count > 0).length;

  // 扫描时间
  const scanDate = new Date(data.scanTime);
  document.getElementById('scan-time').textContent =
    `上次扫描: ${scanDate.toLocaleString('zh-CN')}`;

  // 饼图
  drawPieChart(data.stats);

  // 分类卡片
  renderCategoryCards(data.stats);

  // 详细列表
  renderItemsList(data.items);

  // 存储当前数据供筛选/导出使用
  window._currentData = data;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 饼图 (Canvas)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function drawPieChart(stats) {
  const canvas = document.getElementById('pie-chart');
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const size = 220;
  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = size + 'px';
  canvas.style.height = size + 'px';
  ctx.scale(dpr, dpr);

  const entries = Object.entries(stats)
    .filter(([_, v]) => v.count > 0)
    .sort((a, b) => b[1].count - a[1].count);

  if (entries.length === 0) {
    ctx.fillStyle = '#555';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('无数据', size / 2, size / 2);
    return;
  }

  const total = entries.reduce((sum, [_, v]) => sum + v.count, 0);
  const cx = size / 2, cy = size / 2, r = 90;
  let angle = -Math.PI / 2;

  for (const [cat, { count, color }] of entries) {
    const slice = (count / total) * 2 * Math.PI;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, r, angle, angle + slice);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = '#1a1a2e';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 标签
    const midAngle = angle + slice / 2;
    const labelR = r + 20;
    const lx = cx + Math.cos(midAngle) * labelR;
    const ly = cy + Math.sin(midAngle) * labelR;
    const pct = ((count / total) * 100).toFixed(1);

    if (parseFloat(pct) > 2) {
      ctx.fillStyle = '#ccc';
      ctx.font = '10px sans-serif';
      ctx.textAlign = midAngle > Math.PI / 2 || midAngle < -Math.PI / 2 ? 'right' : 'left';
      ctx.fillText(`${pct}%`, lx, ly);
    }

    angle += slice;
  }

  // 中心圆（甜甜圈效果）
  ctx.beginPath();
  ctx.arc(cx, cy, r * 0.4, 0, 2 * Math.PI);
  ctx.fillStyle = '#1a1a2e';
  ctx.fill();
  ctx.fillStyle = '#F5A623';
  ctx.font = 'bold 16px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(total.toLocaleString(), cx, cy + 5);
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 分类卡片
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function renderCategoryCards(stats) {
  const container = document.getElementById('category-cards');
  const entries = Object.entries(stats)
    .filter(([_, v]) => v.count > 0)
    .sort((a, b) => b[1].count - a[1].count);

  const total = entries.reduce((sum, [_, v]) => sum + v.count, 0);

  container.innerHTML = entries.map(([cat, { count, name, icon, color }]) => {
    const pct = ((count / total) * 100).toFixed(1);
    return `
      <div class="cat-card" style="border-left: 3px solid ${color}" data-cat="${cat}">
        <span class="cat-icon">${icon}</span>
        <div class="cat-info">
          <span class="cat-name">${name}</span>
          <span class="cat-bar-bg">
            <span class="cat-bar-fg" style="width:${pct}%;background:${color}"></span>
          </span>
        </div>
        <span class="cat-count">${count.toLocaleString()}<small> (${pct}%)</small></span>
      </div>
    `;
  }).join('');
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 详细列表
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const ITEMS_PER_PAGE = 100;
let allItems = [];
let currentPage = 0;

function renderItemsList(items) {
  allItems = items;
  currentPage = 0;
  renderPage();
}

function renderPage() {
  const container = document.getElementById('items-list');
  const start = currentPage * ITEMS_PER_PAGE;
  const page = allItems.slice(start, start + ITEMS_PER_PAGE);

  container.innerHTML = page.map((item, i) => {
    const domain = extractSimpleDomain(item.url);
    const time = item.lastVisitTime
      ? new Date(item.lastVisitTime).toLocaleDateString('zh-CN')
      : '—';
    return `
      <div class="history-item" data-cat="${item.cat}">
        <span class="item-cat-dot" style="background:${item.catColor}" title="${item.catName}"></span>
        <div class="item-main">
          <a class="item-title" href="${escapeHtml(item.url)}" target="_blank" title="${escapeHtml(item.url)}">
            ${escapeHtml(item.title || item.url)}
          </a>
          <span class="item-domain">
            ${escapeHtml(domain)} · ${time} · 访问${item.visitCount}次
          </span>
        </div>
      </div>
    `;
  }).join('');

  // 分页
  const totalPages = Math.ceil(allItems.length / ITEMS_PER_PAGE);
  document.getElementById('page-info').textContent =
    `${start + 1}-${Math.min(start + ITEMS_PER_PAGE, allItems.length)} / ${allItems.length.toLocaleString()}`;
  document.getElementById('btn-prev').disabled = currentPage <= 0;
  document.getElementById('btn-next').disabled = currentPage >= totalPages - 1;
  document.getElementById('btn-prev').onclick = () => { if (currentPage > 0) { currentPage--; renderPage(); } };
  document.getElementById('btn-next').onclick = () => { if (currentPage < totalPages - 1) { currentPage++; renderPage(); } };
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 筛选
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function filterItems(query) {
  if (!window._currentData) return;
  const q = query.toLowerCase().trim();
  const catFilter = document.getElementById('filter-cat').value;

  let filtered = window._currentData.items;
  if (catFilter) {
    filtered = filtered.filter(item => item.cat === catFilter);
  }
  if (q) {
    filtered = filtered.filter(item =>
      item.url.toLowerCase().includes(q) ||
      item.title.toLowerCase().includes(q)
    );
  }

  allItems = filtered;
  currentPage = 0;
  renderPage();
}

function filterByCategory(cat) {
  filterItems(document.getElementById('filter-input').value);
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 导出 JSON
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async function prepareExport() {
  // 修复：始终读取当前数据，而不是依赖 DOMContentLoaded 时的闭包变量
  let data = window._currentData;
  if (!data || !data.totalUnique || data.totalUnique <= 0) {
    data = await chrome.runtime.sendMessage({ type: 'GET_STORED_DATA' });
  }
  if (!data || !data.totalUnique || data.totalUnique <= 0) {
    alert('请先扫描历史记录');
    return;
  }
  window._currentData = data;
  showExportModal();
}

function showExportModal() {
  document.getElementById('export-modal').style.display = 'flex';
}

function hideExportModal() {
  document.getElementById('export-modal').style.display = 'none';
}

async function doExport() {
  const data = window._currentData;
  if (!data || !data.totalUnique || data.totalUnique <= 0) {
    alert('请先扫描历史记录');
    return;
  }

  const training = document.getElementById('export-training').checked;
  const includeMeta = document.getElementById('export-include-meta').checked;
  const exportDate = new Date().toISOString().slice(0, 10);
  const filename = `longhun-browser-history-${exportDate}.json`;

  // 构建导出载荷：默认只导出去标识化的 URL/标题/分类，用于本地训练
  const payload = {
    exportedAt: Date.now(),
    exportDate: exportDate,
    trainingMaterial: training,
    totalUnique: data.totalUnique,
    totalRaw: data.totalRaw,
    stats: data.stats,
    scanTime: data.scanTime,
    source: 'longhun-browser-historian-v1.0',
    items: includeMeta
      ? data.items.map(item => ({
          url: item.url,
          title: item.title || '',
          visitCount: item.visitCount || 0,
          lastVisitTime: item.lastVisitTime || 0,
          cat: item.cat,
          catName: item.catName,
          catIcon: item.catIcon,
          catColor: item.catColor,
        }))
      : data.items.map(item => ({
          url: item.url,
          title: item.title || '',
          cat: item.cat,
        })),
  };

  const json = JSON.stringify(payload, null, 2);

  // 优先使用 chrome.downloads.download 的 saveAs: true，弹出系统保存对话框，
  // 让用户自己选目录（包括 U 盘）。弹出框关闭后下载继续，不受 popup 生命周期影响。
  if (chrome.downloads && chrome.downloads.download) {
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    try {
      await chrome.downloads.download({
        url: url,
        filename: filename,
        saveAs: true,
        conflictAction: 'uniquify',
      });
      hideExportModal();
      // 浏览器会自动释放 blob URL 吗？保守起见等几秒再释放
      setTimeout(() => URL.revokeObjectURL(url), 30000);
      return;
    } catch (err) {
      URL.revokeObjectURL(url);
      console.warn('chrome.downloads.download 失败，降级:', err);
    }
  }

  // 降级方案：传统 a[download]（目录由浏览器默认下载设置决定）
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  hideExportModal();
}

// 绑定弹窗按钮
document.addEventListener('DOMContentLoaded', () => {
  const btnExportCancel = document.getElementById('btn-export-cancel');
  const btnExportConfirm = document.getElementById('btn-export-confirm');
  if (btnExportCancel) btnExportCancel.addEventListener('click', hideExportModal);
  if (btnExportConfirm) btnExportConfirm.addEventListener('click', doExport);
});

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Tab 切换
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelector(`.tab-btn[data-tab="${tab}"]`).classList.add('active');
  document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
  document.getElementById(`tab-${tab}`).style.display = 'block';
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 工具函数
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function extractSimpleDomain(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return url.slice(0, 50);
  }
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ═══════════════════════════════════════════════════
// 底座痕迹 Tab 逻辑 (v2.0)
// ═══════════════════════════════════════════════════

const COLLECTOR_API = 'http://127.0.0.1:18775';
const RECONSTRUCTOR_API = 'https://uid9622.cn/api/trace-reconstruct'; // 鲲鹏反代
const RECONSTRUCTOR_DIRECT = 'http://119.13.90.27:8774'; // 鲲鹏直连（备用）

// 事件初始化
document.addEventListener('DOMContentLoaded', () => {
  const btnFetch = document.getElementById('btn-trace-fetch');
  if (btnFetch) btnFetch.addEventListener('click', fetchTraceTimeline);
  
  // 切换到 trace tab 时自动检测采集器状态
  const traceTabBtn = document.querySelector('.tab-btn[data-tab="trace"]');
  if (traceTabBtn) {
    traceTabBtn.addEventListener('click', checkCollectorStatus);
  }
});

async function checkCollectorStatus() {
  const dot = document.getElementById('trace-status-dot');
  const text = document.getElementById('trace-status-text');
  
  try {
    const resp = await fetch(`${COLLECTOR_API}/health`, { signal: AbortSignal.timeout(2000) });
    if (resp.ok) {
      const data = await resp.json();
      dot.className = 'status-dot online';
      text.textContent = `采集引擎运行中 v${data.version || '?'}`;
      return true;
    }
  } catch (e) {
    // 采集器未启动
  }
  
  dot.className = 'status-dot offline';
  text.textContent = '采集引擎未启动 — 请在终端运行: python3 bin/lh_base_trace_collector.py start';
  return false;
}

async function fetchTraceTimeline() {
  const loadingDiv = document.getElementById('trace-loading');
  const loadingText = document.getElementById('trace-loading-text');
  const emptyDiv = document.getElementById('trace-empty');
  const timelineDiv = document.getElementById('trace-timeline');
  const summaryDiv = document.getElementById('trace-summary');
  
  // 检查采集器
  const running = await checkCollectorStatus();
  if (!running) {
    alert('采集引擎未启动。请先在终端运行:\npython3 bin/lh_base_trace_collector.py start');
    return;
  }
  
  // 显示加载
  loadingDiv.style.display = 'flex';
  emptyDiv.style.display = 'none';
  timelineDiv.style.display = 'none';
  summaryDiv.style.display = 'none';
  
  const timeRange = parseInt(document.getElementById('trace-time-range').value) || 1800;
  const useAI = document.getElementById('trace-use-ai').checked;
  
  try {
    loadingText.textContent = '正在从本地采集引擎拉取痕迹...';
    
    // Step 1: 从本地采集器拉取事件
    const eventsResp = await fetch(`${COLLECTOR_API}/events/recent`, {
      signal: AbortSignal.timeout(10000)
    });
    const rawEvents = await eventsResp.json();
    
    if (!rawEvents || rawEvents.length === 0) {
      loadingDiv.style.display = 'none';
      emptyDiv.innerHTML = `
        <div class="icon">📭</div>
        <p>暂无底座痕迹数据</p>
        <p class="hint">采集器运行中但尚未捕获到事件。<br>尝试打开一些应用或编辑文件后再拉取。</p>
      `;
      emptyDiv.style.display = 'block';
      return;
    }
    
    // 筛选时间范围
    const now = Date.now() / 1000;
    const cutoff = now - timeRange;
    const filtered = rawEvents.filter(e => (e.timestamp || 0) >= cutoff);
    
    loadingText.textContent = `已拉取 ${filtered.length} 条痕迹...`;
    
    if (useAI && filtered.length > 0) {
      // Step 2: 提取特征向量
      loadingText.textContent = '正在提取脱敏特征向量...';
      const featuresResp = await fetch(`${COLLECTOR_API}/features?limit=500`, {
        signal: AbortSignal.timeout(5000)
      });
      const featuresData = await featuresResp.json();
      
      if (featuresData.features && featuresData.features.length > 0) {
        // Step 3: 发送到鲲鹏AI复原引擎
        loadingText.textContent = '正在连接鲲鹏AI复原引擎...';
        
        try {
          const aiResp = await fetch(`${RECONSTRUCTOR_API}/v1/reconstruct`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              client_id: 'browser-historian',
              features: featuresData.features,
              session_window: 300
            }),
            signal: AbortSignal.timeout(15000)
          });
          
          if (aiResp.ok) {
            const aiResult = await aiResp.json();
            renderAITimeline(aiResult);
            
            // 标记已上传
            if (featuresData.features.length > 0) {
              try {
                await fetch(`${COLLECTOR_API}/features/mark-uploaded`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ ids: featuresData.features.map((f, i) => i + 1) })
                });
              } catch (e) { /* 非关键 */ }
            }
            
            loadingDiv.style.display = 'none';
            return;
          }
        } catch (aiErr) {
          console.warn('AI复原不可用，使用本地原始数据:', aiErr.message);
        }
      }
    }
    
    // 降级：直接渲染原始事件
    renderRawTimeline(filtered);
    loadingDiv.style.display = 'none';
    
  } catch (err) {
    loadingDiv.style.display = 'none';
    emptyDiv.innerHTML = `
      <div class="icon">⚠️</div>
      <p>拉取失败: ${escapeHtml(err.message)}</p>
      <p class="hint">确认采集引擎已启动: python3 bin/lh_base_trace_collector.py status</p>
    `;
    emptyDiv.style.display = 'block';
  }
}

function renderAITimeline(aiResult) {
  const emptyDiv = document.getElementById('trace-empty');
  const timelineDiv = document.getElementById('trace-timeline');
  const summaryDiv = document.getElementById('trace-summary');
  
  emptyDiv.style.display = 'none';
  
  if (!aiResult.sessions || aiResult.sessions.length === 0) {
    emptyDiv.innerHTML = '<div class="icon">📭</div><p>AI未识别出有效会话</p>';
    emptyDiv.style.display = 'block';
    return;
  }
  
  // 渲染会话摘要
  summaryDiv.style.display = 'block';
  summaryDiv.innerHTML = `
    <div class="trace-summary-header">
      <span>🧠 AI复原 · ${aiResult.total_events} 个事件 · ${aiResult.sessions.length} 个会话</span>
      <span class="trace-confidence">置信度: ${(aiResult.confidence_avg * 100).toFixed(0)}%</span>
    </div>
  `;
  
  // 渲染时间线
  timelineDiv.style.display = 'block';
  let html = '';
  
  aiResult.sessions.forEach((session, si) => {
    html += `
      <div class="trace-session">
        <div class="trace-session-header">
          <span class="session-id">会话 #${session.session_id}</span>
          <span class="session-time">${session.start_time} → ${session.end_time} (${formatDuration(session.duration_seconds)})</span>
        </div>
        <div class="session-summary-text">${escapeHtml(session.summary)}</div>
    `;
    
    session.events.forEach((evt, ei) => {
      const catClass = `cat-${evt.category || 'unknown'}`;
      const confClass = evt.confidence >= 0.6 ? 'high' : evt.confidence >= 0.3 ? 'mid' : 'low';
      
      html += `
        <div class="trace-event ${catClass}">
          <div class="trace-event-time">${evt.time}</div>
          <div class="trace-event-dot ${catClass}"></div>
          <div class="trace-event-content">
            <span class="trace-event-action">${escapeHtml(evt.action)}</span>
            <span class="trace-event-confidence ${confClass}">${(evt.confidence * 100).toFixed(0)}%</span>
            <span class="trace-event-evidence" title="${escapeHtml(evt.evidence)}">${escapeHtml(evt.evidence)}</span>
          </div>
        </div>
      `;
    });
    
    html += '</div>';
  });
  
  timelineDiv.innerHTML = html;
}

function renderRawTimeline(events) {
  const emptyDiv = document.getElementById('trace-empty');
  const timelineDiv = document.getElementById('trace-timeline');
  const summaryDiv = document.getElementById('trace-summary');
  
  emptyDiv.style.display = 'none';
  summaryDiv.style.display = 'block';
  summaryDiv.innerHTML = `
    <div class="trace-summary-header">
      <span>📡 原始痕迹数据 · ${events.length} 个事件</span>
      <span class="trace-confidence" style="color:var(--text-dim)">未启用AI复原</span>
    </div>
  `;
  
  timelineDiv.style.display = 'block';
  
  // 按类型分组
  const grouped = {};
  events.forEach(e => {
    const source = e._source || 'unknown';
    if (!grouped[source]) grouped[source] = [];
    grouped[source].push(e);
  });
  
  const typeLabels = {
    process: '🔄 进程',
    file: '📄 文件',
    network: '🌐 网络',
    user: '👤 用户行为',
  };
  
  let html = '';
  for (const [type, evts] of Object.entries(grouped)) {
    html += `<div class="trace-raw-group">
      <div class="trace-raw-group-header">${typeLabels[type] || type} (${evts.length})</div>`;
    
    evts.slice(0, 30).forEach(e => {
      const ts = e.timestamp ? new Date(e.timestamp * 1000).toLocaleTimeString('zh-CN') : '?';
      let desc = '';
      
      if (type === 'process') {
        desc = `${e.event_type === 'start' ? '▶' : '■'} ${e.name || '?'} (PID:${e.pid})`;
      } else if (type === 'file') {
        desc = `${e.event_type === 'create' ? '+' : e.event_type === 'modify' ? '~' : '-'} ${e.path_hash || '?'} ${e.ext || ''}`;
      } else if (type === 'network') {
        desc = `🔗 ${e.remote_addr_hash || '?'}`;
      } else if (type === 'user') {
        desc = `${e.event_type}: ${e.detail || ''}`;
      }
      
      html += `<div class="trace-raw-event">
        <span class="trace-raw-time">${ts}</span>
        <span>${escapeHtml(desc)}</span>
      </div>`;
    });
    
    if (evts.length > 30) {
      html += `<div class="trace-raw-more">... 还有 ${evts.length - 30} 条</div>`;
    }
    
    html += '</div>';
  }
  
  timelineDiv.innerHTML = html;
}

function formatDuration(seconds) {
  if (seconds < 60) return `${Math.round(seconds)}秒`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}分${Math.round(seconds % 60)}秒`;
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return `${h}小时${m}分`;
}

// ═══════════════════════════════════════════════════
// 防御状态仪表盘 (v2.0 · 四道防线)
// ═══════════════════════════════════════════════════

// 事件初始化
document.addEventListener('DOMContentLoaded', () => {
  const btnRefresh = document.getElementById('btn-defense-refresh');
  if (btnRefresh) btnRefresh.addEventListener('click', fetchDefenseStatus);
  
  const btnDismiss = document.getElementById('btn-alerts-dismiss');
  if (btnDismiss) btnDismiss.addEventListener('click', dismissAlerts);
  
  // 切换到防御 tab 时自动刷新
  const defenseTabBtn = document.querySelector('.tab-btn[data-tab="defense"]');
  if (defenseTabBtn) {
    defenseTabBtn.addEventListener('click', () => {
      fetchDefenseStatus();
    });
  }
});

async function fetchDefenseStatus() {
  setDefenseLoading(true);
  
  try {
    const resp = await fetch(`${COLLECTOR_API}/defense/status`, {
      signal: AbortSignal.timeout(5000)
    });
    
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    
    const data = await resp.json();
    renderDefenseStatus(data);
    
    // 同时拉取网络告警历史
    fetchNetworkAlerts();
  } catch (e) {
    renderDefenseOffline(e.message);
  }
  
  setDefenseLoading(false);
}

function renderDefenseStatus(data) {
  const walls = data.walls || {};
  
  // 整体状态 — v2.1: green bool
  const overallIcon = document.getElementById('defense-overall-icon');
  const overallStatus = document.getElementById('defense-overall-status');
  const overallTime = document.getElementById('defense-overall-time');
  
  if (overallIcon) {
    overallIcon.textContent = data.overall_green ? '🟢' : '🔴';
  }
  if (overallStatus) {
    overallStatus.textContent = data.overall_green
      ? `🟢 四道防线全绿 (${data.green_count}/${data.total_walls})`
      : `🔴 防线未全绿 (${data.green_count}/${data.total_walls})`;
  }
  if (overallTime) overallTime.textContent = new Date().toLocaleTimeString('zh-CN');
  
  // 防线一：网络强制执行防火墙
  const w1 = walls.wall_1_network_guard || {};
  setWallStatus(1, w1);
  setStat('wall-1-blocks', w1.block_count ?? '—');
  setStat('wall-1-alerts', w1.alert_count ?? '—');
  setStat('wall-1-pending', w1.pending_alerts ?? '—');
  setStat('wall-1-firewall', w1.firewall_initialized ? '已激活' : '未初始化');
  setStat('wall-1-whitelist', w1.whitelist_count ?? '—');
  
  // 防线二：恶意代码过滤
  const w2 = walls.wall_2_malware_guard || {};
  setWallStatus(2, w2);
  setStat('wall-2-hits', w2.hit_count ?? '—');
  setStat('wall-2-version', w2.signature_version ?? '—');
  setStat('wall-2-intel-hashes', w2.threat_intel_hash_count ?? '—');
  setStat('wall-2-intel-fresh', w2.threat_intel_fresh ? '✅ 新鲜' : (w2.threat_intel_synced_ever ? '🟡 过期' : '❌ 未同步'));
  
  // 防线三：设备绑定加密
  const w3 = walls.wall_3_device_vault || {};
  setWallStatus(3, w3);
  setStat('wall-3-enc', w3.encryption ?? '—');
  setStat('wall-3-fp', w3.device_fingerprint ?? '—');
  
  // 防线四：导出绑定
  const w4 = walls.wall_4_export_bind || {};
  setWallStatus(4, w4);
  setStat('wall-4-server', '鲲鹏 :8774');
  setStat('wall-4-protocol', 'LH-EXPORT-BIND-v1.0');
}

function setWallStatus(wallNum, wall) {
  const el = document.getElementById(`wall-${wallNum}-status`);
  const card = document.getElementById(`wall-card-${wallNum}`);
  if (!el) return;
  
  // v2.1: green bool, no yellow. 非绿即红.
  const isGreen = wall.green === true;
  const color = isGreen ? 'green' : 'red';
  const status = wall.status || (isGreen ? 'active' : 'fail');
  
  const iconMap = {
    'green': '✅',
    'red': '❌',
  };
  
  el.textContent = `${iconMap[color] || '❓'} ${status}`;
  if (card) {
    card.className = `defense-card card-${color}`;
  }
}

function setStat(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = String(value ?? '—');
}

async function fetchNetworkAlerts() {
  try {
    const resp = await fetch(`${COLLECTOR_API}/defense/network-alerts`, {
      signal: AbortSignal.timeout(5000)
    });
    if (!resp.ok) return;
    
    const data = await resp.json();
    if (data.alerts && data.alerts.length > 0) {
      renderNetworkAlerts(data.alerts);
    }
  } catch (e) {
    // 网络告警非关键
  }
}

function renderNetworkAlerts(alerts) {
  const section = document.getElementById('defense-alerts-section');
  const list = document.getElementById('defense-alerts-list');
  if (!section || !list) return;
  
  section.style.display = 'block';
  
  let html = '';
  alerts.slice(-5).reverse().forEach(a => {
    const timeStr = a.timestamp ? new Date(a.timestamp * 1000).toLocaleTimeString('zh-CN') : '?';
    const icon = a.firewall_executed ? '🚫' : (a.blocked ? '⚠️' : '🔔');
    const action = a.firewall_executed ? '防火墙已阻断' : (a.blocked ? '待阻断' : '仅告警');
    
    html += `
      <div class="defense-alert-item">
        <span class="alert-icon">${icon}</span>
        <div class="alert-info">
          <span class="alert-process">${escapeHtml(a.process_name)} (PID:${a.pid})</span>
          <span class="alert-target">→ ${escapeHtml(a.remote_addr_hash || '?')}</span>
        </div>
        <span class="alert-action ${a.blocked ? 'blocked' : 'warn'}">${action}</span>
        <span class="alert-time">${timeStr}</span>
      </div>
    `;
  });
  
  list.innerHTML = html + list.innerHTML;
}

function dismissAlerts() {
  const section = document.getElementById('defense-alerts-section');
  const list = document.getElementById('defense-alerts-list');
  if (section) section.style.display = 'none';
  if (list) list.innerHTML = '';
}

function renderDefenseOffline(errorMsg) {
  const overallStatus = document.getElementById('defense-overall-status');
  const overallIcon = document.getElementById('defense-overall-icon');
  
  if (overallStatus) overallStatus.textContent = `采集引擎未连接: ${errorMsg}`;
  if (overallIcon) overallIcon.textContent = '🔴';
  
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`wall-${i}-status`);
    if (el) el.textContent = '❌ 离线';
    const card = document.getElementById(`wall-card-${i}`);
    if (card) card.className = 'defense-card card-red';
  }
  
  setStat('wall-1-blocks', '—');
  setStat('wall-1-alerts', '—');
  setStat('wall-1-pending', '—');
  setStat('wall-2-hits', '—');
  setStat('wall-2-version', '—');
  setStat('wall-3-enc', '—');
  setStat('wall-3-fp', '—');
}

function setDefenseLoading(loading) {
  const btn = document.getElementById('btn-defense-refresh');
  if (btn) {
    btn.textContent = loading ? '⏳ 刷新中...' : '🔄 刷新';
    btn.disabled = loading;
  }
}
