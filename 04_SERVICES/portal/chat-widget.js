// ═══════════════════════════════════════════════
// DNA: #龍芯⚡️2026-07-22-CHAT-WIDGET-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0
// 职能: 官网 AI 聊天悬浮组件
// ═══════════════════════════════════════════════

(function () {
  "use strict";

  const API_URL = "/api/v1/li/chat";
  const CSS_ID = "lh-chat-styles";
  const ROOT_ID = "lh-chat-root";

  // ── 样式 ──────────────────────────────────
  const STYLES = `
    #${ROOT_ID} { position:fixed; bottom:24px; right:24px; z-index:99999; font-family:"PingFang SC","Microsoft YaHei",sans-serif; }
    .lh-chat-btn { width:56px; height:56px; border-radius:50%; background:#1a1a2e; border:2px solid #c9a84c; color:#c9a84c; font-size:22px; cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 20px rgba(201,168,76,0.25); transition:all .3s; }
    .lh-chat-btn:hover { background:#c9a84c; color:#1a1a2e; transform:scale(1.08); box-shadow:0 6px 28px rgba(201,168,76,0.4); }
    .lh-chat-panel { position:absolute; bottom:72px; right:0; width:380px; max-height:520px; background:#1a1a2e; border:1px solid #333; border-radius:16px; display:flex; flex-direction:column; overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,.6); transition:all .35s cubic-bezier(.4,0,.2,1); transform-origin:bottom right; }
    .lh-chat-panel:not(.open) { transform:scale(0); opacity:0; pointer-events:none; }
    .lh-chat-panel.open { transform:scale(1); opacity:1; }
    .lh-chat-header { padding:14px 18px; border-bottom:1px solid #333; display:flex; align-items:center; justify-content:space-between; background:linear-gradient(135deg,#1a1a2e,#2d1f1a); }
    .lh-chat-header h4 { margin:0; color:#c9a84c; font-size:15px; font-weight:600; }
    .lh-chat-header small { color:#888; font-size:11px; display:block; }
    .lh-chat-close { background:none; border:none; color:#888; font-size:20px; cursor:pointer; padding:2px 6px; border-radius:6px; transition:.2s; }
    .lh-chat-close:hover { color:#e74c3c; background:rgba(231,76,60,.15); }
    .lh-chat-body { flex:1; overflow-y:auto; padding:14px 16px; display:flex; flex-direction:column; gap:10px; }
    .lh-chat-body::-webkit-scrollbar { width:4px; }
    .lh-chat-body::-webkit-scrollbar-thumb { background:#333; border-radius:2px; }
    .lh-msg { max-width:85%; padding:10px 14px; border-radius:14px; font-size:14px; line-height:1.55; word-break:break-word; }
    .lh-msg.assistant { align-self:flex-start; background:#2a2a3e; color:#e0e0e0; border-bottom-left-radius:4px; }
    .lh-msg.user { align-self:flex-end; background:linear-gradient(135deg,#8b6914,#b8960c); color:#fff; border-bottom-right-radius:4px; }
    .lh-msg.info { align-self:center; background:transparent; color:#888; font-size:12px; max-width:100%; text-align:center; }
    .lh-chat-footer { padding:10px 12px; border-top:1px solid #333; display:flex; gap:8px; align-items:center; }
    .lh-chat-input { flex:1; background:#111; border:1px solid #333; border-radius:20px; padding:10px 16px; color:#e0e0e0; font-size:14px; outline:none; transition:border-color .3s; }
    .lh-chat-input:focus { border-color:#c9a84c; }
    .lh-chat-input::placeholder { color:#555; }
    .lh-chat-send { width:40px; height:40px; border-radius:50%; background:#c9a84c; border:none; color:#1a1a2e; font-size:18px; cursor:pointer; flex-shrink:0; transition:all .3s; display:flex; align-items:center; justify-content:center; }
    .lh-chat-send:hover { background:#d4b45e; transform:scale(1.05); }
    .lh-chat-send:disabled { background:#444; color:#888; cursor:not-allowed; transform:none; }
    .lh-typing { display:flex; gap:4px; padding:14px; }
    .lh-typing span { width:8px; height:8px; background:#c9a84c; border-radius:50%; animation:lh-bounce 1.4s infinite ease-in-out; }
    .lh-typing span:nth-child(2) { animation-delay:.16s; }
    .lh-typing span:nth-child(3) { animation-delay:.32s; }
    @keyframes lh-bounce { 0%,80%,100% { transform:scale(.6); opacity:.4; } 40% { transform:scale(1); opacity:1; } }
    @media (max-width:480px) {
      .lh-chat-panel { width:calc(100vw-40px); right:-8px; bottom:68px; max-height:420px; }
    }
  `;

  // ── HTML ──────────────────────────────────
  const HTML = `
    <button class="lh-chat-btn" aria-label="AI 对话">龍</button>
    <div class="lh-chat-panel">
      <div class="lh-chat-header">
        <div><h4>龍魂 AI 助手</h4><small>uid9622.cn · 本地AI引擎</small></div>
        <button class="lh-chat-close" aria-label="关闭">×</button>
      </div>
      <div class="lh-chat-body">
        <div class="lh-msg info">你好，我是龍魂系统AI助手。有什么可以帮你的？</div>
      </div>
      <div class="lh-chat-footer">
        <input class="lh-chat-input" placeholder="输入消息..." type="text" />
        <button class="lh-chat-send" aria-label="发送">➤</button>
      </div>
    </div>
  `;

  // ── 初始化 ────────────────────────────────
  let open = false;
  let sending = false;

  function inject() {
    const style = document.createElement("style");
    style.id = CSS_ID;
    style.textContent = STYLES;
    document.head.appendChild(style);

    const root = document.createElement("div");
    root.id = ROOT_ID;
    root.innerHTML = HTML;
    document.body.appendChild(root);

    bind();
  }

  function bind() {
    const root = document.getElementById(ROOT_ID);
    if (!root) return;
    const btn = root.querySelector(".lh-chat-btn");
    const close = root.querySelector(".lh-chat-close");
    const panel = root.querySelector(".lh-chat-panel");
    const input = root.querySelector(".lh-chat-input");
    const send = root.querySelector(".lh-chat-send");
    const body = root.querySelector(".lh-chat-body");

    const toggle = () => {
      open = !open;
      panel.classList.toggle("open", open);
      if (open) setTimeout(() => input.focus(), 350);
    };

    btn.addEventListener("click", toggle);
    close.addEventListener("click", toggle);

    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        send.click();
      }
    });

    send.addEventListener("click", async () => {
      const text = input.value.trim();
      if (!text || sending) return;
      sending = true;
      send.disabled = true;
      input.value = "";

      addMsg(body, "user", text);
      const typing = showTyping(body);

      try {
        const r = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text }),
        });
        const d = await r.json();
        typing.remove();
        addMsg(body, "assistant", d.reply || "（无回复）");
      } catch (err) {
        typing.remove();
        addMsg(body, "assistant", "连接失败...龍魂引擎可能暂时离线。请稍后再试。");
      }
      sending = false;
      send.disabled = false;
      input.focus();
      scrollBottom(body);
    });
  }

  function addMsg(body, role, text) {
    const div = document.createElement("div");
    div.className = `lh-msg ${role}`;
    div.textContent = text;
    body.appendChild(div);
    scrollBottom(body);
  }

  function showTyping(body) {
    const div = document.createElement("div");
    div.classList.add("lh-msg", "assistant");
    div.innerHTML = '<div class="lh-typing"><span></span><span></span><span></span></div>';
    body.appendChild(div);
    scrollBottom(body);
    return div;
  }

  function scrollBottom(el) {
    setTimeout(() => { el.scrollTop = el.scrollHeight; }, 50);
  }

  // ── 启动 ──────────────────────────────────
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
