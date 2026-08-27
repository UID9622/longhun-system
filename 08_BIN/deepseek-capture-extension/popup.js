# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 🐉 龍魂 · DeepSeek 采集器 popup.js v1.0
const API = "http://127.0.0.1:8769/api/health";

function setSrv(on) {
  document.getElementById("srvDot").className = "dot " + (on ? "on" : "off");
  document.getElementById("srvTxt").textContent = on ? "已连接" : "未启动";
}

async function refresh() {
  // 本地服务状态
  try {
    const r = await fetch(API);
    if (r.ok) setSrv(true);
    else setSrv(false);
  } catch (e) { setSrv(false); }

  // 离线待补发数量
  chrome.storage.local.get({ pending: [] }, (d) => {
    document.getElementById("pendingCount").textContent = d.pending.length;
  });
}

document.getElementById("flushBtn").addEventListener("click", () => {
  chrome.runtime.sendMessage({ type: "flush" }, () => refresh());
});

chrome.runtime.onMessage.addListener((msg) => {
  if (msg && msg.type === "captured") {
    const el = document.getElementById("capturedCount");
    el.textContent = (parseInt(el.textContent, 10) || 0) + 1;
  }
});

refresh();
