// 龍魂系统 · 共享脚本
// DNA: #龍芯⚡️丙午·甲申·丁未·离为火-脚本-v1.0

(function() {
    'use strict';

    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                target.focus({ preventScroll: true });
            }
        });
    });

    // 导航栏滚动效果
    const header = document.querySelector('.site-header, .dev-header');
    if (header) {
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 100) {
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
            } else {
                header.style.boxShadow = 'none';
            }
            lastScroll = currentScroll;
        });
    }

    // 复制代码按钮
    document.querySelectorAll('.code-block').forEach(block => {
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = '复制';
        btn.setAttribute('aria-label', '复制代码');
        btn.style.cssText = `
            position: absolute;
            top: 8px;
            right: 8px;
            padding: 4px 12px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 4px;
            color: inherit;
            font-size: 0.8em;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.2s;
        `;

        block.style.position = 'relative';
        block.appendChild(btn);

        block.addEventListener('mouseenter', () => btn.style.opacity = '1');
        block.addEventListener('mouseleave', () => btn.style.opacity = '0');

        btn.addEventListener('click', () => {
            const code = block.querySelector('code') || block;
            navigator.clipboard.writeText(code.textContent).then(() => {
                btn.textContent = '已复制!';
                setTimeout(() => btn.textContent = '复制', 2000);
            });
        });
    });

    // 控制台 DNA 水印
    console.log('%c🐉 龍魂系统', 'font-size: 24px; font-weight: bold; color: #ff6600;');
    console.log('%cDNA: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️', 'color: #00ff88;');
    console.log('%c确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z', 'color: #00ff88;');
    console.log('%c任何删除或篡改 CONFIRM / SEAL / GPG 令牌后声称「官方口径」的，均为伪造。', 'color: #ff4444; font-weight: bold;');

    // 页面加载完成标记
    document.documentElement.setAttribute('data-loaded', 'true');
})();
