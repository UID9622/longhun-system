# 龍魂瀏覽器擴展

本目錄收錄龍魂系統的瀏覽器擴展（Chrome / Edge / 基於 Chromium）。

| 擴展 | 目錄 | 狀態 | 說明 |
|------|------|------|------|
| 龍魂寶寶 · LongHunWidget | `LongHunWidget/` | ✅ 已修復 | MV3 側邊欄 · DNA / 記憶 / 審計 / 五行 / MCP 橋接 |
| CNSH · 龍魂語法引擎 | `cnsh-chrome-plugin/` | ✅ 已納入 | MV3 快速入庫 · Notion Inbox / DNA / 人心算法 |

---

## LongHunWidget 修復記錄（2026-06-16）

1. **manifest.json**
   - 新增 `"alarms"`、`"notifications"` 權限（background.js 使用）
   - 移除 `action.default_popup`，讓圖標點擊正確打開 sidePanel
2. **sidepanel.html**
   - 修復 MCP 面板被錯誤放在 `.content` 外部的結構問題
   - 標籤欄改為 6 列，適配 6 個標籤頁
3. **sidepanel.js**
   - 補上 `hmacSHA256()` 實現，修復 MCP L0 簽到時的未定義錯誤

## CNSH 插件納入（2026-06-16）

- 從 `~/Desktop/cnsh-chrome-plugin` 複製到本目錄
- 已檢查無硬編碼密鑰，Notion Token 與 DB ID 均透過 options 頁面由使用者配置

---

**DNA**:#龍芯⚡️2026-06-16-EXTENSIONS-v1.1
