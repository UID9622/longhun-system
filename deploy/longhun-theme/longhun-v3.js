# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/* ═══════════════════════════════════════════════════════
 * 龍魂系统 · frp面板动态注入 v3.0
 * DNA: UID9622-ONLY-ONCE🧬LK9X-772Z
 * 新增: 人格指纹匹配度实时显示 + 节点信任徽章
 * ═══════════════════════════════════════════════════════ */

(function() {
    'use strict';

    var DNA = 'UID9622';
    var VERIFY_API = '/persona-api';
    var START_TIME = Date.now();

    var personaStatus = {
        master_score: 100,
        nodes: {},
        verified_count: 0,
        total_nodes: 0
    };

    // ── 创建底部栏（含人格验证） ──
    function createFooterBar() {
        var bar = document.createElement('div');
        bar.id = 'longhun-footer-bar';
        bar.innerHTML =
            '<div class="lh-bar-left">' +
                '<span class="lh-pulse-dot"></span>' +
                '<span class="lh-status-text">龍魂节点守护中</span>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-clock" id="lh-clock">--:--:--</span>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-uptime" id="lh-uptime">运行: 0s</span>' +
            '</div>' +
            '<div class="lh-bar-center">' +
                '<span class="lh-dragon-icon">🐉</span>' +
                '<span class="lh-brand">龍魂系统 v1.7</span>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-dna">龍芯北辰 ' + DNA + '</span>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-slogan">主权归人民</span>' +
            '</div>' +
            '<div class="lh-bar-right">' +
                '<div class="lh-persona-verify" id="lh-persona-verify">' +
                    '<span class="lh-verify-icon">🔐</span>' +
                    '<span class="lh-verify-label">人格:</span>' +
                    '<span class="lh-verify-score" id="lh-master-score">100%</span>' +
                    '<span class="lh-divider">|</span>' +
                    '<span class="lh-verify-nodes" id="lh-verify-nodes">🟢0/0</span>' +
                '</div>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-nodes-label">节点:</span>' +
                '<span class="lh-nodes-count" id="lh-nodes-count">--</span>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-traffic-label">流量:</span>' +
                '<span class="lh-traffic-value" id="lh-traffic">--</span>' +
            '</div>';

        // v3.0 样式
        var style = document.createElement('style');
        style.textContent = [
            '#longhun-footer-bar {',
            '  position: fixed; bottom: 0; left: 0; right: 0; height: 36px;',
            '  background: #12121a; border-top: 1px solid #2a2a3a;',
            '  display: flex; align-items: center; justify-content: space-between;',
            '  padding: 0 16px; z-index: 99999;',
            '  font-size: 11px; color: #8a8a9a; font-family: -apple-system, "PingFang SC", monospace;',
            '  letter-spacing: 0.5px;',
            '}',
            '.lh-pulse-dot { width: 6px; height: 6px; border-radius: 50%; background: #00c853;',
            '  display: inline-block; margin-right: 6px;',
            '  animation: lh-pulse 2s ease-in-out infinite; }',
            '@keyframes lh-pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(0,200,83,0.6); }',
            '  50% { box-shadow: 0 0 0 6px rgba(0,200,83,0); } }',
            '.lh-divider { color: #2a2a3a; margin: 0 8px; }',
            '.lh-brand { color: #c41e3a; font-weight: 700; }',
            '.lh-dragon-icon { font-size: 14px; }',
            '.lh-dna { color: #d4af37; }',
            '.lh-slogan { color: #5a5a6a; font-style: italic; }',
            '.lh-clock { color: #d4af37; font-weight: 600; }',
            '.lh-uptime, .lh-nodes-count, .lh-traffic-value { color: #e8e8f0; }',
            '.lh-bar-left, .lh-bar-center, .lh-bar-right { display: flex; align-items: center; white-space: nowrap; }',

            /* 人格验证区块 */
            '.lh-persona-verify {',
            '  display: inline-flex; align-items: center; gap: 4px;',
            '  padding: 2px 10px; border-radius: 10px;',
            '  background: rgba(0,200,83,0.1); border: 1px solid rgba(0,200,83,0.2);',
            '  transition: all 0.3s;',
            '}',
            '.lh-persona-verify.warning { background: rgba(255,145,0,0.1) !important;',
            '  border-color: rgba(255,145,0,0.3) !important;',
            '  animation: lh-vw 2s ease-in-out infinite; }',
            '.lh-persona-verify.danger { background: rgba(255,23,68,0.1) !important;',
            '  border-color: rgba(255,23,68,0.3) !important;',
            '  animation: lh-vd 1s ease-in-out infinite; }',
            '@keyframes lh-vw { 0%,100% { box-shadow: 0 0 4px rgba(255,145,0,0.2); }',
            '  50% { box-shadow: 0 0 12px rgba(255,145,0,0.4); } }',
            '@keyframes lh-vd { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }',
            '.lh-verify-score { font-family: monospace; font-weight: 700; color: #00c853; min-width: 36px; text-align: center; }',
            '.lh-verify-score.low { color: #ff9100 !important; }',
            '.lh-verify-score.unverified { color: #ff1744 !important; animation: lh-sb 1s ease-in-out infinite; }',
            '@keyframes lh-sb { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }',
            '.lh-verify-nodes { font-size: 10px; color: #8a8a9a; }',

            /* 节点人格徽章 */
            '.lh-persona-badge {',
            '  display: inline-block; padding: 1px 6px; border-radius: 8px;',
            '  font-size: 9px; font-weight: 600; margin-left: 6px;',
            '}',
            '.lh-persona-badge.master { background: linear-gradient(135deg,#c41e3a,#ff2d55); color:#fff;',
            '  box-shadow: 0 0 8px rgba(196,30,58,0.4); }',
            '.lh-persona-badge.high { background: rgba(0,200,83,0.2); color:#00c853;',
            '  border:1px solid rgba(0,200,83,0.3); }',
            '.lh-persona-badge.medium { background: rgba(255,145,0,0.2); color:#ff9100;',
            '  border:1px solid rgba(255,145,0,0.3); }',
            '.lh-persona-badge.low { background: rgba(255,23,68,0.2); color:#ff1744;',
            '  border:1px solid rgba(255,23,68,0.3); }',
            '.lh-persona-badge.unverified { background: rgba(90,90,106,0.2); color:#5a5a6a;',
            '  border:1px solid rgba(90,90,106,0.3); }',

            '@media (max-width: 768px) {',
            '  .lh-bar-center { display: none; }',
            '  #longhun-footer-bar { font-size: 10px; padding: 0 10px; }',
            '}'
        ].join('\n');
        document.head.appendChild(style);

        var existing = document.getElementById('longhun-footer-bar');
        if (existing) existing.remove();
        document.body.appendChild(bar);
        document.body.style.paddingBottom = '36px';
    }

    // ── 获取人格验证状态 ──
    function updatePersonaStatus() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', VERIFY_API + '/status/all', true);
        xhr.timeout = 5000;
        xhr.onload = function() {
            if (xhr.status !== 200) return;
            try {
                var data = JSON.parse(xhr.responseText);
            } catch(e) { return; }

            personaStatus.master_score = (data.master && data.master.trust_score) || 100;
            personaStatus.nodes = data.nodes || {};
            personaStatus.verified_count = data.verified_count || 0;
            personaStatus.total_nodes = data.total || 0;

            var scoreEl = document.getElementById('lh-master-score');
            var nodesEl = document.getElementById('lh-verify-nodes');
            var verifyBox = document.getElementById('lh-persona-verify');

            if (scoreEl) {
                scoreEl.textContent = personaStatus.master_score + '%';
                scoreEl.className = 'lh-verify-score';
                if (personaStatus.master_score < 60) scoreEl.classList.add('low');
                if (personaStatus.master_score < 30) scoreEl.classList.add('unverified');
            }

            if (nodesEl) {
                var v = personaStatus.verified_count;
                var t = personaStatus.total_nodes;
                var icon = (v === t && t > 0) ? '🟢' : (v > 0) ? '🟡' : '🔴';
                nodesEl.textContent = icon + v + '/' + t;
            }

            if (verifyBox) {
                verifyBox.className = 'lh-persona-verify';
                if (personaStatus.verified_count < personaStatus.total_nodes) {
                    verifyBox.classList.add('warning');
                }
                if (personaStatus.verified_count === 0 && personaStatus.total_nodes > 0) {
                    verifyBox.classList.add('danger');
                }
            }

            addPersonaBadges();
        };
        xhr.onerror = function() {};
        xhr.send();
    }

    // ── 节点列表人格标记 ──
    function addPersonaBadges() {
        var rows = document.querySelectorAll('tr');
        rows.forEach(function(row) {
            var nameEl = row.querySelector('td:first-child, [class*="name"]');
            if (!nameEl || row.querySelector('.lh-persona-badge')) return;

            var name = nameEl.textContent.toLowerCase();
            var nodeId = null;

            if (name.includes('longhun-mac') || name.includes('mac-m4')) nodeId = 'UID9622-mac';
            else if (name.includes('longhun-kunpeng') || name.includes('kunpeng')) nodeId = 'UID9622-kunpeng';
            else if (name.includes('longhun')) nodeId = 'UID9622-node';

            if (!nodeId) return;

            // 尝试匹配已知节点
            var status = null;
            for (var nid in personaStatus.nodes) {
                if (nodeId.includes(nid) || nid.includes(nodeId.replace('UID9622-',''))) {
                    status = personaStatus.nodes[nid];
                    break;
                }
            }
            if (!status) status = personaStatus.nodes[nodeId];
            if (!status) return;

            var badge = document.createElement('span');
            badge.className = 'lh-persona-badge ' + status.trust_level;

            var labels = {
                master: '👑 主控', high: '✅ 可信', medium: '⚠️ 一般',
                low: '❓ 低信', unverified: '❌ 未验'
            };
            badge.textContent = labels[status.trust_level] || status.trust_level;
            badge.title = '匹配度: ' + status.match_score + '%';
            nameEl.appendChild(badge);
        });
    }

    // ── 时钟 ──
    function updateClock() {
        var now = new Date();
        var t = [now.getHours(), now.getMinutes(), now.getSeconds()]
            .map(function(n) { return (n < 10 ? '0' : '') + n; }).join(':');
        var clockEl = document.getElementById('lh-clock');
        if (clockEl) clockEl.textContent = t;

        var uptime = Math.floor((Date.now() - START_TIME) / 1000);
        var h = Math.floor(uptime / 3600);
        var m = Math.floor((uptime % 3600) / 60);
        var s = uptime % 60;
        var uptimeEl = document.getElementById('lh-uptime');
        if (uptimeEl) uptimeEl.textContent = '运行: ' + h + 'h' + m + 'm' + s + 's';
    }

    // ── 节点计数 ──
    function updateNodeCount() {
        var greenTags = document.querySelectorAll('.ant-tag-green, .status-online, [class*="online"]');
        var count = greenTags.length;
        var countEl = document.getElementById('lh-nodes-count');
        if (countEl) {
            countEl.textContent = count;
            countEl.style.color = count === 0 ? '#ff1744' : count < 2 ? '#ff9100' : '#e8e8f0';
        }
    }

    // ── 流量估算 ──
    function estimateTraffic() {
        var trafficEl = document.getElementById('lh-traffic');
        if (!trafficEl) return;
        var tables = document.querySelectorAll('table');
        var totalIn = 0, totalOut = 0;
        tables.forEach(function(table) {
            var cells = table.querySelectorAll('td');
            cells.forEach(function(cell) {
                var text = cell.textContent || '';
                var m;
                if ((m = text.match(/([\d.]+)\s*(MB|GB|KB)/i))) {
                    var val = parseFloat(m[1]);
                    if (m[2].toUpperCase() === 'GB') val *= 1024;
                    if (m[2].toUpperCase() === 'KB') val /= 1024;
                    if (cell.previousElementSibling && /in|入/i.test(cell.previousElementSibling.textContent || '')) {
                        totalIn += val;
                    } else {
                        totalOut += val;
                    }
                }
            });
        });
        if (totalIn + totalOut > 0) {
            var t = totalIn + totalOut;
            trafficEl.textContent = t > 1024 ? (t/1024).toFixed(1) + 'GB' : t.toFixed(1) + 'MB';
        }
    }

    // ── 初始化 ──
    function init() {
        if (document.getElementById('longhun-footer-bar')) return;

        createFooterBar();
        setInterval(updateClock, 1000);
        setInterval(updateNodeCount, 5000);
        setInterval(updatePersonaStatus, 10000);
        setInterval(estimateTraffic, 15000);

        updateClock();
        updateNodeCount();
        updatePersonaStatus();
        setTimeout(estimateTraffic, 3000);

        console.log('🐉 龍魂人格验证面板 v3.0 | ' + DNA);
    }

    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
        setTimeout(init, 3000);
    }

    // DOM 变化时重试
    var observer = new MutationObserver(function() {
        if (!document.getElementById('longhun-footer-bar')) init();
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
