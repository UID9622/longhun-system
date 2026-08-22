// ============================================================
// DNA: #龍芯⚡️丙午·乙未·丁酉·子时·䷀乾-GUANLAN-POPUP-v1.0-js4b1e29
// 创建者: 诸葛鑫 (UID9622)
// 协议: CC BY-NC-SA 4.0
// ============================================================
// 龍魂 · 观澜主权网关 — Popup UI
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initToggle();
  initBreaker();
  initKillSwitch();
  initDashboardLink();
  loadStatus();
  loadCurrentTabThreats();

  // 每3秒刷新
  setInterval(loadStatus, 3000);
});

// ============================================================
// Tab切换
// ============================================================
function initTabs() {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(`panel-${tab.dataset.tab}`).classList.add('active');
    });
  });
}

// ============================================================
// 开关
// ============================================================
function initToggle() {
  document.getElementById('toggleBtn').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'getStatus' }, (status) => {
      const newValue = !status.enabled;
      chrome.runtime.sendMessage(
        { action: 'toggleEnabled', value: newValue },
        () => updateToggleUI(newValue)
      );
    });
  });
}

function updateToggleUI(enabled) {
  const indicator = document.getElementById('statusIndicator');
  const text = document.getElementById('statusText');
  const btn = document.getElementById('toggleBtn');

  if (enabled) {
    indicator.className = 'status-indicator active';
    text.textContent = '守卫中';
    btn.textContent = '■';
    btn.className = 'toggle-btn active';
  } else {
    indicator.className = 'status-indicator inactive';
    text.textContent = '已暂停';
    btn.textContent = '▶';
    btn.className = 'toggle-btn inactive';
  }
}

// ============================================================
// 加载状态
// ============================================================
function loadStatus() {
  chrome.runtime.sendMessage({ action: 'getStatus' }, (status) => {
    if (!status) return;

    updateToggleUI(status.enabled);
    updateAIList(status.activeAI || []);
    updateBreakerUI(status.circuitBreaker);
    updateThreats();
  });
}

function updateAIList(aiList) {
  const container = document.getElementById('aiList');
  if (!aiList || aiList.length === 0) {
    container.innerHTML = '<div class="empty-state">暂无检测到的AI连接</div>';
    return;
  }

  container.innerHTML = aiList.map(ai => `
    <div class="ai-card">
      <div class="ai-card-header">
        <span class="ai-name">${escapeHTML(ai.name || '未知AI')}</span>
        <span class="ai-type">${ai.type || ''}</span>
      </div>
      <div class="ai-card-url">${escapeHTML(ai.url || '').substring(0, 60)}</div>
      <div class="ai-card-time">${formatTime(ai.startTime)}</div>
      <div class="ai-card-actions">
        <button class="ai-action-btn allow" data-url="${escapeHTML(ai.url)}">允许</button>
        <button class="ai-action-btn block" data-url="${escapeHTML(ai.url)}">阻断</button>
      </div>
    </div>
  `).join('');

  // 按钮事件
  container.querySelectorAll('.ai-action-btn.allow').forEach(btn => {
    btn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'whitelistAI', url: btn.dataset.url });
      btn.textContent = '已允许';
      btn.disabled = true;
    });
  });

  container.querySelectorAll('.ai-action-btn.block').forEach(btn => {
    btn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'blockAI', url: btn.dataset.url });
      btn.textContent = '已阻断';
      btn.disabled = true;
    });
  });
}

// ============================================================
// 威胁列表
// ============================================================
function updateThreats() {
  chrome.storage.local.get(['privacy_events'], (result) => {
    const events = (result.privacy_events || []).slice(-20).reverse();
    const container = document.getElementById('threatList');

    if (events.length === 0) {
      container.innerHTML = '<div class="empty-state">未检测到隐私威胁</div>';
      return;
    }

    container.innerHTML = events.map(e => `
      <div class="threat-item ${e.type}">
        <span class="threat-icon">${getThreatIcon(e.type)}</span>
        <div class="threat-detail">
          <div class="threat-type">${getThreatLabel(e.type)}</div>
          <div class="threat-url">${escapeHTML(e.url || e.detail || '').substring(0, 50)}</div>
          <div class="threat-time">${formatTime(e.timestamp)}</div>
        </div>
      </div>
    `).join('');
  });
}

function getThreatIcon(type) {
  const map = {
    'third_party_cookie': '🍪', 'tracking_domain': '👁️',
    'canvas_fingerprint': '🖼️', 'webrtc_leak': '📡',
    'websocket': '🔌', 'ai_script': '🤖'
  };
  return map[type] || '⚠️';
}

function getThreatLabel(type) {
  const map = {
    'third_party_cookie': '第三方Cookie',
    'tracking_domain': '追踪脚本',
    'canvas_fingerprint': 'Canvas指纹',
    'webrtc_leak': 'WebRTC泄露',
    'websocket': 'WebSocket',
    'ai_script': 'AI脚本'
  };
  return map[type] || type;
}

// ============================================================
// 当前标签页威胁扫描
// ============================================================
async function loadCurrentTabThreats() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) return;

  // 请求content script检测
  chrome.tabs.sendMessage(tab.id, { action: 'scan' }, (response) => {
    if (response) {
      updateScoreDisplay(response);
    }
  });
}

function updateScoreDisplay(data) {
  const score = data.score || 0;
  document.getElementById('scoreValue').textContent = score;
  document.getElementById('aiCount').textContent = data.findings?.aiScripts?.length || 0;
  document.getElementById('trackerCount').textContent = data.findings?.trackers?.length || 0;
  document.getElementById('fingerprintDetected').textContent = data.findings?.canvasFingerprint ? '⚠️是' : '否';
  document.getElementById('webrtcDetected').textContent = data.findings?.webrtcDetected ? '⚠️是' : '否';

  const circle = document.getElementById('scoreCircle');
  circle.className = 'score-circle';
  if (score >= 70) circle.classList.add('danger');
  else if (score >= 40) circle.classList.add('warning');
  else circle.classList.add('safe');
}

// ============================================================
// 断路器
// ============================================================
function initBreaker() {
  document.getElementById('breakerLockBtn').addEventListener('click', () => {
    chrome.runtime.sendMessage({
      action: 'toggleBreaker',
      lock: true,
      reason: '用户手动熔断'
    });
  });

  document.getElementById('breakerUnlockBtn').addEventListener('click', () => {
    chrome.runtime.sendMessage({
      action: 'toggleBreaker',
      lock: false
    });
  });
}

function updateBreakerUI(cb) {
  const header = document.getElementById('breakerHeader');
  const info = document.getElementById('breakerInfo');

  if (cb.locked && Date.now() < cb.lockUntil) {
    header.innerHTML = '<span class="breaker-active">🚨 已熔断</span>';
    const remaining = Math.ceil((cb.lockUntil - Date.now()) / 1000);
    info.innerHTML = `剩余锁定时间: ${remaining}秒<br>到期: ${new Date(cb.lockUntil).toLocaleTimeString()}`;
  } else {
    header.innerHTML = '<span class="breaker-normal">🟢 正常运行</span>';
    info.innerHTML = '断路器待命中，异常行为将自动触发熔断。';
  }
}

// ============================================================
// 一键切断
// ============================================================
function initKillSwitch() {
  document.getElementById('killAllBtn').addEventListener('click', () => {
    if (confirm('确定要切断所有AI连接吗？\n\n所有正在进行中的AI请求将被拒绝。')) {
      chrome.runtime.sendMessage({
        action: 'toggleBreaker',
        lock: true,
        reason: '用户一键切断所有AI'
      });
    }
  });
}

// ============================================================
// 仪表盘链接
// ============================================================
function initDashboardLink() {
  document.getElementById('dashboardBtn').addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://127.0.0.1:8770/guanlan' });
  });
}

// ============================================================
// 工具函数
// ============================================================
function formatTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function pad(n) {
  return n < 10 ? '0' + n : '' + n;
}

function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
