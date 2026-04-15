// ==UserScript==
// @name         龍魂 · Notion工作区增强
// @namespace    https://github.com/UID9622
// @version      1.0
// @description  Notion页面增加快捷导航、DNA标记、三工作区切换
// @author       诸葛鑫（UID9622）
// @match        https://www.notion.so/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    // ── 龍魂快捷面板 ──
    const panel = document.createElement('div');
    panel.id = 'longhun-notion-panel';
    panel.innerHTML = `
        <div id="lh-toggle" style="position:fixed;top:50%;right:0;z-index:99999;
             background:#d4af37;color:#0a0a14;padding:8px 4px;border-radius:8px 0 0 8px;
             font-size:12px;cursor:pointer;writing-mode:vertical-lr;letter-spacing:2px;
             font-weight:bold;box-shadow:-2px 0 10px rgba(0,0,0,0.3)">龍魂</div>
        <div id="lh-panel" style="display:none;position:fixed;top:10%;right:0;z-index:99998;
             background:#0e0e1a;border:1px solid #d4af37;border-radius:12px 0 0 12px;
             padding:20px;width:280px;font-family:monospace;font-size:12px;color:#c8b896;
             box-shadow:-4px 0 20px rgba(0,0,0,0.5);max-height:80vh;overflow-y:auto">
            <div style="color:#d4af37;font-size:14px;margin-bottom:16px;letter-spacing:2px">
                ☰☰ 龍🇨🇳魂 ☷
            </div>

            <div style="color:#666;margin-bottom:12px">三工作区导航</div>

            <a href="https://www.notion.so" style="display:block;color:#4a6fa5;margin-bottom:8px;text-decoration:none">
                💎 主工作区（操作台）
            </a>
            <a href="https://www.notion.so" style="display:block;color:#4a6fa5;margin-bottom:8px;text-decoration:none">
                ⭐ 北极星（记忆存储）
            </a>
            <a href="https://www.notion.so/31bb3d78066a803baf7ee00839288f4d" style="display:block;color:#4a6fa5;margin-bottom:16px;text-decoration:none">
                🌐 官方展示（导航总台）
            </a>

            <div style="border-top:1px solid #1a1a2e;padding-top:12px;margin-top:8px">
                <div style="color:#666;margin-bottom:8px">页面信息</div>
                <div id="lh-page-info" style="color:#888;line-height:1.8;font-size:11px">加载中...</div>
            </div>

            <div style="border-top:1px solid #1a1a2e;padding-top:12px;margin-top:12px;color:#333;font-size:10px">
                DNA: #龍芯⚡️2026<br>
                UID9622 · 诸葛鑫
            </div>
        </div>
    `;
    document.body.appendChild(panel);

    // 切换面板
    document.getElementById('lh-toggle').addEventListener('click', () => {
        const p = document.getElementById('lh-panel');
        const isOpen = p.style.display !== 'none';
        p.style.display = isOpen ? 'none' : 'block';
        // 更新页面信息
        if (!isOpen) updatePageInfo();
    });

    function updatePageInfo() {
        const title = document.title.replace(' | Notion', '');
        const blocks = document.querySelectorAll('[data-block-id]').length;
        const url = location.href;
        const info = document.getElementById('lh-page-info');
        info.innerHTML = `
            📄 ${title}<br>
            🧱 ${blocks} 个Block<br>
            🔗 ${url.length > 60 ? url.substring(0, 60) + '...' : url}
        `;
    }

    // 快捷键 Alt+L 打开面板
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key === 'l') {
            document.getElementById('lh-toggle').click();
        }
    });

    console.log('🐉 龍魂Notion增强器已加载 · Alt+L打开面板');
})();
