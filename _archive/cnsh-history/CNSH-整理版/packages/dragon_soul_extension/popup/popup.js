// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: popup.js | 标记时间: 2026-06-03T07:46:00+0800
document.addEventListener('DOMContentLoaded', async () => {
  await loadStatistics();

  document.getElementById('clearQuarantine').addEventListener('click', clearQuarantine);
  document.getElementById('exportLogs').addEventListener('click', exportLogs);
  document.getElementById('viewDashboard').addEventListener('click', viewDashboard);
});

async function loadStatistics() {
  const { auditLogs, quarantine } = await chrome.storage.local.get(['auditLogs', 'quarantine']);

  const today = new Date().toISOString().substring(0, 10);
  const todayLogs = (auditLogs || []).filter(log =>
    log.timestamp.startsWith(today)
  );

  const blocked = todayLogs.filter(log => log.status === 'BLOCKED').length;
  const quarantined = todayLogs.filter(log => log.status === 'QUARANTINE').length;
  const normalized = todayLogs.filter(log => log.status === 'NORMALIZED').length;

  document.getElementById('blockedCount').textContent = blocked;
  document.getElementById('quarantineCount').textContent = quarantined;
  document.getElementById('normalizedCount').textContent = normalized;
}

async function clearQuarantine() {
  if (confirm('确认清空隔离区？')) {
    await chrome.storage.local.set({ quarantine: [] });
    alert('✅ 隔离区已清空');
    await loadStatistics();
  }
}

async function exportLogs() {
  const { auditLogs } = await chrome.storage.local.get(['auditLogs']);
  const blob = new Blob([JSON.stringify(auditLogs, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = `dragon_audit_${new Date().toISOString().substring(0, 10)}.json`;
  a.click();

  URL.revokeObjectURL(url);
}

function viewDashboard() {
  // 这里只是一个示例，您可以创建一个dashboard.html文件来实现更复杂的仪表盘
  alert('仪表盘功能待开发，当前仅导出日志。');
  exportLogs();
}
