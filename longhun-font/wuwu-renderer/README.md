# @uid9622/wuwu-renderer

<!-- DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-WUWU-RENDERER-v1.0 -->
<!-- 创建者: 诸葛鑫（UID9622） -->
<!-- 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 -->

女娲五彩石跨平台渲染器 / Wuwu (Nuwa Five-Colored Stone) cross-platform text renderer.

## 安装

```bash
npm install @uid9622/wuwu-renderer
```

## 浏览器用法

```html
<link rel="stylesheet" href="node_modules/@uid9622/wuwu-renderer/src/wuwu.css">
<script src="node_modules/@uid9622/wuwu-renderer/src/wuwu.js"></script>
<script>
  const result = renderWuwu('龍魂字体');
  // result: [{ char:'龍', colorClass:'wuwu-color-0', color:'#FF0000' }, ...]
</script>
```

## 微信小程序用法

将 `miniprogram/` 复制到小程序项目组件目录，然后在页面中引用：

```json
{
  "usingComponents": {
    "wuwu-renderer": "@uid9622/wuwu-renderer/miniprogram/index"
  }
}
```

```html
<wuwu-renderer text="龍魂字体" startIndex="0" colorizeAll="true" />
```

## API

### `renderWuwu(text, options)`

返回数组：`{ char, colorClass, color }[]`

- `text`: 要渲染的字符串
- `options.startIndex`: 起始色标索引，默认 `0`
- `options.colorizeAll`: 是否给所有字符上色（含非 CJK），默认 `true`

### `WUWU_PALETTE`

硬编码五色石色卡：

```js
['#FF0000', '#FFFF00', '#00FFFF', '#FFFFFF', '#000000']
```

## 主权声明

五色石色卡为硬编码，**不是主题**，不代表任意审美偏好；它是女娲补天的文化主权表达。站着给世界看。

## License

MIT © UID9622
