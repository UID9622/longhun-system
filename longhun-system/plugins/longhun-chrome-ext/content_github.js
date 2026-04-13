/**
 * 龍魂 · GitHub增强器
 * DNA: #龍芯⚡️2026-04-13-GITHUB-v1.0
 * 在GitHub页面高亮自己的提交和核心目录
 */
(function() {
    'use strict';

    // 龍魂徽章（右下角）
    const badge = document.createElement('div');
    badge.innerHTML = `
        <div style="position:fixed;bottom:32px;right:20px;z-index:2147483646;
                    background:#0e0e1a;border:1px solid #d4af37;border-radius:10px;
                    padding:8px 14px;font-family:monospace;font-size:11px;
                    color:#d4af37;box-shadow:0 4px 20px rgba(0,0,0,0.5);
                    cursor:pointer;transition:all .3s;opacity:0.8"
             id="longhun-gh-badge"
             onmouseenter="this.style.opacity='1'"
             onmouseleave="this.style.opacity='0.8'"
             onclick="this.querySelector('.d').style.display=
                      this.querySelector('.d').style.display==='none'?'block':'none'">
            ☰☰ 龍🇨🇳魂 ☷
            <div class="d" style="display:none;margin-top:8px;color:#888;font-size:10px;line-height:2;border-top:1px solid #1a1a2e;padding-top:6px">
                UID9622 · 诸葛鑫<br>
                DNA: #龍芯⚡️2026<br>
                <a href="https://github.com/UID9622/longhun-system" style="color:#4a6fa5;text-decoration:none">→ 主仓库</a>
            </div>
        </div>`;
    document.body.appendChild(badge);

    // 高亮自己的提交
    function highlightMine() {
        document.querySelectorAll('a[data-hovercard-type="user"], .commit-author, .user-mention, [data-testid="commit-author"]').forEach(el => {
            const text = el.textContent || '';
            if (text.includes('UID9622') || text.includes('zuimeidedeyihan')) {
                el.style.color = '#d4af37';
                el.style.fontWeight = 'bold';
                el.style.textShadow = '0 0 8px rgba(212,175,55,0.3)';
            }
        });
    }

    // 高亮核心目录
    function highlightDirs() {
        const coreNames = ['core', 'CNSH引擎', 'bin', 'fonts', 'plugins', 'web', 'logs'];
        document.querySelectorAll('[role="rowheader"] a, .js-navigation-open, .Link--primary').forEach(el => {
            const name = el.textContent.trim();
            if (coreNames.includes(name)) {
                el.style.color = '#d4af37';
                el.style.fontWeight = 'bold';
            }
        });
    }

    highlightMine();
    highlightDirs();

    // 监听页面变化（GitHub用SPA）
    const observer = new MutationObserver(() => {
        highlightMine();
        highlightDirs();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    console.log('🐉 龍魂GitHub增强器已加载');
})();
