// ============================================================
// DNA: #龍芯⚡️丙午·乙未·丁酉·子时·☰乾-GUANLAN-CONTENT-v1.0-ct7c9e3a
// 创建者: 诸葛鑫 (UID9622)
// 协议: CC BY-NC-SA 4.0
// ============================================================
// 龍魂 · 观澜主权网关 — Content Script
// 职责: 页面注入检测 | AI脚本识别 | 隐私风险评分
// ============================================================

(function() {
  'use strict';

  const findings = {
    aiScripts: [],
    trackers: [],
    fingerprinters: [],
    thirdPartyCookies: [],
    websockets: [],
    webrtcDetected: false,
    canvasFingerprint: false
  };

  // ============================================================
  // 一、页面注入检测 — 识别AI相关脚本
  // ============================================================
  function detectAIScripts() {
    const scripts = document.querySelectorAll('script[src]');
    const AI_SCRIPT_PATTERNS = [
      /openai/i, /chatgpt/i, /copilot/i, /bard/i, /gemini/i,
      /deepseek/i, /kimi/i, /tongyi/i, /hunyuan/i, /zhipu/i,
      /chatbot/i, /ai-assistant/i, /ai-widget/i, /llm/i, /gpt/i,
      /claude/i, /anthropic/i, /vertex/i, /bedrock/i
    ];

    scripts.forEach(script => {
      for (const pattern of AI_SCRIPT_PATTERNS) {
        if (pattern.test(script.src)) {
          findings.aiScripts.push({
            url: script.src,
            type: script.type || 'text/javascript',
            detected: pattern.source
          });
          break;
        }
      }
    });

    // 检测内联AI脚本
    const inlineScripts = document.querySelectorAll('script:not([src])');
    inlineScripts.forEach(script => {
      const content = script.textContent;
      if (content.includes('AI_AGENT') || content.includes('coze') ||
          content.includes('chatbot') || content.includes('copilot')) {
        findings.aiScripts.push({
          inline: true,
          type: 'inline_ai',
          snippet: content.substring(0, 200),
          detected: 'inline_ai'
        });
      }
    });

    // 检测 AI iframe
    const iframes = document.querySelectorAll('iframe');
    const AI_IFRAME_PATTERNS = [
      /chat\.openai\.com/i, /copilot\.microsoft\.com/i,
      /gemini\.google\.com/i, /chat\.deepseek\.com/i,
      /kimi\.moonshot\.cn/i, /tongyi\.aliyun\.com/i
    ];
    iframes.forEach(iframe => {
      for (const pattern of AI_IFRAME_PATTERNS) {
        if (pattern.test(iframe.src)) {
          findings.aiScripts.push({
            url: iframe.src,
            type: 'ai_iframe',
            detected: pattern.source
          });
          break;
        }
      }
    });
  }

  // ============================================================
  // 二、Canvas 指纹检测
  // ============================================================
  function detectCanvasFingerprinting() {
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    const originalToBlob = HTMLCanvasElement.prototype.toBlob;

    HTMLCanvasElement.prototype.toDataURL = function(...args) {
      const canvasInfo = {
        width: this.width,
        height: this.height,
        method: 'toDataURL',
        stack: new Error().stack?.split('\n').slice(1,4).join('\n') || ''
      };

      if (isFingerprintCanvas(this)) {
        findings.canvasFingerprint = true;
        findings.fingerprinters.push({
          type: 'canvas_toDataURL',
          details: canvasInfo,
          timestamp: Date.now()
        });
      }

      return originalToDataURL.apply(this, args);
    };

    CanvasRenderingContext2D.prototype.getImageData = function(...args) {
      const canvas = this.canvas;
      if (canvas && isFingerprintCanvas(canvas)) {
        findings.canvasFingerprint = true;
        findings.fingerprinters.push({
          type: 'canvas_getImageData',
          timestamp: Date.now()
        });
      }
      return originalGetImageData.apply(this, args);
    };
  }

  function isFingerprintCanvas(canvas) {
    // 指纹canvas特征：很小尺寸 (通常小于200x200)
    if (canvas.width < 200 && canvas.height < 200) {
      try {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          const data = ctx.getImageData(0, 0, 1, 1).data;
          // 检测是否绘制了文字（指纹通常包含文字渲染）
          // 简化判定：小canvas + 有内容 = 可疑
          return true;
        }
      } catch {}
    }
    return false;
  }

  // ============================================================
  // 三、第三方追踪检测
  // ============================================================
  function detectTrackers() {
    const currentDomain = window.location.hostname;
    const KNOWN_TRACKERS = [
      'doubleclick.net', 'google-analytics.com', 'googletagmanager.com',
      'facebook.net', 'fbcdn.net', 'hotjar.com', 'clarity.ms',
      'amplitude.com', 'mixpanel.com', 'segment.io', 'fullstory.com',
      'mouseflow.com', 'crazyegg.com', 'optimizely.com', 'vwo.com',
      'adnxs.com', 'rubiconproject.com', 'pubmatic.com', 'openx.net',
      'criteo.com', 'casalemedia.com', 'adsrvr.org', 'moatads.com'
    ];

    // 检测页面上的第三方跟踪脚本
    const allScripts = document.querySelectorAll('script[src]');
    allScripts.forEach(script => {
      try {
        const scriptDomain = new URL(script.src).hostname;
        if (scriptDomain !== currentDomain) {
          for (const tracker of KNOWN_TRACKERS) {
            if (scriptDomain.includes(tracker)) {
              findings.trackers.push({
                domain: scriptDomain,
                url: script.src,
                type: 'third_party_tracker',
                tracker: tracker
              });
              break;
            }
          }
        }
      } catch {}
    });

    // 检测第三方 Cookie
    if (document.cookie) {
      const cookies = document.cookie.split(';');
      cookies.forEach(c => {
        const domain = c.split('=')[0].trim();
        // 检查是否包含跨域cookie迹象
        if (domain.includes('__') || domain.includes('_ga') ||
            domain.includes('_fbp') || domain.includes('_gid') ||
            domain.includes('_hj') || domain.includes('_mkto')) {
          findings.thirdPartyCookies.push({ name: domain });
        }
      });
    }
  }

  // ============================================================
  // 四、WebRTC 泄露检测
  // ============================================================
  function detectWebRTCLeak() {
    if (window.RTCPeerConnection) {
      const originalRTCPeerConnection = window.RTCPeerConnection;
      window.RTCPeerConnection = function(...args) {
        findings.webrtcDetected = true;
        return new originalRTCPeerConnection(...args);
      };
      window.RTCPeerConnection.prototype = originalRTCPeerConnection.prototype;
    }
  }

  // ============================================================
  // 五、WebSocket 监控
  // ============================================================
  function monitorWebSockets() {
    const originalWS = window.WebSocket;
    window.WebSocket = function(...args) {
      findings.websockets.push({
        url: args[0],
        timestamp: Date.now()
      });

      const ws = new originalWS(...args);

      const originalSend = ws.send;
      ws.send = function(data) {
        // 检测是否发送了敏感数据
        if (typeof data === 'string') {
          const sensitivePatterns = [
            /password/i, /token/i, /secret/i, /api[_-]?key/i,
            /bearer/i, /authorization/i
          ];
          for (const pattern of sensitivePatterns) {
            if (pattern.test(data)) {
              findings.fingerprinters.push({
                type: 'websocket_sensitive_data',
                url: args[0],
                pattern: pattern.source,
                timestamp: Date.now()
              });
              break;
            }
          }
        }
        return originalSend.call(this, data);
      };

      return ws;
    };

    window.WebSocket.prototype = originalWS.prototype;
  }

  // ============================================================
  // 六、隐私风险评分 (0-100)
  // ============================================================
  function calculatePrivacyScore() {
    let score = 0;

    // AI脚本: 每发现1个 +5分
    score += Math.min(findings.aiScripts.length * 5, 25);

    // 追踪器: 每发现1个 +10分
    score += Math.min(findings.trackers.length * 10, 30);

    // 指纹采集: +15分
    if (findings.canvasFingerprint) score += 15;

    // WebRTC: +10分
    if (findings.webrtcDetected) score += 10;

    // 第三方Cookie: 每1个 +3分
    score += Math.min(findings.thirdPartyCookies.length * 3, 10);

    // WebSocket: 每1个 +2分
    score += Math.min(findings.websockets.length * 2, 5);

    // 指纹收集器额外惩罚
    if (findings.fingerprinters.length > 0) {
      score += Math.min(findings.fingerprinters.length * 5, 10);
    }

    return Math.min(score, 100);
  }

  // ============================================================
  // 七、执行检测
  // ============================================================
  function runAllDetections() {
    detectAIScripts();
    detectTrackers();
    detectCanvasFingerprinting();
    detectWebRTCLeak();
    monitorWebSockets();

    const score = calculatePrivacyScore();

    // 发送结果到 background
    chrome.runtime.sendMessage({
      action: 'privacyReport',
      data: {
        url: window.location.href,
        domain: window.location.hostname,
        score: score,
        findings: findings,
        riskLevel: score >= 70 ? 'high' : score >= 40 ? 'medium' : 'low',
        timestamp: Date.now()
      }
    });

    // 高分告警
    if (score >= 70) {
      chrome.runtime.sendMessage({
        action: 'highRiskAlert',
        data: {
          url: window.location.href,
          score: score,
          topThreats: getTopThreats()
        }
      });
    }
  }

  function getTopThreats() {
    const threats = [];
    if (findings.trackers.length > 0) threats.push(`${findings.trackers.length}个追踪脚本`);
    if (findings.canvasFingerprint) threats.push('Canvas指纹采集');
    if (findings.webrtcDetected) threats.push('WebRTC泄露风险');
    if (findings.aiScripts.length > 0) threats.push(`${findings.aiScripts.length}个AI脚本`);
    if (findings.thirdPartyCookies.length > 0) threats.push('第三方Cookie');
    return threats.slice(0, 5);
  }

  // DOM加载完成后执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(runAllDetections, 2000); // 延迟2秒等页面稳定
    });
  } else {
    setTimeout(runAllDetections, 2000);
  }

  console.log('[观澜] Content Script 已注入，开始监控页面。');
})();
