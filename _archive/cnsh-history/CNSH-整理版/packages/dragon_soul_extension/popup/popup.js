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
