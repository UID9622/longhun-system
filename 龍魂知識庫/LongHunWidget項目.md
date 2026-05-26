---
title: LongHunWidget·DNA追溯助手項目
tags: [Widget, 項目, iOS, 瀏覽器, S0-S7]
---


# LongHunWidget 項目

**DNA**: #龍芯⚡️20260525|LONGHUNWIDGET-PROJECT|v1.0
**完成度**:
  - iOS 版本：✅ 100%
  - 瀏覽器擴展：🟡 S0 框架完成，S1-S7 待建設

> **注意**：`LongHunWidget`（本地桌面/iOS/macOS）与 `LongHunWidget-Browser`（浏览器插件）构成同一套逻辑体系，前端展示和浏览器内容采集两端协同，密不可分。

---

## 🌊 三节点主干流场 v1.0

- 通心译 × CNSH × LH-ANCHOR
- 本地宝宝读取不变味，边重于节点
- 设计原则：
  1. 本地优先：核心审计、DNA、规则均在本地可见、可追溯
  2. 语义分离：回答层、审计层、追溯层三段式输出
  3. 节点内聚：UI 展示、浏览器采集、人格审计共构同一生态

---

## 1. 项目定位

- 这是一个“本地 AI 审计辅助器”，不是普通浏览器插件。
- 目标是把 AI 回答变成“可追溯、可审计、可落盘”的知识资产。
- 本地端和浏览器端双向配合，保证“本地宝宝读取不变味”。

---

## 2. AI 回答与人格审计闭环

本项目不仅是终端界面与浏览器插件的组合，更是“回答必须有人格审计”的生态规则载体。

- 任何回复必须先经过**人格审计**，不是直接给结论。
- 一个回复，只回答一个问题；不打搅、不打断用户当前流程。
- 回复正文与审计说明必须分开显示：
  - 正文：实际结论 / 建议 / 方案
  - 审计注释：DNA追溯码 + 评语 + 风险/确认状态
- 每次回答的末尾必须附带**DNA追溯码**，并写明审计结论与可信级别。
- 语义不清、未确认、信息不足、未看到关键事实，统一标记为**黑箱**。
- 黑箱不输出最终建议；只能返回“已标记为黑箱，需要进一步确认/补全信息”。
- DNA追溯不是附加显示，而是闭环机制：
  - 任何一条回答都应有一个短小 DNA 码
  - 该 DNA 可追溯到原始规则、审计链与判断源头
  - 十年、百年后仍能可查可验

### 黑箱判定标准

- 未确认来源
- 未验证事实
- 无效输入
- 语义不明确

### 语义分离策略

- 回答内容与审计内容必须明确分层：
  1. 核心回答／方案
  2. 语义补充（必要时）
  3. 审计注释（DNA + 评语 + 风险标签）
- 不允许把审计信息藏在正文里。
- 不允许把普通建议直接写成审计结论。

---

## 3. 版本状态

### 📱 iOS 版本·完全版

**狀態**: ✅ 100% 完成 · 已部署
**部署設備**: iPhone 16 Pro Max

**功能**:
- DNA 掃描（三層檢測）
- 釣鉤分析
- 黑名單檢查
- 證據導出

**位置**: `~/longhun-system/LongHunWidget/`

---

### 🌐 瀏覽器擴展·建設中

**項目結構**:

```
LongHunWidget-Browser/
├── manifest.json
├── package.json
│
├── src/
│   ├── background/
│   │   └── service-worker.js
│   │
│   ├── content/
│   │   ├── dna-detector.js
│   │   ├── watermark-scanner.js
│   │   └── hook-detector.js
│   │
│   ├── popup/
│   │   ├── panel.html
│   │   └── panel.js
│   │
│   └── guards/
│       ├── boundary-engine.js
│       └── permission-check.js
│
├── public/
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
│
├── dist/
├── tests/
└── S0_PROJECT_README.md
```

---

## 4. 开发阶段 (S0-S7)

### S0：框架搭建 ✅ 完成

**已交付**:
- manifest.json
- service-worker.js
- dna-detector.js
- panel.html
- panel.js
- package.json
- 文档结构

**核心功能**:
- 右鍵菜單
- DNA 三層檢測
- 本地存儲
- Chrome 開發版可加載

### S1：DNA 嵌入器 ⏳ 待實現

**目標**: 在發佈時自動打水印

**任務**:
- [ ] 檢測 CSDN 編輯器
- [ ] 檢測知乎編輯器
- [ ] 檢測掘金編輯器
- [ ] 發佈時自動觸發嵌入
- [ ] 生成帶水印版本

**文件**: `src/content/watermark-scanner.js`

### S2：監聽與指令 ⏳ 待實現

**目標**: 補齊 18+11 類釣鉤檢測

**任務**:
- [ ] 實現剩餘 9 類寫作釣鉤
- [ ] 實現 11 類論證手法
- [ ] 優化評分算法

**文件**: `src/content/hook-detector.js`

### S3：三層邊界引擎 ⏳ 待實現

**目標**: 綠/黃/紅三層權限控制

**文件**:
- `src/guards/boundary-engine.js`
- `src/guards/permission-check.js`

### S4：隱私鐵律 ⏳ 待實現

**任務**:
- [ ] 黑名單敏感字段
- [ ] 本地加密存儲
- [ ] 定期清理
- [ ] 離線驗證

### S5：自測與審計 ⏳ 待實現

**任務**:
- [ ] 單元測試
- [ ] 集成測試
- [ ] 審計規範檢查
- [ ] 性能測試

### S6：打包 ⏳ 待實現

**輸出**: `dist/longhun-widget-v1.0.crx`

### S7：發佈 ⏳ 待實現

**目標**: 上傳 Chrome Web Store

---

## 5. 核心模塊概览

### manifest.json

```json
{
  "manifest_version": 3,
  "name": "🐉 龍魂宝宝·DNA追溯助手",
  "version": "1.0.0",
  "permissions": [
    "activeTab",
    "scripting",
    "tabs",
    "storage",
    "webRequest",
    "clipboardRead",
    "clipboardWrite",
    "contextMenus",
    "notifications",
    "downloads"
  ],
  "background": {
    "service_worker": "src/background/service-worker.js"
  },
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["src/content/dna-detector.js"]
  }],
  "action": {
    "default_popup": "src/popup/panel.html",
    "default_title": "🐉 龍魂DNA追溯助手"
  },
  "context_menus": [
    { "id": "mark-infringement", "title": "🚨 標記侵權" },
    { "id": "add-dna", "title": "✍️ 添加DNA簽名" },
    { "id": "copy-dna", "title": "📋 複製DNA" },
    { "id": "export-evidence", "title": "📦 導出證據包" }
  ]
}
```

### service-worker.js

**職責**:
- 管理右鍵菜單事件
- 與 DNA API 通信
- 管理本地存儲
- 生成通知
- 導出證據包

**主要函數**:
```javascript
setupContextMenus()
markAsInfringement(tab)
addDNAToPage(tab)
copyPageDNA(tab)
exportEvidence(tab)
saveEvidence(evidence)
addToRegistry(dna, url)
addToBlacklist(url, domain)
```

**已修復**（2026-05-25）:
- ✅ 移除不存在的 welcome.html
- ✅ 修復 Service Worker 中的 navigator.clipboard
- ✅ onInstalled 時調用 setupContextMenus()

### dna-detector.js

**職責**:
- 三層水印檢測
- 釣鉤識別
- DNA 驗證
- DNA 嵌入

**接口**:
```javascript
detectExplicitWatermark()
detectFixedPointWatermark()
detectZeroWidthWatermark()
scanAll()
verifyDNA(dna)
embedDNAToPage(dna)
detectHooks(doc)
```

### panel.html + panel.js

**UI 佈局**:
- 📊 狀態欄
- 🔍 快速掃描區
- 📋 DNA 顯示區
- 🎣 釣鉤分析區
- 🚀 快速操作區
- 📦 證據管理區

**已修復**（2026-05-25）:
- ✅ 複製 DNA 改由 content script 執行
- ✅ panel.js DOM 操作已修復

---

## 6. 立刻可用的操作

### 加載開發版

```
① chrome://extensions
② 開啟開發者模式
③ 加載已解壓擴展
④ 選擇 ~/longhun-system/LongHunWidget-Browser/
```

### 測試步驟

1. 打開任意網頁
2. 右鍵 → 龍魂 菜單
3. 檢查 4 個菜單項
4. DevTools → Application → Local Storage

---

## 7. 集成點

### 與 DNA 流水線的連接

```
Widget 右鍵菜單
  ├─ 標記侵權 → Step 2 檢測
  ├─ 添加 DNA → Step 1 發佈
  ├─ 複製 DNA → 剪貼板
  └─ 導出證據 → JSON 包
```

### API 端點（待部署）

```
POST http://localhost:5000/dna/generate
POST http://localhost:5000/dna/verify
POST http://localhost:5000/scan/watermark
POST http://localhost:5000/evidence/save
```

---

## 8. 檢查清單

- [x] 項目結構建立
- [x] manifest.json 完成
- [x] service-worker.js 完成
- [x] dna-detector.js 完成
- [x] panel.html/js 完成
- [x] 文檔完善
- [x] Chrome 開發版可加載
- [ ] watermark-scanner.js
- [ ] 平台編輯器檢測
- [ ] 自動發佈觸發
- [ ] 釣鉤檢測補全
- [ ] 三層邊界引擎
- [ ] 本地隱私保護
- [ ] 單元/集成測試
- [ ] .crx 打包
- [ ] 上傳商店

---

## 9. 安全與隱私

✅ 本地優先：chrome.storage.local
✅ 零追蹤：無 Google Analytics
✅ 離線可用
✅ 敏感字段保護：password/payment

---


## 10. 自动化归档·批量签名·Notion同步

### 10.1 自动提取DNA/颜色/元数据
- 支持自动从文件名、内容、元数据区块提取DNA追溯码、数字根、三色标签。
- 可扩展正则/脚本，批量处理归档目录下所有文件。
- DNA提取示例：
  - 文件名如 `xxx_DNA-xxxx.md` 自动识别DNA字段
  - 文件头部 `DNA: #龍芯⚡️...` 自动解析
- 颜色/三色：按数字根/规则自动分配 🟢/🟡/🔴

### 10.2 支持附件归档
- 支持将图片、PDF、音频等作为Notion页面附件上传，归档时自动关联DNA/元数据。
- 附件与主文档同一追溯链，便于证据管理。

### 10.3 GPG批量签名
- 提供Shell批量签名脚本，对所有归档/追溯文件自动加数字签名，保证可验证性。
- 签名流程：
  1. 生成/导入GPG密钥对
  2. `for f in *.md; do gpg --output "$f.sig" --detach-sign "$f"; done`
  3. 验证：`gpg --verify xxx.md.sig xxx.md`
- 支持批量验签、签名链归档。

### 10.4 Notion自动同步
- Python脚本支持批量上传归档/追溯文件，自动写入DNA/颜色/备注/附件。
- 支持定时同步、本地→Notion主权知识库一体化。
- 可扩展为多数据库/多页面同步。

### 10.5 自动化脚本与接口示例
- Python: notion-client 批量归档/同步
- Shell: GPG批量签名/验签
- C++: 可扩展为本地归档/元数据提取工具
- 详见 `~/longhun-system/工具/`、`~/longhun-system/龍魂知識庫/DNA流水線自動化.md`

---

## 11. 主权声明与合规性

- 本项目所有归档、追溯、同步、签名均在本地完成，主权归属UID9622。
- 不依赖第三方云端存储，所有数据可本地验证、可追溯、可回滚。
- GPG签名、DNA追溯、Notion同步均有完整日志与责任链。

---

## 12. 版本追溯与变更记录

- 2026-05-25 v1.0 初版结构整理
- 2026-05-26 v1.1 增补自动化归档、批量签名、Notion同步、主权声明等区块

---

## 13. 常见问题FAQ

**Q: 如何批量归档并同步到Notion？**
A: 运行Python脚本，自动提取DNA/颜色/备注，批量上传到指定数据库。

**Q: 如何批量GPG签名/验签？**
A: 见10.3区块，Shell一行命令即可。

**Q: 附件如何归档？**
A: 支持图片/PDF/音频等自动上传为Notion页面附件。

**Q: DNA/颜色如何自动提取？**
A: 支持正则/脚本自动识别，详见10.1区块。

---

## 14. 相关文件与子页

- `~/longhun-system/LongHunWidget-Browser/S0_PROJECT_README.md`
- `~/longhun-system/LongHunWidget-Browser/src/`
- `~/longhun-system/龍魂知識庫/DNA追溯系統.md`
- `~/longhun-system/龍魂知識庫/DNA流水線自動化.md`
- `~/longhun-system/龍魂知識庫/快速操作.md`
- `~/longhun-system/龍魂知識庫/人格自動化_決策矩陣.md`
- `~/longhun-system/龍魂知識庫/熔断系統_推演報告.md`
- `~/longhun-system/龍魂知識庫/索引.md`

---

DNA: `#龍芯⚡️20260526|LONGHUNWIDGET-PROJECT|v1.1`
責任: UID9622·不免責

---

DNA: `#龍芯⚡️20260525|LONGHUNWIDGET-PROJECT|v1.0`
責任: UID9622·不免責
