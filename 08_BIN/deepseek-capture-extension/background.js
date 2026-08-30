// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-95b17fbf
// 🐉 龍魂 · DeepSeek 对话采集器 background.js v1.0
// Service Worker：服务恢复后批量补发离线暂存的对话
const API = "http://127.0.0.1:8769/api/capture";

async function flushPending() {
  const { pending = [] } = await chrome.storage.local.get({ pending: [] });
  if (!pending.length) return;
  const ok = [];
  for (const entry of pending) {
    try {
      const resp = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(entry),
      });
      if (resp.ok) ok.push(entry);
      else break; // 服务异常，停止本轮
    } catch (e) {
      break; // 服务未启动，等下次
    }
  }
  if (ok.length) {
    const rest = pending.slice(ok.length);
    await chrome.storage.local.set({ pending: rest });
    console.log(`🐉 补发 ${ok.length} 条离线对话`);
  }
}

// 每 60 秒尝试补发一次
chrome.alarms.create("flushPending", { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener((a) => {
  if (a.name === "flushPending") flushPending();
});

// 浏览器启动时也尝试一次
chrome.runtime.onStartup.addListener(() => flushPending());
