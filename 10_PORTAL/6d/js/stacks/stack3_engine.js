# DNA: #龍芯⚡️2026-08-31-stack3_engine-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 引擎堆 · 六端口齿轮 v1.0
function renderEngine() {
    const s = STATE.engine;
    const grid = document.getElementById('engine-grid');
    grid.innerHTML = '';

    s.ports.forEach(p => {
        const gear = document.createElement('div');
        gear.className = 'engine-gear ' + (p.status === 'up' ? 'up' : 'down');
        gear.innerHTML = `
            <div class="port"><span class="dot ${p.status === 'up' ? 'green' : 'red'}"></span>${p.port}</div>
            <div class="name">${p.name}</div>
            <div class="latency">${p.status === 'up' ? p.latency + 'ms' : 'DOWN'}</div>`;
        grid.appendChild(gear);
    });

    const upCount = s.ports.filter(p => p.status === 'up').length;
    document.getElementById('engine-status').textContent = upCount === s.ports.length ? '🟢' : (upCount > 0 ? '🟡' : '🔴');
}
window.renderEngine = renderEngine;
