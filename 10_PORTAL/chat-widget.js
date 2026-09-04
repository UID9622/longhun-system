/**
 * 龍魂 AI Chat Widget v2.0
 * DNA: #龍芯⚡️丙午·乙未·丁丑·丙午·䷀乾-CHAT-WIDGET-V2.0-a3b7f0e2
 * 创建者: 诸葛鑫（UID9622）
 * 协议: CC BY-NC-SA 4.0
 * 
 * 自包含悬浮聊天组件 - 引入即用
 * <script src="/chat-widget.js"></script>
 */
(function() {
  'use strict';

  const STYLES = `
.chat-widget *{box-sizing:border-box;margin:0;padding:0}
.chat-widget-bubble{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);border:2px solid #d4a574;cursor:pointer;z-index:99999;display:flex;align-items:center;justify-content:center;transition:all .3s ease;box-shadow:0 4px 20px rgba(212,165,116,.3)}
.chat-widget-bubble:hover{transform:scale(1.08);box-shadow:0 6px 28px rgba(212,165,116,.5)}
.chat-widget-bubble svg{width:28px;height:28px;fill:#d4a574;transition:all .3s}
.chat-widget-bubble .pulse{position:absolute;inset:-6px;border-radius:50%;border:2px solid rgba(212,165,116,.4);animation:bubblePulse 2s infinite}
.chat-widget-bubble .unread-dot{position:absolute;top:2px;right:2px;width:10px;height:10px;border-radius:50%;background:#e74c3c;display:none}
@keyframes bubblePulse{0%{transform:scale(1);opacity:1}70%{transform:scale(1.25);opacity:0}100%{transform:scale(1);opacity:0}}
.chat-widget-panel{position:fixed;bottom:96px;right:24px;width:380px;height:560px;max-height:calc(100vh - 120px);background:linear-gradient(180deg,#1a1a2e 0%,#0f0f23 100%);border:1px solid rgba(212,165,116,.25);border-radius:16px;z-index:99998;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.5);opacity:0;transform:translateY(16px) scale(.95);pointer-events:none;transition:all .3s cubic-bezier(.34,1.56,.64,1)}
.chat-widget-panel.open{opacity:1;transform:translateY(0) scale(1);pointer-events:all}
.chat-widget-header{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid rgba(212,165,116,.15);flex-shrink:0}
.chat-widget-header .avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#d4a574,#b8854a);display:flex;align-items:center;justify-content:center;font-size:18px;color:#1a1a2e;font-weight:700}
.chat-widget-header .info{flex:1;min-width:0}
.chat-widget-header .name{font-size:14px;font-weight:600;color:#f0e6d8}
.chat-widget-header .status{font-size:11px;color:#d4a574;display:flex;align-items:center;gap:4px}
.chat-widget-header .status::before{content:'';width:6px;height:6px;border-radius:50%;background:#27ae60;display:inline-block;animation:statusPulse 2s infinite}
@keyframes statusPulse{0%,100%{opacity:1}50%{opacity:.4}}
.chat-widget-header .close-btn{width:30px;height:30px;border-radius:50%;border:none;background:rgba(255,255,255,.05);color:#a09080;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:all .2s}
.chat-widget-header .close-btn:hover{background:rgba(255,255,255,.1);color:#f0e6d8}
.chat-widget-body{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:8px}
.chat-widget-body::-webkit-scrollbar{width:4px}
.chat-widget-body::-webkit-scrollbar-thumb{background:rgba(212,165,116,.2);border-radius:2px}
.chat-widget-msg{max-width:85%;padding:10px 14px;border-radius:14px;font-size:13px;line-height:1.55;word-break:break-word;animation:msgIn .3s ease}
@keyframes msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.chat-widget-msg.user{align-self:flex-end;background:rgba(212,165,116,.15);color:#f0e6d8;border-bottom-right-radius:4px}
.chat-widget-msg.ai{align-self:flex-start;background:rgba(255,255,255,.04);color:#d4c8b8;border-bottom-left-radius:4px}
.chat-widget-msg .time{font-size:10px;color:rgba(255,255,255,.3);margin-top:4px;text-align:right}
.chat-widget-msg.typing{color:rgba(255,255,255,.4);font-style:italic}
.chat-widget-msg.typing .dot-flash{display:inline-block;animation:dotBounce 1.4s infinite}
.chat-widget-msg.typing .dot-flash:nth-child(2){animation-delay:.2s}
.chat-widget-msg.typing .dot-flash:nth-child(3){animation-delay:.4s}
@keyframes dotBounce{0%,80%,100%{opacity:.2}40%{opacity:1}}
.chat-widget-footer{display:flex;align-items:center;gap:8px;padding:12px 16px;border-top:1px solid rgba(212,165,116,.15);flex-shrink:0}
.chat-widget-footer textarea{flex:1;min-height:38px;max-height:100px;padding:9px 14px;border-radius:20px;border:1px solid rgba(212,165,116,.2);background:rgba(255,255,255,.04);color:#f0e6d8;font-size:13px;resize:none;outline:none;font-family:inherit;line-height:1.4;transition:border-color .2s}
.chat-widget-footer textarea:focus{border-color:rgba(212,165,116,.5)}
.chat-widget-footer textarea::placeholder{color:rgba(255,255,255,.25)}
.chat-widget-footer .send-btn{width:38px;height:38px;min-width:38px;border-radius:50%;border:none;background:linear-gradient(135deg,#d4a574,#b8854a);color:#1a1a2e;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all .2s}
.chat-widget-footer .send-btn:hover{transform:scale(1.05);box-shadow:0 2px 12px rgba(212,165,116,.4)}
.chat-widget-footer .send-btn:disabled{opacity:.4;cursor:not-allowed;transform:none}
.chat-widget-footer .brand{font-size:10px;color:rgba(255,255,255,.15);flex-shrink:0;padding-right:4px}
@media(max-width:460px){.chat-widget-panel{width:calc(100vw - 32px);right:16px;bottom:88px;border-radius:12px}}
@media(max-width:380px){.chat-widget-panel{height:480px}}
  `;

  const API = '/api/v1/li/chat';
  const MAX_HISTORY = 50;
  const TYPING_MS = 1200;

  function h(messages) {
    return `\n<div class="chat-widget-body">
      ${messages.map(m => `
        <div class="chat-widget-msg ${m.role}">
          <div>${escapeHtml(m.content)}</div>
          ${m.time ? `<div class="time">${m.time}</div>` : ''}
        </div>
      `).join('')}
    </div>`;
  }

  function escapeHtml(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML.replace(/\n/g, '<br>');
  }

  function render() {
    const p = document.querySelector('.chat-widget-panel');
    if (!p) return;
    const oldBody = p.querySelector('.chat-widget-body');
    const newBody = document.createElement('div');
    newBody.innerHTML = h(chat.history).trim();
    if (oldBody) oldBody.replaceWith(newBody.firstElementChild);
    const body = p.querySelector('.chat-widget-body');
    if (body) body.scrollTop = body.scrollHeight;
  }

  function addTyping() {
    chat.history.push({ role: 'ai', content: '<span class="dot-flash">.</span><span class="dot-flash">.</span><span class="dot-flash">.</span>', className: 'typing' });
    render();
    const body = document.querySelector('.chat-widget-body');
    if (body) body.scrollTop = body.scrollHeight;
  }

  function removeTyping() {
    const idx = chat.history.findIndex(m => m.className === 'typing');
    if (idx >= 0) chat.history.splice(idx, 1);
  }

  function now() {
    const d = new Date();
    return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
  }

  function saveHistory() {
    try {
      sessionStorage.setItem('lh_chat_history', JSON.stringify(chat.history.slice(-MAX_HISTORY)));
    } catch(e) {}
  }

  function loadHistory() {
    try {
      const raw = sessionStorage.getItem('lh_chat_history');
      return raw ? JSON.parse(raw) : [];
    } catch(e) { return []; }
  }

  async function sendMessage(msg) {
    if (chat.loading || !msg.trim()) return;
    chat.loading = true;
    updateSendBtn(true);

    chat.history.push({ role: 'user', content: msg, time: now() });
    render();
    saveHistory();

    addTyping();

    try {
      const res = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      removeTyping();
      chat.history.push({ role: 'ai', content: data.reply || '收到，请再试一次。', time: now(), dna: data.dna });
    } catch(e) {
      removeTyping();
      chat.history.push({ role: 'ai', content: '龍魂引擎暂时无法连接。请稍后重试，或直接联系 UID9622。', time: now() });
    }

    render();
    saveHistory();
    chat.loading = false;
    updateSendBtn(false);
  }

  function updateSendBtn(disabled) {
    const btn = document.querySelector('.chat-widget-footer .send-btn');
    if (btn) btn.disabled = disabled;
  }

  function buildHTML() {
    return `
<div class="chat-widget-bubble" id="cwBubble" title="和龍魂对话">
  <div class="pulse"></div>
  <div class="unread-dot" id="cwUnread"></div>
  <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/><circle cx="9" cy="10" r="1.5"/><circle cx="15" cy="10" r="1.5"/></svg>
</div>
<div class="chat-widget-panel" id="cwPanel">
  <div class="chat-widget-header">
    <div class="avatar">龍</div>
    <div class="info">
      <div class="name">龍魂 AI</div>
      <div class="status">在线·为人民服务</div>
    </div>
    <button class="close-btn" id="cwClose" title="关闭">×</button>
  </div>
  <div class="chat-widget-body">
    <div class="chat-widget-msg ai">
      <div>你好！我是龍魂 AI 助手 👋<br><br>我能帮你：<br>· 了解龍魂系统<br>· 回答技术问题<br>· 知识查询<br><br>直接问我吧～</div>
    </div>
  </div>
  <div class="chat-widget-footer">
    <span class="brand">龍魂</span>
    <textarea id="cwInput" placeholder="输入消息..." rows="1" maxlength="1000"></textarea>
    <button class="send-btn" id="cwSend" title="发送">➤</button>
  </div>
</div>`;
  }

  function bindEvents() {
    const bubble = document.getElementById('cwBubble');
    const panel = document.getElementById('cwPanel');
    const closeBtn = document.getElementById('cwClose');
    const input = document.getElementById('cwInput');
    const sendBtn = document.getElementById('cwSend');

    let wasClosedByUser = false;

    bubble.addEventListener('click', () => {
      chat.open = !chat.open;
      wasClosedByUser = !chat.open;
      panel.classList.toggle('open', chat.open);
      if (chat.open) {
        bubble.style.opacity = '0';
        bubble.style.pointerEvents = 'none';
        input.focus();
        render();
      } else {
        bubble.style.opacity = '1';
        bubble.style.pointerEvents = 'all';
      }
    });

    closeBtn.addEventListener('click', () => {
      chat.open = false;
      wasClosedByUser = true;
      panel.classList.remove('open');
      bubble.style.opacity = '1';
      bubble.style.pointerEvents = 'all';
    });

    function doSend() {
      const msg = input.value.trim();
      if (!msg) return;
      input.value = '';
      input.style.height = 'auto';
      sendMessage(msg);
    }

    sendBtn.addEventListener('click', doSend);

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        doSend();
      }
    });

    input.addEventListener('input', () => {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 100) + 'px';
    });

    // Click outside to close
    document.addEventListener('click', (e) => {
      if (chat.open && !wasClosedByUser) {
        const isInside = panel.contains(e.target) || bubble.contains(e.target);
        if (!isInside) {
          chat.open = false;
          panel.classList.remove('open');
          bubble.style.opacity = '1';
          bubble.style.pointerEvents = 'all';
        }
      }
      wasClosedByUser = false;
    });
  }

  const chat = {
    open: false,
    loading: false,
    history: loadHistory()
  };

  // Inject
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    if (document.getElementById('cwPanel')) return; // Already initialized

    const style = document.createElement('style');
    style.textContent = STYLES;
    document.head.appendChild(style);

    const wrap = document.createElement('div');
    wrap.className = 'chat-widget';
    wrap.innerHTML = buildHTML();
    document.body.appendChild(wrap);

    bindEvents();

    // Open from URL hash
    if (window.location.hash === '#chat') {
      setTimeout(() => {
        document.getElementById('cwBubble').click();
      }, 500);
    }
  }
})();
