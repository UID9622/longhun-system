---
name: longhun-cloud-notion
description: '龍魂Notion集成 v5.0 — Notion API雙向同步+自動化週報+DNA校驗+訓練進度。 支持周檢查自動化、協議完整性驗證、團隊統計。
  API端點: http://api:8443/notion/ 當需要Notion同步、週報生成、DNA校驗、進度統計時觸發。

  '
metadata:
  author: 龍魂體系
  tags:
  - notion
  - sync
  - weekly-report
  - dna-check
  - team-stats
  - cloud
  version: 5.0.0
  dna: '#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-NOTION-v5.0'
  protocol_version: '5.0'
  api_endpoint: http://api:8443/notion/
  id: longhun-cloud-notion
  trigger:
    keywords:
    - cloudnotion
    - 龍魂Notion集成
    - v5.0
    - Notion
    - API雙向同步+自動化週報+DNA校驗+訓練進度。
    - 支持周檢查自動化
    context: longhun-cloud-notion 相关操作
  category: general
---
# 龍魂Notion同步器 v5.0

## 1. 技能概述 (Skill Overview)

**龍魂Notion同步器**是龍魂體系雲端技能群的Notion集成核心模組。提供Notion API雙向同步、自動化週報生成、DNA完整性校驗、團隊訓練進度統計等功能。

**核心價值**：
- 打通龍魂體系與Notion工作空間的數據通道
- 自動化週報生成，減少手動統計負擔
- DNA校驗鏈確保數據完整性與血統追溯
- 三色審計系統標記操作安全等級

**適用場景**：
- 需要將龍魂任務數據同步至Notion數據庫
- 需要自動化生成團隊週報
- 需要驗證數據完整性與DNA追溯
- 需要統計團隊成員訓練進度

## 2. DNA追溯 (DNA Traceability)

```
血統鏈: 龍魂體系 → 雲端技能群 → Notion集成模組 → longhun-cloud-notion
DNA標記: #龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-NOTION-v5.0
版本血統: v1.0(原型) → v2.0(基礎同步) → v3.0(週報生成) → v4.0(DNA校驗) → v5.0(完整集成)
父技能: longhun-core-ethics (君子協議), longhun-cloud-base (雲端基礎)
創建日期: 2026-06-19
三色審計: 🔴禁止-數據偽造 🟡小心-API限流 🟢允許-安全同步
```

## 3. 觸發條件 (Activation Conditions)

**顯式觸發**：
- 用戶輸入包含「Notion同步」「同步到Notion」「Notion更新」
- 用戶輸入包含「生成週報」「週報」「weekly report」
- 用戶輸入包含「DNA校驗」「校驗數據」「檢查完整性」
- 用戶輸入包含「團隊統計」「訓練進度」「進度統計」
- 用戶輸入包含「啟動定時任務」「cron」「自動同步」

**隱式觸發**：
- 定時任務到達執行時間
- 其他技能調用API端點
- 數據變更事件通知

**權限要求**：
- 需要 `NOTION_API_KEY` 環境變量或配置文件
- 需要有效的Notion數據庫ID

## 4. 執行流程 (Execution Flow)

### 4.1 雙向同步流程
```
[開始]
  ↓
[讀取配置] → API密鑰 + 數據庫ID
  ↓
[連接Notion API] → 驗證憑證
  ↓
[拉取Notion數據] → 查詢數據庫所有頁面
  ↓
[生成DNA標記] → 為每條數據生成SHA-256哈希
  ↓
[比較本地快取] → 檢測變更
  ↓
[解決衝突] → 以時間戳為準
  ↓
[推送本地變更] → 更新Notion數據
  ↓
[保存快取] → 更新本地狀態
  ↓
[生成同步報告]
  ↓
[結束]
```

### 4.2 週報生成流程
```
[開始]
  ↓
[確定週次範圍] → 本週一起始日至本週日
  ↓
[拉取任務數據] → 從Notion或本地快取
  ↓
[分類任務] → 已完成 / 進行中 / 阻塞
  ↓
[統計團隊數據] → 成員完成率 + 技能掌握
  ↓
[生成DNA校驗摘要]
  ↓
[渲染Markdown週報]
  ↓
[保存週報文件] → JSON + Markdown
  ↓
[結束]
```

### 4.3 DNA校驗流程
```
[開始]
  ↓
[讀取所有記錄] → 從快取或Notion
  ↓
[逐條驗證] → 重新計算SHA-256哈希
  ↓
[比較哈希值] → 匹配=已驗證 / 不匹配=異常
  ↓
[標記狀態] → 🟢已驗證 / 🔴異常 / 🟡待驗證
  ↓
[生成校驗報告] → 完整性分數
  ↓
[結束]
```

## 5. 輸入規範 (Input Schema)

### 5.1 同步命令輸入
```json
{
  "命令": "sync",
  "參數": {
    "db_id": "string (可選, 默認從配置讀取)",
    "api_key": "string (可選, 優先環境變量)"
  }
}
```

### 5.2 週報命令輸入
```json
{
  "命令": "weekly",
  "參數": {
    "輸出格式": "json | md (默認兩種都生成)"
  }
}
```

### 5.3 DNA校驗輸入
```json
{
  "命令": "dna-check",
  "參數": {
    "檢查範圍": "all | 指定數據類型 (默認all)"
  }
}
```

### 5.4 統計命令輸入
```json
{
  "命令": "stats",
  "參數": {
    "團隊ID": "string (可選)"
  }
}
```

## 6. 輸出規範 (Output Schema)

### 6.1 同步輸出
```json
{
  "同步時間": "ISO8601時間戳",
  "數據類型": "任務|週報|團隊",
  "拉取數量": 0,
  "DNA標記": "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-NOTION-v5.0",
  "狀態": "成功|失敗",
  "詳情": {}
}
```

### 6.2 週報輸出 (Markdown格式)
```markdown
# 📊 龍魂週報 — 2026-W25
> **週期**: 2026-06-15 ~ 2026-06-21
> **DNA**: `#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-NOTION-v5.0`
## ✅ 已完成項目
## 🔄 進行中項目
## 🚧 阻塞項目
## 👥 團隊統計
## 🔐 DNA 校驗
```

### 6.3 DNA校驗輸出
```json
{
  "DNA標記": "#龍芯⚡️...",
  "校驗時間": "ISO8601時間戳",
  "總記錄數": 0,
  "已驗證": 0,
  "異常": 0,
  "待驗證": 0,
  "完整性分數": 100.0
}
```

### 6.4 統計輸出
```json
{
  "團隊名稱": "龍魂團隊",
  "成員總數": 0,
  "本週總完成任務": 0,
  "平均完成率": 0.0,
  "成員詳情": {}
}
```

## 7. API接口 (API Endpoints)

### 7.1 端點列表

| 方法 | 端點 | 描述 |
|------|------|------|
| GET | `/notion/health` | 健康檢查 |
| POST | `/notion/sync` | 執行雙向同步 |
| GET | `/notion/weekly` | 獲取最新週報 |
| POST | `/notion/weekly` | 生成新週報 |
| GET | `/notion/dna-check` | DNA完整性校驗 |
| GET | `/notion/stats` | 團隊訓練統計 |
| GET | `/notion/audit` | 獲取審計日誌 |

### 7.2 健康檢查
**請求**: `GET /notion/health`
**響應**:
```json
{
  "狀態": "健康",
  "服務": "龍魂Notion同步器",
  "版本": "5.0.0",
  "DNA": "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-NOTION-v5.0"
}
```

### 7.3 執行同步
**請求**: `POST /notion/sync`
**響應**: 同步報告JSON

### 7.4 獲取週報
**請求**: `GET /notion/weekly`
**響應**: 最新週報JSON

### 7.5 DNA校驗
**請求**: `GET /notion/dna-check`
**響應**: 校驗報告JSON

## 8. 依賴清單 (Dependencies)

### 8.1 Python標準庫
- `os` — 環境變量與路徑操作
- `sys` — 系統接口
- `json` — JSON序列化
- `time` — 時間與速率限制
- `hashlib` — SHA-256 DNA哈希
- `logging` — 日誌記錄
- `argparse` — 命令行解析
- `dataclasses` — 數據模型
- `pathlib` — 路徑操作
- `datetime` — 日期時間處理
- `typing` — 類型提示
- `functools` — 函數工具
- `http.server` — API服務器 (僅serve模式)

### 8.2 第三方庫
- `requests` — Notion API HTTP調用

### 8.3 環境依賴
- Python 3.8+
- Notion Integration Token
- Notion Database ID

## 9. 君子協議 (Junzi Protocol)

### 9.1 數據真實性承諾
```
吾承諾:
1. 不偽造Notion API響應數據
2. 不篡改DNA校驗哈希值
3. 不虛報團隊成員進度
4. 如實記錄同步狀態與錯誤
5. 透明公開所有操作日誌
```

### 9.2 隱私保護
```
吾承諾:
1. API密鑰僅存儲於本地配置文件
2. 不上傳敏感數據至未授權服務
3. 日誌中不記錄完整API密鑰
4. 團隊數據僅用於內部統計
```

### 9.3 API使用規範
```
吾承諾:
1. 遵守Notion API速率限制 (3 req/sec)
2. 合理緩存減少API調用
3. 錯誤時重試不超過3次
4. 不使用API進行未授權操作
```

### 9.4 三色審計準則
| 顏色 | 含義 | 操作 |
|------|------|------|
| 🔴 禁止 | 數據偽造、未授權訪問、完整性破壞 | 立即阻止並報警 |
| 🟡 小心 | API限流、網路波動、配置異常 | 記錄警告並重試 |
| 🟢 允許 | 正常同步、成功操作、安全狀態 | 記錄並繼續 |

## 10. 錯誤處理 (Error Handling)

### 10.1 錯誤碼定義

| 錯誤碼 | 描述 | 處理建議 |
|--------|------|----------|
| NOTION_AUTH_001 | API密鑰無效或過期 | 檢查NOTION_API_KEY環境變量 |
| NOTION_DB_002 | 數據庫ID不存在或無權限 | 確認Integration已共享數據庫 |
| NOTION_RATE_003 | API速率限制觸發 | 等待後自動重試 |
| NOTION_NET_004 | 網路連接失敗 | 檢查網路連接 |
| DNA_INVALID_005 | DNA校驗失敗 | 數據可能被篡改，需人工核查 |
| CONFIG_006 | 配置文件缺失或無效 | 運行初始化生成默認配置 |
| SYNC_007 | 同步過程中發生衝突 | 查看日誌手動解決衝突 |

### 10.2 重試策略
- API速率限制: 等待Retry-After秒後重試
- 網路錯誤: 指數退避 (1s → 2s → 4s → 8s)，最多3次
- 其他錯誤: 記錄並終止當前操作

## 11. 參考資料 (References)

### 11.1 內部參考
- `references/WEEK_EXECUTION_PLAN.md` — 週執行計劃規範
- `references/NOTION_SYNC_SPEC.md` — Notion同步規範
- `references/DNA_CHECK_PROTOCOL.md` — DNA校驗協議

### 11.2 外部參考
- Notion API文檔: https://developers.notion.com/
- Notion API版本: 2022-06-28
- 速率限制: 3 requests per second

### 11.3 相關技能
- `longhun-core-ethics` — 君子協議核心
- `longhun-cloud-base` — 雲端基礎設施
- `longhun-cloud-monitor` — 監控告警

## 12. 更新日誌 (Changelog)

### v5.0.0 (2026-06-19)
- ✅ 完整Notion API雙向同步
- ✅ 自動化週報生成 (JSON + Markdown)
- ✅ DNA校驗鏈驗證系統
- ✅ 團隊訓練進度統計
- ✅ Cron定時任務排程
- ✅ HTTP API服務 (端口8443)
- ✅ 三色審計日誌系統
- ✅ CNSH中文編程規範
- ✅ 君子協議集成

### v4.0.0 (2026-05-15)
- 新增DNA校驗功能
- 新增SHA-256完整性驗證

### v3.0.0 (2026-04-01)
- 新增自動化週報生成
- 新增Markdown輸出格式

### v2.0.0 (2026-02-20)
- 新增雙向同步引擎
- 新增本地快取機制

### v1.0.0 (2026-01-10)
- 初始版本，基礎Notion查詢
