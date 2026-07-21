/* ═══════════════════════════════════════════════════════
 * 龍魂系统 · frp面板动态注入 v5.0
 * DNA: UID9622-ONLY-ONCE🧬LK9X-772Z
 * 新增: 训练进度可视化 + AI模型版本显示 + 训练完成通知
 * 继承: v4隔离牢房 + 申诉队列 + AI初审
 * ═══════════════════════════════════════════════════════ */

(function() {
    'use strict';

    var DNA = 'UID9622';
    var VERIFY_API = '/persona-api';
    var START_TIME = Date.now();
    var QUARANTINE_VISIBLE = false;
    var TRAINING_POLL_INTERVAL = null;
    var CURRENT_MODEL_VERSION = 0;

    var personaStatus = {
        master_score: 100, nodes: {}, verified_count: 0,
        total_nodes: 0, quarantine_count: 0, ban_count: 0, pending_appeals: 0
    };

    // ── 底部栏（含模型版本预留位） ──
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
                    '<span id="lh-appeal-status" style="display:none;"></span>' +
                    '<span id="lh-quarantine-count" style="display:none;"></span>' +
                '</div>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-nodes-label">节点:</span>' +
                '<span class="lh-nodes-count" id="lh-nodes-count">--</span>' +
                '<span class="lh-divider">|</span>' +
                '<span class="lh-traffic-label">流量:</span>' +
                '<span class="lh-traffic-value" id="lh-traffic">--</span>' +
            '</div>';

        // 注入样式（v4基础 + v5新增）
        var style = document.createElement('style');
        style.textContent = buildStyles();
        document.head.appendChild(style);

        var existing = document.getElementById('longhun-footer-bar');
        if (existing) existing.remove();
        document.body.appendChild(bar);
        document.body.style.paddingBottom = '36px';

        // v5: 添加模型版本元素
        addModelVersionEl();
    }

    function buildStyles() {
        return [
            '#longhun-footer-bar { position:fixed;bottom:0;left:0;right:0;height:36px;',
            '  background:#12121a;border-top:1px solid #2a2a3a;display:flex;align-items:center;',
            '  justify-content:space-between;padding:0 16px;z-index:99999;',
            '  font-size:11px;color:#8a8a9a;font-family:-apple-system,"PingFang SC",monospace;',
            '  letter-spacing:0.5px; }',
            '.lh-pulse-dot { width:6px;height:6px;border-radius:50%;background:#00c853;',
            '  display:inline-block;margin-right:6px;animation:lh-pulse 2s ease-in-out infinite; }',
            '@keyframes lh-pulse { 0%,100%{box-shadow:0 0 0 0 rgba(0,200,83,0.6)}',
            '  50%{box-shadow:0 0 0 6px rgba(0,200,83,0)} }',
            '.lh-divider { color:#2a2a3a;margin:0 8px; }',
            '.lh-brand { color:#c41e3a;font-weight:700; }',
            '.lh-dragon-icon { font-size:14px; }',
            '.lh-dna { color:#d4af37; }',
            '.lh-slogan { color:#5a5a6a;font-style:italic; }',
            '.lh-clock { color:#d4af37;font-weight:600; }',
            '.lh-uptime,.lh-nodes-count,.lh-traffic-value { color:#e8e8f0; }',
            '.lh-bar-left,.lh-bar-center,.lh-bar-right { display:flex;align-items:center;white-space:nowrap; }',

            // 模型版本显示
            '#lh-model-version { margin-left:10px;padding:2px 10px;border-radius:10px;',
            '  font-size:10px;font-family:"Courier New",monospace;font-weight:600;',
            '  letter-spacing:0.5px;transition:all 0.3s;cursor:help;display:inline-block; }',
            '#lh-model-version.good { background:rgba(0,200,83,0.15);color:#00c853;',
            '  border:1px solid rgba(0,200,83,0.3); }',
            '#lh-model-version.warning { background:rgba(212,175,55,0.15);color:#d4af37;',
            '  border:1px solid rgba(212,175,55,0.3); }',
            '#lh-model-version.caution { background:rgba(255,145,0,0.15);color:#ff9100;',
            '  border:1px solid rgba(255,145,0,0.3); }',
            '#lh-model-version.training { opacity:0.3; }',

            // 个人验证区块
            '.lh-persona-verify { display:inline-flex;align-items:center;gap:4px;',
            '  padding:2px 10px;border-radius:10px;background:rgba(0,200,83,0.1);',
            '  border:1px solid rgba(0,200,83,0.2);transition:all 0.3s; }',
            '.lh-persona-verify.warning { background:rgba(255,145,0,0.1)!important;',
            '  border-color:rgba(255,145,0,0.3)!important;',
            '  animation:lh-vw 2s ease-in-out infinite; }',
            '.lh-persona-verify.danger { background:rgba(255,23,68,0.1)!important;',
            '  border-color:rgba(255,23,68,0.3)!important;',
            '  animation:lh-vd 1s ease-in-out infinite; }',
            '@keyframes lh-vw { 0%,100%{box-shadow:0 0 4px rgba(255,145,0,0.2)}',
            '  50%{box-shadow:0 0 12px rgba(255,145,0,0.4)} }',
            '@keyframes lh-vd { 0%,100%{opacity:1}50%{opacity:0.5} }',
            '.lh-verify-score { font-family:monospace;font-weight:700;color:#00c853;',
            '  min-width:36px;text-align:center; }',
            '.lh-verify-score.low { color:#ff9100!important; }',

            // 隔离/申诉计数
            '#lh-quarantine-count,#lh-appeal-status { margin-left:4px;padding:1px 6px;',
            '  border-radius:8px;font-size:10px;font-weight:600;cursor:pointer; }',
            '#lh-quarantine-count.active { background:rgba(255,23,68,0.15);color:#ff1744;',
            '  border:1px solid rgba(255,23,68,0.3);animation:lh-danger-pulse 2s ease-in-out infinite; }',
            '#lh-quarantine-count.clean { background:rgba(0,200,83,0.15);color:#00c853;',
            '  border:1px solid rgba(0,200,83,0.3); }',
            '#lh-appeal-status.pending { background:rgba(255,145,0,0.15);color:#ff9100;',
            '  border:1px solid rgba(255,145,0,0.3);animation:lh-pulse 2s ease-in-out infinite; }',
            '@keyframes lh-danger-pulse { 0%,100%{box-shadow:0 0 4px rgba(255,23,68,0.3)}',
            '  50%{box-shadow:0 0 12px rgba(255,23,68,0.6)} }',

            // 隔离面板
            '#lh-quarantine-panel { position:fixed;top:60px;right:20px;',
            '  background:rgba(10,10,15,0.97);border:1px solid #2a2a3a;border-radius:12px;',
            '  padding:16px;min-width:300px;max-width:380px;max-height:450px;overflow-y:auto;',
            '  z-index:100001;font-size:12px;display:none;box-shadow:0 8px 32px rgba(0,0,0,0.6); }',
            '#lh-quarantine-panel::-webkit-scrollbar { width:4px; }',
            '#lh-quarantine-panel::-webkit-scrollbar-thumb { background:#2a2a3a;border-radius:2px; }',

            // v5: 训练进度面板
            '#lh-training-indicator { position:fixed;bottom:50px;left:50%;',
            '  transform:translateX(-50%);background:linear-gradient(135deg,rgba(10,10,15,0.98),rgba(26,10,10,0.98));',
            '  border:1px solid #c41e3a;border-radius:16px;padding:20px 32px;z-index:100003;',
            '  min-width:400px;box-shadow:0 8px 32px rgba(196,30,58,0.3);',
            '  animation:lh-train-slide-up 0.5s ease; }',
            '#lh-training-indicator.error { border-color:#ff1744; }',
            '@keyframes lh-train-slide-up {',
            '  from{opacity:0;transform:translateX(-50%) translateY(20px)}',
            '  to{opacity:1;transform:translateX(-50%) translateY(0)} }',
            '@keyframes lh-spin { from{transform:rotate(0deg)}to{transform:rotate(360deg)} }',

            // v5: 训练完成通知
            '#lh-training-notification { position:fixed;top:80px;right:20px;',
            '  background:linear-gradient(135deg,rgba(0,200,83,0.15),rgba(0,200,83,0.05));',
            '  border:1px solid rgba(0,200,83,0.3);border-radius:12px;padding:16px 20px;',
            '  z-index:100004;min-width:280px;animation:lh-notif-slide-in 0.5s ease;',
            '  box-shadow:0 4px 16px rgba(0,200,83,0.2); }',
            '@keyframes lh-notif-slide-in {',
            '  from{opacity:0;transform:translateX(100px)}',
            '  to{opacity:1;transform:translateX(0)} }',
            '@keyframes lh-notif-fade-out {',
            '  from{opacity:1;transform:translateX(0)}',
            '  to{opacity:0;transform:translateX(100px)} }',

            // 响应式
            '@media(max-width:768px){',
            '  .lh-bar-center{display:none}',
            '  #longhun-footer-bar{font-size:10px;padding:0 10px;min-width:auto}',
            '  #lh-training-indicator{min-width:300px;left:50%;right:auto;max-width:95vw}',
            '  #lh-quarantine-panel{right:5px;min-width:260px;max-width:calc(100vw-10px)}',
            '}',
        ].join('\n');
    }

    // ── v5: 添加模型版本元素到底部栏 ──
    function addModelVersionEl() {
        var centerDiv = document.querySelector('.lh-bar-center');
        if (!centerDiv) return;
        var el = document.createElement('span');
        el.id = 'lh-model-version';
        el.className = 'good';
        el.textContent = 'AIv?';
        el.title = '龍魂AI初审模型版本 | 点击刷新';
        el.onclick = function() {
            el.style.transform = 'scale(0.95)';
            setTimeout(function() { el.style.transform = 'scale(1)'; }, 150);
            fetchModelVersion();
            updatePersonaStatus();
        };
        centerDiv.appendChild(el);
    }

    // ── 创建隔离面板 ──
    function createQuarantinePanel() {
        var panel = document.getElementById('lh-quarantine-panel');
        if (panel) return;
        panel = document.createElement('div');
        panel.id = 'lh-quarantine-panel';
        panel.innerHTML =
            '<div class="lh-qp-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">' +
                '<span style="color:#c41e3a;font-weight:700;font-size:14px">🔒 隔离观察区</span>' +
                '<span style="color:#5a5a6a;cursor:pointer;font-size:16px;line-height:1" id="lh-qp-close">✕</span>' +
            '</div>' +
            '<div id="lh-qp-content">加载中...</div>';
        document.body.appendChild(panel);
        document.getElementById('lh-qp-close').onclick = function() {
            panel.style.display = 'none'; QUARANTINE_VISIBLE = false;
        };
    }

    // ── 获取人格验证状态 ──
    function updatePersonaStatus() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', VERIFY_API + '/status/all', true); xhr.timeout = 5000;
        xhr.onload = function() {
            if (xhr.status !== 200) return;
            var data;
            try { data = JSON.parse(xhr.responseText); } catch(e) { return; }
            personaStatus.master_score = (data.master && data.master.trust_score) || 100;
            personaStatus.nodes = data.nodes || {};
            personaStatus.verified_count = data.verified_count || 0;
            personaStatus.total_nodes = data.total || 0;
            personaStatus.quarantine_count = data.quarantine_count || 0;
            personaStatus.ban_count = data.ban_count || 0;
            personaStatus.pending_appeals = (data.appeals && data.appeals.pending) || 0;
            var scoreEl = document.getElementById('lh-master-score');
            var nodesEl = document.getElementById('lh-verify-nodes');
            var verifyBox = document.getElementById('lh-persona-verify');
            if (scoreEl) {
                scoreEl.textContent = personaStatus.master_score + '%';
                scoreEl.className = 'lh-verify-score';
                if (personaStatus.master_score < 60) scoreEl.classList.add('low');
            }
            if (nodesEl) {
                var v = personaStatus.verified_count, t = personaStatus.total_nodes;
                nodesEl.textContent = (v === t && t > 0 ? '🟢' : v > 0 ? '🟡' : '🔴') + v + '/' + t;
            }
            if (verifyBox) {
                verifyBox.className = 'lh-persona-verify';
                if (personaStatus.verified_count < personaStatus.total_nodes) verifyBox.classList.add('warning');
                if (personaStatus.verified_count === 0 && personaStatus.total_nodes > 0) verifyBox.classList.add('danger');
            }
            updateQuarantineCountBadge(); updateAppealCountBadge();
            addPersonaBadges(); updateQuarantinePanel();
        };
        xhr.onerror = function() {};
        xhr.send();
    }

    // ── 隔离/申诉计数（v4逻辑） ──
    function updateQuarantineCountBadge() {
        var el = document.getElementById('lh-quarantine-count');
        if (!el) return;
        var total = personaStatus.quarantine_count + personaStatus.ban_count;
        if (total > 0) {
            el.style.display = 'inline-block'; el.className = 'active';
            el.textContent = '🔒' + personaStatus.quarantine_count + '/' + (total > 0 ? '🚫' + personaStatus.ban_count : '');
            el.title = '隔离:' + personaStatus.quarantine_count + ' | 封禁:' + personaStatus.ban_count + ' | 点击查看';
            el.onclick = toggleQuarantinePanel;
        } else {
            el.style.display = 'inline-block'; el.className = 'clean'; el.textContent = '✅ 无隔离';
            el.title = '所有节点验证通过'; el.onclick = toggleQuarantinePanel;
        }
    }

    function updateAppealCountBadge() {
        var el = document.getElementById('lh-appeal-status');
        if (!el) return;
        if (personaStatus.pending_appeals > 0) {
            el.style.display = 'inline-block'; el.className = 'pending';
            el.textContent = '📋' + personaStatus.pending_appeals;
            el.title = personaStatus.pending_appeals + ' 个申诉待审核';
        } else { el.style.display = 'none'; }
    }

    function toggleQuarantinePanel() {
        var panel = document.getElementById('lh-quarantine-panel');
        if (!panel) { createQuarantinePanel(); panel = document.getElementById('lh-quarantine-panel'); }
        QUARANTINE_VISIBLE = !QUARANTINE_VISIBLE;
        panel.style.display = QUARANTINE_VISIBLE ? 'block' : 'none';
        if (QUARANTINE_VISIBLE) updateQuarantinePanel();
    }

    function updateQuarantinePanel() {
        var content = document.getElementById('lh-qp-content');
        if (!content) return;
        var xhrQ = new XMLHttpRequest();
        xhrQ.open('GET', VERIFY_API + '/quarantine/list', true); xhrQ.timeout = 3000;
        xhrQ.onload = function() {
            if (xhrQ.status !== 200) return;
            var qData;
            try { qData = JSON.parse(xhrQ.responseText); } catch(e) { return; }
            var xhrB = new XMLHttpRequest();
            xhrB.open('GET', VERIFY_API + '/ban/list', true); xhrB.timeout = 3000;
            xhrB.onload = function() {
                if (xhrB.status !== 200) return;
                var bData;
                try { bData = JSON.parse(xhrB.responseText); } catch(e) { return; }
                renderQuarantineContent(content, qData, bData);
            };
            xhrB.onerror = function() { renderQuarantineContent(content, qData, null); };
            xhrB.send();
        };
        xhrQ.onerror = function() { content.innerHTML = '<div style="text-align:center;padding:20px;color:#00c853;">⚠️ 查询失败</div>'; };
        xhrQ.send();
    }

    function renderQuarantineContent(content, qData, bData) {
        var html = '';
        if (qData && qData.nodes && qData.nodes.length > 0) {
            html += '<div style="color:#8a8a9a;font-size:11px;margin:12px 0 6px;font-weight:600">🔒 隔离中 (' + qData.total + ')</div>';
            qData.nodes.forEach(function(n) {
                var r = Math.max(0, n.remaining_hours);
                html += '<div style="padding:10px;border-radius:8px;margin-bottom:8px;font-size:11px;background:rgba(255,145,0,0.08);border:1px solid rgba(255,145,0,0.2)">' +
                    '<div style="font-weight:600;color:#e8e8f0">' + escHtml(n.node_id) + '</div>' +
                    '<div style="color:#5a5a6a;margin-top:4px;font-size:10px">匹配度: <span style="color:#ff9100;font-weight:600">' + n.match_score.toFixed(1) + '%</span> | 剩余: <span style="color:#d4af37">' + r + 'h</span></div>' +
                    '<div style="color:#8a8a9a;font-size:10px;margin-top:4px">' + escHtml(n.reason) + '</div>' +
                    (n.appeal_status === 'pending' ? '<div style="color:#ff9100;font-size:10px;margin-top:4px">📋 申诉审核中</div>' : '') +
                '</div>';
            });
        }
        if (bData && bData.nodes && bData.nodes.length > 0) {
            html += '<div style="color:#8a8a9a;font-size:11px;margin:12px 0 6px;font-weight:600">🚫 永久封禁 (' + bData.total + ')</div>';
            bData.nodes.forEach(function(n) {
                html += '<div style="padding:10px;border-radius:8px;margin-bottom:8px;font-size:11px;background:rgba(255,23,68,0.08);border:1px solid rgba(255,23,68,0.2)">' +
                    '<div style="font-weight:600;color:#ff1744">🚫 ' + escHtml(n.node_id) + '</div>' +
                    '<div style="color:#5a5a6a;margin-top:4px;font-size:10px">匹配度: <span style="color:#ff9100;font-weight:600">' + n.match_score.toFixed(1) + '%</span></div>' +
                '</div>';
            });
        }
        if ((!qData || !qData.nodes || qData.nodes.length === 0) && (!bData || !bData.nodes || bData.nodes.length === 0)) {
            html += '<div style="text-align:center;padding:20px;color:#00c853">✅ 所有节点验证通过<br><span style="font-size:10px;color:#5a5a6a">隔离区为空 · AI初审守护中</span></div>';
        }
        content.innerHTML = html;
    }

    function escHtml(str) {
        var div = document.createElement('div'); div.textContent = str; return div.innerHTML;
    }

    function addPersonaBadges() {
        // 同 v4: 在节点名后加人格标记
        var rows = document.querySelectorAll('tr');
        rows.forEach(function(row) {
            var nameEl = row.querySelector('td:first-child, [class*="name"]');
            if (!nameEl || row.querySelector('.lh-persona-badge')) return;
            var name = nameEl.textContent.toLowerCase(); var nodeId = null;
            if (name.includes('longhun-mac') || name.includes('mac-m4')) nodeId = 'UID9622-mac';
            else if (name.includes('longhun-kunpeng') || name.includes('kunpeng')) nodeId = 'UID9622-kunpeng';
            else if (name.includes('longhun')) nodeId = 'UID9622-node';
            if (!nodeId) return;
            var status = null;
            for (var nid in personaStatus.nodes) {
                if (nodeId.includes(nid) || nid.includes(nodeId.replace('UID9622-',''))) { status = personaStatus.nodes[nid]; break; }
            }
            if (!status) status = personaStatus.nodes[nodeId];
            if (!status) return;
            var badge = document.createElement('span');
            badge.className = 'lh-persona-badge ' + status.trust_level;
            var labels = {master:'👑主控',high:'✅可信',medium:'⚠️一般',low:'❓低信',unverified:'❌未验',quarantine:'🔒隔离',banned:'🚫封禁'};
            badge.textContent = labels[status.trust_level] || status.trust_level;
            badge.title = '匹配度:' + status.match_score + '%';
            nameEl.appendChild(badge);
        });
    }

    // ═══════════════════════════════════════════════════════
    // v5 新增: 训练状态轮询 & 可视化
    // ═══════════════════════════════════════════════════════

    function startTrainingPoll() {
        if (TRAINING_POLL_INTERVAL) return;
        checkTrainingStatus();
        TRAINING_POLL_INTERVAL = setInterval(checkTrainingStatus, 2000);
    }

    function checkTrainingStatus() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', VERIFY_API + '/training/status', true); xhr.timeout = 3000;
        xhr.onload = function() {
            if (xhr.status !== 200) return;
            var status;
            try { status = JSON.parse(xhr.responseText); } catch(e) { return; }
            updateTrainingDisplay(status);
            if (status.state === 'done' && status.to_version !== CURRENT_MODEL_VERSION) {
                showTrainingCompleteNotification(status);
                CURRENT_MODEL_VERSION = status.to_version;
                fetchModelVersion();
            }
            if (status.state === 'error') {
                showTrainingError(status);
            }
        };
        xhr.onerror = function() {};
        xhr.send();
    }

    function updateTrainingDisplay(status) {
        var existing = document.getElementById('lh-training-indicator');
        if (existing) existing.remove();

        var modelEl = document.getElementById('lh-model-version');
        if (modelEl && status.state !== 'idle') {
            modelEl.classList.add('training');
        } else if (modelEl) {
            modelEl.classList.remove('training');
        }

        if (status.state === 'idle' || status.state === 'done') return;

        var indicator = document.createElement('div');
        indicator.id = 'lh-training-indicator';
        if (status.state === 'error') indicator.classList.add('error');

        var progress = status.progress || 0;
        var stage = status.stage || '处理中...';
        var fromVer = status.from_version || '?';
        var toVer = status.to_version || '?';

        var progressColor = progress > 80 ? '#00c853' : progress > 50 ? '#d4af37' : '#c41e3a';
        var timeInfo = status.remaining_formatted ? '预计剩余: ' + status.remaining_formatted : (status.elapsed_formatted ? '已用: ' + status.elapsed_formatted : '');

        indicator.innerHTML =
            '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">' +
                '<div style="display:flex;align-items:center;gap:8px">' +
                    '<span style="font-size:20px;animation:lh-spin 2s linear infinite">🐉</span>' +
                    '<span style="color:#c41e3a;font-weight:700;font-size:14px;letter-spacing:2px">龍魂AI模型进化中</span>' +
                '</div>' +
                '<span style="color:#5a5a6a;font-size:11px;font-family:monospace">' + status.state.toUpperCase() + '</span>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">' +
                '<span style="color:#8a8a9a;font-size:12px">AIv' + fromVer + '</span>' +
                '<span style="color:#c41e3a;font-size:16px">→</span>' +
                '<span style="color:#d4af37;font-size:12px;font-weight:700">AIv' + toVer + '</span>' +
            '</div>' +
            '<div style="background:#1a1a24;border-radius:8px;height:8px;overflow:hidden;margin-bottom:8px">' +
                '<div style="width:' + progress + '%;height:100%;background:linear-gradient(90deg,' + progressColor + ',' + progressColor + '88);border-radius:8px;transition:width 0.5s ease;box-shadow:0 0 8px ' + progressColor + '44"></div>' +
            '</div>' +
            '<div style="display:flex;justify-content:space-between;align-items:center">' +
                '<span style="color:#8a8a9a;font-size:11px">' + stage + '</span>' +
                '<span style="color:' + progressColor + ';font-family:monospace;font-size:12px;font-weight:700">' + progress.toFixed(1) + '%</span>' +
            '</div>' +
            (timeInfo ? '<div style="color:#5a5a6a;font-size:10px;margin-top:8px;text-align:right">' + timeInfo + '</div>' : '') +
            (status.metrics && status.metrics.samples ? '<div style="color:#5a5a6a;font-size:10px;margin-top:4px;border-top:1px solid #2a2a3a;padding-top:8px">训练样本: ' + status.metrics.samples.toLocaleString() + (status.metrics.features ? ' | 特征: ' + status.metrics.features : '') + '</div>' : '');

        document.body.appendChild(indicator);
    }

    function showTrainingCompleteNotification(status) {
        var existing = document.getElementById('lh-training-notification');
        if (existing) existing.remove();

        var notification = document.createElement('div');
        notification.id = 'lh-training-notification';
        var metrics = status.metrics || {};
        notification.innerHTML =
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">' +
                '<span style="font-size:20px">✅</span>' +
                '<span style="color:#00c853;font-weight:700;font-size:14px">模型进化完成</span>' +
            '</div>' +
            '<div style="color:#e8e8f0;font-size:13px;margin-bottom:4px">AIv' + status.from_version + ' → AIv' + status.to_version + '</div>' +
            '<div style="color:#8a8a9a;font-size:11px">准确率: ' + ((metrics.accuracy || 0) * 100).toFixed(1) + '% | 样本: ' + (metrics.training_samples || 0).toLocaleString() + '</div>';

        document.body.appendChild(notification);

        setTimeout(function() {
            notification.style.animation = 'lh-notif-fade-out 0.5s ease forwards';
            setTimeout(function() { if (notification.parentNode) notification.remove(); }, 500);
        }, 5000);
    }

    function showTrainingError(status) {
        var existing = document.getElementById('lh-training-indicator');
        if (!existing) return;

        existing.style.borderColor = '#ff1744';
        existing.innerHTML =
            '<div style="text-align:center">' +
                '<div style="font-size:24px;margin-bottom:8px">❌</div>' +
                '<div style="color:#ff1744;font-weight:700;margin-bottom:8px">训练失败</div>' +
                '<div style="color:#8a8a9a;font-size:12px">' + (status.error || '未知错误') + '</div>' +
                '<div style="color:#5a5a6a;font-size:10px;margin-top:8px">已回滚至 AIv' + (status.from_version || '?') + '</div>' +
            '</div>';

        setTimeout(function() {
            if (existing.parentNode) existing.remove();
            var modelEl = document.getElementById('lh-model-version');
            if (modelEl) modelEl.classList.remove('training');
        }, 5000);
    }

    // ═══════════════════════════════════════════════════════
    // v5 新增: 模型版本获取 & 显示
    // ═══════════════════════════════════════════════════════

    function fetchModelVersion() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', VERIFY_API + '/model-version', true); xhr.timeout = 3000;
        xhr.onload = function() {
            if (xhr.status !== 200) return;
            var data;
            try { data = JSON.parse(xhr.responseText); } catch(e) { return; }
            updateModelVersionDisplay(data);
        };
        xhr.onerror = function() {};
        xhr.send();
    }

    function updateModelVersionDisplay(data) {
        var el = document.getElementById('lh-model-version');
        if (!el) { addModelVersionEl(); el = document.getElementById('lh-model-version'); }
        if (!el) return;

        var version = data.version || 0;
        var accuracy = (data.metrics && data.metrics.accuracy) || 0;
        var f1 = (data.metrics && data.metrics.f1) || 0;
        var samples = data.training_samples || 0;
        var status = data.status || 'unknown';

        var accPct = (accuracy * 100).toFixed(0);
        var samplesK = samples >= 1000 ? (samples / 1000).toFixed(1) + 'k' : samples;

        CURRENT_MODEL_VERSION = version;
        el.textContent = 'AIv' + version + ' | ' + accPct + '% | ' + samplesK;

        // 颜色等级
        el.className = '';
        if (status === 'active') {
            if (accuracy >= 0.9) el.className = 'good';
            else if (accuracy >= 0.7) el.className = 'warning';
            else el.className = 'caution';
        } else {
            el.className = 'caution';
        }

        // 悬停提示
        var uptime = data.uptime_seconds || 0;
        var uptimeStr = uptime > 86400 ? Math.floor(uptime / 86400) + 'd' + Math.floor((uptime % 86400) / 3600) + 'h' :
            uptime > 3600 ? Math.floor(uptime / 3600) + 'h' + Math.floor((uptime % 3600) / 60) + 'm' :
            Math.floor(uptime / 60) + 'm';

        el.title = [
            '龍魂AI初审模型',
            '版本: v' + version,
            '准确率: ' + accPct + '% | F1: ' + (f1 * 100).toFixed(1) + '%',
            '训练样本: ' + (samples || 0).toLocaleString(),
            '运行: ' + uptimeStr,
            'DNA: ' + (data.dna || 'UID9622'),
            '状态: ' + status,
            '',
            '点击刷新模型状态',
        ].join('\n');

        // 待切换版本提示
        var oldPending = document.getElementById('lh-pending-version');
        if (oldPending) oldPending.remove();

        if (data.pending_version) {
            var pv = data.pending_version;
            var pendingEl = document.createElement('span');
            pendingEl.id = 'lh-pending-version';
            pendingEl.textContent = '→v' + (pv.version || '?');
            pendingEl.style.cssText = 'margin-left:4px;font-size:9px;color:#ff9100;animation:lh-pulse 1s ease-in-out infinite';
            pendingEl.title = '新版本待切换\n预计准确率: ' + ((pv.metrics && pv.metrics.accuracy ? pv.metrics.accuracy * 100 : 0)).toFixed(1) + '%';
            el.appendChild(pendingEl);
        }
    }

    // ── 时钟 / 节点计数 / 流量（同 v4） ──
    function updateClock() {
        var now = new Date();
        var t = [now.getHours(), now.getMinutes(), now.getSeconds()].map(function(n) { return (n < 10 ? '0' : '') + n; }).join(':');
        var clockEl = document.getElementById('lh-clock'); if (clockEl) clockEl.textContent = t;
        var uptime = Math.floor((Date.now() - START_TIME) / 1000);
        var h = Math.floor(uptime / 3600), m = Math.floor((uptime % 3600) / 60), s = uptime % 60;
        var uptimeEl = document.getElementById('lh-uptime'); if (uptimeEl) uptimeEl.textContent = '运行: ' + h + 'h' + m + 'm' + s + 's';
    }

    function updateNodeCount() {
        var greenTags = document.querySelectorAll('.ant-tag-green, .status-online, [class*="online"]');
        var count = greenTags.length;
        var countEl = document.getElementById('lh-nodes-count');
        if (countEl) { countEl.textContent = count; countEl.style.color = count === 0 ? '#ff1744' : count < 2 ? '#ff9100' : '#e8e8f0'; }
    }

    function estimateTraffic() {
        var trafficEl = document.getElementById('lh-traffic'); if (!trafficEl) return;
        var tables = document.querySelectorAll('table'); var totalIn = 0, totalOut = 0;
        tables.forEach(function(table) {
            var cells = table.querySelectorAll('td');
            cells.forEach(function(cell) {
                var text = cell.textContent || ''; var m;
                if ((m = text.match(/([\d.]+)\s*(MB|GB|KB)/i))) {
                    var val = parseFloat(m[1]);
                    if (m[2].toUpperCase() === 'GB') val *= 1024;
                    if (m[2].toUpperCase() === 'KB') val /= 1024;
                    if (cell.previousElementSibling && /in|入/i.test(cell.previousElementSibling.textContent || '')) totalIn += val;
                    else totalOut += val;
                }
            });
        });
        if (totalIn + totalOut > 0) {
            var t = totalIn + totalOut;
            trafficEl.textContent = t > 1024 ? (t / 1024).toFixed(1) + 'GB' : t.toFixed(1) + 'MB';
        }
    }

    // ── 初始化 ──
    function init() {
        if (document.getElementById('longhun-footer-bar')) return;

        createFooterBar();
        createQuarantinePanel();

        setInterval(updateClock, 1000);
        setInterval(updateNodeCount, 5000);
        setInterval(updatePersonaStatus, 10000);
        setInterval(estimateTraffic, 15000);

        updateClock(); updateNodeCount(); updatePersonaStatus();
        setTimeout(estimateTraffic, 3000);

        // v5: 启动训练轮询 + 获取模型版本
        startTrainingPoll();
        setTimeout(fetchModelVersion, 2000);

        console.log('🐉 龍魂人格验证面板 v5.0 | ' + DNA + ' | 训练进度+模型版本');
    }

    if (document.readyState === 'complete') { init(); }
    else { window.addEventListener('load', init); setTimeout(init, 3000); }

    var observer = new MutationObserver(function() {
        if (!document.getElementById('longhun-footer-bar')) init();
        addPersonaBadges();
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
