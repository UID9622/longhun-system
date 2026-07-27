// ============================================================
// DNA: #龍芯⚡️丙午·乙未·丁酉·子时·☰乾-GUANLAN-BACKGROUND-v1.0-bg7fa2d1
// 创建者: 诸葛鑫 (UID9622)
// 协议: CC BY-NC-SA 4.0
// ============================================================
// 龍魂 · 观澜主权网关 — Background Service Worker
// 四大职责: AI检测 | 请求拦截 | 隐私扫描 | 断路器
// ============================================================

const GUANLAN_API = 'http://127.0.0.1:8770';

// ============================================================
// 状态管理
// ============================================================
const State = {
  enabled: true,
  activeAI: new Map(),       // 当前活跃AI: url -> {name, type, permissions, startTime}
  blockedRequests: [],       // 被拦截的请求记录
  privacyScore: {},          // 每个tab的隐私评分
  circuitBreaker: {
    locked: false,
    lockUntil: 0,
    failures: {},
    violations: {},
    anomalyFreq: {}
  }
};

// ============================================================
// 初始化
// ============================================================
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    guanlan_enabled: true,
    ai_whitelist: [],
    privacy_alert_threshold: 70,
    circuit_breaker_enabled: true,
    circuit_breaker_cooldown: 600
  });
  syncToAPI('status', { action: 'installed', timestamp: Date.now() });
  console.log('[观澜] 主权网关已安装，开始守卫。');
});

chrome.runtime.onStartup.addListener(async () => {
  const config = await chrome.storage.local.get(['guanlan_enabled']);
  State.enabled = config.guanlan_enabled !== false;
  syncToAPI('status', { action: 'startup', timestamp: Date.now() });
});

// ============================================================
// 天条一: 所有AI请求必须经过观澜网关
// ============================================================
chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    if (!State.enabled) return { cancel: false };

    const url = details.url;
    const tabId = details.tabId;

    // 检查断路器
    if (isCircuitBroken(url)) {
      logBlocked(details, 'circuit_breaker');
      return { cancel: false }; // 记录但不阻断（由断路器决定）
    }

    // 检测是否为AI相关请求
    const aiCheck = detectAIRequest(url, details);
    if (aiCheck.isAI) {
      // 检查白名单
      if (!isWhitelisted(url)) {
        // 触发用户确认流程
        triggerAIAlert(tabId, {
          aiName: aiCheck.name,
          aiType: aiCheck.type,
          url: url,
          method: details.method,
          requestId: details.requestId
        });
      }

      // 记录到审计账本
      recordAudit({
        type: 'ai_request',
        url: url,
        method: details.method,
        aiInfo: aiCheck,
        tabId: tabId,
        timestamp: Date.now()
      });
    }

    // 检测隐私泄露
    scanForPrivacyLeak(details);

    return { cancel: false };
  },
  { urls: ["<all_urls>"] },
  ["blocking", "requestBody"]
);

// ============================================================
// AI检测引擎
// ============================================================
function detectAIRequest(url, details) {
  const AI_DOMAINS = new Set([
    'api.openai.com', 'api.anthropic.com', 'api.deepseek.com',
    'api.moonshot.cn', 'api.baichuan-ai.com', 'api.zhipuai.cn',
    'api.minimax.chat', 'api.stepfun.com', 'dashscope.aliyuncs.com',
    'hunyuan.tencentcloudapi.com', 'generativelanguage.googleapis.com',
    'api.coze.cn', 'api.coze.com', 'api.302.ai',
    'api.siliconflow.cn', 'api.groq.com', 'api.mistral.ai',
    'api.together.xyz', 'api.perplexity.ai', 'api.phind.com'
  ]);

  const AI_PATH_PATTERNS = [
    /\/v1\/chat\/completions/,
    /\/v1\/completions/,
    /\/v1\/embeddings/,
    /\/v1\/images\/generations/,
    /\/api\/chat/,
    /\/api\/generate/,
    /\/generateContent/,
    /\/streamGenerateContent/,
    /\/workflows\/run/,
  ];

  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname;

    // 域名匹配
    if (AI_DOMAINS.has(hostname)) {
      return { isAI: true, name: mapAIDomain(hostname), type: 'openai_compatible' };
    }

    // 路径匹配
    for (const pattern of AI_PATH_PATTERNS) {
      if (pattern.test(urlObj.pathname)) {
        return { isAI: true, name: hostname, type: 'api_endpoint' };
      }
    }

    // 检测请求头中的AI标记
    if (details.requestHeaders) {
      for (const header of details.requestHeaders) {
        if (header.name.toLowerCase() === 'x-ai-provider' ||
            header.name.toLowerCase() === 'x-ai-model') {
          return { isAI: true, name: header.value, type: 'header_detected' };
        }
      }
    }

    return { isAI: false, name: '', type: '' };
  } catch {
    return { isAI: false, name: '', type: '' };
  }
}

function mapAIDomain(domain) {
  const map = {
    'api.openai.com': 'OpenAI',
    'api.anthropic.com': 'Anthropic Claude',
    'api.deepseek.com': 'DeepSeek',
    'api.moonshot.cn': 'Moonshot/Kimi',
    'api.zhipuai.cn': '智谱 ChatGLM',
    'api.minimax.chat': 'MiniMax',
    'dashscope.aliyuncs.com': '通义千问',
    'hunyuan.tencentcloudapi.com': '腾讯混元',
    'generativelanguage.googleapis.com': 'Google Gemini',
    'api.baichuan-ai.com': '百川智能',
    'api.stepfun.com': '阶跃星辰',
    'api.siliconflow.cn': 'SiliconFlow',
    'api.groq.com': 'Groq',
    'api.mistral.ai': 'Mistral AI',
    'api.together.xyz': 'Together AI',
    'api.perplexity.ai': 'Perplexity',
    'api.coze.cn': 'Coze/扣子',
    'api.coze.com': 'Coze',
    'api.302.ai': '302.AI',
    'api.phind.com': 'Phind'
  };
  return map[domain] || domain;
}

// ============================================================
// 隐私扫描器
// ============================================================
function scanForPrivacyLeak(details) {
  const url = details.url;

  // 检测第三方Cookie
  if (details.requestHeaders) {
    const cookieHeader = details.requestHeaders.find(h => h.name.toLowerCase() === 'cookie');
    if (cookieHeader) {
      recordLeakEvent('third_party_cookie', url);
    }
  }

  // 检测已知追踪域名
  const TRACKING_DOMAINS = [
    'doubleclick.net', 'google-analytics.com', 'googletagmanager.com',
    'facebook.com/tr', 'bat.bing.com', 'ad.doubleclick.net',
    'analytics.twitter.com', 'ads.linkedin.com', 'pixel.quantserve.com'
  ];
  for (const td of TRACKING_DOMAINS) {
    if (url.includes(td)) {
      recordLeakEvent('tracking_domain', url, td);
      break;
    }
  }

  // 向本地API报告
  syncToAPI('privacy_scan', {
    url: url,
    method: details.method,
    tabId: details.tabId,
    timestamp: Date.now()
  });
}

function recordLeakEvent(type, url, detail = '') {
  const event = { type, url, detail, timestamp: Date.now() };
  chrome.storage.local.get(['privacy_events'], (result) => {
    const events = result.privacy_events || [];
    events.push(event);
    // 只保留最近1000条
    if (events.length > 1000) events.shift();
    chrome.storage.local.set({ privacy_events: events });
  });
}

// ============================================================
// 白名单管理
// ============================================================
async function isWhitelisted(url) {
  const config = await chrome.storage.local.get(['ai_whitelist']);
  const whitelist = config.ai_whitelist || [];
  return whitelist.some(entry => url.includes(entry));
}

// ============================================================
// 天条三: AI自报家门 — 记录所有AI
// ============================================================
function triggerAIAlert(tabId, aiInfo) {
  // 实时弹窗通知
  chrome.notifications.create(`ai-${aiInfo.requestId}`, {
    type: 'basic',
    iconUrl: 'icons/icon48.png',
    title: '⚡ AI请求检测',
    message: `${aiInfo.aiName || '未知AI'} 正在请求访问数据\nURL: ${aiInfo.url.substring(0, 80)}... \n点击查看详情`,
    priority: 2,
    buttons: [{ title: '查看详情 →' }]
  });

  // 更新活跃AI列表
  State.activeAI.set(aiInfo.url, {
    name: aiInfo.aiName,
    type: aiInfo.aiType,
    url: aiInfo.url,
    startTime: Date.now(),
    tabId: tabId
  });

  // 同步到API
  syncToAPI('ai_alert', aiInfo);
}

// ============================================================
// 审计账本
// ============================================================
function recordAudit(event) {
  const auditKey = `audit_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
  chrome.storage.local.get(['audit_log'], (result) => {
    const log = result.audit_log || [];
    log.push({ ...event, dna: generateDNA() });
    if (log.length > 5000) log.splice(0, log.length - 5000);
    chrome.storage.local.set({ audit_log: log });
    syncToAPI('audit', event);
  });
}

function logBlocked(details, reason) {
  State.blockedRequests.push({
    url: details.url,
    method: details.method,
    reason: reason,
    timestamp: Date.now()
  });
  if (State.blockedRequests.length > 100) State.blockedRequests.shift();
}

function generateDNA() {
  const now = new Date();
  const hash = Math.random().toString(36).substring(2, 10);
  const stems = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
  const branches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  const s = stems[now.getHours() % 10];
  const b = branches[(now.getHours() + 2) % 12];
  return `#龍芯⚡️${s}${b}-GUANLAN-AUDIT-${hash}`;
}

// ============================================================
// 天条五: 断路器
// ============================================================
function isCircuitBroken(url) {
  if (State.circuitBreaker.locked) {
    if (Date.now() < State.circuitBreaker.lockUntil) {
      return true;
    } else {
      // 自动解锁
      State.circuitBreaker.locked = false;
      console.log('[观澜] 断路器自动解锁');
    }
  }
  return false;
}

function tripCircuitBreaker(reason, url) {
  const cooldown = 600000; // 600秒
  State.circuitBreaker.locked = true;
  State.circuitBreaker.lockUntil = Date.now() + cooldown;

  chrome.notifications.create('breaker-trip', {
    type: 'basic',
    iconUrl: 'icons/icon48.png',
    title: '🚨 断路器已熔断',
    message: `原因: ${reason}\n锁定至: ${new Date(State.circuitBreaker.lockUntil).toLocaleString()}\n点击手动解锁`,
    priority: 2
  });

  syncToAPI('circuit_break', {
    reason: reason,
    url: url,
    lockUntil: State.circuitBreaker.lockUntil,
    timestamp: Date.now()
  });
}

function recordFailure(url) {
  State.circuitBreaker.failures[url] = (State.circuitBreaker.failures[url] || 0) + 1;
  if (State.circuitBreaker.failures[url] >= 3) {
    tripCircuitBreaker(`连续3次失败: ${url}`, url);
  }
}

function unlockCircuitBreaker() {
  State.circuitBreaker.locked = false;
  State.circuitBreaker.lockUntil = 0;
  State.circuitBreaker.failures = {};
  State.circuitBreaker.violations = {};
  State.circuitBreaker.anomalyFreq = {};
  console.log('[观澜] 断路器已手动解锁');
}

// ============================================================
// 与本地API同步
// ============================================================
function syncToAPI(endpoint, data) {
  fetch(`${GUANLAN_API}/api/v1/guanlan/${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).catch(err => {
    // 静默失败，本地API可能未启动
  });
}

// ============================================================
// 消息处理
// ============================================================
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.action) {
    case 'getStatus':
      sendResponse({
        enabled: State.enabled,
        activeAI: Array.from(State.activeAI.values()),
        blockedCount: State.blockedRequests.length,
        circuitBreaker: {
          locked: State.circuitBreaker.locked,
          lockUntil: State.circuitBreaker.lockUntil
        }
      });
      break;

    case 'toggleEnabled':
      State.enabled = message.value;
      chrome.storage.local.set({ guanlan_enabled: message.value });
      sendResponse({ success: true });
      break;

    case 'toggleBreaker':
      if (message.lock) {
        tripCircuitBreaker(`用户手动熔断: ${message.reason || '手动操作'}`, 'manual');
      } else {
        unlockCircuitBreaker();
      }
      sendResponse({ success: true });
      break;

    case 'whitelistAI':
      chrome.storage.local.get(['ai_whitelist'], (result) => {
        const wl = result.ai_whitelist || [];
        if (!wl.includes(message.url)) {
          wl.push(message.url);
          chrome.storage.local.set({ ai_whitelist: wl });
        }
        sendResponse({ success: true });
      });
      return true; // 异步

    case 'blockAI':
      tripCircuitBreaker(`用户手动阻断: ${message.url}`, message.url);
      sendResponse({ success: true });
      break;

    case 'injectDetection':
      if (message.tabId) {
        chrome.scripting.executeScript({
          target: { tabId: message.tabId },
          files: ['content.js']
        });
      }
      break;

    default:
      sendResponse({ error: 'unknown action' });
  }
  return false;
});

// ============================================================
// 定时任务：清理过期数据
// ============================================================
chrome.alarms.create('cleanup', { periodInMinutes: 5 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'cleanup') {
    // 清理过期AI连接 (>30分钟无活动)
    const now = Date.now();
    const THIRTY_MIN = 30 * 60 * 1000;
    for (const [url, info] of State.activeAI.entries()) {
      if (now - info.startTime > THIRTY_MIN) {
        State.activeAI.delete(url);
      }
    }
  }
});

console.log('[观澜] 主权网关 Background Worker 已就绪。数据不出本地，AI守规矩。');
