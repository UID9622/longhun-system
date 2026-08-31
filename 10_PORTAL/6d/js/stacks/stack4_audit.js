# DNA: #龍芯⚡️2026-08-31-stack4_audit-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 审计堆 · 三色 + DNA链 v1.0
function renderAudit() {
    const s = STATE.audit;
    document.getElementById('audit-tri').textContent = s.triColor + ' ' + s.triStatus;
    document.getElementById('audit-dna-chain').textContent = 'DNA链: ' + s.dnaChainLength;
    document.getElementById('audit-shame').textContent = '耻辱墙: ' + s.shameWallCount;
    document.getElementById('audit-fuse').textContent = '熔断: ' + (s.fuseTriggered ? '🔴 已触发' : '⚪ 待命');
    document.getElementById('audit-status').textContent = s.triColor;

    // 三色环高亮
    document.querySelectorAll('.audit-ring .ring').forEach(el => el.style.opacity = '0.35');
    const map = { '🟢': 'green', '🟡': 'yellow', '🔴': 'red' };
    const target = document.querySelector('.ring.' + map[s.triColor]);
    if (target) target.style.opacity = '1';

    // 点击切换审计视图
    document.querySelectorAll('.audit-ring .ring').forEach(el => {
        el.onclick = () => {
            const colorMap = { green: '🟢', yellow: '🟡', red: '🔴' };
            const statusMap = { green: '通过', yellow: '待核', red: '拒绝' };
            const c = colorMap[el.dataset.color];
            STATE.audit.triColor = c;
            STATE.audit.triStatus = statusMap[el.dataset.color];
            renderAudit();
        };
    });
}
window.renderAudit = renderAudit;
