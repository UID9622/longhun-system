// ==UserScript==
// @name         龍魂 · 开发者信息栏
// @namespace    https://github.com/UID9622
// @version      1.0
// @description  任何网页底部显示开发者信息栏：页面加载时间、DOM元素数、请求数、Cookie数
// @author       诸葛鑫（UID9622）
// @match        *://*/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    // 排除特定页面（避免干扰）
    if (location.hostname === 'localhost') return;

    const bar = document.createElement('div');
    bar.id = 'longhun-dev-bar';

    // 收集数据
    const perf = performance.timing;
    const loadTime = ((perf.loadEventEnd - perf.navigationStart) / 1000).toFixed(2);
    const domCount = document.querySelectorAll('*').length;
    const cookieCount = document.cookie ? document.cookie.split(';').length : 0;
    const scripts = document.querySelectorAll('script').length;
    const links = document.querySelectorAll('a').length;
    const images = document.querySelectorAll('img').length;
    const protocol = location.protocol === 'https:' ? '🔒' : '⚠️';

    bar.innerHTML = `
        <span>${protocol} ${location.hostname}</span>
        <span>⏱ ${loadTime}s</span>
        <span>🏗 DOM: ${domCount.toLocaleString()}</span>
        <span>📜 JS: ${scripts}</span>
        <span>🔗 链接: ${links}</span>
        <span>🖼 图片: ${images}</span>
        <span>🍪 Cookie: ${cookieCount}</span>
        <span style="color:#d4af37">龍魂·UID9622</span>
    `;

    bar.style.cssText = `
        position: fixed; bottom: 0; left: 0; right: 0; z-index: 99999;
        background: #0a0a14; border-top: 1px solid #1a1a2e;
        padding: 4px 16px; font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: #666; display: flex; gap: 20px;
        align-items: center; opacity: 0.85; transition: opacity .3s;
    `;

    bar.addEventListener('mouseenter', () => bar.style.opacity = '1');
    bar.addEventListener('mouseleave', () => bar.style.opacity = '0.85');
    bar.addEventListener('dblclick', () => bar.style.display = 'none');

    // 延迟加载确保数据准确
    setTimeout(() => document.body.appendChild(bar), 1500);

    console.log('🐉 龍魂开发者信息栏已加载');
})();
