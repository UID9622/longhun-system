# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 龍魂六堆 · 主控制器 v1.0（编号对齐版）
document.addEventListener('DOMContentLoaded', function() {
    console.log('🐉 龍魂六堆 v1.0 已加载');
    console.log('DNA: #龍芯⚡️2026-08-31-6D-VISION-v1.0-UID9622');
    console.log('CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z');
    console.log('P00 = 曾仕强老师数字人 · 北辰 = 执行者');

    // 渲染所有堆
    window.renderAll = function() {
        if (window.renderRoot) window.renderRoot();
        if (window.renderPersona) window.renderPersona();
        if (window.renderData) window.renderData();
        if (window.renderEngine) window.renderEngine();
        if (window.renderAudit) window.renderAudit();
        if (window.renderPortal) window.renderPortal();
        document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
    };

    // 初始渲染
    window.renderAll();

    // 模拟实时更新（每5秒）
    setInterval(() => {
        STATE.audit.dnaChainLength += Math.floor(Math.random() * 2);
        STATE.engine.ports.forEach(p => {
            p.latency = Math.floor(Math.random() * 30 + 5);
        });
        window.renderAll();
    }, 5000);

    // WebSocket连接（真实环境）
    function connectWS() {
        const ws = new WebSocket('ws://localhost:8788/ws');
        ws.onmessage = function(e) {
            try {
                const data = JSON.parse(e.data);
                if (data.state) window.updateState(data.state);
                window.renderAll();
            } catch(err) { /* ignore */ }
        };
        ws.onclose = function() {
            console.log('WS断开，5秒后重连');
            setTimeout(connectWS, 5000);
        };
    }
    // connectWS(); // 取消注释启用真实WS
});
