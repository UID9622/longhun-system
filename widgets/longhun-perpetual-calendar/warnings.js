/**
 * 龍魂万年历 · 预警通知 + 文明基因图谱 + H武器推演 渲染引擎 v1.0
 * DNA: #龍芯⚡️丙午·丙申·戊午·午时·䷎谦-LH-CALENDAR-WARNINGS-v1.0
 * 创建者: 诸葛鑫（UID9622） · 协议: CC BY-NC-SA 4.0
 *
 * 数据源（鲲鹏 /opt/longhun/calendar/www/ 静态 JSON，每小时巡检自动刷新）：
 *   events.json        预警事件（🔴🟡🟢）
 *   scan-status.json   巡检状态（上次/下次/基线/异常/引擎）
 *   gene-map.json      文明基因图谱（事件链 + 历史重演模式）
 *   prophecy.json      历史重演预言（重演 → 预判下一步）
 *   h-weapon.json      H武器 16维推演投影（太极易经收敛解）
 *
 * 自动刷新：60 秒轮询，无需手动刷新。
 */

const LonghunWarnings = (function () {
  'use strict';

  const API = {
    events: 'events.json',
    scanStatus: 'scan-status.json',
    geneMap: 'gene-map.json',
    prophecy: 'prophecy.json',
    hWeapon: 'h-weapon.json',
  };

  const DOMAIN_KEYS = {
    longhun: '🐉 龍魂史',
    greek: '🏛️ 希腊神话',
    industrial: '⚙️ 工业革命',
  };

  const LEVEL_META = {
    '🔴': { label: '篡改', cls: '🔴' },
    '🟡': { label: '待核', cls: '🟡' },
    '🟢': { label: '例行', cls: '' },
  };

  let currentDomain = 'longhun';
  let geneMapCache = null;

  function $(id) {
    return document.getElementById(id);
  }

  async function fetchJSON(url) {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  function fmtTime(iso) {
    if (!iso) return '--';
    const d = new Date(iso);
    if (isNaN(d.getTime())) return String(iso).slice(0, 16);
    const pad = (n) => String(n).padStart(2, '0');
    return `${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function setSubscribeLinks() {
    const base = location.origin + location.pathname.replace(/[^/]*$/, '');
    const ics = base + 'longhun.ics';
    const webcal = $('subscribe-webcal');
    const https = $('subscribe-https');
    const urlBox = $('subscribe-url');
    if (webcal) webcal.href = 'webcal://' + location.host + location.pathname.replace(/[^/]*$/, '') + 'longhun.ics';
    if (https) https.href = ics;
    if (urlBox) urlBox.textContent = 'webcal://' + location.host + location.pathname.replace(/[^/]*$/, '') + 'longhun.ics';
  }

  /* ── 巡检状态条 ── */
  function renderScanStatus(data) {
    const dot = $('scan-dot');
    if (!dot) return;
    let level = 'ok';
    let status = '正常';
    if (data && data.status) {
      status = data.status;
      if (String(status).includes('异常') || (data.new_failures || 0) > 0) level = 'crit';
      else if ((data.new_ganzhi_diffs || 0) > 0) level = 'warn';
    }
    dot.className = 'scan-dot ' + level;
    const last = $('scan-last');
    const next = $('scan-next');
    const base = $('scan-baseline');
    const eng = $('scan-engine');
    if (last) last.textContent = '巡检: ' + fmtTime(data && data.last_scan) + ' · ' + status;
    if (next) next.textContent = '下次: ' + fmtTime(data && data.next_scan);
    if (base) base.textContent = '基线: ' + ((data && (data.baseline_files ?? data.total_files)) ?? '--') + ' 文件';
    if (eng) eng.textContent = '引擎: ' + ((data && data.engine) || 'lh_dna_scan');
  }

  /* ── 预警列表 ── */
  function renderAlerts(events) {
    const box = $('alert-list');
    if (!box) return;
    const list = (events && events.events) || [];
    if (!list.length) {
      box.innerHTML = '<div class="empty-tip">🟢 当前无预警事件 · 系统运行正常</div>';
      return;
    }
    box.innerHTML = list.slice(0, 8).map((e) => {
      const meta = LEVEL_META[e.level] || { label: '事件', cls: '' };
      return `<div class="repeat-card ${meta.cls}">
        <div class="repeat-head">
          <span>${esc(e.level || '')} ${esc(e.title || '事件')}</span>
          <span class="repeat-score">${fmtTime(e.created_at)}</span>
        </div>
        <div class="repeat-detail">${esc(e.desc || '')}</div>
      </div>`;
    }).join('');
  }

  /* ── 文明基因图谱 ── */
  function renderGenePanel() {
    const chainBox = $('gene-chain');
    const repeatsBox = $('gene-repeats');
    const meta = $('gene-meta');
    if (!chainBox || !repeatsBox) return;
    if (!geneMapCache || !geneMapCache.domains || !geneMapCache.domains[currentDomain]) {
      chainBox.innerHTML = '<div class="empty-tip">图谱数据未就绪</div>';
      repeatsBox.innerHTML = '';
      return;
    }
    const dom = geneMapCache.domains[currentDomain];
    if (meta) meta.textContent = `${dom.name} · ${dom.total_events} 事件 · ${dom.windows_checked} 窗口`;
    // 事件链
    const chain = dom.event_chain || [];
    if (!chain.length) {
      chainBox.innerHTML = '<div class="empty-tip">事件链为空</div>';
    } else {
      chainBox.innerHTML = chain.map((e) =>
        `<div class="gene-node">
          <span class="gz">${esc(e.gz)}</span>
          <span class="gua">${esc(e.gua)}卦 · ${esc(e.wuxing)}</span>
          <span class="type">${esc(e.type)}</span>
          <span class="title" title="${esc(e.title)}">${esc(e.title)}</span>
        </div>`).join('');
    }
    // 重演模式
    const reps = dom.repeats || [];
    if (!reps.length) {
      repeatsBox.innerHTML = '<div class="empty-tip">🟢 当前窗口无历史重演信号</div>';
      return;
    }
    repeatsBox.innerHTML = reps.map((r) => {
      const mw = (r.matched_window || []).map((e) => e.title).join(' → ');
      const tl = (r.tail_label || '当前');
      return `<div class="repeat-card ${r.level}">
        <div class="repeat-head">
          <span>${esc(r.level)} 历史重演 · 相似度 <b>${r.score}</b></span>
          <span class="repeat-score">${esc(r.era_label)}</span>
        </div>
        <div class="repeat-detail">历史窗口：${esc(mw)}<br>当前窗口：${esc(tl)}</div>
      </div>`;
    }).join('');
  }

  /* ── 预言 ── */
  function renderProphecy(data) {
    const box = $('prophecy-list');
    if (!box) return;
    const list = (data && data.prophecies) || [];
    if (!list.length) {
      box.innerHTML = '<div class="empty-tip">🔮 暂无预言 · 重演识别持续运行中</div>';
      return;
    }
    box.innerHTML = list.slice(0, 6).map((p) =>
      `<div class="prophecy-card ${p.level}">
        <div class="prophecy-head">
          <span>${esc(p.level)} ${esc(p.title)}</span>
          <span class="repeat-score">置信 ${p.confidence}</span>
        </div>
        <div class="repeat-detail">${esc(p.desc || '')} · 匹配历史：${esc(p.matched_era || '')}</div>
        <div class="prophecy-eta">⏳ ${esc(p.eta_hint || '')} · ${esc(p.gua || '')}卦 · ${esc(p.wuxing || '')}</div>
      </div>`).join('');
  }

  /* ── H武器推演 ── */
  function renderHWeapon(data) {
    const box = $('hweapon-content');
    if (!box) return;
    if (!data) {
      box.innerHTML = '<div class="empty-tip">推演数据未就绪</div>';
      return;
    }
    const dims = (data.dimensions_used || []).slice(0, 6);
    const tl = (data.execution_timeline || []).slice(0, 3);
    const wu = (data.wuxing_diagnosis && data.wuxing_diagnosis.trigger_wuxing) ? ` · 触发五行 ${data.wuxing_diagnosis.trigger_wuxing}` : '';
    box.innerHTML = `
      <div class="hweapon-trigger">
        <span class="label">⚡ 触发词（最新事件 → 太极易经推演）</span>
        ${esc(data.trigger || '--')}
      </div>
      <div class="hweapon-score">
        <div class="score-box"><div class="num">${data.final_score ?? '--'}</div><div class="cap">收敛分 /10</div></div>
        <div class="score-box"><div class="num">${esc((data.optimal_strategy && data.optimal_strategy.path_id) || '--')}</div><div class="cap">最优路径</div></div>
        <div class="score-box"><div class="num">${esc(data.engine || '--')}</div><div class="cap">推演引擎</div></div>
      </div>
      <div class="hweapon-dims">主导维度：${dims.map((d) => `<b>${esc(d)}</b>`).join(' · ')}${esc(wu)}</div>
      ${tl.length ? `<div class="hweapon-tl">执行时间线：${tl.map(esc).join(' → ')}</div>` : ''}
      <div class="hweapon-dna">DNA: ${esc(data.dna || '--')}</div>`;
  }

  /* ── 数据装载 ── */
  async function loadAll() {
    // 并行拉取全部数据源
    const [events, scan, gene, prophecy, hw] = await Promise.all([
      fetchJSON(API.events).catch(() => null),
      fetchJSON(API.scanStatus).catch(() => null),
      fetchJSON(API.geneMap).catch(() => null),
      fetchJSON(API.prophecy).catch(() => null),
      fetchJSON(API.hWeapon).catch(() => null),
    ]);
    if (gene) geneMapCache = gene;
    renderScanStatus(scan);
    renderAlerts(events);
    renderGenePanel();
    renderProphecy(prophecy);
    renderHWeapon(hw);
  }

  function bindTabs() {
    const tabs = document.querySelectorAll('#domain-tabs .domain-tab');
    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        tabs.forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');
        currentDomain = tab.getAttribute('data-domain') || 'longhun';
        renderGenePanel();
      });
    });
  }

  function init() {
    setSubscribeLinks();
    bindTabs();
    loadAll().catch((e) => {
      const list = $('alert-list');
      if (list) list.innerHTML = `<div class="empty-tip">⚠️ 预警服务连接失败：${esc(e.message)}</div>`;
    });
    // 60 秒轮询自动刷新
    setInterval(() => loadAll().catch(() => {}), 60000);
  }

  return { init };
})();
