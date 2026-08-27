# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/* 龍魂·六层来源链 / LongHun Six-Layer Source Chain */
/* DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-WUWU-JS-v1.0 */

/**
 * 女娲五彩石渲染器 (Wuwu Renderer)
 *
 * 跨平台原理：把文本按字符拆成 <span>，每个 span 循环绑定五色石色卡。
 * 浏览器、WebView、小程序、Electron、PWA 均可使用。
 *
 * 五色石色卡（主权声明，硬编码，不随系统主题改变）：
 *   0 红 #FF0000
 *   1 黄 #FFFF00
 *   2 青 #00FFFF
 *   3 白 #FFFFFF
 *   4 黑 #000000
 *
 * 用法：
 *   1. 引入 wuwu.css 和 wuwu.js
 *   2. 给任意元素加 data-wuwu="true"，页面加载后自动渲染
 *   3. 或手动调用 Wuwu.render(element)
 */
(function (global) {
  'use strict';

  const PALETTE = ['#FF0000', '#FFFF00', '#00FFFF', '#FFFFFF', '#000000'];
  const PALETTE_SIZE = PALETTE.length;

  function isCJK(char) {
    const code = char.codePointAt(0);
    return (
      (code >= 0x4E00 && code <= 0x9FFF) || // CJK Unified Ideographs
      (code >= 0x3400 && code <= 0x4DBF) || // CJK Extension A
      (code >= 0xF900 && code <= 0xFAFF)    // CJK Compatibility
    );
  }

  /**
   * 渲染单个元素：把子文本节点拆成带颜色的 span。
   * @param {HTMLElement} element
   * @param {Object} options
   * @param {number} options.startIndex 起始色标（默认 0）
   * @param {boolean} options.colorizeAll 是否给所有字符上色（包括非 CJK）。默认 true，与 HarmonyOS 示例一致。
   */
  function render(element, options) {
    options = options || {};
    let index = options.startIndex || 0;
    const colorizeAll = options.colorizeAll !== false;

    // 避免重复渲染
    if (element.dataset.wuwuRendered === 'true') return;

    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);

    textNodes.forEach(function (node) {
      const text = node.textContent;
      if (!text) return;
      const fragment = document.createDocumentFragment();
      for (const char of text) {
        if (char === '\n') {
          fragment.appendChild(document.createTextNode('\n'));
          continue;
        }
        const shouldColor = colorizeAll || isCJK(char);
        if (shouldColor) {
          const span = document.createElement('span');
          span.className = 'wuwu-char wuwu-color-' + (index % PALETTE_SIZE);
          span.textContent = char;
          fragment.appendChild(span);
          index++;
        } else {
          fragment.appendChild(document.createTextNode(char));
        }
      }
      node.parentNode.replaceChild(fragment, node);
    });

    element.dataset.wuwuRendered = 'true';
  }

  function renderAll() {
    document.querySelectorAll('[data-wuwu="true"]').forEach(function (el) {
      render(el);
    });
  }

  // 自动初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAll);
  } else {
    renderAll();
  }

  global.Wuwu = {
    palette: PALETTE,
    render: render,
    renderAll: renderAll,
  };
})(window);
