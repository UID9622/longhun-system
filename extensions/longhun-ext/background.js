// 龍魂9622·background.js v2.0
// DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-BG-v2.0-6d1b7f9a
// 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 支持：Chrome / Safari MV3 / Edge

const ENGINE = "http://127.0.0.1:9622";

// ─── 右键菜单初始化 ───────────────────────────────────────
chrome.runtime.onInstalled.addListener(() => {
  const menus = [
    { id: "sep0",      type: "separator", contexts: ["selection"] },
    { id: "ethics",    title: "⚖️ 伦理审查",  contexts: ["selection"] },
    { id: "tongxin",   title: "🟡 通心译",    contexts: ["selection"] },
    { id: "wuxing",    title: "🔥 五行分析",  contexts: ["selection"] },
    { id: "cnsh",      title: "📐 CNSH语法",  contexts: ["selection"] },
    { id: "errata",    title: "📓 上报记错本", contexts: ["selection"] },
    { id: "sep1",      type: "separator", contexts: ["selection"] },
    { id: "voice",     title: "🎙️ 语音输入",  contexts: ["page"] },
    { id: "mcp",       title: "🔌 MCP工具",   contexts: ["selection", "page"] },
    { id: "sep2",      type: "separator", contexts: ["selection", "page"] },
    { id: "dna_check", title: "🧬 DNA验证",   contexts: ["selection", "page"] },
  ];
  menus.forEach(m => {
    if (m.type === "separator") {
      chrome.contextMenus.create({ id: m.id, type: "separator", contexts: m.contexts, parentId: undefined });
    } else {
      chrome.contextMenus.create({
        id: m.id, title: m.title, contexts: m.contexts,
        parentId: undefined
      });
    }
  });
});

// ─── 端点映射 ─────────────────────────────────────────────
const ENDPOINTS = {
  ethics:    "/api/ethics/review",
  tongxin:   "/api/tongxin/translate",
  wuxing:    "/api/wuxing/analyze",
  cnsh:      "/api/cnsh/align",
  errata:    "/api/errata/submit",
  mcp:       "/api/mcp/call",
  dna_check: "/api/dna/check",
  voice:     null, // handled by content.js
};

// ─── 右键点击处理 ──────────────────────────────────────────
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  const ep = ENDPOINTS[info.menuItemId];

  // 语音：发消息给content.js启动Web Speech API
  if (info.menuItemId === "voice") {
    chrome.tabs.sendMessage(tab.id, { type: "LONGHUN_VOICE_START" });
    return;
  }

  if (!ep) return;
  const text = info.selectionText || "";

  try {
    const res = await callEngine(ep, {
      text,
      url:   tab.url,
      title: tab.title,
      lang:  "zh"
    });

    // 通知
    showNotif(res);

    // 发给content脚本显示侧边栏
    chrome.tabs.sendMessage(tab.id, { type: "LONGHUN_RESULT", data: res });

    // 存到本地storage供popup读取
    chrome.storage.local.set({ lastResult: res, lastTs: Date.now() });

  } catch (e) {
    chrome.notifications.create({
      type: "basic", iconUrl: "icons/128.png",
      title: "🔴 9622引擎离线",
      message: "请运行: python3 ~/longhun-engine/main.py"
    });
  }
});

// ─── 核心请求函数 ──────────────────────────────────────────
async function callEngine(endpoint, payload) {
  const res = await fetch(ENGINE + endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

// ─── 通知函数 ──────────────────────────────────────────────
function showNotif(data) {
  chrome.notifications.create({
    type: "basic", iconUrl: "icons/128.png",
    title: `🐉 ${data.color || "🟢"} ${data.title || "完成"}`,
    message: String(data.summary || "").slice(0, 200)
  });
}

// ─── 接收popup消息 ─────────────────────────────────────────
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "LONGHUN_CALL") {
    callEngine(msg.endpoint, msg.payload)
      .then(sendResponse)
      .catch(e => sendResponse({ error: e.message }));
    return true; // 保持async通道
  }

  if (msg.type === "LONGHUN_VOICE_RESULT") {
    // 语音转文字后自动发送到引擎
    callEngine("/api/chat", { text: msg.text, mode: "auto", lang: "zh" })
      .then(data => {
        chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
          if (tabs[0]) chrome.tabs.sendMessage(tabs[0].id, { type: "LONGHUN_RESULT", data });
        });
      });
  }
});
