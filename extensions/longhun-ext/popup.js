// 龍魂9622·popup.js v2.0
// DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-POPUP-v2.0-3c8a5e2b
// 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 深度集成: longhun-system/extensions/longhun-ext (2026-09-04)

const ENGINE = "http://127.0.0.1:9622";
let isRecording = false;
let recognition = null;

// ─── 引擎健康检查 ──────────────────────────────────────────
async function checkEngine() {
  const pill = document.getElementById("status-pill");
  try {
    const r = await fetch(ENGINE + "/api/health", { signal: AbortSignal.timeout(2000) });
    const d = await r.json();
    pill.textContent = `🟢 ${d.version || "在线"}`;
    pill.className = "status-pill online";
  } catch {
    pill.textContent = "🔴 引擎离线";
    pill.className = "status-pill offline";
  }
}

// ─── 标签页切换 ────────────────────────────────────────────
document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(`panel-${tab.dataset.tab}`).classList.add("active");
  });
});

// ─── 工具按钮 ──────────────────────────────────────────────
document.querySelectorAll(".btn[data-ep]").forEach(btn => {
  btn.addEventListener("click", async () => {
    const text = document.getElementById("tool-input").value.trim();
    const ep = btn.dataset.ep;
    const resultBox = document.getElementById("tool-result");

    btn.textContent = "⏳ 处理中...";
    btn.disabled = true;
    resultBox.textContent = "正在调用9622引擎...";

    try {
      const res = await callEngine(ep, { text, lang: "zh" });
      resultBox.innerHTML = `<strong>${res.title || "结果"}</strong>\n\n${escHtml(String(res.summary || ""))}\n\n<span class="dna">${escHtml(res.dna || "")}</span>`;
    } catch (e) {
      resultBox.textContent = `❌ 引擎离线：${e.message}\n请运行：\npython3 ~/longhun-engine/main.py`;
    } finally {
      // 恢复按钮文字（从原始label映射）
      const labels = {
        "/api/ethics/review":    "⚖️ 伦理审查",
        "/api/tongxin/translate":"🟡 通心译",
        "/api/wuxing/analyze":   "🔥 五行分析",
        "/api/cnsh/align":       "📐 CNSH语法",
        "/api/errata/submit":    "📓 记错本",
        "/api/dna/check":        "🧬 DNA验证",
      };
      btn.textContent = labels[ep] || ep;
      btn.disabled = false;
    }
  });
});

// ─── 语音输入 ──────────────────────────────────────────────
const btnVoice = document.getElementById("btn-voice");
const btnStop  = document.getElementById("btn-stop-voice");

btnVoice.addEventListener("click", startVoice);
btnStop.addEventListener("click",  stopVoice);

function startVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    document.getElementById("tool-result").textContent =
      "❌ 此浏览器不支持语音\n请用 Safari 14.1+ 或 Chrome";
    return;
  }

  recognition = new SR();
  recognition.lang = "zh-CN";
  recognition.interimResults = true;
  recognition.continuous = false;

  recognition.onstart = () => {
    isRecording = true;
    btnVoice.classList.add("recording");
    btnVoice.textContent = "🔴 录音中...";
    btnStop.style.display = "inline-block";
  };

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    document.getElementById("tool-input").value = transcript;
    if (event.results[event.results.length - 1].isFinal) {
      stopVoice();
    }
  };

  recognition.onerror = (e) => {
    stopVoice();
    document.getElementById("tool-result").textContent = `语音错误：${e.error}`;
  };

  recognition.onend = () => stopVoice();
  recognition.start();
}

function stopVoice() {
  if (recognition) { try { recognition.stop(); } catch {}; recognition = null; }
  isRecording = false;
  btnVoice.classList.remove("recording");
  btnVoice.textContent = "🎙️ 语音输入（中文）";
  btnStop.style.display = "none";
}

// ─── 对话面板 ──────────────────────────────────────────────
document.getElementById("chat-send").addEventListener("click", sendChat);
document.getElementById("chat-input").addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendChat(); }
});

async function sendChat() {
  const input = document.getElementById("chat-input");
  const msgs  = document.getElementById("chat-msgs");
  const mode  = document.getElementById("chat-mode").value;
  const text  = input.value.trim();
  if (!text) return;

  appendMsg("user", "您", text, msgs);
  input.value = "";

  const thinking = appendMsg("ai", "🐉 龍魂", "思考中...", msgs);

  try {
    const res = await callEngine("/api/chat", { text, mode, lang: "zh" });
    thinking.querySelector(".body").textContent = res.reply || res.summary || JSON.stringify(res);
  } catch (e) {
    thinking.querySelector(".body").textContent = `引擎离线：${e.message}`;
  }
  msgs.scrollTop = msgs.scrollHeight;
}

function appendMsg(role, label, body, container) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.innerHTML = `<div class="role">${escHtml(label)}</div><div class="body">${escHtml(body)}</div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

// ─── MCP工具面板 ───────────────────────────────────────────
document.getElementById("btn-mcp-refresh").addEventListener("click", loadMcpTools);

async function loadMcpTools() {
  const list = document.getElementById("mcp-tool-list");
  list.innerHTML = '<div style="color:#aaa;font-size:12px;padding:8px;">加载中...</div>';
  try {
    const res = await callEngine("/api/mcp/list", {});
    const tools = res.tools || [];
    if (!tools.length) {
      list.innerHTML = '<div style="color:#aaa;font-size:12px;padding:8px;">暂无MCP工具</div>';
      return;
    }
    list.innerHTML = tools.map(t => `
      <div class="tool-item" data-tool="${escHtml(t.name || t)}">
        <span class="icon">🔧</span>
        <div>
          <div class="name">${escHtml(t.name || t)}</div>
          <div class="desc">${escHtml(t.desc || t.description || "")}</div>
        </div>
      </div>
    `).join("");

    list.querySelectorAll(".tool-item").forEach(item => {
      item.addEventListener("click", async () => {
        const toolName = item.dataset.tool;
        const arg = prompt(`调用 ${toolName} 的参数（JSON格式，可留空）：`);
        let args = {};
        try { if (arg) args = JSON.parse(arg); } catch {}
        try {
          const res = await callEngine("/api/mcp/call", { tool: toolName, args });
          alert(JSON.stringify(res, null, 2).slice(0, 500));
        } catch (e) {
          alert("调用失败：" + e.message);
        }
      });
    });
  } catch {
    list.innerHTML = '<div style="color:#c33;font-size:12px;padding:8px;">❌ 引擎离线，无法加载MCP工具</div>';
  }
}

// ─── 苹果面板按钮 ──────────────────────────────────────────
document.getElementById("btn-dl-shortcut").addEventListener("click", () => {
  // 在真实部署中这里提供捷径文件下载
  alert("iOS 捷径文件将从 http://127.0.0.1:9622/static/longhun.shortcut 下载\n\n请先确保9622引擎在线");
});

document.getElementById("btn-safari-guide").addEventListener("click", () => {
  // 打开Safari扩展打包说明
  chrome.tabs.create({ url: "http://127.0.0.1:9622/docs/safari-guide" });
});

// ─── 工具函数 ──────────────────────────────────────────────
async function callEngine(endpoint, payload) {
  const res = await fetch(ENGINE + endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(15000)
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

function escHtml(str) {
  return String(str)
    .replace(/&/g,"&amp;")
    .replace(/</g,"&lt;")
    .replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;");
}

// ─── 初始化 ────────────────────────────────────────────────
checkEngine();
loadMcpTools();

// 读取上次结果
chrome.storage.local.get(["lastResult"], data => {
  if (data.lastResult) {
    const r = data.lastResult;
    document.getElementById("tool-result").innerHTML =
      `<strong>${r.title || "上次结果"}</strong>\n\n${escHtml(String(r.summary || ""))}\n\n<span class="dna">${escHtml(r.dna || "")}</span>`;
  }
});
