# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-CNSH-CONTENT-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 内容脚本：桥接网页与 background
 * 监听选中文本的消息请求，并支持从 popup / 右键菜单触发
 */

(function () {
  'use strict';

  // 对外暴露 "获取当前选中文本" 的消息响应
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg && msg.type === 'CNSH_GET_SELECTION') {
      const sel = (window.getSelection && window.getSelection().toString()) || '';
      sendResponse({
        ok: true,
        text: sel,
        url: window.location.href,
        title: document.title
      });
      return true;
    }
    if (msg && msg.type === 'CNSH_RESCAN') {
      if (window.CNSH && typeof window.CNSH.scanAndHighlight === 'function') {
        window.CNSH.scanAndHighlight();
        sendResponse({ ok: true });
      } else {
        sendResponse({ ok: false, err: 'highlighter not ready' });
      }
      return true;
    }
    if (msg && msg.type === 'CNSH_TOAST') {
      showToast(msg.text || '已入库', msg.level || 'info');
      sendResponse({ ok: true });
      return true;
    }
  });

  /**
   * 页面内小提示条（不依赖 Chrome notifications，避免权限弹窗）
   */
  function showToast(text, level) {
    const colors = {
      info: '#8b5cf6',
      success: '#10b981',
      warn: '#eab308',
      error: '#ef4444'
    };
    const el = document.createElement('div');
    el.textContent = `⚡ ${text}`;
    Object.assign(el.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      zIndex: '2147483647',
      padding: '10px 18px',
      background: colors[level] || colors.info,
      color: '#fff',
      borderRadius: '6px',
      fontFamily: '"PingFang SC", "Microsoft YaHei", sans-serif',
      fontSize: '14px',
      fontWeight: '600',
      boxShadow: '0 4px 20px rgba(0,0,0,0.35)',
      transition: 'opacity 0.3s ease',
      opacity: '0'
    });
    document.documentElement.appendChild(el);
    requestAnimationFrame(() => { el.style.opacity = '1'; });
    setTimeout(() => {
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 2500);
  }

  // 暴露给 popup / options 调试用
  window.__CNSH_TOAST__ = showToast;
})();
