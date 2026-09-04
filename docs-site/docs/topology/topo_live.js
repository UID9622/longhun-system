(function () {
  'use strict';
  var TYPE_CN = { document: '文档', article: '文章', asset: '素材', copy: '平台文案', endpoint: '入口', issue: '公告', report: '报告' };
  var style = document.createElement('style');
  style.textContent = [
    '#topo-live{font-size:14px;line-height:1.75;margin:10px 0}',
    '#topo-live-q{width:100%;box-sizing:border-box;padding:10px 14px;font-size:15px;border:1px solid #d1d5db;border-radius:10px;outline:none;background:#fff}',
    '#topo-live-q:focus{border-color:#4f46e5;box-shadow:0 0 0 3px rgba(79,70,229,.15)}',
    '.tlc{color:#64748b;font-size:13px;margin:8px 2px}',
    '.tlr{display:flex;gap:10px;align-items:baseline;padding:7px 10px;border-bottom:1px solid #f1f5f9;border-radius:8px}',
    '.tlr:hover{background:#f8fafc}',
    '.tldot{width:8px;height:8px;border-radius:50%;flex:none;align-self:center}',
    '.tln{font-weight:600;white-space:nowrap}',
    '.tldna{flex:none;font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#6d4c41;background:#efe6d5;border-radius:4px;padding:1px 6px;cursor:pointer;white-space:nowrap;max-width:22em;overflow:hidden}',
    '.tlm{color:#64748b;font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
    '.tla{margin-left:auto;flex:none;text-decoration:none;color:#4f46e5;font-size:13px;font-weight:600}',
    '.tle{margin:12px 2px;color:#334155;font-size:13px;line-height:1.9}'
  ].join('\n');
  document.head.appendChild(style);
  var q = document.getElementById('topo-live-q');
  var cnt = document.getElementById('topo-live-count');
  var list = document.getElementById('topo-live-list');
  if (!q || !cnt || !list) { return; }
  var data = null;
  fetch('data.json', { cache: 'no-store' })
    .then(function (r) { if (!r.ok) { throw new Error('HTTP ' + r.status); } return r.json(); })
    .then(function (d) { data = d; render(''); })
    .catch(function () { cnt.textContent = '⚠️ 交互数据加载失败（data.json 未就绪）'; });
  function find(f) {
    if (!f) { return data.nodes; }
    var k = f.toLowerCase();
    return data.nodes.filter(function (n) {
      return [n.name, n.group, n.type, TYPE_CN[n.type] || '', n.doc_type, n.title, n.desc, n.dna]
        .join(' ').toLowerCase().indexOf(k) >= 0;
    });
  }
  function row(n) {
    var r = document.createElement('div'); r.className = 'tlr';
    var dot = document.createElement('span'); dot.className = 'tldot';
    var st = String(n.status || '');
    dot.style.background = st.indexOf('🟢') >= 0 ? '#16a34a' : (st.indexOf('🟡') >= 0 ? '#d97706' : '#94a3b8');
    dot.title = st;
    var name = document.createElement('span'); name.className = 'tln';
    name.textContent = n.name;
    var meta = document.createElement('span'); meta.className = 'tlm';
    meta.textContent = '  ' + (TYPE_CN[n.type] || n.type || '节点')
      + (n.doc_type ? ' · ' + n.doc_type : '') + ' · ' + (n.group || '');
    r.appendChild(dot); r.appendChild(name);
    if (n.dna) {
      var dna = document.createElement('span'); dna.className = 'tldna';
      dna.textContent = (n.dna.slice(0, 8) || '?');
      dna.title = 'DNA 前缀（v2.0 可验证）· 点击展开/收起完整 DNA';
      dna.addEventListener('click', function () {
        dna.textContent = dna._full ? (n.dna.slice(0, 8)) : n.dna;
        dna._full = !dna._full;
      });
      r.appendChild(dna);
    }
    r.appendChild(meta);
    var tail = document.createElement('span'); tail.className = 'tla';
    if (n.link) {
      var a = document.createElement('a');
      a.href = n.link; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.textContent = '↗ 打开';
      r.appendChild(a);
    } else {
      tail.style.color = '#94a3b8'; tail.style.fontWeight = 'normal';
      tail.textContent = '🔒 内部资产';
      r.appendChild(tail);
    }
    return r;
  }
  function edgesBlock() {
    var w = document.createElement('div'); w.className = 'tle';
    w.textContent = '🔗 关联边 ' + (data.edges ? data.edges.length : 0) + ' 条：'
      + (data.edges || []).map(function (e) {
        return e.source + ' → ' + e.target + (e.label ? '（' + e.label + '）' : '');
      }).join(' · ');
    return w;
  }
  function render(f) {
    if (!data) { return; }
    var rows = find(f);
    cnt.textContent = '共 ' + data.nodes.length + ' 个节点 · 当前匹配 ' + rows.length + ' 个';
    list.innerHTML = '';
    rows.forEach(function (n) { list.appendChild(row(n)); });
    if (!f) { list.appendChild(edgesBlock()); }
  }
  q.addEventListener('input', function () { render(q.value.trim()); });
  // v2.0: 5 分钟轮询公共 status API → 根哈希变化即提示刷新（无后端 · 404 静默）
  var banner = document.getElementById('topo-live-updated');
  function pollStatus() {
    fetch('/api/topo/status.json', { cache: 'no-store' })
      .then(function (r) { if (!r.ok) { return null; } return r.json(); })
      .then(function (st) {
        if (st && data && banner && st.root_hash && st.root_hash !== data.root_hash) {
          banner.style.display = 'inline';
        }
      })
      .catch(function () { /* 本地/未部署 API → 静默 */ });
  }
  setInterval(pollStatus, 300000);
  pollStatus();
})();