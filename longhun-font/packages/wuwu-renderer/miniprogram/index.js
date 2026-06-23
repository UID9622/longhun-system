/* DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-WUWU-RENDERER-v1.0 */

const { renderWuwu } = require('../src/wuwu.js');

Component({
  properties: {
    text: {
      type: String,
      value: '',
    },
    startIndex: {
      type: Number,
      value: 0,
    },
    colorizeAll: {
      type: Boolean,
      value: true,
    },
  },
  data: {
    chars: [],
  },
  observers: {
    'text, startIndex, colorizeAll': function (text, startIndex, colorizeAll) {
      const rendered = renderWuwu(text || '', {
        startIndex: startIndex || 0,
        colorizeAll: colorizeAll !== false,
      });
      this.setData({
        chars: rendered.map(function (item) {
          return { char: item.char, cls: item.colorClass };
        }),
      });
    },
  },
});
