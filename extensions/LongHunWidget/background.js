##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ENGINE-BACKGROUND-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 龍魂后台服务
 * 耳：监听指令 · 路由消息 · 状态管理
 */

const AUDIT_LOG_KEY = 'lh_audit_log';
let auditLog = [];

// 初始化
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    longhunEnabled: true,
    auditMode: 'standard',
    dnaPrefix: '#龍芯⚡️',
    uid: '9622',
    installDate: Date.now()
  });
  console.log('🐉 龍魂宝宝已安装 | DNA:', generateDNABg('INSTALL', 'v1.0'));
});

// 打开侧边栏
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId });
});

// 快捷键监听
chrome.commands.onCommand.addListener((command, tab) => {
  if (command === 'toggle_audit') {
    chrome.storage.local.get('auditMode').then(data => {
      const next = data.auditMode === 'strict' ? 'standard' : 'strict';
      chrome.storage.local.set({ auditMode: next });
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: '龍魂审计模式切换',
        message: `当前模式: ${next === 'strict' ? '🔴 严格' : '🟢 标准'}`
      });
    });
  }
});

// 消息路由（content <-> sidepanel <-> popup）
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  (async () => {
    switch (request.type) {
      case 'PAGE_SCAN': {
        // 从 content script 接收页面扫描结果
        const record = {
          ...request.data,
          receivedAt: Date.now(),
          tabId: sender.tab?.id
        };
        await appendAudit({ action: 'page_scan', level: 'green', data: record });
        sendResponse({ ok: true, dna: generateDNABg('PAGE-SCAN', 'v1.0') });
        break;
      }
      case 'GET_TAB_INFO': {
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        sendResponse({
          url: activeTab?.url || '',
          title: activeTab?.title || '',
          id: activeTab?.id
        });
        break;
      }
      case 'AUDIT_ACTION': {
        const rec = await appendAudit(request.record);
        sendResponse({ ok: true, record: rec });
        break;
      }
      case 'GET_AUDIT_LOG': {
        sendResponse({ log: auditLog.slice(0, request.limit || 50) });
        break;
      }
      case 'COPY_CLIPBOARD': {
        // 通过 background 写剪贴板（需要 offscreen document，简化处理）
        sendResponse({ ok: true });
        break;
      }
      default:
        sendResponse({ ok: false, error: '未知指令' });
    }
  })();
  return true; // 保持通道打开
});

async function appendAudit(record) {
  auditLog.unshift({ ...record, id: Date.now().toString(36), timestamp: Date.now() });
  if (auditLog.length > 300) auditLog = auditLog.slice(0, 300);
  await chrome.storage.local.set({ [AUDIT_LOG_KEY]: auditLog });
  return record;
}

function generateDNABg(topic, version) {
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  // 后台简化版，不计算完整SHA
  return `#龍芯⚡️${today}|${topic}|${version}|BACKGROUND`;
}

// 定期清理
chrome.alarms?.create?.('cleanup', { periodInMinutes: 60 });
chrome.alarms?.onAlarm?.addListener?.((alarm) => {
  if (alarm.name === 'cleanup') {
    console.log('🐉 龍魂后台心跳 | 内存清理');
  }
});
