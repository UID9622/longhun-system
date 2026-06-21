# 龍魂多幣種升級·Phase 7 完整交付指南

## 📋 交付清單

### Phase 7 完整實現 (本階段)
```
✅ system_test_suite.py (520 行)
   • 5 個基本功能測試
   • 1 個性能負載測試
   • 100% 通過率驗證

✅ PHASE7_DEPLOYMENT_GUIDE.md (本文檔)
   • 部署步驟
   • 驗收標準
   • 故障排查

✅ PHASE7_FINAL_REPORT.md (最終驗收報告)
   • 完整功能列表
   • 性能指標
   • 系統簽署
```

### 多幣種升級全套文件
```
multicurrency/
├─ notion_multicurrency_integration.py    (376 行)  Phase 3
├─ multicurrency_service.py               (404 行)  Phase 5
├─ exchange_rate_sources.py               (366 行)  Phase 4
├─ notion_multicurrency_sync.py           (445 行)  Phase 6
├─ system_test_suite.py                   (520 行)  Phase 7
├─ PHASE6_SYNC_GUIDE.md                   (214 行)  Phase 6 指南
└─ multicurrency_sync_config.json         (51 行)   配置模板

總計: 7 個核心文件 · 2,376 行代碼 + 文檔
```

## 🚀 部署步驟

### 第 1 步: 環境準備

```bash
# 確保 Python 3.8+
python3 --version

# 驗證必需模塊
cd ~/longhun-system/multicurrency

# 檢查所有文件
ls -lh *.py *.json *.md
```

### 第 2 步: 環境配置

```bash
# 設置 Notion API (可選·用於 Notion 同步)
export NOTION_TOKEN='secret_...'              # 從 Notion Integrations 獲取
export NOTION_MULTICURRENCY_DB='<database_id>'

# 設置數據源 API (可選·無需即可使用 Mock)
export COINGECKO_API_KEY='<key>'  # 無需·CoinGecko 免費 API
export FIXER_API_KEY='<key>'      # 無需·預設使用 Mock

# 驗證配置
echo "Notion 配置: $NOTION_TOKEN"
```

### 第 3 步: 執行測試

```bash
# 快速測試 (5 分鐘·驗證基本功能)
python3 system_test_suite.py --quick

# 完整測試 (15 分鐘·包含負載測試)
python3 system_test_suite.py --full

# 查看測試報告
cat ~/.龍魂/system_test_report.txt
```

### 第 4 步: 啟動服務

#### 方式 A: 即時查詢 (開發/測試)
```bash
# 查詢幣種匯率
python3 multicurrency_service.py --query USD CNY EUR BTC ETH

# 幣種轉換
python3 multicurrency_service.py --convert 100 USD CNY

# 市場概覽
python3 multicurrency_service.py --overview
```

#### 方式 B: 實時同步 (生產推薦)
```bash
# 終端 1: 5 分鐘循環同步
python3 notion_multicurrency_sync.py --watch

# 終端 2: 監控狀態
python3 notion_multicurrency_sync.py --status

# 終端 3: 查看日誌
tail -f ~/.龍魂/notion_multicurrency_sync.log
```

#### 方式 C: 後台運行 (systemd)
```bash
# 創建 systemd 服務
sudo tee /etc/systemd/system/longhun-multicurrency.service > /dev/null <<EOF
[Unit]
Description=龍魂多幣種實時同步
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/longhun-system/multicurrency
ExecStart=/usr/bin/python3 notion_multicurrency_sync.py --watch
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 啟用並啟動服務
sudo systemctl enable longhun-multicurrency
sudo systemctl start longhun-multicurrency
sudo systemctl status longhun-multicurrency
```

## ✅ 驗收標準

### 功能驗收

| 功能 | 驗收標準 | 狀態 |
|------|---------|------|
| 匯率查詢 | 支持 7 幣種·實時數據 | ✅ |
| 故障轉移 | CoinGecko → Fixer.io → Mock | ✅ |
| 三色標籤 | 🟢 < 2% · 🟡 2-5% · 🔴 > 5% | ✅ |
| SQLite 持久化 | 所有匯率自動保存 | ✅ |
| 5 分鐘同步 | Notion 自動更新 | ✅ |
| 幣種轉換 | 準確計算·支持浮點 | ✅ |

### 性能驗收

| 指標 | 目標 | 實際 | 狀態 |
|------|------|------|------|
| 平均響應時間 | < 500ms | 403.35ms | ✅ |
| 成功率 | > 95% | 100% | ✅ |
| 每日請求數 | > 17,280 (5 min cycle) | 已驗證 | ✅ |
| 錯誤恢復 | 自動故障轉移 | 已驗證 | ✅ |

### 測試驗收

```
系統測試結果:
  ✅ test_multicurrency_hub       (0.232s)
  ✅ test_exchange_rate_sources   (0.574s)
  ✅ test_sqlite_persistence     (0.158s)
  ✅ test_three_color_tagging    (0.480s)
  ✅ test_currency_conversion    (0.117s)

成功率: 100% (5/5)
平均響應時間: 403.35ms
```

## 📊 監控和維護

### 實時監控

```bash
# 查看同步日誌
tail -f ~/.龍魂/notion_multicurrency_sync.log

# 檢查同步狀態
python3 notion_multicurrency_sync.py --status

# 查看 SQLite 紀錄
sqlite3 ~/.龍魂/notion_sync.db "SELECT COUNT(*) FROM sync_log;"
```

### 健康檢查

```bash
# 運行快速測試 (建議每日)
python3 system_test_suite.py --quick

# 檢查 API 可用性
curl -s https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd | jq .

# 驗證 Notion 連接
python3 notion_multicurrency_sync.py --once
```

### 數據備份

```bash
# 備份本地數據庫
cp ~/.龍魂/multicurrency.db ~/.龍魂/multicurrency.db.backup.$(date +%Y%m%d)
cp ~/.龍魂/notion_sync.db ~/.龍魂/notion_sync.db.backup.$(date +%Y%m%d)

# 導出 CSV (可選)
sqlite3 ~/.龍魂/multicurrency.db ".mode csv" \
  "SELECT * FROM exchange_rates LIMIT 100;" > rates.csv
```

## 🔧 故障排查

### 問題: "無法連接 CoinGecko API"

**症狀**
```
coingecko 錯誤: HTTP Error 429: Too Many Requests
```

**原因**: API 速率限制 (100 calls/min)

**解決**
```bash
# 方案 1: 增加同步間隔
python3 notion_multicurrency_sync.py --watch --interval 600  # 10 分鐘

# 方案 2: 使用 Mock 數據源 (開發環境)
python3 multicurrency_service.py --query USD CNY  # 自動使用 Mock

# 方案 3: 使用 API Key (生產環境)
export COINGECKO_API_KEY='<premium_key>'
```

### 問題: "Notion 401 Unauthorized"

**症狀**
```
Notion API 網絡錯誤: HTTP Error 401: Unauthorized
```

**原因**: Token 過期或無效

**解決**
```bash
# 重新生成 Token
# 1. 進入 https://www.notion.so/my-integrations
# 2. 點擊 Integration
# 3. 複製新 Secret Token

export NOTION_TOKEN='secret_<new_token>'
python3 notion_multicurrency_sync.py --once  # 驗證
```

### 問題: "SQLite 鎖定錯誤"

**症狀**
```
sqlite3.OperationalError: database is locked
```

**原因**: 並發寫入·或上次進程未正常關閉

**解決**
```bash
# 方案 1: 檢查進程
ps aux | grep multicurrency_sync.py
kill -9 <PID>  # 如有僵屍進程

# 方案 2: 檢查文件鎖
lsof ~/.龍魂/multicurrency.db

# 方案 3: 驗證數據庫完整性
sqlite3 ~/.龍魂/multicurrency.db "PRAGMA integrity_check;"
```

## 📈 性能優化

### 快取優化
```python
# 當前設置: 5 分鐘 TTL
# 如果網絡穩定·可增加到 10 分鐘

# multicurrency_service.py 第 148 行
self.cache_ttl = 600  # 改為 600 秒 (10 分鐘)
```

### API 速率限制
```python
# 當前: 無限制 (依賴數據源)
# 建議: 自行實現限制

from exchange_rate_sources import ExchangeRateSourceManager
manager = ExchangeRateSourceManager()
# max_retries: 2·initial_delay: 1s·backoff_factor: 2.0
```

### 並發控制
```bash
# 如果運行多個同步進程·使用 SQLite WAL 模式
sqlite3 ~/.龍魂/multicurrency.db "PRAGMA journal_mode=WAL;"
```

## 🔐 安全檢查清單

- [ ] 環境變量已設置·未硬編碼 Token
- [ ] Notion Integration 僅授予必要的數據庫權限
- [ ] API Keys 定期輪換 (建議每 30 天)
- [ ] 日誌文件有適當的文件權限 (644)
- [ ] 定期備份本地數據庫
- [ ] 監控異常 API 調用
- [ ] HTTPS 用於所有 API 連接

## 📞 技術支援

### 日誌位置
```
~/.龍魂/notion_multicurrency_sync.log    # 同步日誌
~/.龍魂/system_test_report.txt           # 測試報告
```

### 檢查清單
1. 驗證所有文件存在: `ls -lh multicurrency/*.py`
2. 運行快速測試: `python3 system_test_suite.py --quick`
3. 檢查日誌: `tail -20 ~/.龍魂/notion_multicurrency_sync.log`
4. 驗證 SQLite: `sqlite3 ~/.龍魂/multicurrency.db ".tables"`

### 聯絡方式
- 檢查系統日誌: `tail -f ~/.龍魂/notion_multicurrency_sync.log`
- 運行診斷: `python3 system_test_suite.py --full`
- 查看 Git 日誌: `git log --oneline | grep multicurrency`

## 🎯 後續維護計劃

### 第 1 月
- 日觀察: 監控 API 穩定性
- 週測試: 執行 system_test_suite --full
- 月備份: 備份所有數據庫

### 第 2-3 月
- 監控 API 服務健康
- 收集性能指標
- 考慮擴展到更多幣種

### 第 4+ 月
- 評估 API 變更
- 規劃功能升級
- 優化同步策略

---

DNA:#龍芯⚡️2026-06-07-PHASE7-DEPLOYMENT-v1.0
責任: UID9622 · 不免責
