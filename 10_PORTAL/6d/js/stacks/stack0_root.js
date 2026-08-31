# DNA: #龍芯⚡️2026-08-31-stack0_root-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 根堆 · 协议 + 熔断律 v1.0
function renderRoot() {
    const s = STATE.root;

    document.getElementById('root-protocol').textContent = s.protocol;
    document.getElementById('root-killswitch').textContent = s.killswitch ? '🔴 关机键 · ' + s.killswitch : '⚪ 关机键 · 未激活';
    document.getElementById('root-seal').textContent = 'SEAL: ' + s.seal;
    document.getElementById('root-dna-count').textContent = 'DNA签章: ' + s.dnaCount;
    document.getElementById('root-status').textContent = s.triColor;

    const ring = document.getElementById('root-ring');
    ring.style.borderColor = s.triColor === '🟢' ? '#34D399' : s.triColor === '🟡' ? '#FBBF24' : '#F87171';
}
window.renderRoot = renderRoot;
