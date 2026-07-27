/**
 * 龍魂 · 浏览器史官 — Background Service Worker
 * 负责全量读取 Chrome 历史记录 + 增量监听
 */

importScripts('classifier.js');

const DB_KEY = 'longhun_history_scan';
const SCAN_STATUS_KEY = 'longhun_scan_status';

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 消息路由
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  switch (msg.type) {
    case 'SCAN_HISTORY':
      scanHistory(msg.daysBack, msg.onProgress)
        .then(result => sendResponse({ success: true, ...result }))
        .catch(err => sendResponse({ success: false, error: err.message }));
      return true; // async response

    case 'GET_STATUS':
      getScanStatus().then(sendResponse);
      return true;

    case 'GET_STORED_DATA':
      getStoredData().then(sendResponse);
      return true;
  }
});

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 核心：全量扫描历史记录
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async function scanHistory(daysBack = 0, onProgress) {
  const startTime = daysBack > 0
    ? Date.now() - daysBack * 24 * 60 * 60 * 1000
    : 0; // 0 = 全部历史

  const allItems = [];
  let hasMore = true;
  let endTime = Date.now();
  let batchNum = 0;

  while (hasMore) {
    batchNum++;
    const items = await chrome.history.search({
      text: '',
      startTime: startTime,
      endTime: endTime,
      maxResults: 10000,
    });

    if (items.length === 0) {
      hasMore = false;
    } else {
      for (const item of items) {
        allItems.push({
          id: item.id,
          url: item.url,
          title: item.title || '',
          visitCount: item.visitCount || 0,
          typedCount: item.typedCount || 0,
          lastVisitTime: item.lastVisitTime || 0,
        });
      }

      // 用最旧的时间戳作为下一批的 endTime
      endTime = items[items.length - 1].lastVisitTime - 1;
      if (endTime < startTime || batchNum > 500) {
        hasMore = false;
      }

      // 进度回调
      if (onProgress) {
        onProgress({
          batch: batchNum,
          totalItems: allItems.length,
          hasMore,
        });
      }
    }
  }

  // 去重（按URL）
  const seen = new Set();
  const unique = [];
  for (const item of allItems) {
    const key = item.url;
    if (!seen.has(key)) {
      seen.add(key);
      unique.push(item);
    }
  }

  // 分类
  const classified = classifyBatch(unique);
  const stats = getStats(classified);

  // 按分类排序
  const sorted = classified.sort((a, b) => {
    if (a.cat !== b.cat) return a.cat.localeCompare(b.cat);
    return b.visitCount - a.visitCount;
  });

  // 存储结果
  const scanResult = {
    scanTime: Date.now(),
    totalRaw: allItems.length,
    totalUnique: unique.length,
    stats: Object.fromEntries(
      Object.entries(stats).map(([k, v]) => [k, { ...v, items: undefined }])
    ),
    items: sorted.map(item => ({
      url: item.url,
      title: item.title,
      visitCount: item.visitCount,
      lastVisitTime: item.lastVisitTime,
      cat: item.cat,
      catName: item.name,
      catIcon: item.icon,
      catColor: item.color,
    })),
    batches: batchNum,
  };

  await chrome.storage.local.set({ [DB_KEY]: scanResult });
  await chrome.storage.local.set({
    [SCAN_STATUS_KEY]: {
      lastScan: Date.now(),
      totalItems: unique.length,
      status: 'done',
    },
  });

  return {
    totalRaw: allItems.length,
    totalUnique: unique.length,
    batches: batchNum,
    stats: scanResult.stats,
  };
}

async function getScanStatus() {
  const data = await chrome.storage.local.get(SCAN_STATUS_KEY);
  return data[SCAN_STATUS_KEY] || { status: 'never' };
}

async function getStoredData() {
  const data = await chrome.storage.local.get(DB_KEY);
  return data[DB_KEY] || null;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 安装/更新时初始化
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    [SCAN_STATUS_KEY]: { status: 'never' },
  });
  console.log('龍魂 · 浏览器史官 v1.0 已安装');
  console.log('数据主权归你，一切在本地。');
});
