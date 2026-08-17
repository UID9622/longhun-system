// 🐉 龍魂 · DeepSeek 对话采集器 content.js v1.0
// DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-CAPTURE-EXT-CONTENT-UID9622
// 注入 DeepSeek 网页版，采集对话消息 → 本地采集服务(8769)；离线时暂存 chrome.storage
(() => {
  const API = "http://127.0.0.1:8769/api/capture";
  const captured = new WeakSet();
  const seenText = new Set();

  function topicFromPage() {
    const t = (document.title || "").replace(/DeepSeek/i, "").replace(/[|｜\-–—].*$/, "").trim();
    return t || "DeepSeek对话";
  }

  function sendToServer(entry) {
    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    })
      .then((r) => r.json())
      .catch(() => {
        // 本地服务未启动 → 暂存，等服务恢复后由 background 补发
        try {
          chrome.storage.local.get({ pending: [] }, (d) => {
            d.pending.push(Object.assign({ savedAt: Date.now() }, entry));
            if (d.pending.length > 200) d.pending = d.pending.slice(-200);
            chrome.storage.local.set({ pending: d.pending });
          });
        } catch (e) {
          /* 忽略 */
        }
      });
  }

  function captureMessage(el) {
    if (captured.has(el)) return;
    const content = (el.innerText || el.textContent || "").trim();
    if (!content || content.length < 4) return;
    if (seenText.has(content)) return;
    seenText.add(content);
    captured.add(el);
    el.dataset.lhCaptured = "true";

    const isUser = /(user|human|用户)/i.test(el.className || "") ||
      !!el.closest("[class*='user']");
    sendToServer({
      source: "deepseek",
      role: isUser ? "user" : "assistant",
      content: content.slice(0, 4000),
      topic: topicFromPage(),
      metadata: { url: location.href, ts: new Date().toISOString() },
    });
  }

  function scan() {
    document
      .querySelectorAll(".message, .chat-message, [class*='message'], [class*='Message']")
      .forEach(captureMessage);
  }

  // MutationObserver 监听动态加载的新消息
  const observer = new MutationObserver(() => scan());
  observer.observe(document.body, { childList: true, subtree: true });

  // 首屏已有消息立即采集
  setTimeout(scan, 1200);

  console.log("🐉 龍魂采集器已注入 DeepSeek");
})();
