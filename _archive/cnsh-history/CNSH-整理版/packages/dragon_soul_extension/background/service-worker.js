// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: service-worker.js | 标记时间: 2026-06-03T07:46:00+0800
// background/service-worker.js
// DNA: #龍芯⚡️2026-03-03-后台服务-熔断监控

chrome.runtime.onInstalled.addListener(() => {
  console.log('🐉 龍魂系统后台服务已启动');

  // 初始化存储
  chrome.storage.local.set({
    auditLogs: [],
    quarantine: [],
    fuseRecords: [],
    config: {
      uid: "9622",
      gpgFingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
      version: "v1.0-ETERNAL"
    }
  });

  // 设置定时清理任务（每天凌晨2点）
  chrome.alarms.create('dailyCleanup', {
    when: getNextCleanupTime(),
    periodInMinutes: 24 * 60
  });
});

// 监听定时任务
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'dailyCleanup') {
    performDailyCleanup();
  }
});

// 每日清理
async function performDailyCleanup() {
  console.log('🧹 执行每日清理任务');

  const { auditLogs, quarantine } = await chrome.storage.local.get(['auditLogs', 'quarantine']);
  // 保留最近30天的日志
  const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);

  const cleanedLogs = auditLogs.filter(log =>
    new Date(log.timestamp).getTime() > thirtyDaysAgo
  );

  const cleanedQuarantine = quarantine.filter(q =>
    new Date(q.timestamp).getTime() > thirtyDaysAgo
  );

  await chrome.storage.local.set({
    auditLogs: cleanedLogs,
    quarantine: cleanedQuarantine
  });

  console.log(`✅ 清理完成: 日志 ${auditLogs.length - cleanedLogs.length} 条, 隔离 ${quarantine.length - cleanedQuarantine.length} 条`);
}

function getNextCleanupTime() {
  const now = new Date();
  const next = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 2, 0, 0);
  return next.getTime();
}

// 监听来自content script的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'recordFuse') {
    recordFuseEvent(request.data);
    sendResponse({ success: true });
  }
  return true;
});

async function recordFuseEvent(data) {
  const { fuseRecords } = await chrome.storage.local.get(['fuseRecords']);
  fuseRecords.push({
    timestamp: new Date().toISOString(),
    ...data
  });
  await chrome.storage.local.set({ fuseRecords });
}
