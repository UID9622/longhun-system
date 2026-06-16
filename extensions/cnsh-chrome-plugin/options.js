/**
 * Options 页逻辑 - 加载 / 保存 / 测试连接
 */

// UID9622 已有的四大数据库 ID（来自龍魂系统记忆）
const UID9622_DBS = {
  db_inbox: '1d9af383-6784-42db-827f-c035be3f1458',
  db_dna:   '6f1ddacc-289c-46fc-9369-a07e3d937f5e',
  db_tasks: '58953efd-0588-40df-b30c-b763e76b0ae9',
  db_heart: '9702a79e-c4e2-40c1-ab28-cc7721fb19e9'
};

const fields = ['notion_token', 'db_inbox', 'db_dna', 'db_tasks', 'db_heart'];

function $ (id) { return document.getElementById(id); }

function showStatus(elId, text, ok) {
  const el = $(elId);
  el.textContent = text;
  el.className = 'status ' + (ok ? 'ok' : 'err');
  setTimeout(() => { el.className = 'status'; }, 4000);
}

// ── 加载 ──
chrome.storage.local.get(fields, (cfg) => {
  fields.forEach(k => {
    if (cfg[k]) $(k).value = cfg[k];
  });
});

// ── 保存 ──
$('save').addEventListener('click', async () => {
  const data = {};
  fields.forEach(k => { data[k] = $(k).value.trim(); });
  if (!data.notion_token) {
    showStatus('save-status', '⚠️ 至少要填 Token 才能工作', false);
    return;
  }
  await chrome.storage.local.set(data);
  showStatus('save-status', '✅ 已保存到 chrome.storage.local', true);
});

// ── 显 / 隐 Token ──
$('show-token').addEventListener('click', () => {
  const el = $('notion_token');
  el.type = el.type === 'password' ? 'text' : 'password';
});

// ── 测试连接 ──
$('test-conn').addEventListener('click', async () => {
  const token = $('notion_token').value.trim();
  if (!token) {
    showStatus('conn-status', '请先填 Token', false);
    return;
  }
  showStatus('conn-status', '⏳ 测试中...', true);
  const resp = await chrome.runtime.sendMessage({ type: 'CNSH_TEST_CONN', token });
  if (resp && resp.ok) {
    const name = (resp.bot && (resp.bot.name || (resp.bot.bot && resp.bot.bot.owner && resp.bot.bot.owner.type))) || 'Bot';
    showStatus('conn-status', `✅ 连接成功 · ${name}`, true);
  } else {
    showStatus('conn-status', `❌ ${resp && resp.error || '未知错误'}`, false);
  }
});

// ── 预填我的 ──
$('fill-mine').addEventListener('click', () => {
  Object.entries(UID9622_DBS).forEach(([k, v]) => { $(k).value = v; });
  showStatus('save-status', '⚡ 已预填 UID9622 四大库，别忘了按保存', true);
});
