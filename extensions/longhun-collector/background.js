// ============================================================
// 龍魂系统 · 浏览器后台引擎 v2.1
// DNA: #龍芯⚡️丙午·乙申·COLLECTOR-v2.1-BG
// UID9622 | 龍芯北辰
// 角色：离线队列保底 · popup交互 · 定时健康检查
// 主采集路径已迁移到 content.js 直连
// ============================================================

const CONFIG = {
  serverUrl: 'http://localhost:9622',
  dna: '#龍芯⚡️丙午·乙申·COLLECTOR-v2.0',
  uid: '9622',
  autoSaveInterval: 5,       // 分钟
  retryInterval: 1,           // 重试间隔（分钟）
  maxRetries: 10,
  maxQueueSize: 500,
  batchSize: 5,              // 批量上报条数
  debounceMs: 8000,
};

// ---- 状态 ----
let state = {
  connected: false,
  queueSize: 0,
  totalCollected: 0,
  totalSent: 0,
  lastCollectTime: null,
  lastError: null,
  sitesCollected: {},
};

// ---- 初始化 ----
async function init() {
  const stored = await chrome.storage.local.get(['state', 'offlineQueue']);
  if (stored.state) state = { ...state, ...stored.state };
  await chrome.storage.local.set({ state });
  chrome.alarms.create('lh-auto-save', { periodInMinutes: CONFIG.autoSaveInterval });
  chrome.alarms.create('lh-retry-queue', { periodInMinutes: CONFIG.retryInterval });
  chrome.alarms.create('lh-health-check', { periodInMinutes: 1 });
  await checkServerHealth();
  console.log('🐉 龍魂后台引擎 v2.0 已启动 | UID9622 | 队列:', state.queueSize);
}

// ---- 服务健康检查 ----
async function checkServerHealth() {
  try {
    const resp = await fetch(`${CONFIG.serverUrl}/health`, { signal: AbortSignal.timeout(3000) });
    state.connected = resp.ok;
  } catch {
    state.connected = false;
  }
  await chrome.storage.local.set({ state });
}

// ---- 离线队列管理 ----
async function getQueue() {
  const { offlineQueue } = await chrome.storage.local.get(['offlineQueue']);
  return offlineQueue || [];
}

async function enqueue(data) {
  const { offlineQueue } = await chrome.storage.local.get(['offlineQueue']);
  const queue = offlineQueue || [];
  if (queue.length >= CONFIG.maxQueueSize) queue.shift();
  queue.push({ data, timestamp: Date.now(), retries: 0 });
  state.queueSize = queue.length;
  state.totalCollected++;
  state.lastCollectTime = Date.now();
  const site = data.site || 'unknown';
  state.sitesCollected[site] = (state.sitesCollected[site] || 0) + 1;
  await chrome.storage.local.set({ offlineQueue: queue, state });
}

async function flushQueue() {
  const { offlineQueue } = await chrome.storage.local.get(['offlineQueue']);
  if (!offlineQueue || offlineQueue.length === 0) return;

  const queue = [...offlineQueue];
  let sent = 0;

  for (let i = 0; i < queue.length; i += CONFIG.batchSize) {
    const batch = queue.slice(i, i + CONFIG.batchSize);
    const results = await Promise.allSettled(
      batch.map(item => sendToServer(item.data))
    );

    results.forEach((r, j) => {
      if (r.status === 'fulfilled' && r.value) {
        queue[i + j] = null;
        sent++;
        state.totalSent++;
      } else if (r.status === 'fulfilled' && !r.value) {
        queue[i + j].retries++;
        if (queue[i + j].retries > CONFIG.maxRetries) queue[i + j] = null;
      } else {
        if (queue[i + j]) queue[i + j].retries++;
        if (queue[i + j] && queue[i + j].retries > CONFIG.maxRetries) queue[i + j] = null;
      }
    });
  }

  const remaining = queue.filter(item => item !== null);
  state.queueSize = remaining.length;
  await chrome.storage.local.set({ offlineQueue: remaining, state });
  if (sent > 0) console.log(`🐉 龍魂: 批量上报 ${sent} 条 | 队列剩余 ${remaining.length}`);
}

async function sendToServer(data) {
  try {
    const resp = await fetch(`${CONFIG.serverUrl}/collect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      signal: AbortSignal.timeout(5000),
    });
    return resp.ok;
  } catch {
    return false;
  }
}

// ---- 定时器 ----
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'lh-auto-save') triggerCollectCurrentTab();
  if (alarm.name === 'lh-retry-queue') flushQueue();
  if (alarm.name === 'lh-health-check') checkServerHealth();
});

// ---- 采集当前标签页 ----
async function triggerCollectCurrentTab() {
  try {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tabs[0]?.url || tabs[0].url.startsWith('chrome://')) return;

    const hostname = new URL(tabs[0].url).hostname;
    const supported = ['kimi.com', 'moonshot.cn', 'douyin.com', 'csdn.net',
      'notion.site', 'github.com', 'gitee.com', 'weibo.com',
      'zhihu.com', 'juejin.cn', 'bilibili.com', 'mp.weixin.qq.com'];
    if (!supported.some(s => hostname.includes(s))) return;

    await chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: () => { if (window.__lhCollect) window.__lhCollect(); },
    }).catch(() => {});
  } catch {}
}

// ---- 标签页切换监听 ----
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    const tab = await chrome.tabs.get(activeInfo.tabId);
    if (tab?.url && !tab.url.startsWith('chrome://')) {
      triggerCollectForTab(activeInfo.tabId);
    }
  } catch {}
});

async function triggerCollectForTab(tabId) {
  await chrome.scripting.executeScript({
    target: { tabId },
    func: () => { if (window.__lhCollect) window.__lhCollect(); },
  }).catch(() => {});
}

// ---- 消息通信（popup ↔ background ↔ content） ----
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  (async () => {
    switch (request.action) {
      case 'collect-now':
        await triggerCollectCurrentTab();
        sendResponse({ status: 'triggered', queueSize: state.queueSize });
        break;
      case 'get-state':
        sendResponse({
          connected: state.connected,
          queueSize: state.queueSize,
          totalCollected: state.totalCollected,
          totalSent: state.totalSent,
          lastCollectTime: state.lastCollectTime,
          lastError: state.lastError,
          sitesCollected: state.sitesCollected,
          serverUrl: CONFIG.serverUrl,
          dna: CONFIG.dna,
        });
        break;
      case 'get-queue':
        const queue = await getQueue();
        sendResponse({ queue: queue.slice(0, 50), total: queue.length });
        break;
      case 'flush-queue':
        await flushQueue();
        sendResponse({ status: 'flushed', remaining: state.queueSize });
        break;
      case 'clear-queue':
        await chrome.storage.local.set({ offlineQueue: [] });
        state.queueSize = 0;
        await chrome.storage.local.set({ state });
        sendResponse({ status: 'cleared' });
        break;
      case 'collect-result':
        // content script 采集完成，入队列
        await enqueue(request.data);
        if (state.connected) await flushQueue();
        sendResponse({ status: 'queued', queueSize: state.queueSize });
        break;
      default:
        sendResponse({ error: 'unknown action' });
    }
  })();
  return true;
});

// ---- 安装/更新 ----
chrome.runtime.onInstalled.addListener(async (details) => {
  console.log(`🐉 龍魂采集器 ${details.reason === 'install' ? '已安装' : '已更新'} | v2.0.0 | UID9622`);
  await init();
});

// 冷启动
init();
