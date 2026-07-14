##龍芯⚡️2026-06-21-CNSH-BACKGROUND-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 龍魂 CNSH · Service Worker
 * 职责: 右键菜单 · 快捷键 · 消息中继 · Notion 写入
 */

import {
  sendToInbox, sendToDNA, sendToHeart,
  testConnection, getConfig
} from './lib/notion-api.js';

// ─────────────────────────────────────────
// 右键菜单注册
// ─────────────────────────────────────────
chrome.runtime.onInstalled.addListener(async () => {
  chrome.contextMenus.removeAll();

  chrome.contextMenus.create({
    id: 'cnsh_send_inbox',
    title: '🧩 送入 Inbox（待净化）',
    contexts: ['selection', 'page', 'link']
  });
  chrome.contextMenus.create({
    id: 'cnsh_send_dna',
    title: '🧬 直接入 DNA 库（已净化）',
    contexts: ['selection']
  });
  chrome.contextMenus.create({
    id: 'cnsh_send_heart',
    title: '💖 录入人心算法',
    contexts: ['selection']
  });
  chrome.contextMenus.create({
    id: 'cnsh_sep', type: 'separator', contexts: ['all']
  });
  chrome.contextMenus.create({
    id: 'cnsh_options',
    title: '⚙️ 配置龍魂连接',
    contexts: ['all']
  });

  // 首次安装提示
  const cfg = await getConfig();
  if (!cfg.notion_token) {
    chrome.runtime.openOptionsPage();
  }
});

// ─────────────────────────────────────────
// 右键点击处理
// ─────────────────────────────────────────
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  try {
    const selText = info.selectionText || '';
    const url = info.pageUrl || (tab && tab.url) || '';
    const title = (tab && tab.title) || '未命名';

    if (info.menuItemId === 'cnsh_send_inbox') {
      await sendToInbox({
        title: selText ? selText.slice(0, 60) : title,
        url,
        sourceText: selText || title
      });
      await toast(tab, '已送入 Inbox', 'success');
    }
    else if (info.menuItemId === 'cnsh_send_dna') {
      await sendToDNA({
        concept: selText.slice(0, 60),
        techPoint: selText,
        direction: '待补充',
        purity: 70
      });
      await toast(tab, '已入 DNA 库', 'success');
    }
    else if (info.menuItemId === 'cnsh_send_heart') {
      await sendToHeart({
        title: selText.slice(0, 40),
        insight: selText,
        scene: '网页选段'
      });
      await toast(tab, '已录入人心算法', 'success');
    }
    else if (info.menuItemId === 'cnsh_options') {
      chrome.runtime.openOptionsPage();
    }
  } catch (e) {
    console.error('[CNSH]', e);
    await toast(tab, `失败: ${e.message}`, 'error');
  }
});

// ─────────────────────────────────────────
// 快捷键处理
// ─────────────────────────────────────────
chrome.commands.onCommand.addListener(async (command) => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) return;

  if (command === 'quick_capture') {
    try {
      const sel = await getSelection(tab.id);
      const text = (sel && sel.text) || tab.title || '';
      await sendToInbox({
        title: text.slice(0, 60),
        url: tab.url,
        sourceText: text
      });
      await toast(tab, '⚡ 快速入 Inbox 成功', 'success');
    } catch (e) {
      await toast(tab, `失败: ${e.message}`, 'error');
    }
  }
  else if (command === 'open_popup') {
    try {
      await chrome.action.openPopup();
    } catch (_) {
      // 无法编程打开 popup 时，兜底打开 options
      chrome.runtime.openOptionsPage();
    }
  }
});

// ─────────────────────────────────────────
// popup / options 消息通道
// ─────────────────────────────────────────
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    try {
      if (msg.type === 'CNSH_TEST_CONN') {
        const r = await testConnection(msg.token);
        sendResponse(r);
        return;
      }
      if (msg.type === 'CNSH_SEND_INBOX') {
        const r = await sendToInbox(msg.payload);
        sendResponse({ ok: true, page: r });
        return;
      }
      if (msg.type === 'CNSH_SEND_DNA') {
        const r = await sendToDNA(msg.payload);
        sendResponse({ ok: true, page: r });
        return;
      }
      if (msg.type === 'CNSH_SEND_HEART') {
        const r = await sendToHeart(msg.payload);
        sendResponse({ ok: true, page: r });
        return;
      }
      sendResponse({ ok: false, error: 'unknown message' });
    } catch (e) {
      sendResponse({ ok: false, error: e.message, status: e.status });
    }
  })();
  return true; // 异步响应
});

// ─────────────────────────────────────────
// 辅助: 获取选中文本
// ─────────────────────────────────────────
async function getSelection(tabId) {
  try {
    const r = await chrome.tabs.sendMessage(tabId, { type: 'CNSH_GET_SELECTION' });
    return r;
  } catch (_) {
    return { text: '' };
  }
}

// ─────────────────────────────────────────
// 辅助: 页面内 toast
// ─────────────────────────────────────────
async function toast(tab, text, level = 'info') {
  if (!tab || !tab.id) return;
  try {
    await chrome.tabs.sendMessage(tab.id, { type: 'CNSH_TOAST', text, level });
  } catch (_) {
    // 内容脚本不在页面（例如 chrome:// 页），降级为系统通知
    try {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: '龍魂 CNSH',
        message: text
      });
    } catch (_) {}
  }
}
