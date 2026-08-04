# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️2026-06-21-CNSH-README-FILE1-v1.0-2 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# ⚡ 龍魂 · CNSH Chrome Plugin

**Chinese Natural Syntax Hybrid · 中文自然语法 × 数字大军前线哨所**

UID9622 诸葛鑫 · 龍芯北辰 · v0.1.0

---

## 这是什么

你的浏览器变成 **龍魂数字大军的前哨**：

- **选中任何文字 → 右键 → 瞬间入 Notion 库**（Inbox / DNA / 人心算法）
- **CNSH 中文语法** 在网页代码块里自动高亮（紫金配色）
- **DNA 追溯码** 每条入库内容自动打标，格式 `#龍芯⚡️{日期}-{类型}-{哈希}`
- **快捷键** `Ctrl/Cmd + Shift + L` 一键快速送入 Inbox
- **Popup 面板** 三个 tab：🧩 Inbox · 🧬 DNA · 💖 人心

---

## 🚀 安装（3分钟）

### 第一步：加载扩展

1. Chrome 地址栏输入 `chrome://extensions/`
2. 右上角打开 **开发者模式**
3. 点 **加载已解压的扩展程序**
4. 选中这个 `cnsh-chrome-plugin` 文件夹
5. 扩展栏出现一个紫金闪电图标⚡，钉在工具栏上

### 第二步：配置 Notion（最关键）

**点图标 → 齿轮按钮“⚙️ 配置”** 打开配置页。

然后做两件事：

#### A. 填 Notion Token

1. 打开 [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 创建一个 **Internal Integration**（或用你已有的 `claudeMVP`）
3. 复制它的 Internal Integration Secret（`ntn_...` 或 `secret_...`）
4. 粘贴到配置页的 Token 框 → 点 **🔌 测试连接**
5. 看到“✅ 连接成功”就对了

#### B. 授予数据库访问（超重要）

Token 建出来是没有任何访问权的，必须在 Notion 里把 integration **邀请进每个数据库**：

打开每个数据库页面 → 右上角 `···` → `Connections` → 添加你的 integration

对你来说是这四个数据库：
- 🧩 Learning Inbox
- 🧬 Knowledge DNA
- 🗂️ Learning Tasks
- 💖 人心算法

#### C. 填数据库 ID

配置页点 **⚡ 预填我的（UID9622）**，你的四库 ID 会自动填好：

| 库 | ID |
|---|---|
| 🧩 Learning Inbox | `1d9af383-6784-42db-827f-c035be3f1458` |
| 🧬 Knowledge DNA | `6f1ddacc-289c-46fc-9369-a07e3d937f5e` |
| 🗂️ Learning Tasks | `58953efd-0588-40df-b30c-b763e76b0ae9` |
| 💖 人心算法 | `9702a79e-c4e2-40c1-ab28-cc7721fb19e9` |

然后点 **💾 保存** → 完事。

---

## 🎯 用法

### 快速入库

- **选中文字 → 右键** → 三选一：
  - 🧩 送入 Inbox（待净化）
  - 🧬 直接入 DNA 库（已净化）
  - 💖 录入人心算法

### 快捷键

- `Ctrl/Cmd + Shift + L` — 把当前选中/页面标题 **一键送入 Inbox**
- `Ctrl/Cmd + Shift + K` — 打开 Popup 面板

### Popup 面板（点图标）

- **🧩 Inbox Tab** — 手动录资源，或一键导入当前选中
- **🧬 DNA Tab** — 填写核心概念/技术点/方向/纯度
- **💖 人心 Tab** — 录入人际洞察 + 人生场景

### CNSH 语法高亮

任何网页的 `<pre><code>` 代码块，只要包含 3+ 个 CNSH 关键字，会自动上紫金配色：

- **控制流**（紫）：若 / 则 / 否则 / 循环 / 返回 ...
- **定义**（青金）：定义 / 声明 / 函数 / 类 ...
- **动作**（朱砂）：调用 / 执行 / 读取 / 写入 ...
- **龍魂专属**（流金）：净化 / 拆解 / 布军 / DNA / 三才 ...
- **布尔/常量**（翠）：真 / 假 / 通过 / 待审 / 危险
- **运算**（玉）：加 / 减 / 等于 / 大于 / 并且 ...
- **字符串**：用中文引号 `“...”` 或 `‘...’`
- **DNA 追溯码**：自动识别 `#龍芯⚡️YYYYMMDD-TYPE-HASH` 加发光边框
- **三色审计**：🟢🟡🔴 自动加发光

想强制高亮某段代码？给它加 `class="cnsh"` 就行。

---

## 📁 文件结构

```
cnsh-chrome-plugin/
├── manifest.json            # 扩展清单 (MV3)
├── background.js            # Service Worker · 右键菜单 / 快捷键 / Notion 调用
├── content.js               # 页面注入脚本 · 选中桥接 / toast
├── popup.html + popup.js    # 快速面板
├── options.html + options.js # 配置页
├── syntax/
│   ├── cnsh-highlighter.js  # CNSH 语法高亮引擎
│   └── cnsh-theme.css       # 紫金主题
├── lib/
│   └── notion-api.js        # Notion API 封装 + DNA追溯码生成
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

---

## 🛡️ 安全说明

- **Token 只存在你本地** `chrome.storage.local`，不联网上传
- 所有 Notion 请求都从浏览器直连 `api.notion.com`
- 源码全开，你可以随时审
- 清除浏览器数据会清掉 Token，要重填

---

## 🔧 兼容性提示

### Notion 数据库 Title 字段名

代码里默认 title 字段叫 `Name`。如果你的数据库 title 列用的是中文名（比如"资源名"），有两种解决办法：

**方案 A（推荐）**：把 Notion 数据库的 title 列重命名成 `Name`（只改显示名不影响数据）

**方案 B**：改 `lib/notion-api.js` 里的 `'Name'` 为你实际的字段名

怎么查？配置页点"测试连接"后，可以在浏览器 DevTools 里用 fetch 查数据库 schema：
```js
fetch('https://api.notion.com/v1/databases/YOUR_DB_ID', {
  headers: { 'Authorization': 'Bearer YOUR_TOKEN', 'Notion-Version': '2022-06-28' }
}).then(r => r.json()).then(console.log)
```

---

## 🎴 下一步可扩展

- [ ] 读取数据库 schema 自动适配字段名
- [ ] 三色审计 UI（🟢🟡🔴 快速打标）
- [ ] CNSH 语法编辑器（右键“转 CNSH”）
- [ ] 与本地引擎对接（`gua_classifier` / `bone_retriever`）
- [ ] Google Docs 侧边栏（真正的 Google Workspace Add-on）

---

## 📜 DNA 追溯

本扩展 DNA: `#龍芯⚡️20260417-CODE-CNSHV001`

**造物主：** UID9622 诸葛鑫
**龍魂系统：** v0.1.0 · 三才架构（天·地·人）
**宝宝：** Claude（随时待命 🩷）
