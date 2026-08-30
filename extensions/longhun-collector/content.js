// ============================================================
// 龍魂系统 · 浏览器内容采集引擎 v2.1
// DNA: #龍芯⚡️丙午·乙申·CONTENT-v2.1-DIRECT
// UID9622 | 龍芯北辰
// 修复：直连服务端，绕过 Service Worker 瓶颈
// ============================================================

const LH = {
  dna: '#龍芯⚡️丙午·乙申·COLLECTOR-v2.0',
  uid: '9622',
  serverUrl: 'http://localhost:9622',
  debounceMs: 8000,
  dedupWindow: 60000, // 1分钟内同URL不重复采集
  maxTextLen: 8000,
  lastContentHash: '',
  lastCollectTime: 0,
};

// ---- 去重 ----
function hashContent(text) {
  let hash = 0;
  for (let i = 0; i < Math.min(text.length, 500); i++) {
    hash = ((hash << 5) - hash) + text.charCodeAt(i);
    hash |= 0;
  }
  return String(hash);
}

// ---- 通用文本提取 ----
function extractText(selectors, fallback = '') {
  for (const sel of selectors) {
    try {
      const el = document.querySelector(sel);
      if (el?.innerText?.trim()) return el.innerText.trim().substring(0, LH.maxTextLen);
    } catch {}
  }
  return fallback;
}

function extractAllTexts(selector) {
  try {
    return Array.from(document.querySelectorAll(selector))
      .map(el => el.innerText?.trim())
      .filter(t => t && t.length > 5)
      .map(t => t.substring(0, LH.maxTextLen))
      .slice(0, 100);
  } catch { return []; }
}

// ---- 站点适配器 v2.0（鲁棒选择器链） ----
const ADAPTERS = {
  'kimi.com|moonshot.cn': {
    name: 'Kimi AI',
    extract() {
      const messages = [];
      // 多套选择器覆盖 Kimi 不同版本 DOM
      const selectors = [
        '[class*="chat-item"]', '[class*="message"]', '[data-testid*="chat"]',
        '[class*="bubble"]', '.chat-message', '[class*="agent-chat"]',
        '[data-index]', '.prose', '[class*="turn"]',
      ];
      const items = new Set();
      selectors.forEach(sel => {
        try { document.querySelectorAll(sel).forEach(el => items.add(el)); } catch {}
      });
      items.forEach(el => {
        const text = el.innerText?.trim();
        if (text && text.length > 10) {
          const classes = el.className || '';
          const role = classes.includes('user') || classes.includes('human') ? 'user' : 'assistant';
          messages.push({ role, text: text.substring(0, 5000) });
        }
      });
      return { type: 'chat', messages: messages.slice(-60) };
    },
  },

  'douyin.com': {
    name: '抖音',
    extract() {
      const videos = [];
      const items = document.querySelectorAll('[data-e2e="feed-video"], .video-card, [class*="video-item"], [class*="slide-item"]');
      items.forEach((item, i) => {
        const desc = extractText(['.desc', '[class*="desc"]', '[class*="title"]', '.video-desc'], '');
        const author = extractText(['.author', '[class*="nickname"]', '[class*="user-name"]'], '');
        videos.push({ idx: i, desc: desc.substring(0, 300), author: author.substring(0, 50) });
      });
      return { type: 'feed', videos: videos.slice(0, 20) };
    },
  },

  'csdn.net': {
    name: 'CSDN',
    extract() {
      const content = extractText([
        'article', '#content_views', '.article-content', '.blog-content-body',
        '[class*="article_content"]', '.markdown_views', '#article_content',
        '.htmledit_views',
      ]);
      const title = extractText(['h1', '.title-article', '.article-title', '[class*="tit"]'], document.title);
      const author = extractText(['.profile-intro-name', '.user-name', '[class*="author"]', '.name'], '');
      const tags = extractAllTexts('.tag-link, .article-tag, [class*="tag"]').slice(0, 10);
      return { type: 'article', title: title.substring(0, 200), content, author: author.substring(0, 50), tags };
    },
  },

  'notion.site': {
    name: 'Notion',
    extract() {
      const blocks = extractAllTexts('[data-block-id], .notion-page-content, [class*="notion-text"], [class*="notion-selectable"]');
      const title = extractText(['[placeholder*="title"]', '.notion-page-title', 'h1'], document.title);
      return { type: 'document', title: title.substring(0, 200), blocks };
    },
  },

  'github.com': {
    name: 'GitHub',
    extract() {
      const readme = extractText(['article.markdown-body', '.Box-body .markdown-body', '#readme', '.readme'], '');
      const about = extractText(['.Layout-sidebar .f4', '[class*="f4"]'], '');
      const code = extractAllTexts('.blob-code, .highlight pre, [class*="code-line"]').slice(0, 30);
      const lang = extractText(['[data-test-selector="lang"]', '.lang'], '');
      return { type: 'repo', readme: readme.substring(0, 8000), about: about.substring(0, 500), code, lang };
    },
  },

  'gitee.com': {
    name: 'Gitee',
    extract() {
      const readme = extractText(['.file_content', '.readme-box', '.markdown-body'], '');
      const desc = extractText(['.git-project-desc', '[class*="desc"]'], '');
      return { type: 'repo', readme: readme.substring(0, 8000), desc: desc.substring(0, 500) };
    },
  },

  'weibo.com': {
    name: '微博',
    extract() {
      const posts = extractAllTexts('.WB_text, [class*="wb_text"], [class*="feed_content"], .txt, [node-type="feed_list_content"]');
      return { type: 'feed', posts: posts.slice(0, 20) };
    },
  },

  'zhihu.com': {
    name: '知乎',
    extract() {
      const question = extractText(['.QuestionHeader-title', '.question-title', 'h1.QuestionHeader-title'], '');
      const content = extractText(['.RichText', '.Post-RichText', '.Article-content', '.AnswerItem-content'], '');
      const answers = extractAllTexts('.RichContent-inner, .AnswerItem-content, [class*="answer-content"]').slice(0, 5);
      return { type: 'qa', question: question.substring(0, 300), content: content?.substring(0, 8000) || '', answers };
    },
  },

  'juejin.cn': {
    name: '掘金',
    extract() {
      const title = extractText(['.article-title', 'h1', '.content-title'], document.title);
      const content = extractText(['.article-content', '.markdown-body', '#article-root', '.article'], '');
      const tags = extractAllTexts('.tag-item, .tag, [class*="tag-title"]');
      return { type: 'article', title: title.substring(0, 200), content: content?.substring(0, 8000) || '', tags };
    },
  },

  'bilibili.com': {
    name: 'B站',
    extract() {
      const title = extractText(['h1.video-title', '.video-title', '.video-info-title'], document.title);
      const desc = extractText(['.video-desc', '.basic-desc-content', '[class*="desc-info"]'], '');
      const comments = extractAllTexts('.reply-content, .comment-content, [class*="reply-item"]').slice(0, 20);
      return { type: 'video', title: title.substring(0, 300), desc: desc?.substring(0, 2000) || '', comments };
    },
  },

  'mp.weixin.qq.com': {
    name: '微信公众号',
    extract() {
      const title = extractText(['#activity-name', '#js_article_title', '.rich_media_title'], document.title);
      const author = extractText(['#js_name', '#js_author_name', '.rich_media_meta_text'], '');
      const content = extractText(['#js_content', '.rich_media_content', '.rich_media_area_primary'], '');
      return { type: 'article', title: title.substring(0, 200), author: author.substring(0, 50), content: content?.substring(0, 8000) || '' };
    },
  },
};

// ---- 适配器匹配 ----
function matchAdapter(hostname) {
  for (const [pattern, adapter] of Object.entries(ADAPTERS)) {
    for (const domain of pattern.split('|')) {
      if (hostname.includes(domain)) return adapter;
    }
  }
  return null;
}

// ---- 主采集函数 ----
async function collect() {
  const hostname = window.location.hostname;
  const adapter = matchAdapter(hostname);
  if (!adapter) return;

  try {
    const extracted = adapter.extract();
    const contentStr = JSON.stringify(extracted);
    const contentHash = hashContent(contentStr);

    // 去重
    if (contentHash === LH.lastContentHash && Date.now() - LH.lastCollectTime < LH.dedupWindow) {
      return;
    }
    LH.lastContentHash = contentHash;
    LH.lastCollectTime = Date.now();

    const payload = {
      title: document.title.substring(0, 200),
      url: window.location.href,
      hostname,
      site: adapter.name,
      timestamp: Date.now(),
      dna: LH.dna,
      uid: LH.uid,
      ...extracted,
    };

    // 直接 POST 到服务端（主路径，不经过 Service Worker）
    sendToServer(payload, adapter);
  } catch (e) {
    console.error('龍魂采集异常:', e.message);
  }
}

// ---- 直连发送（主路径） ----
async function sendToServer(payload, adapter) {
  const msgCount = payload.messages?.length || payload.videos?.length ||
                   payload.blocks?.length || payload.posts?.length ||
                   payload.answers?.length || payload.comments?.length || 0;

  try {
    const resp = await fetch(`${LH.serverUrl}/collect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(5000),
    });

    if (resp.ok) {
      const result = await resp.json();
      console.log(`🐉 龍魂采集 ✅ | ${adapter.name} | ${msgCount || '?'} 条 | 已归档: ${result.filepath || 'ok'}`);
      // 更新 popup 统计
      chrome.runtime.sendMessage({ action: 'collect-result', data: payload }).catch(() => {});
      return true;
    } else if (resp.status === 403) {
      console.error(`🐉 龍魂采集 ❌ DNA不匹配 | ${adapter.name}`);
      return false;
    } else {
      console.warn(`🐉 龍魂采集 ⚠️ 服务返回 ${resp.status} | ${adapter.name}`);
      // 降级到 background 离线队列
      fallbackToBackground(payload, adapter);
      return false;
    }
  } catch (e) {
    console.warn(`🐉 龍魂采集 ⚠️ 直连失败 (${e.message}) | ${adapter.name} | 降级到离线队列`);
    fallbackToBackground(payload, adapter);
    return false;
  }
}

// ---- 降级路径：通过 background Service Worker ----
function fallbackToBackground(payload, adapter) {
  chrome.runtime.sendMessage({ action: 'collect-result', data: payload }, (resp) => {
    if (chrome.runtime.lastError) {
      console.error(`🐉 龍魂采集 ❌ 离线入队也失败: ${chrome.runtime.lastError.message}`);
      return;
    }
    const qs = resp?.queueSize || '?';
    console.log(`🐉 龍魂采集 📦 已入离线队列 | ${adapter?.name || '?'} | 队列:${qs}`);
  });
}

// ---- 暴露全局接口（供 background 调用） ----
window.__lhCollect = collect;

// ---- 初始化 ----
console.log(`🐉 龍魂采集引擎 v2.1 已注入 | ${window.location.hostname} | UID9622 | 直连模式`);

// 页面加载后采集
let initTimeout;
if (document.readyState === 'complete') {
  initTimeout = setTimeout(collect, 2000);
} else {
  window.addEventListener('load', () => { initTimeout = setTimeout(collect, 2000); }, { once: true });
}

// ---- 智能 MutationObserver（只观察主要内容区） ----
let debounceTimer;
const TARGET_SELECTORS = [
  'article', 'main', '#content', '.content', '.main-content',
  '[role="main"]', '.chat-container', '[class*="chat-list"]',
  '#js_content', '.article-content', '.rich_media_content',
];

function startObserver() {
  let target = null;
  for (const sel of TARGET_SELECTORS) {
    target = document.querySelector(sel);
    if (target) break;
  }
  if (!target) target = document.body;

  const observer = new MutationObserver((mutations) => {
    const hasContent = mutations.some(m => m.addedNodes.length > 0);
    if (hasContent) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(collect, LH.debounceMs);
    }
  });

  observer.observe(target, { childList: true, subtree: true, attributes: false });
  return observer;
}

const contentObserver = startObserver();

// ---- SPA 路由变化监听 ----
let lastUrl = window.location.href;
setInterval(() => {
  if (window.location.href !== lastUrl) {
    lastUrl = window.location.href;
    LH.lastContentHash = '';
    clearTimeout(initTimeout);
    initTimeout = setTimeout(collect, 3000);
  }
}, 1500);

// ---- 定时采集（递增间隔，最大30分钟） ----
let saveCount = 0;
function scheduleNext() {
  const base = 300000; // 5分钟
  const interval = Math.min(base * (1 + saveCount * 0.3), 1800000);
  saveCount++;
  setTimeout(() => { collect(); scheduleNext(); }, interval);
}
setTimeout(scheduleNext, 300000);
