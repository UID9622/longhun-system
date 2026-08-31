# DNA: #龍芯⚡️2026-08-31-stack1_persona-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 人格堆 · 30星群（编号对齐·P00=曾仕强老师）
function renderPersona() {
    const s = STATE.persona;
    const container = document.getElementById('persona-galaxy');
    container.innerHTML = '';

    s.list.forEach(p => {
        const star = document.createElement('span');
        star.className = 'persona-star' + (p.active ? ' active' : ' inactive');
        if (p.p00) star.className += ' p00';
        if (p.guardian) star.className += ' guardian';
        const size = 16 + (p.weight || 5) * 1.2;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        star.style.lineHeight = size + 'px';
        star.style.fontSize = Math.max(8, size * 0.32) + 'px';
        star.style.background = p.p00
            ? 'radial-gradient(circle, rgba(240,192,64,0.9), rgba(240,192,64,0.25))'
            : (p.active
                ? `rgba(167,139,250,${0.3 + (p.weight || 5) * 0.05})`
                : 'rgba(167,139,250,0.08)');
        star.style.border = p.p00 ? '2px solid #F0C040' : '1px solid rgba(167,139,250,0.3)';
        star.textContent = p.id.replace('P', '');
        star.title = p.id + ' ' + p.name + ' | ' + p.layer + ' | 权重:' + (p.weight || 5);
        star.addEventListener('click', () => {
            alert(p.id + ' ' + p.name + '\n' + p.layer + ' · 权重 ' + (p.weight || 5) + (p.active ? ' · 🟢激活' : ' · ⚪未激活'));
        });
        container.appendChild(star);
    });

    document.getElementById('persona-active').textContent = s.active + '/' + s.total;
    document.getElementById('persona-p00').textContent = 'P00: 曾仕强老师·智慧总师';
    document.getElementById('persona-status').textContent = s.active === s.total ? '🟢' : '🟡';
}
window.renderPersona = renderPersona;
