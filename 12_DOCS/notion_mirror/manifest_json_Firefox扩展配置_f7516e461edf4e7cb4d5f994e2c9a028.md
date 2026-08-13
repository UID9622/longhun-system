# manifest.json | Firefox扩展配置

> Notion URL: https://app.notion.com/p/manifest-json-Firefox-f7516e461edf4e7cb4d5f994e2c9a028
> Created: 2025-12-13T05:06:00.000Z
> Last edited: 2026-07-01T15:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# manifest.json | Firefox扩展配置清单
DNA确认码：#ZHUGEXIN⚡️2025-LU-SYNC-MANIFEST-JSON-V1.0
## 🎯 核心配置
### 扩展信息
- 名称：LU-SYNC Dashboard - Visual Edition
- 版本：0.2.0
- Manifest版本：3（Firefox推荐）
### 权限声明
- storage - 本地存储（IndexedDB）
- scripting - 注入脚本能力
- <all_urls> - 全域访问（可选，后续接engine）
## 📋 完整代码
```json
{
  "manifest_version": 3,
  "name": "LU-SYNC Dashboard - Visual Edition",
  "version": "0.2.0",
  "description": "LU-SYNC-LOG — 太极视觉版：五行矩阵 / 炼化炉 / Kanban 动效（本地）",
  "icons": {
    "128": "icons/icon-128.png"
  },
  "action": {
    "default_popup": "popup/popup.html",
    "default_title": "LU-SYNC Dashboard"
  },
  "permissions": ["storage", "scripting"],
  "host_permissions": ["<all_urls>"],
  "background": {
    "service_worker": "background.js"
  }
}
```
## 📐 字段说明
### manifest_version
- 值：3
- 说明：Firefox推荐使用Manifest V3
- 兼容性：Chrome/Edge也支持V3
### icons
```json
"icons": {
  "128": "icons/icon-128.png"
}
```
- 工具栏图标路径
- 建议提供128x128 PNG
### action
```json
"action": {
  "default_popup": "popup/popup.html",
  "default_title": "LU-SYNC Dashboard"
}
```
- default_popup - 点击图标打开的页面
- default_title - 悬停提示文字
### permissions
```json
"permissions": ["storage", "scripting"]
```
- storage - 使用chrome.storage API
- scripting - 注入内容脚本
### host_permissions
```json
"host_permissions": ["<all_urls>"]
```
- 允许访问所有网站（可选）
- 后续接engine时需要
### background
```json
"background": {
  "service_worker": "background.js"
}
```
- 后台Service Worker脚本
- 当前留空，后续接引擎时实现
## ⚠️ 注意事项
### 最小权限原则
如果不需要host_permissions，可以删除该字段：
```json
{
  "permissions": ["storage"]
}
```
### background可选
如果不需要后台脚本，删除background字段：
```json
{
  "action": {...}
  // 删除 background 字段
}
```
### V2兼容
如果需要支持旧版Firefox，改为Manifest V2：
```json
{
  "manifest_version": 2,
  "browser_action": {
    "default_popup": "popup/popup.html"
  }
}
```
## 🚀 部署流程
### 1. 创建文件结构
```javascript
lu-sync-dashboard-ui/
├─ manifest.json          ← 此文件
├─ icons/icon-128.png
├─ popup/popup.html
└─ ...
```
### 2. Firefox临时加载
1. 打开 about:debugging#/runtime/this-firefox
1. 点击 Load Temporary Add-on
1. 选择 manifest.json
1. 扩展图标出现在工具栏
### 3. 永久安装
- 需要签名打包为.xpi文件
- 提交到Firefox Add-ons商店
- 或使用开发者账号自签名
---
创建人：💖 文心（技术归档）
安全审核：🛡️ 雯雯（隐私保护） ✅ 通过
