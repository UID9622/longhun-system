// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-696a33c1
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ENGINE-CONTENT-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * 龍魂眼 · Content Script
 * 只读，不写，不修改页面
 */

(function() {
  'use strict';

  // 防止重复注入
  if (window.__longhun_eye_injected) return;
  window.__longhun_eye_injected = true;

  const IRON_LAW = {
    no_password: true,
    no_bank: true,
    no_private: true
  };

  // 页面扫描（非侵入式）
  function scanPage() {
    const isPasswordPage = !!document.querySelector('input[type="password"]');
    const isBankPage = /bank|支付|支付宝|微信|pay|card|credit/i.test(location.hostname + document.title);
    const isPrivate = document.body.innerText.includes('🔴私密') || document.body.innerText.includes('机密');

    // 铁律检查
    if (isPasswordPage || isBankPage || isPrivate) {
      console.log('🔴 龍魂眼：检测到敏感页面，进入静默模式');
      return { restricted: true, reason: '敏感页面' };
    }

    const data = {
      url: location.href,
      domain: location.hostname,
      title: document.title,
      textLength: document.body?.innerText?.length || 0,
      images: document.images?.length || 0,
      links: document.links?.length || 0,
      headings: document.querySelectorAll('h1,h2,h3').length,
      hasForm: !!document.querySelector('form'),
      restricted: false
    };

    // 发送给后台
    if (typeof chrome !== 'undefined' && chrome.runtime) {
      chrome.runtime.sendMessage({
        type: 'PAGE_SCAN',
        data
      }).catch(() => {});
    }

    return data;
  }

  // 延迟扫描，避免干扰页面加载
  setTimeout(scanPage, 2000);

  // 监听来自 sidepanel 的请求
  if (typeof chrome !== 'undefined' && chrome.runtime) {
    chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
      if (req.type === 'EYE_READ_PAGE') {
        const data = scanPage();
        if (data.restricted) {
          sendResponse({ restricted: true, reason: data.reason });
          return;
        }
        // 返回结构化内容（摘要）
        const paragraphs = Array.from(document.querySelectorAll('p, article, section'))
          .map(el => el.innerText.trim())
          .filter(t => t.length > 20)
          .slice(0, 10);
        sendResponse({
          restricted: false,
          summary: paragraphs.join('\n\n').slice(0, 2000),
          stats: data
        });
      }
      return true;
    });
  }

  console.log('🐉 龍魂眼已激活 | 只读 · 不修改 · 有边界');
})();
