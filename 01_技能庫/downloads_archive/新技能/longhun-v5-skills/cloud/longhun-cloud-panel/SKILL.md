---
name: longhun-cloud-panel
description: >
  龍魂操作台 v5.0 — FastAPI统一API+Web UI，10项Skill+底座能力联动。
  本地技能与云端技能的统一入口，请求路由分发，health check监控。
  API端点: http://api:8443/panel/
  当需要统一操作台、API网关、Skill联动调度、Web UI时触发。
---

# 龍魂操作台 (longhun-cloud-panel)

## Overview

龍魂操作台是龍魂體系 v5.0 的統一 API 網關與 Web 管理界面。它集成了十項 Skill 的聯動調度、三大底座能力（龍盾安全、CNSH 中文編程、融合審計）以及完整的 DNA 追溯與三色審計系統。

**當觸發條件**:
- 需要統一操作台管理多項 Skill
- 需要 API 網關進行請求路由分發
- 需要 Web UI 可視化管理界面
- 需要 health check 監控系統
- 需要龍盾安全認證與 CNSH 規範檢查
- 需要融合審計日誌記錄

## Core Capabilities

### 1. 十項 Skill 聯動管理

操作台註冊並管理全部十項龍魂 Skill:

| 編號 | 名稱 | 類型 | 核心功能 |
|------|------|------|----------|
| 1 | algorithmic-art | HTML | Perlin 噪聲·Flow Field·粒子系統·實時控制 |
| 2 | brand-guidelines | HTML | 品牌色彩·字體規範·視覺元素·設計規範 |
| 3 | canvas-design | HTML | Canvas 繪畫·圖層系統·濾鏡效果·實時渲染 |
| 4 | doc-coauthoring | HTML | 實時編輯·版本控制·評論系統·權限管理 |
| 5 | internal-comms | HTML | 消息通知·任務分配·進度追蹤·團隊協作 |
| 6 | mcp-builder | Python | FastMCP 集成·自動代碼生成·Docker 支持 |
| 7 | skill-creator | Python | 模板生成·框架搭建·配置向導·驗證檢查 |
| 8 | slack-gif-creator | Python | GIF 動畫生成·Slack 發送·自動化流程 |
| 9 | theme-factory | Python | 色彩系統·字體組合·主題導出·CSS 生成 |
| 10 | web-artifacts-builder | Python | React 組件·HTML 模板·CSS 框架·即時預覽 |

**API 端點**:
```
GET  /panel/api/v1/skills              → 列出所有 Skills
GET  /panel/api/v1/skills/{id}         → 獲取 Skill 詳情
GET  /panel/api/v1/skills/{id}/content → 獲取代碼內容
POST /panel/api/v1/skills/{id}/execute → 執行 Python Skill
GET  /panel/api/v1/config/export       → 導出配置
```

### 2. 底座能力接口

三大底座能力模塊通過統一接口調用:

#### 龍盾安全 (longhun-shield)
- 身份認證 · 權限控制 · 請求簽名 · 流量限制 · 入侵檢測
- 端點: `POST /panel/api/v1/foundation/call`
- 操作: 認證 · 授權 · 簽名驗證 · 流量檢查

#### CNSH 中文編程 (cnsh-core)
- 中文變量名 · 繁體龍字 · DNA 追溯 · 三色審計 · 君子協議
- 端點: `POST /panel/api/v1/foundation/call`
- 操作: 規範檢查 · DNA 生成 · 審計報告

#### 融合審計 (fusion-audit)
- 日誌記錄 · 行為追蹤 · 異常告警 · 合規檢查 · 報表生成
- 端點: `POST /panel/api/v1/foundation/call`
- 操作: 日誌查詢 · 行為分析 · 報表生成 · 合規檢查

### 3. 健康監控

```
GET /health                          → 基礎健康檢查
GET /panel/api/v1/health/detailed    → 詳細健康狀態
```

響應包含: 狀態 · 版本 · DNA · 技能總數 · 底座模塊數 · 運行時長

### 4. DNA 追溯系統

```
GET /panel/api/v1/dna         → DNA 信息
GET /panel/api/v1/dna/chain   → 完整追溯鏈
```

DNA 標記: `#龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0`

### 5. 三色審計日誌

```
GET /panel/api/v1/audit/logs?限制=100&級別=信息
```

三色標準:
- 🔴 紅色 = 錯誤 · 異常 · 嚴重事件
- 🟡 黃色 = 警告 · 需要注意
- 🟢 綠色 = 信息 · 正常操作

### 6. Web UI 管理界面

訪問 `http://api:8443/panel/` 進入可視化操作台:
- 技能卡片展示 (10 項 Skill 狀態)
- 底座模塊監控 (3 大底座能力)
- API 文檔入口 (Swagger + ReDoc)
- 系統統計面板

## Workflow Decision Tree

```
用戶請求 → 操作台接收
    ↓
審計中間件攔截 → DNA 追溯標記 → 三色審計記錄
    ↓
請求類型判斷:
    ├── /health          → 健康檢查響應
    ├── /panel/          → Web UI 渲染
    ├── /panel/api/v1/skills/*   → Skill 管理/執行
    ├── /panel/api/v1/foundation/* → 底座能力調用
    ├── /panel/api/v1/dna/*      → DNA 追溯查詢
    ├── /panel/api/v1/audit/*    → 審計日誌查詢
    └── /panel/api/v1/config/*   → 配置管理
    ↓
響應返回 (含 X-Longhun-DNA 頭)
```

## Scripts

### `scripts/操作台API.py`

主服務入口。包含:
- FastAPI 應用創建與配置
- 十項 Skill 註冊表定義
- 三大底座能力模塊定義
- 三色審計日誌系統
- DNA 追溯中間件
- 全部 API 路由處理器
- Web UI HTML 渲染
- 系統啟動/關閉事件

**啟動方式**:
```bash
python scripts/操作台API.py
# 或
uvicorn scripts.操作台API:應用 --host 0.0.0.0 --port 8443
```

**環境變量**:
| 變量 | 默認值 | 說明 |
|------|--------|------|
| PANEL_PORT | 8443 | 服務端口 |
| PANEL_HOST | 0.0.0.0 | 監聽地址 |
| PANEL_RELOAD | false | 熱重載 |

## Resources

### references/

- `API規範.md` — 完整 API 端點規範與請求/響應示例
- `底座能力說明.md` — 龍盾 + CNSH + 融合審計詳細文檔

### assets/

- `favicon.ico` — 龍魂操作台圖標
- `logo.png` — 龍魂 Logo

## DNA 追溯鏈

```
#龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0
├── 面板名稱: 龍魂操作台
├── 面板標識: longhun-cloud-panel
├── 版本: 5.0.0
├── 責任人: UID9622
├── 君子協議: 君子協議·不免責
├── 技能數量: 10
├── 底座模塊: 3 (龍盾安全 + CNSH中文編程 + 融合審計)
└── CNSH規範: 全部啟用 ✅
    ├── 中文變量名 ✅
    ├── 繁體龍字 ✅
    ├── DNA追溯 ✅
    ├── 三色審計 ✅
    └── 君子協議 ✅
```

## 技術規格

| 項目 | 規格 |
|------|------|
| 框架 | FastAPI + Uvicorn |
| Python | 3.9+ |
| API 文檔 | Swagger UI + ReDoc (自動生成) |
| CORS | 已啟用 (allow_origins=["*"]) |
| 日誌 | Python logging + 三色審計 |
| 數據模型 | Pydantic BaseModel |
| 運行時長追蹤 | time.time() 啟動基準 |
