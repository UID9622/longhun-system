# 龍魂多幣種·Phase 6 Notion 實時同步指南

## 🎯 目的
自動將實時匯率同步到 Notion 數據庫，5 分鐘更新一次，支持故障轉移和三色標籤。

## 📋 環境配置

### 必需環境變量
```bash
# Notion API 金鑰
export NOTION_TOKEN='secret_...'  # 從 https://www.notion.so/my-integrations 獲取

# Notion 數據庫 ID
export NOTION_MULTICURRENCY_DB='<database_id>'  # 從 Notion 頁面 URL 中提取
```

### 可選環境變量
```bash
# 數據源 API 金鑰 (無 key 時使用 Mock 或上級源)
export COINGECKO_API_KEY='<key>'     # CoinGecko (可選·免費 API 無需)
export FIXER_API_KEY='<key>'         # Fixer.io (可選)
```

## 🚀 快速開始

### 方式 1: 5 分鐘循環同步 (推薦)
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --watch
```

### 方式 2: 執行一次同步
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --once
```

### 方式 3: 查看同步狀態
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --status
```

### 方式 4: 自定義同步間隔 (秒)
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --watch --interval 600
# 每 600 秒 (10 分鐘) 同步一次
```

## 📊 同步內容

### 支持的幣種對 (6 對)
| 幣種對 | 說明 | 數據源 |
|--------|------|--------|
| USD/CNY | 美元→人民幣 | CoinGecko (實時) |
| USD/EUR | 美元→歐元 | CoinGecko (實時) |
| USD/GBP | 美元→英鎊 | CoinGecko (實時) |
| USD/JPY | 美元→日元 | CoinGecko (實時) |
| USD/BTC | 美元→比特幣 | Mock (故障轉移) |
| USD/ETH | 美元→以太坊 | Mock (故障轉移) |

### 更新的 Notion 字段
| 字段 | 類型 | 內容 |
|------|------|------|
| 幣種對 | title | USD/CNY |
| 匯率 | number | 6.84 |
| 基礎幣 | select | USD |
| 目標幣 | select | CNY |
| 狀態 | select | 🟢 正常 / 🟡 波動 / 🔴 異常 |
| 偏離% | number | 0.64 |
| 數據源 | select | coingecko / fixer.io / mock |
| 更新時間 | date | 2026-06-07 |
| 備註 | rich_text | 自動同步·時間戳 |

## 🔄 故障轉移流程

```
查詢 USD/BTC:

1️⃣ CoinGeckoSource.fetch_rate('USD', 'BTC')
   ↓ (失敗·API 無法轉換)
   
2️⃣ FixerIOSource.fetch_rate('USD', 'BTC')
   ↓ (失敗·不支持加密)
   
3️⃣ MockExchangeRateSource.fetch_rate('USD', 'BTC')
   ↓ (成功)
   
✅ 返回: rate=0.000023, source='mock'
```

## 📈 三色標籤邏輯

```
偏離百分比 (deviation) 計算:
|當前匯率 - 基準匯率| / 基準匯率 × 100%

顯示規則:
< 2%   → 🟢 正常 (綠色)
2-5%   → 🟡 波動 (黃色)
> 5%   → 🔴 異常 (紅色)
```

## 📝 日誌位置

```bash
# 實時日誌查看
tail -f ~/.龍魂/notion_multicurrency_sync.log

# 日誌示例
2026-06-07 12:35:26,075 - __main__ - INFO - 🔄 開始多幣種同步
2026-06-07 12:35:26,339 - __main__ - INFO - ✅ 同步成功: USD/CNY = 6.84 (coingecko)
2026-06-07 12:35:27,949 - __main__ - INFO - ✅ 同步完成: 6 成功, 0 失敗
```

## 💾 SQLite 本地紀錄

### sync_log 表
```sql
SELECT * FROM sync_log;
-- pair, notion_page_id, rate, source, sync_time, status
```

### page_mappings 表
```sql
SELECT * FROM page_mappings;
-- pair, notion_page_id, created_time, last_sync
```

查看數據庫:
```bash
sqlite3 ~/.龍魂/notion_sync.db
sqlite> SELECT * FROM sync_log LIMIT 5;
```

## 🛠️ 模塊架構

```
notion_multicurrency_sync.py (445 行)
├─ NotionAPI (Notion API 客戶端)
│  ├─ is_configured(): 檢查配置
│  ├─ query_database(): 查詢頁面
│  ├─ create_page(): 創建頁面
│  └─ update_page(): 更新屬性
│
└─ NotionMulticurrencySyncManager (同步管理)
   ├─ sync_all(): 批量同步
   ├─ sync_rate(): 單對同步
   ├─ _get_or_create_page(): 頁面自動管理
   └─ get_status(): 狀態報告

依賴:
├─ multicurrency_service.py (MultiCurrencyHub)
├─ exchange_rate_sources.py (ExchangeRateSourceManager)
└─ notion_multicurrency_integration.py (配置參考)
```

## ⚠️ 常見問題

### Q: Notion 返回 401 錯誤
**A:** NOTION_TOKEN 已過期或無效·重新生成:
1. 進入 https://www.notion.so/my-integrations
2. 選擇你的 integration
3. 複製新的 Secret Token

### Q: 無法找到數據庫
**A:** 確保:
1. NOTION_MULTICURRENCY_DB 與實際數據庫 ID 相符
2. Integration 有訪問該數據庫的權限
3. 在 Notion 數據庫設置中授予 Integration 權限

### Q: 同步很慢
**A:** 檢查:
1. 網絡連接
2. CoinGecko API 速率限制 (100 calls/min)
3. 增加 --interval 間隔

### Q: 顯示 "Notion 未配置"
**A:** 環境變量未設置:
```bash
# 設置環境變量
export NOTION_TOKEN='...'
export NOTION_MULTICURRENCY_DB='...'

# 驗證
echo $NOTION_TOKEN
echo $NOTION_MULTICURRENCY_DB

# 重新運行
python3 notion_multicurrency_sync.py --status
```

## 🔐 安全最佳實踐

✅ **做**:
- 使用環境變量存儲 API Key
- 定期輪換 Notion Token
- 限制 Integration 的數據庫訪問範圍
- 監控同步日誌的異常

❌ **不做**:
- 在代碼中硬編碼 Token
- 在 Git 中提交 .env 文件
- 分享 NOTION_TOKEN 給他人
- 用生產 Token 進行測試

## 📞 支援

問題排查步驟:
1. 檢查 ~/.龍魂/notion_multicurrency_sync.log
2. 驗證環境變量: `env | grep NOTION`
3. 測試 Notion API: `python3 notion_multicurrency_sync.py --status`
4. 查看 SQLite 紀錄: `sqlite3 ~/.龍魂/notion_sync.db`

---

DNA:#龍芯⚡️2026-06-07-PHASE6-SYNC-GUIDE-v1.0
