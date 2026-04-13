/**
 * 龍魂 · Notion增强器
 * DNA: #龍芯⚡️2026-04-13-NOTION-v1.0
 * 右侧快捷面板 + 页面信息 + Alt+L快捷键
 */
(function() {
    'use strict';

    // 侧边toggle按钮
    const toggle = document.createElement('div');
    toggle.id = 'lh-toggle';
    toggle.textContent = '龍';
    toggle.style.cssText = `
        position:fixed; top:50%; right:0; z-index:2147483647;
        transform:translateY(-50%);
        background:#d4af37; color:#0a0a14;
        padding:12px 6px; border-radius:8px 0 0 8px;
        font-size:16px; font-weight:bold; cursor:pointer;
        writing-mode:vertical-lr; letter-spacing:4px;
        box-shadow:-2px 0 12px rgba(0,0,0,0.3);
        transition:all .3s; opacity:0.8;
    `;
    toggle.addEventListener('mouseenter', () => toggle.style.opacity = '1');
    toggle.addEventListener('mouseleave', () => toggle.style.opacity = '0.8');
    document.body.appendChild(toggle);

    // 面板
    const panel = document.createElement('div');
    panel.id = 'lh-panel';
    panel.style.cssText = `
        display:none; position:fixed; top:8%; right:0; z-index:2147483646;
        background:#0e0e1a; border:1px solid #d4af37; border-right:none;
        border-radius:12px 0 0 12px;
        padding:20px; width:260px; font-family:monospace; font-size:12px;
        color:#c8b896; box-shadow:-4px 0 24px rgba(0,0,0,0.5);
        max-height:80vh; overflow-y:auto;
    `;
    panel.innerHTML = `
        <div style="color:#d4af37;font-size:16px;margin-bottom:4px;letter-spacing:3px">☰☰ 龍🇨🇳魂 ☷</div>
        <div style="color:#555;font-size:10px;margin-bottom:16px">UID9622 · Notion增强</div>

        <div style="color:#888;font-size:10px;margin-bottom:8px;letter-spacing:1px">三工作区</div>
        <a href="https://www.notion.so" style="display:block;color:#4a6fa5;margin-bottom:6px;text-decoration:none;font-size:12px">💎 主工作区（操作台）</a>
        <a href="https://www.notion.so" style="display:block;color:#4a6fa5;margin-bottom:6px;text-decoration:none;font-size:12px">⭐ 北极星（记忆存储）</a>
        <a href="https://www.notion.so/31bb3d78066a803baf7ee00839288f4d" style="display:block;color:#4a6fa5;margin-bottom:16px;text-decoration:none;font-size:12px">🌐 官方展示（导航总台）</a>

        <div style="border-top:1px solid #1a1a2e;padding-top:12px">
            <div style="color:#888;font-size:10px;margin-bottom:8px;letter-spacing:1px">当前页面</div>
            <div id="lh-page-info" style="color:#666;line-height:2;font-size:11px">点击刷新...</div>
        </div>

        <div style="border-top:1px solid #1a1a2e;padding-top:10px;margin-top:12px">
            <a href="https://github.com/UID9622/longhun-system" target="_blank"
               style="color:#4a6fa5;text-decoration:none;font-size:11px">📦 GitHub主仓库</a>
        </div>

        <div style="margin-top:14px;color:#222;font-size:9px;line-height:1.8">
            DNA: #龍芯⚡️2026<br>
            理论指导: 曾仕强老师
        </div>
    `;
    document.body.appendChild(panel);

    // toggle点击
    toggle.addEventListener('click', () => {
        const isOpen = panel.style.display !== 'none';
        panel.style.display = isOpen ? 'none' : 'block';
        if (!isOpen) updateInfo();
    });

    function updateInfo() {
        const title = document.title.replace(/ \|.*$/, '').replace(/ [-–].*$/, '');
        const blocks = document.querySelectorAll('[data-block-id]').length;
        const el = document.getElementById('lh-page-info');
        if (el) {
            el.innerHTML = `
                📄 ${title}<br>
                🧱 ${blocks} 个Block<br>
                🕐 ${new Date().toLocaleTimeString('zh-CN')}
            `;
        }
    }

    // Alt+L 快捷键
    document.addEventListener('keydown', (e) => {
        if (e.altKey && (e.key === 'l' || e.key === 'L')) {
            toggle.click();
            e.preventDefault();
        }
    });

    console.log('🐉 龍魂Notion增强器已加载 · Alt+L打开面板');
})();
