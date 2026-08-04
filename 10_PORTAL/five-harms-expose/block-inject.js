/**
 * 龍魂·五害曝光台 — 熔断插针 v1.0
 * DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-BLOCK-INJECT-v1.0
 * 
 * 职能: 当企业被标记为严重危害时，自动阻断该企业域名的第三方脚本、Cookie追踪和API调用。
 * 用法: <script src="./block-inject.js" async></script>
 * 铁律: 仅阻断第三方请求，不影响用户主动访问的主页面。
 */

(function() {
  'use strict';

  // ═══ 危害企业域名清单（由五害曝光台API动态更新） ═══
  const BLOCKED_DOMAINS = new Set([
    // 这些域名下的第三方资源将被阻断
    // 标记🔴严重危害的企业域名会出现在这里
    // 示例 (替换为实际被标记的企业CDN/统计/广告域名):
    // 'cdn-harmful-company.com',
    // 'analytics-bad-actor.net',
  ]);

  // ═══ 阻断Cookie追踪 ␐══
  const BLOCKED_COOKIE_PATTERNS = [
    // 已知的追踪Cookie名称模式
  ];

  // ═══ 屏蔽规则类型 ␐══
  const BLOCK_TYPES = {
    SCRIPT: 'script',
    IMAGE: 'image',
    IFRAME: 'iframe',
    XHR: 'xhr',
    COOKIE: 'cookie',
  };

  let blockedCount = 0;
  const blockedLog = [];

  /**
   * 检查URL是否匹配被阻断域名
   */
  function isBlockedDomain(url) {
    if (!url) return false;
    try {
      const hostname = new URL(url, window.location.origin).hostname;
      for (const domain of BLOCKED_DOMAINS) {
        if (hostname === domain || hostname.endsWith('.' + domain)) {
          return true;
        }
      }
    } catch (e) {
      // 相对路径不检查
    }
    return false;
  }

  /**
   * 拦截动态创建的<script>标签
   */
  const originalCreateElement = Document.prototype.createElement;
  Document.prototype.createElement = function(tagName, options) {
    const element = originalCreateElement.call(this, tagName, options);
    
    if (tagName.toLowerCase() === 'script') {
      const originalSetAttribute = element.setAttribute;
      const _this = this;
      
      element.setAttribute = function(name, value) {
        if (name === 'src' && isBlockedDomain(value)) {
          console.warn(
            `%c🛡️ 龍魂·熔断插针 %c已阻断有害脚本: %c${value}`,
            'color:#c9a84c;font-weight:bold;',
            'color:#c8c8d4;',
            'color:#e5534b;'
          );
          blockedCount++;
          blockedLog.push({ type: BLOCK_TYPES.SCRIPT, url: value, time: new Date().toISOString() });
          return; // 阻断设置
        }
        return originalSetAttribute.call(this, name, value);
      };
      
      // 也拦截直接属性赋值
      const originalSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src');
      if (originalSrcDescriptor && originalSrcDescriptor.set) {
        Object.defineProperty(element, 'src', {
          get: function() { return this.getAttribute('src'); },
          set: function(value) {
            if (isBlockedDomain(value)) {
              console.warn(
                `%c🛡️ 龍魂·熔断插针 %c已阻断有害脚本: %c${value}`,
                'color:#c9a84c;font-weight:bold;',
                'color:#c8c8d4;',
                'color:#e5534b;'
              );
              blockedCount++;
              blockedLog.push({ type: BLOCK_TYPES.SCRIPT, url: value, time: new Date().toISOString() });
              return;
            }
            this.setAttribute('src', value);
          }
        });
      }
    }
    
    if (tagName.toLowerCase() === 'iframe') {
      const originalSetAttribute = element.setAttribute;
      element.setAttribute = function(name, value) {
        if (name === 'src' && isBlockedDomain(value)) {
          console.warn(
            `%c🛡️ 龍魂·熔断插针 %c已阻断有害iframe: %c${value}`,
            'color:#c9a84c;font-weight:bold;',
            'color:#c8c8d4;',
            'color:#e5534b;'
          );
          blockedCount++;
          blockedLog.push({ type: BLOCK_TYPES.IFRAME, url: value, time: new Date().toISOString() });
          return;
        }
        return originalSetAttribute.call(this, name, value);
      };
    }
    
    return element;
  };

  /**
   * 拦截 XMLHttpRequest 和 fetch
   */
  const originalXHROpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    if (isBlockedDomain(url)) {
      console.warn(
        `%c🛡️ 龍魂·熔断插针 %c已阻断有害XHR: %c${method} ${url}`,
        'color:#c9a84c;font-weight:bold;',
        'color:#c8c8d4;',
        'color:#e5534b;'
      );
      blockedCount++;
      blockedLog.push({ type: BLOCK_TYPES.XHR, url, time: new Date().toISOString() });
      // 返回一个永远不resolve也不reject的Promise等价物
      throw new Error('Blocked by LongHun Block Inject');
    }
    return originalXHROpen.call(this, method, url, ...rest);
  };

  const originalFetch = window.fetch;
  window.fetch = function(input, init) {
    const url = typeof input === 'string' ? input : (input instanceof Request ? input.url : '');
    if (isBlockedDomain(url)) {
      console.warn(
        `%c🛡️ 龍魂·熔断插针 %c已阻断有害fetch: %c${url}`,
        'color:#c9a84c;font-weight:bold;',
        'color:#c8c8d4;',
        'color:#e5534b;'
      );
      blockedCount++;
      blockedLog.push({ type: BLOCK_TYPES.XHR, url, time: new Date().toISOString() });
      return Promise.reject(new Error('Blocked by LongHun Block Inject'));
    }
    return originalFetch.call(this, input, init);
  };

  /**
   * 拦截图片（追踪像素）
   */
  const originalImageSrcDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');
  if (originalImageSrcDescriptor && originalImageSrcDescriptor.set) {
    Object.defineProperty(HTMLImageElement.prototype, 'src', {
      get: function() { return this.getAttribute('src'); },
      set: function(value) {
        if (isBlockedDomain(value)) {
          blockedCount++;
          blockedLog.push({ type: BLOCK_TYPES.IMAGE, url: value, time: new Date().toISOString() });
          return; // 阻断
        }
        this.setAttribute('src', value);
      }
    });
  }

  /**
   * 定期清理第三方Cookie
   */
  function cleanBlockedCookies() {
    const cookies = document.cookie.split(';');
    for (const pattern of BLOCKED_COOKIE_PATTERNS) {
      for (const cookie of cookies) {
        if (cookie.trim().toLowerCase().includes(pattern.toLowerCase())) {
          // 尝试删除（同域cookie才能删）
          document.cookie = cookie.split('=')[0] + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
          blockedCount++;
        }
      }
    }
  }

  // 定时清理
  setInterval(cleanBlockedCookies, 30000);

  // ═══ 公开API ═══
  window.LongHunBlockInject = {
    /**
     * 动态添加阻断域名
     */
    addDomain: function(domain) {
      BLOCKED_DOMAINS.add(domain);
      console.log(`%c🛡️ 龍魂·熔断插针 %c已添加阻断域名: ${domain}`,
        'color:#c9a84c;font-weight:bold;', 'color:#c8c8d4;');
    },

    /**
     * 添加阻断Cookie模式
     */
    addCookiePattern: function(pattern) {
      BLOCKED_COOKIE_PATTERNS.push(pattern);
    },

    /**
     * 获取阻断统计
     */
    getStats: function() {
      return {
        blockedCount: blockedCount,
        domainsBlocked: BLOCKED_DOMAINS.size,
        cookiePatterns: BLOCKED_COOKIE_PATTERNS.length,
        recentBlocks: blockedLog.slice(-10),
      };
    },

    /**
     * 获取阻断日志
     */
    getLog: function() {
      return blockedLog.slice();
    },

    /**
     * 检查域名是否在阻断列表中
     */
    isBlocked: function(domain) {
      return BLOCKED_DOMAINS.has(domain);
    },

    /**
     * 同步阻断名单（从API拉取最新）
     */
    syncFromAPI: async function(apiUrl) {
      try {
        const resp = await fetch(apiUrl || '/five-harms/api/blocklist');
        const data = await resp.json();
        if (data.domains) {
          data.domains.forEach(d => BLOCKED_DOMAINS.add(d));
          console.log(
            `%c🛡️ 龍魂·熔断插针 %c已同步 ${data.domains.length} 个阻断域名`,
            'color:#c9a84c;font-weight:bold;', 'color:#c8c8d4;'
          );
        }
      } catch (e) {
        console.debug('熔断插针同步失败（非关键）:', e.message);
      }
    },
  };

  // 启动时同步
  try {
    window.LongHunBlockInject.syncFromAPI();
  } catch (e) {
    // 静默失败
  }

  console.log(
    `%c🛡️ %c龍魂·熔断插针 v1.0 %c已激活 | 阻断域名: ${BLOCKED_DOMAINS.size} | 护你周全`,
    'color:#c9a84c;font-weight:bold;',
    'color:#e8c84c;',
    'color:#c8c8d4;'
  );
})();
