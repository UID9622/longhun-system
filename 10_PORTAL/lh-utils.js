// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-3392a589
/**
 * 龍魂公共工具库 v1.0
 * #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-LH-UTILS-v1.0-7A3E1F2B
 * 
 * 提供所有页面共用的安全工具函数
 */

// ============================================================
// 1. HTML 转义 — 防止 XSS
// ============================================================
function escHtml(str) {
  if (str == null) return '';
  const s = String(str);
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// 安全设置 innerHTML（仅当 content 已信任时使用）
function safeSetHTML(el, html) {
  if (typeof el === 'string') el = document.querySelector(el);
  if (!el) return;
  el.innerHTML = html;
}

// 安全设置文本内容（总是安全的）
function safeSetText(el, text) {
  if (typeof el === 'string') el = document.querySelector(el);
  if (!el) return;
  el.textContent = text;
}

// ============================================================
// 2. Toast 通知 — 替代 alert()
// ============================================================
function showToast(msg, type) {
  type = type || 'info'; // info | success | warn | error
  // 移除已有 toast
  var existing = document.querySelector('.lh-toast');
  if (existing) existing.remove();

  var toast = document.createElement('div');
  toast.className = 'lh-toast lh-toast-' + type;
  toast.textContent = msg || '';
  toast.style.cssText = [
    'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:99999',
    'padding:12px 28px;border-radius:10px;font-size:15px;font-weight:600',
    'color:#fff;box-shadow:0 4px 20px rgba(0,0,0,0.25);pointer-events:none',
    'animation:lhToastIn 0.3s ease, lhToastOut 0.3s ease 2.4s forwards',
    'max-width:90vw;text-align:center;word-break:break-word',
    type === 'success' ? 'background:#10b981' :
    type === 'error'   ? 'background:#ef4444' :
    type === 'warn'    ? 'background:#f59e0b' :
                         'background:#3b82f6'
  ].join(';');
  document.body.appendChild(toast);

  setTimeout(function() { if (toast.parentNode) toast.remove(); }, 2800);
}

// Toast 样式动画（只注入一次）
(function() {
  if (document.getElementById('lh-toast-style')) return;
  var style = document.createElement('style');
  style.id = 'lh-toast-style';
  style.textContent = [
    '@keyframes lhToastIn  { from{opacity:0;transform:translateX(-50%) translateY(16px)} to{opacity:1;transform:translateX(-50%) translateY(0)} }',
    '@keyframes lhToastOut { from{opacity:1;transform:translateX(-50%) translateY(0)}    to{opacity:0;transform:translateX(-50%) translateY(-8px)} }'
  ].join(' ');
  document.head.appendChild(style);
})();

// ============================================================
// 3. 统一 API 配置 — 替代硬编码 localhost
// ============================================================
var LH_API = {
  // 自动检测：使用当前页面的 host，端口号从常见服务端口列表匹配
  // 也可通过 URL 参数 ?api_base=http://x.x.x.x 覆盖
  get baseURL() {
    if (this._cachedBase) return this._cachedBase;
    var params = new URLSearchParams(location.search);
    var override = params.get('api_base');
    if (override) { this._cachedBase = override.replace(/\/+$/, ''); return this._cachedBase; }
    this._cachedBase = location.protocol + '//' + location.hostname;
    return this._cachedBase;
  },
  _cachedBase: null,
  // 各服务端口映射
  ports: {
     audit:    '9622',
     brain:    '9625',
     identity: '8444',
     persona:  '9001',
     backend:  '8001',
     baobao:   '8002',
     gua:      '9623',
     heart:    '9624',
     kg:       '8088',
     portal:   '8844',
     exp:      '8445',
     ollama:   '11434',
     dsBridge: '8788',
     matrix:   '9627'
  },
  url: function(service, path) {
    var p = this.ports[service] || '';
    return this.baseURL + (p ? ':' + p : '') + (path || '');
  }
};

// 兼容旧代码 — 渐进迁移期间保留旧全局变量引用
var API_BASE = LH_API.baseURL;
