/**
 * 龍魂玄機閣 · 增强插件 v1.0
 * 五行议事会可视化 · 八卦状态 · 主题切换
 * DNA: #龍芯⚡️丙午·癸未·癸未·NOTION-BRIDGE-ENHANCED-v1.0-UID9622
 */
(function() {
  'use strict';

  const THEMES = [
    { id: 'theme-xuanji', label: '玄機閣' },
    { id: 'theme-cyber', label: '赛博龍魂' },
    { id: 'theme-minimal', label: '极简白纸' },
  ];

  const WUXING_META = {
    '木': { name: '木·生发', emoji: '🌲', color: '#4a7c59' },
    '火': { name: '火·转化', emoji: '🔥', color: '#b93a32' },
    '土': { name: '土·承载', emoji: '🟫', color: '#8b7355' },
    '金': { name: '金·收敛', emoji: '⚜️', color: '#c9a227' },
    '水': { name: '水·流动', emoji: '💧', color: '#4a7c9c' },
  };

  const BAGUA_DESC = {
    '乾': '开天启问', '坤': '厚德载物', '震': '雷动变革',
    '巽': '风行渗透', '坎': '水险渊深', '离': '火光照物',
    '艮': '山止为界', '兑': '泽悦交流'
  };

  // ===== 主题切换 =====
  function initTheme() {
    const saved = localStorage.getItem('notionBridgeTheme') || 'theme-xuanji';
    document.body.classList.remove(...THEMES.map(t => t.id));
    document.body.classList.add(saved);

    const actions = document.querySelector('.topbar-actions');
    if (!actions || document.getElementById('themeSwitcher')) return;

    const switcher = document.createElement('div');
    switcher.className = 'theme-switcher';
    switcher.id = 'themeSwitcher';
    switcher.innerHTML = THEMES.map(t =>
      `<button class="${t.id === saved ? 'active' : ''}" data-theme="${t.id}" onclick="window.setNotionTheme('${t.id}')">${t.label}</button>`
    ).join('');
    actions.insertBefore(switcher, actions.firstChild);
  }

  window.setNotionTheme = function(themeId) {
    document.body.classList.remove(...THEMES.map(t => t.id));
    document.body.classList.add(themeId);
    localStorage.setItem('notionBridgeTheme', themeId);
    document.querySelectorAll('#themeSwitcher button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === themeId);
    });
  };

  // ===== 八卦状态指示器 =====
  function initBaguaIndicator() {
    const breadcrumb = document.querySelector('.breadcrumb');
    if (!breadcrumb || document.getElementById('baguaIndicator')) return;

    const indicator = document.createElement('span');
    indicator.className = 'bagua-indicator';
    indicator.id = 'baguaIndicator';
    indicator.title = '当前对话八卦状态';
    indicator.innerHTML = '<span class="gua">☰</span><span id="baguaText">乾·启</span>';
    breadcrumb.appendChild(indicator);
    refreshBaguaState();
  }

  async function refreshBaguaState() {
    try {
      const res = await fetch(`${API_BASE}/api/bagua/state?session_id=${encodeURIComponent(currentPageId || 'default')}`);
      const data = await res.json();
      const el = document.getElementById('baguaIndicator');
      if (el && data.state) {
        el.querySelector('.gua').textContent = data.emoji || '☰';
        el.querySelector('#baguaText').textContent = `${data.state}·${BAGUA_DESC[data.state] || data.mood}`;
        el.title = `${data.name || ''}\n${data.desc || ''}\n偏好角色：${(data.roles || []).join('/')}`;
      }
    } catch (e) {
      // 静默失败
    }
  }

  // ===== 议事会模式开关 =====
  function initCouncilToggle() {
    const toolbar = document.querySelector('.chat-toolbar');
    if (!toolbar || document.getElementById('councilToggle')) return;

    const saved = localStorage.getItem('notionBridgeCouncilMode') === 'true';
    const toggle = document.createElement('label');
    toggle.className = 'council-toggle' + (saved ? ' active' : '');
    toggle.id = 'councilToggle';
    toggle.innerHTML = `<input type="checkbox" ${saved ? 'checked' : ''} onchange="window.toggleCouncilMode(this)"> 五行议事会`;
    toolbar.appendChild(toggle);
  }

  window.toggleCouncilMode = function(cb) {
    localStorage.setItem('notionBridgeCouncilMode', cb.checked);
    const toggle = document.getElementById('councilToggle');
    if (toggle) toggle.classList.toggle('active', cb.checked);
  };

  // ===== 拦截 sendMessage =====
  const originalSendMessage = window.sendMessage;
  window.sendMessage = async function(text) {
    const useCouncil = localStorage.getItem('notionBridgeCouncilMode') === 'true';
    if (!useCouncil) {
      return originalSendMessage(text);
    }
    await sendCouncilMessage(text);
  };

  // ===== 重新绑定 chatInput =====
  // 原 inline 脚本在增强脚本之前绑定 keydown，某些浏览器作用域解析导致覆盖不生效。
  // 用 cloneNode 替换输入框并重新绑定，确保 Enter 一定走 council/原始函数。
  function rebindChatInput() {
    const oldInput = document.getElementById('chatInput');
    if (!oldInput || oldInput.dataset.rebound === 'true') return;

    const newInput = oldInput.cloneNode(true);
    newInput.dataset.rebound = 'true';
    oldInput.parentNode.replaceChild(newInput, oldInput);

    newInput.addEventListener('keydown', async (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const text = newInput.value.trim();
        if (!text) return;
        newInput.value = '';
        newInput.style.height = 'auto';
        if (typeof hideMenus === 'function') hideMenus();

        const useCouncil = localStorage.getItem('notionBridgeCouncilMode') === 'true';
        if (useCouncil) {
          await sendCouncilMessage(text);
        } else if (typeof originalSendMessage === 'function') {
          await originalSendMessage(text);
        }
      } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        if (typeof isCommandMenuVisible === 'function' && isCommandMenuVisible()) {
          e.preventDefault();
          navigateCommandMenu(e.key === 'ArrowDown' ? 1 : -1);
        } else if (typeof isMentionMenuVisible === 'function' && isMentionMenuVisible()) {
          e.preventDefault();
          navigateMentionMenu(e.key === 'ArrowDown' ? 1 : -1);
        }
      } else if (e.key === 'Escape') {
        if (typeof hideMenus === 'function') hideMenus();
      }
    });

    newInput.addEventListener('input', (e) => {
      const text = newInput.value;
      const cmdMatch = text.match(/\/(\w*)$/);
      const mentionMatch = text.match(/@(\w*)$/);
      if (cmdMatch) {
        commandQuery = cmdMatch[1].toLowerCase();
        if (typeof showCommandMenu === 'function') showCommandMenu();
      } else if (mentionMatch) {
        mentionQuery = mentionMatch[1].toLowerCase();
        if (typeof showMentionMenu === 'function') showMentionMenu();
      } else {
        if (typeof hideMenus === 'function') hideMenus();
      }
      if (typeof autoResize === 'function') autoResize(newInput);
    });
  }

  async function sendCouncilMessage(text) {
    const page = pages.find(p => p.id === currentPageId);
    page.title = document.getElementById('pageTitle').value || text.slice(0, 20) || '新对话';
    page.blocks.push({ type: 'user', content: text });
    savePages();
    renderBlocks(page.blocks);

    const loadingId = 'loading_' + Date.now();
    page.blocks.push({ id: loadingId, type: 'loading', content: '' });
    renderBlocks(page.blocks);

    try {
      const res = await fetch(`${API_BASE}/api/chat/council`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: currentPageId,
          use_persona: true,
          temperature: 0.35,
          max_tokens: 512
        })
      });
      const data = await res.json();
      page.blocks = page.blocks.filter(b => b.id !== loadingId);

      const block = {
        type: 'ai',
        content: data.reply || data.response || '[无回复]',
        provider: 'council',
        model: data.model || 'wuxing-council-v1.0',
        mode: 'council',
        audit_status: data.audit_status || 'yellow',
        consensus_score: data.consensus_score || 0,
        bagua_state: data.bagua_state || {},
        council_members: data.council_members || [],
        synthesis_log: data.synthesis_log || {},
        similarities: data.similarities || [],
        fallback_chain: data.fallback_chain || []
      };
      page.blocks.push(block);
      refreshBaguaState();
    } catch (err) {
      page.blocks = page.blocks.filter(b => b.id !== loadingId);
      page.blocks.push({ type: 'ai', content: '请求失败：' + err.message, provider: 'error' });
    }
    savePages();
    renderBlocks(page.blocks);
    renderPageList();
    scrollToBottom();
  }

  // ===== 增强 renderBlockContent =====
  const originalRenderBlockContent = window.renderBlockContent;
  window.renderBlockContent = function(block) {
    if (block.type !== 'ai' || !block.council_members || !block.council_members.length) {
      return originalRenderBlockContent(block);
    }

    const members = block.council_members;
    const participated = members.filter(m => m.status === 'participated');
    const auditClass = 'audit-' + (block.audit_status || 'yellow');
    const bagua = block.bagua_state || {};

    const wuxingBar = `<div class="wuxing-bar">` +
      members.map(m => {
        const meta = WUXING_META[m.role] || { name: m.role, emoji: '●' };
        const activeClass = m.status === 'participated' ? 'participated active' : 'active';
        const title = `${meta.name} (${m.provider}/${m.model})\n权重 ${m.weight || 0}\n${m.status === 'participated' ? '参与本轮议事' : '补位委员'}`;
        return `<span class="wuxing-badge ${activeClass}" title="${escapeHtml(title)}">${meta.emoji} ${m.role} ${m.provider}</span>`;
      }).join('') +
      `</div>`;

    const synthesisDetails = members.map(m => {
      const meta = WUXING_META[m.role] || { name: m.role, emoji: '●' };
      return `<div class="member-reply"><span class="role">${meta.emoji} ${meta.name}</span> · ${m.provider}/${m.model}<br><span style="color:var(--text-secondary)">${escapeHtml(m.reply_preview || '')}</span></div>`;
    }).join('');

    const similarityText = (block.similarities || []).map(s => `${s.pair}: ${s.similarity}`).join(' · ');

    return `
      <div class="ai-model-badge">
        <span class="provider">五行议事会</span>
        <span class="mode">${bagua.emoji || '☰'} ${bagua.state || '乾'}·${bagua.name || '启'}</span>
        <span>共识度 ${(block.consensus_score * 100).toFixed(0)}%</span>
        <span style="margin-left:auto;font-size:11px;color:var(--text-tertiary)">三色审计：${auditColor(block.audit_status)}</span>
      </div>
      ${wuxingBar}
      <div>${markdownToHtml(block.content)}</div>
      <details class="synthesis-panel ${auditClass}">
        <summary>展开合成过程 · ${participated.length} 位委员 · ${similarityText || '无相似度'}</summary>
        ${synthesisDetails}
      </details>
    `;
  };

  function auditColor(status) {
    if (status === 'green') return '🟢';
    if (status === 'yellow') return '🟡';
    if (status === 'red') return '🔴';
    return '⚪';
  }

  // ===== 兼容原始变量 =====
  // API_BASE / currentPageId / pages / renderBlocks / scrollToBottom 等已在主脚本中定义

  // ===== 初始化 =====
  function init() {
    initTheme();
    initBaguaIndicator();
    initCouncilToggle();
    rebindChatInput();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
