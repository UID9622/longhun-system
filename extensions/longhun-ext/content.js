// 龍魂9622·content.js v2.0
// DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-CONTENT-v2.0-8a4f6d3b
// 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 功能：悬浮侧边栏 + Web Speech API (Safari/Chrome 通用) + 语音转文字

// ─── 侧边栏 ────────────────────────────────────────────────
function ensureSidebar() {
  let box = document.getElementById("longhun-9622-box");
  if (box) return box;

  box = document.createElement("div");
  box.id = "longhun-9622-box";
  box.setAttribute("lang", "zh");
  box.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    width: 400px;
    max-height: 70vh;
    overflow-y: auto;
    background: #ffffff;
    border: 2px solid #D4AF37;
    border-radius: 14px;
    padding: 18px;
    z-index: 2147483647;
    font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", system-ui, sans-serif;
    font-size: 14px;
    line-height: 1.7;
    box-shadow: 0 12px 36px rgba(0,0,0,0.18);
    color: #1a1a1a;
    transition: opacity 0.2s;
  `;

  // 关闭按钮
  const close = document.createElement("div");
  close.style.cssText = "position:absolute;top:10px;right:14px;cursor:pointer;font-size:18px;color:#aaa;";
  close.textContent = "✕";
  close.onclick = () => box.remove();
  box.appendChild(close);

  document.body.appendChild(box);
  return box;
}

function renderResult(data) {
  const box = ensureSidebar();
  const color = data.color || "🟢";
  const dna = data.dna || "";
  const notionLink = data.notion_url
    ? `<a href="${data.notion_url}" target="_blank" style="color:#D4AF37;text-decoration:none;font-size:12px;">📓 已入Notion →</a>`
    : "";

  box.innerHTML = `
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;padding-right:24px;">
      <span style="font-size:20px;">🐉</span>
      <strong style="font-size:15px;">龍魂9622 · ${color}</strong>
    </div>
    <div style="font-weight:600;margin-bottom:8px;font-size:14px;">${data.title || "结果"}</div>
    <pre style="white-space:pre-wrap;background:#f8f6f0;padding:10px 12px;border-radius:8px;font-family:inherit;font-size:13px;margin:0 0 10px;">${escHtml(String(data.summary || ""))}</pre>
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="color:#aaa;font-size:11px;font-family:monospace;">${escHtml(dna)}</span>
      ${notionLink}
    </div>
  `;

  // 重新添加关闭按钮（因为innerHTML覆盖）
  const close = document.createElement("div");
  close.style.cssText = "position:absolute;top:10px;right:14px;cursor:pointer;font-size:18px;color:#aaa;";
  close.textContent = "✕";
  close.onclick = () => box.remove();
  box.appendChild(close);
}

function escHtml(str) {
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

// ─── 语音输入 (Web Speech API · Chrome/Safari 通用) ─────────
let recognition = null;

function startVoice() {
  // Safari: webkitSpeechRecognition / Chrome: SpeechRecognition
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    showVoiceError("此浏览器不支持语音识别（请用Safari 14.1+或Chrome）");
    return;
  }

  recognition = new SR();
  recognition.lang = "zh-CN";      // 中文普通话
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  recognition.continuous = false;

  showVoiceOverlay("🎙️ 正在监听中文语音...");

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    updateVoiceOverlay(`🎙️ "${transcript}"`);

    if (event.results[event.results.length - 1].isFinal) {
      hideVoiceOverlay();
      // 把识别文字发给background.js
      chrome.runtime.sendMessage({
        type: "LONGHUN_VOICE_RESULT",
        text: transcript
      });
    }
  };

  recognition.onerror = (e) => {
    hideVoiceOverlay();
    showVoiceError(`语音错误：${e.error}`);
  };

  recognition.onend = () => hideVoiceOverlay();
  recognition.start();
}

function stopVoice() {
  if (recognition) { recognition.stop(); recognition = null; }
  hideVoiceOverlay();
}

// ─── 语音覆盖层 UI ─────────────────────────────────────────
function showVoiceOverlay(msg) {
  let ov = document.getElementById("longhun-voice-ov");
  if (!ov) {
    ov = document.createElement("div");
    ov.id = "longhun-voice-ov";
    ov.style.cssText = `
      position:fixed;bottom:30px;left:50%;transform:translateX(-50%);
      background:rgba(20,20,20,0.92);color:#fff;padding:14px 24px;
      border-radius:50px;font-family:-apple-system,sans-serif;font-size:14px;
      z-index:2147483647;display:flex;align-items:center;gap:10px;
      box-shadow:0 6px 20px rgba(0,0,0,.4);
    `;
    // 停止按钮
    const stop = document.createElement("button");
    stop.textContent = "■ 停止";
    stop.style.cssText = "background:#D4AF37;border:none;color:#fff;padding:4px 12px;border-radius:20px;cursor:pointer;font-size:12px;";
    stop.onclick = stopVoice;
    ov.appendChild(stop);
    document.body.appendChild(ov);
  }
  ov.firstChild.textContent = msg + " ";
}

function updateVoiceOverlay(msg) {
  const ov = document.getElementById("longhun-voice-ov");
  if (ov) ov.firstChild.textContent = msg + " ";
}

function hideVoiceOverlay() {
  const ov = document.getElementById("longhun-voice-ov");
  if (ov) ov.remove();
}

function showVoiceError(msg) {
  renderResult({ title: "🎙️ 语音错误", color: "🔴", summary: msg, dna: "" });
}

// ─── 消息监听 ──────────────────────────────────────────────
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "LONGHUN_RESULT")      renderResult(msg.data);
  if (msg.type === "LONGHUN_VOICE_START") startVoice();
});
