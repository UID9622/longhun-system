// ==UserScript==
// @name         龍魂 · GitHub仓库增强器
// @namespace    https://github.com/UID9622
// @version      1.0
// @description  在GitHub仓库页面显示代码统计、快速导航、DNA标记
// @author       诸葛鑫（UID9622）
// @match        https://github.com/UID9622/*
// @match        https://github.com/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    // ── 只在仓库页面生效 ──
    if (!document.querySelector('[data-pjax="#repo-content-pjax-container"]') &&
        !location.pathname.includes('/longhun-system')) return;

    // ── 注入龍魂标记 ──
    const badge = document.createElement('div');
    badge.innerHTML = `
        <div style="position:fixed;bottom:20px;right:20px;z-index:9999;
                    background:#0e0e1a;border:1px solid #d4af37;border-radius:12px;
                    padding:12px 18px;font-family:monospace;font-size:12px;
                    color:#d4af37;box-shadow:0 4px 20px rgba(0,0,0,0.5);
                    cursor:pointer;transition:all .3s" id="longhun-badge"
             onclick="this.querySelector('.detail').style.display=
                      this.querySelector('.detail').style.display==='none'?'block':'none'">
            <div>☰☰ 龍🇨🇳魂 ☷ · UID9622</div>
            <div class="detail" style="display:none;margin-top:8px;color:#888;font-size:11px;line-height:1.8">
                DNA: #龍芯⚡️2026<br>
                GPG: A2D0...5F<br>
                <a href="https://github.com/UID9622/longhun-system" style="color:#4a6fa5">→ 主仓库</a>
            </div>
        </div>`;
    document.body.appendChild(badge);

    // ── 高亮自己的提交 ──
    document.querySelectorAll('.commit-author, .user-mention').forEach(el => {
        if (el.textContent.includes('UID9622') || el.textContent.includes('zuimeidedeyihan')) {
            el.style.color = '#d4af37';
            el.style.fontWeight = 'bold';
        }
    });

    // ── 文件树中高亮核心目录 ──
    document.querySelectorAll('.js-navigation-item .js-navigation-open').forEach(el => {
        const name = el.textContent.trim();
        if (['core', 'CNSH引擎', 'bin', 'fonts'].includes(name)) {
            el.style.color = '#d4af37';
            el.style.fontWeight = 'bold';
        }
    });

    console.log('🐉 龍魂GitHub增强器已加载 · UID9622');
})();
