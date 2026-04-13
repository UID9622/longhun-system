/**
 * 龍魂 · 开发者信息栏
 * DNA: #龍芯⚡️2026-04-13-DEVBAR-v1.0
 * 任何网页底部显示技术数据 · 开发者的味道
 */
(function() {
    'use strict';

    // 排除本地和扩展页面
    if (location.protocol === 'chrome-extension:' ||
        location.protocol === 'chrome:' ||
        location.hostname === 'localhost' ||
        location.hostname === '127.0.0.1') return;

    // 等页面加载完
    setTimeout(() => {
        const bar = document.createElement('div');
        bar.id = 'longhun-devbar';

        // 收集数据
        const domCount = document.querySelectorAll('*').length;
        const cookieCount = document.cookie ? document.cookie.split(';').length : 0;
        const scripts = document.querySelectorAll('script').length;
        const links = document.querySelectorAll('a').length;
        const images = document.querySelectorAll('img').length;
        const protocol = location.protocol === 'https:' ? '🔒' : '⚠️';

        // 加载时间
        let loadTime = '...';
        try {
            const entries = performance.getEntriesByType('navigation');
            if (entries.length > 0) {
                loadTime = (entries[0].loadEventEnd / 1000).toFixed(2);
            }
        } catch(e) {
            loadTime = '-';
        }

        bar.innerHTML = `
            <span>${protocol} ${location.hostname}</span>
            <span>⏱ ${loadTime}s</span>
            <span>🏗 DOM:${domCount.toLocaleString()}</span>
            <span>📜 JS:${scripts}</span>
            <span>🔗 ${links}链接</span>
            <span>🖼 ${images}图</span>
            <span>🍪 ${cookieCount}</span>
            <span style="color:#d4af37;font-weight:bold">龍魂·9622</span>
        `;

        bar.style.cssText = `
            position:fixed; bottom:0; left:0; right:0; z-index:2147483647;
            background:#0a0a14; border-top:1px solid #d4af37;
            padding:3px 16px; font-family:'JetBrains Mono','SF Mono',monospace;
            font-size:11px; color:#666; display:flex; gap:16px;
            align-items:center; opacity:0.7; transition:opacity .3s;
            height:24px;
        `;

        bar.addEventListener('mouseenter', () => bar.style.opacity = '1');
        bar.addEventListener('mouseleave', () => bar.style.opacity = '0.7');
        // 双击隐藏
        bar.addEventListener('dblclick', () => {
            bar.style.display = 'none';
        });

        document.body.appendChild(bar);
        // 给body加padding防止遮挡
        document.body.style.paddingBottom = (parseInt(getComputedStyle(document.body).paddingBottom) + 28) + 'px';

    }, 2000);
})();
