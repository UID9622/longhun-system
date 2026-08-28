/* 龍魂·六层来源链 / LongHun Six-Layer Source Chain */
/* DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-WUWU-RENDERER-v1.0 */
/* 创建者: 诸葛鑫（UID9622） */
/* 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 */

/**
 * 女娲五彩石渲染器 (Wuwu Renderer) —— 跨平台通用版
 *
 * 跨平台原理：把文本按字符拆分，每个字符循环绑定五色石色卡。
 * 浏览器、WebView、小程序、Electron、PWA 均可使用。
 *
 * 五色石色卡（主权声明，硬编码，不随系统主题改变）：
 *   0 红 #FF0000
 *   1 黄 #FFFF00
 *   2 青 #00FFFF
 *   3 白 #FFFFFF
 *   4 黑 #000000
 */
(function (global) {
  'use strict';

  const WUWU_PALETTE = ['#FF0000', '#FFFF00', '#00FFFF', '#FFFFFF', '#000000'];
  const PALETTE_SIZE = WUWU_PALETTE.length;

  /**
   * 将文本渲染为女娲五彩石字符数组。
   * @param {string} text 要渲染的文本
   * @param {Object} [options={}] 选项
   * @param {number} [options.startIndex=0] 起始色标索引
   * @param {boolean} [options.colorizeAll=true] 是否给所有字符上色（包括非 CJK）。默认 true。
   * @returns {Array<{char:string, colorClass:string, color:string}>} 渲染结果数组
   */
  function renderWuwu(text, options) {
    options = options || {};
    let index = options.startIndex || 0;
    const colorizeAll = options.colorizeAll !== false;

    const chars = [];
    for (const char of String(text || '')) {
      if (char === '\n') {
        chars.push({ char: char, colorClass: '', color: '' });
        continue;
      }
      const shouldColor = colorizeAll || isCJK(char);
      if (shouldColor) {
        const colorIndex = index % PALETTE_SIZE;
        chars.push({
          char: char,
          colorClass: 'wuwu-color-' + colorIndex,
          color: WUWU_PALETTE[colorIndex],
        });
        index++;
      } else {
        chars.push({ char: char, colorClass: '', color: '' });
      }
    }
    return chars;
  }

  function isCJK(char) {
    const code = char.codePointAt(0);
    return (
      (code >= 0x4E00 && code <= 0x9FFF) || // CJK Unified Ideographs
      (code >= 0x3400 && code <= 0x4DBF) || // CJK Extension A
      (code >= 0xF900 && code <= 0xFAFF)    // CJK Compatibility
    );
  }

  // CommonJS
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { renderWuwu: renderWuwu, WUWU_PALETTE: WUWU_PALETTE };
  }

  // AMD
  if (typeof define === 'function' && define.amd) {
    define(function () {
      return { renderWuwu: renderWuwu, WUWU_PALETTE: WUWU_PALETTE };
    });
  }

  // Browser / WeChat Mini Program global
  if (typeof global !== 'undefined') {
    global.renderWuwu = renderWuwu;
    global.WUWU_PALETTE = WUWU_PALETTE;
  }
})(typeof globalThis !== 'undefined' ? globalThis : typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : this);
