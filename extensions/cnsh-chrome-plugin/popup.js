/**
 * Popup 逻辑
 */

const statusEl = document.getElementById('status');

// ── Tabs ──
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const name = tab.dataset.pane;
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t === tab));
    document.querySelectorAll('.pane').forEach(p => p.classList.toggle('active', p.dataset.pane === name));
  });
});

// ── 辅助 ──
function showStatus(text, ok) {
  statusEl.textContent = text;
  statusEl.className = 'status ' + (ok ? 'ok' : 'err');
  setTimeout(() => { statusEl.className = 'status'; }, 3500);
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function getSelectionFromTab(tab) {
  try {
    const r = await chrome.tabs.sendMessage(tab.id, { type: 'CNSH_GET_SELECTION' });
    return r || { text: '' };
  } catch (_) {
    return { text: '' };
  }
}

// 预填当前页标题
(async () => {
  const tab = await getActiveTab();
  if (tab) {
    document.getElementById('inbox-title').placeholder = tab.title || '当前页';
  }
})();

// ── Inbox ──
document.getElementById('inbox-pull').addEventListener('click', async () => {
  const tab = await getActiveTab();
  const sel = await getSelectionFromTab(tab);
  if (sel.text) {
    document.getElementById('inbox-content').value = sel.text;
    showStatus('已导入选中', true);
  } else {
    showStatus('当前页无选中文本', false);
  }
});

document.getElementById('inbox-submit').addEventListener('click', async () => {
  const tab = await getActiveTab();
  const title = document.getElementById('inbox-title').value.trim() || (tab && tab.title) || '';
  const content = document.getElementById('inbox-content').value.trim();
  if (!title && !content) {
    showStatus('请至少填写标题或内容', false);
    return;
  }
  const resp = await chrome.runtime.sendMessage({
    type: 'CNSH_SEND_INBOX',
    payload: { title, url: tab && tab.url, sourceText: content }
  });
  if (resp && resp.ok) {
    showStatus('✅ 已送入 Inbox', true);
    document.getElementById('inbox-content').value = '';
  } else {
    showStatus('❌ ' + (resp && resp.error || '失败'), false);
  }
});

// ── DNA ──
document.getElementById('dna-submit').addEventListener('click', async () => {
  const concept = document.getElementById('dna-concept').value.trim();
  const techPoint = document.getElementById('dna-tech').value.trim();
  const direction = document.getElementById('dna-direction').value.trim();
  const purity = parseInt(document.getElementById('dna-purity').value, 10) || 70;
  if (!concept) { showStatus('请填写核心概念', false); return; }
  const resp = await chrome.runtime.sendMessage({
    type: 'CNSH_SEND_DNA',
    payload: { concept, techPoint, direction, purity }
  });
  if (resp && resp.ok) {
    showStatus('✅ 已入 DNA 库', true);
    document.getElementById('dna-concept').value = '';
    document.getElementById('dna-tech').value = '';
  } else {
    showStatus('❌ ' + (resp && resp.error || '失败'), false);
  }
});

// ── 人心 ──
document.getElementById('heart-submit').addEventListener('click', async () => {
  const title = document.getElementById('heart-title').value.trim();
  const insight = document.getElementById('heart-insight').value.trim();
  const scene = document.getElementById('heart-scene').value.trim();
  if (!title) { showStatus('请填写洞察标题', false); return; }
  const resp = await chrome.runtime.sendMessage({
    type: 'CNSH_SEND_HEART',
    payload: { title, insight, scene }
  });
  if (resp && resp.ok) {
    showStatus('✅ 已录入人心算法', true);
    document.getElementById('heart-title').value = '';
    document.getElementById('heart-insight').value = '';
  } else {
    showStatus('❌ ' + (resp && resp.error || '失败'), false);
  }
});

// ── 打开配置 ──
document.getElementById('open-options').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});
