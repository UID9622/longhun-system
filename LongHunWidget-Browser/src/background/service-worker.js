/**
 * 🐉 龍魂宝宝·DNA追溯助手 · 后台服务脚本
 * DNA: #龍芯⚡️20260525|LONGHUNWIDGET-BACKGROUND|v1.0|xxxxx
 *
 * 职责：
 * ① 管理DNA注册表和侵权黑名单
 * ② 监听右键菜单事件
 * ③ 与DNA追溯流水线通信
 * ④ 管理证据包导出
 */

const UID9622 = "9622";
const CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";
const API_ENDPOINT = "http://localhost:5000"; // 本地龍魂API

// ========== 初始化 ==========

chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('🐉 龍魂DNA追溯助手已安装');

    // 初始化存储
    chrome.storage.local.get(null, (items) => {
      if (Object.keys(items).length === 0) {
        initializeStorage();
      }
    });

    // 设置菜单
    setupContextMenus();
  }
});

function initializeStorage() {
  const initialData = {
    uid: UID9622,
    confirm_code: CONFIRM_CODE,
    dna_registry: [],
    blacklist: [],
    evidence_cache: {},
    settings: {
      auto_detect: true,
      auto_watermark: false,
      show_notifications: true
    }
  };

  chrome.storage.local.set(initialData);
  console.log('✅ 本地存储已初始化');
}

// ========== 右键菜单 ==========

chrome.runtime.onStartup.addListener(() => {
  console.log('✅ Browser 啟動');
  setupContextMenus();
});

function setupContextMenus() {
  // 清除旧菜单
  chrome.contextMenus.removeAll();

  // 菜单1: 标记侵权
  chrome.contextMenus.create({
    id: 'mark-infringement',
    title: '🚨 标记为侵权',
    contexts: ['page'],
    icons: { '16': 'public/icon-16.png' }
  });

  // 菜单2: 添加DNA
  chrome.contextMenus.create({
    id: 'add-dna',
    title: '✍️ 添加DNA签名',
    contexts: ['page']
  });

  // 菜单3: 复制DNA
  chrome.contextMenus.create({
    id: 'copy-dna',
    title: '📋 复制页面DNA',
    contexts: ['page']
  });

  // 菜单4: 导出证据
  chrome.contextMenus.create({
    id: 'export-evidence',
    title: '📦 导出证据包',
    contexts: ['page']
  });
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  switch (info.menuItemId) {
    case 'mark-infringement':
      markAsInfringement(tab);
      break;
    case 'add-dna':
      addDNAToPage(tab);
      break;
    case 'copy-dna':
      copyPageDNA(tab);
      break;
    case 'export-evidence':
      exportEvidence(tab);
      break;
  }
});

// ========== DNA检测与追溯 ==========

async function markAsInfringement(tab) {
  console.log(`🚨 标记侵权: ${tab.url}`);

  // 生成证据
  const evidence = {
    url: tab.url,
    title: tab.title,
    timestamp: new Date().toISOString(),
    detected_dna: null,
    hooks: []
  };

  // 向content script发送消息扫描水印
  chrome.tabs.sendMessage(tab.id, {
    action: 'scan_watermark',
    payload: {}
  }, (response) => {
    if (response && response.dna) {
      evidence.detected_dna = response.dna;
      evidence.hooks = response.hooks || [];

      // 保存到本地
      saveEvidence(evidence);

      // 显示通知
      chrome.notifications.create('infringement-' + Date.now(), {
        type: 'basic',
        iconUrl: 'public/icon-128.png',
        title: '🚨 侵权已记录',
        message: `URL: ${tab.url}\nDNA: ${evidence.detected_dna}`
      });
    }
  });
}

async function addDNAToPage(tab) {
  console.log(`✍️ 为页面添加DNA: ${tab.url}`);

  // 调用DNA生成API
  const response = await fetch(`http://localhost:5000/dna/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      topic: extractTopicFromPage(tab.title),
      platform: extractPlatform(tab.url),
      uid: UID9622
    })
  }).catch(err => {
    console.error('API调用失败:', err);
    return null;
  });

  if (response && response.ok) {
    const data = await response.json();
    const dna = data.dna;

    // 向content script发送消息嵌入DNA
    chrome.tabs.sendMessage(tab.id, {
      action: 'embed_dna',
      dna: dna
    });

    // 显示通知
    chrome.notifications.create('dna-added-' + Date.now(), {
      type: 'basic',
      iconUrl: 'public/icon-128.png',
      title: '✅ DNA已添加',
      message: dna
    });

    // 保存到注册表
    addToRegistry(dna, tab.url, tab.title);
  }
}

async function copyPageDNA(tab) {
  // 从页面中提取DNA
  chrome.tabs.sendMessage(tab.id, {
    action: 'copy_dna_to_clipboard',
    payload: {}
  }, (response) => {
    if (response && response.dna) {
      // 显示通知（由content script负责复制）
      chrome.notifications.create('dna-copied-' + Date.now(), {
        type: 'basic',
        iconUrl: 'public/icon-128.png',
        title: '📋 已复制DNA',
        message: response.dna
      });
    }
  });
}

// ========== 数据管理 ==========

function saveEvidence(evidence) {
  chrome.storage.local.get('evidence_cache', (items) => {
    const cache = items.evidence_cache || {};
    const id = Date.now().toString();
    cache[id] = evidence;
    chrome.storage.local.set({ evidence_cache: cache });
  });
}

function addToRegistry(dna, url, title) {
  chrome.storage.local.get('dna_registry', (items) => {
    const registry = items.dna_registry || [];
    registry.push({
      dna: dna,
      url: url,
      title: title,
      timestamp: new Date().toISOString()
    });
    chrome.storage.local.set({ dna_registry: registry });
  });
}

function addToBlacklist(url, platform) {
  chrome.storage.local.get('blacklist', (items) => {
    const blacklist = items.blacklist || [];
    if (!blacklist.find(item => item.url === url)) {
      blacklist.push({
        url: url,
        platform: platform,
        added_date: new Date().toISOString(),
        violation_count: 1
      });
      chrome.storage.local.set({ blacklist: blacklist });
    }
  });
}

async function exportEvidence(tab) {
  chrome.storage.local.get(['evidence_cache', 'dna_registry', 'blacklist'], (items) => {
    const exportData = {
      uid: UID9622,
      confirm_code: CONFIRM_CODE,
      export_date: new Date().toISOString(),
      evidence: items.evidence_cache || {},
      registry: items.dna_registry || [],
      blacklist: items.blacklist || [],
      current_page: {
        url: tab.url,
        title: tab.title,
        timestamp: new Date().toISOString()
      }
    };

    // 生成JSON并下载
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    chrome.downloads.download({
      url: url,
      filename: `longhun-evidence-${Date.now()}.json`,
      saveAs: true
    });
  });
}

// ========== 工具函数 ==========

function extractTopicFromPage(title) {
  // 从页面标题提取主题
  return title.split('|')[0].trim().toUpperCase().replace(/\s+/g, '-');
}

function extractPlatform(url) {
  // 从URL识别平台
  const platforms = {
    'csdn.net': 'CSDN',
    'zhihu.com': '知乎',
    'juejin.cn': '掘金',
    'github.com': 'GitHub',
    'medium.com': 'Medium',
    'dev.to': 'Dev.to'
  };

  for (const [domain, platform] of Object.entries(platforms)) {
    if (url.includes(domain)) return platform;
  }

  return 'Custom';
}

// ========== 监听消息 ==========

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'get_storage') {
    chrome.storage.local.get(request.key, (items) => {
      sendResponse(items);
    });
    return true; // 异步响应
  }

  if (request.action === 'save_to_storage') {
    chrome.storage.local.set(request.data);
    sendResponse({ success: true });
  }

  if (request.action === 'dna_embedded') {
    // 记录已嵌入的DNA
    const dnaRecord = {
      dna: request.dna,
      title: request.title,
      platform: request.platform,
      content_length: request.content_length,
      timestamp: request.timestamp,
      url: sender.url
    };

    // 添加到注册表
    addToRegistry(request.dna, sender.url, request.title);

    // 显示通知
    chrome.notifications.create('dna-embedded-' + Date.now(), {
      type: 'basic',
      iconUrl: 'public/icon-128.png',
      title: '✅ DNA 已嵌入',
      message: `${request.platform} - ${request.title}\nDNA: ${request.dna}`
    });

    console.log('📝 DNA 嵌入已记录:', dnaRecord);
    sendResponse({ success: true });
    return true;
  }
});

console.log('🐉 龍魂DNA追溯助手·后台服务已启动');
