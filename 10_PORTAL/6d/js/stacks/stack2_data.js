# DNA: #龍芯⚡️2026-08-31-stack2_data-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 数据堆 · 知识库树 v1.0
function renderData() {
    const s = STATE.data;
    const tree = document.getElementById('data-tree');
    tree.innerHTML = '';

    s.categories.forEach(c => {
        const node = document.createElement('span');
        node.className = 'data-node';
        node.textContent = c.name + ' <span class="count">' + c.count + '</span>';
        node.innerHTML = c.name + ' <span class="count">' + c.count + '</span>';
        tree.appendChild(node);
    });

    document.getElementById('data-count').textContent = s.count + '+ 条';
    document.getElementById('data-index').textContent = 'INDEX ' + (s.indexStatus === 'ok' ? '✅' : '⚠️');
    document.getElementById('data-daemon').textContent = 'kb-daemon ' + (s.daemon === 'running' ? '🟢' : '🔴');
    document.getElementById('data-status').textContent = s.indexStatus === 'ok' ? '🟢' : '🟡';
}
window.renderData = renderData;
