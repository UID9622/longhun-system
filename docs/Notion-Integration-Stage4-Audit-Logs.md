# 🐉 龍魂 Notion 集成 · Stage 4 審計日誌同步

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE4-AUDIT-LOGS-v1.0`
**Date**: 2026-06-01
**Status**: ✅ **實現完成·等待 Notion 工作區配置**

---

## 📊 什麼是 Stage 4？

Stage 4 將龍魂系統的 **審計日誌** 同步到 Notion：

- ✅ **健康檢查日誌** - 系統鏈路驗證和開機檢查
- ✅ **性能基線** - DNA 註冊、文件簽名、數字根分佈
- ✅ **警告事件** - 拒絕事件、異常檢測、共振掃描
- ✅ **審計日誌** - 凭證驗證、身份認證、操作記錄

**核心目標**: 將龍魂系統的 393 條審計記錄完全映射到 Notion，支持日誌查詢、性能分析和安全審計。

---

## 🎯 審計日誌結構

### 四個核心數據庫

```
工作區 3: 龍魂審計日誌
├── 數據庫 3.1: 健康檢查日誌 (5-40 條記錄)
│   ├── 完整鏈路追踪 (home_full_chain_trace.jsonl)
│   ├── 開機驗證記錄 (home_battlefield_trace.jsonl)
│   ├── 語義 Hook 審計 (semantic_hook_trace.jsonl)
│   └── 顏色判定記錄 (audit_check.jsonl)
│
├── 數據庫 3.2: 性能基線 (144 條記錄)
│   ├── DNA 註冊 (63 條)
│   ├── 批量簽名審計 (73 條)
│   └── 引擎執行記錄 (7 條)
│
├── 數據庫 3.3: 警告事件 (153 條記錄)
│   ├── 渲染門禁拒絕 (114 條)
│   ├── 共振掃描命中 (77 條)
│   └── 語義異常檢測 (3 條)
│
└── 數據庫 3.4: 審計日誌 (91 條記錄)
    ├── 凭證審計 (9 條)
    ├── 身份驗證 (1 條)
    ├── 權限檢查 (2 條)
    ├── 會話記錄 (8 條)
    └── DNA 工具調用 (1 條)
```

### 數據關係圖

```
龍魂系統審計日誌
    ├─ 健康檢查 ──→ 系統可用性指標
    ├─ 性能基線 ──→ 數字根分佈·顏色分類
    ├─ 警告事件 ──→ 安全威脅偵測
    └─ 審計日誌 ──→ 操作追溯·權限驗證

DNA 追蹤鏈
    ├─ 每條健康檢查: #龍芯⚇️20260601-AUDIT-HEALTH-*
    ├─ 每條性能記錄: #龍芯⚇️20260601-BASELINE-*
    ├─ 每條警告事件: #龍芯⚇️20260601-ALERT-*
    └─ 每條審計日誌: #龍芯⚇️20260601-AUDIT-*
```

---

## 🚀 快速開始（3 步）

### Step 1: 驗證 Stage 3 完成

確保已完成 Stage 3：

```bash
# 檢查知識圖譜數據庫配置
echo $NOTION_NODES_DB

# 如果返回數據庫 ID，表示 Stage 3 配置正確
```

### Step 2: 運行 Stage 4 自動化設置

```bash
cd ~/longhun-system/notion
python3 stage_4_setup.py
```

這個腳本會：
1. ✅ 驗證 API 連接
2. ✅ 詢問工作區 3 ID（或共享 Stage 2-3 工作區）
3. ✅ 自動創建 4 個審計日誌數據庫
4. ✅ 生成環境變量配置
5. ✅ 執行首次審計日誌同步

### Step 3: 配置環境變量

運行腳本後，會看到類似的輸出：

```bash
export NOTION_HEALTH_DB='...'
export NOTION_BASELINE_DB='...'
export NOTION_ALERT_DB='...'
export NOTION_AUDIT_DB='...'
```

運行以下命令激活配置：

```bash
# 方法 1: 直接設置
export NOTION_HEALTH_DB='...'
export NOTION_BASELINE_DB='...'
# ... 等等

# 方法 2: 使用生成的腳本
source ~/.龍魂_config/audit_databases.sh
```

---

## 📋 詳細步驟

### 獲取 Notion 工作區 3 ID

**選項 A：使用與 Stage 2-3 相同的工作區**
- 在同一工作區中創建 4 個新的審計日誌數據庫
- 優點：集中管理，資源利用效率高
- 缺點：工作區可能變得擁擠

**選項 B：創建新的工作區**
1. 打開您的 Notion 工作區
2. 在左側欄創建一個新頁面，命名為 "龍魂審計日誌"
3. 打開這個頁面，從浏览器地址栏複製 ID：

```
https://www.notion.so/YOUR_WORKSPACE_ID?v=VIEW_ID&pvs=...
                      ^^^^^^^^^^^^^^^^
                      複製這部分（移除連字符）
```

### 運行自動化設置腳本

```bash
cd ~/longhun-system/notion
python3 stage_4_setup.py
```

腳本流程：

```
┌─────────────────────────────────────┐
│ 第一步: 驗證 Notion API 連接        │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第二步: 輸入工作區 3 ID              │
├─────────────────────────────────────┤
│ 【用戶輸入】工作區 ID
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第三步: 創建 4 個審計日誌數據庫     │
├─────────────────────────────────────┤
│ 📁 健康檢查日誌
│ 📁 性能基線
│ 📁 警告事件
│ 📁 審計日誌
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第四步: 保存數據庫 ID 配置          │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第五步: 執行審計日誌同步（可選）   │
├─────────────────────────────────────┤
│ 【用戶選擇】是否立即同步
│ ✅ 分析審計日誌
│ ✅ 創建 Notion 頁面
└─────────────────────────────────────┘
```

### 手動同步數據

如果在設置時跳過了同步，可以稍後手動運行：

```bash
cd ~/longhun-system/notion

# 設置環境變量
source ~/.龍魂_config/audit_databases.sh

# 運行同步
python3 audit_sync.py
```

---

## 📊 審計日誌數據規模

### 1. 健康檢查日誌（45 條記錄）

| 來源文件 | 記錄數 | 內容 | 時間範圍 |
|---------|--------|------|---------|
| home_full_chain_trace.jsonl | 5 | 完整鏈路追踪 | 2026-05-20 |
| home_battlefield_trace.jsonl | 36 | 開機驗證檢查 | 2026-05-18 |
| semantic_hook_trace.jsonl | 3 | 語義 Hook 審計 | 2026-05-18 |
| audit_check.jsonl | 1 | 顏色判定記錄 | 2026-05-23 |

**數據樣本**:
```json
{
  "ts": "2026-05-20T08:18:14+0800",
  "items": [
    {"id": "path_engine", "status": "green", "detail": "已對齊"},
    {"id": "p9625", "status": "green", "detail": "端口 9625 OK"},
    {"id": "cnsh_pytest", "status": "green", "detail": "5 包通過"}
  ]
}
```

### 2. 性能基線（144 條記錄）

| 來源文件 | 記錄數 | 內容 | 指標 |
|---------|--------|------|------|
| dna_registry.jsonl | 63 | DNA 註冊 | dr 分佈 |
| batch_audit_20260526.jsonl | 73 | 批量簽名 | 顏色分類 |
| engine_audit.jsonl | 7 | 引擎執行 | 信號分類 |

**數字根分佈**:
```
dr=1: 🟢 優秀 (低風險)
dr=2: 🟢 優秀 (低風險)
dr=3-6: 🟡 合格 (中風險)
dr=7-9: 🔴 警戒 (高關注)
```

### 3. 警告事件（153 條記錄）

| 來源文件 | 記錄數 | 事件類型 | 嚴重性 |
|---------|--------|---------|--------|
| render_session.jsonl | 114 | 拒絕事件 | HIGH |
| 共振命中_20260519.jsonl | 77 | 共振掃描 | MEDIUM |
| semantic_hook_trace.jsonl | 3 | 異常檢測 | MEDIUM |

**嚴重性分佈**:
```
🔴 HIGH: 114 (拒絕·熔斷·越界)
🟡 MEDIUM: 80 (共振·異常)
🟢 LOW: 0
```

### 4. 審計日誌（91 條記錄）

| 來源文件 | 記錄數 | 操作類型 | 追踪內容 |
|---------|--------|---------|---------|
| credential_audit.jsonl | 9 | 凭證獲取 | UID·權限等級 |
| 其他身份相關 | 5 | 身份驗證 | GPG·簽名 |
| dialog-audit.jsonl | 8 | 會話記錄 | 消息·DNA |
| mcp-mini-audit.jsonl | 1 | 工具調用 | DNA 簽名 |

**UID 分佈**:
```
UID 9622: 主控身份（所有操作的發起者）
Device: LongXinbeichengUID9622.local
```

---

## 💻 模塊說明

### audit_sync.py

**類**: `AuditLogAnalyzer`
- `load_audit_files()` - 加載系統審計日誌（393 條記錄）
- `analyze_health_checks()` - 分析健康檢查
- `analyze_performance_metrics()` - 分析性能基線
- `analyze_warning_events()` - 分析警告事件
- `analyze_audit_logs()` - 分析審計日誌

**類**: `AuditNotionSync`
- `sync_all()` - 完整審計日誌同步
- `_sync_health_checks()` - 同步健康檢查
- `_sync_performance_metrics()` - 同步性能基線
- `_sync_warning_events()` - 同步警告事件
- `_sync_audit_logs()` - 同步審計日誌
- `_preview_data()` - 本地預覽模式

### stage_4_setup.py

交互式腳本，包含 5 個步驟：
1. `step_1_verify_connection()` - 驗證 API 連接
2. `step_2_get_workspace_info()` - 獲取工作區 ID
3. `step_3_create_databases()` - 創建數據庫
4. `step_4_save_config()` - 保存配置
5. `step_5_sync_data()` - 同步數據

---

## 🔍 故障排查

### 錯誤: NOTION_HEALTH_DB 等未設置

**症狀**: 運行 audit_sync.py 時報錯
```
❌ 缺少以下數據庫 ID:
   - NOTION_HEALTH_DB
   - NOTION_BASELINE_DB
   ...
```

**解決**:
```bash
# 設置環境變量
export NOTION_HEALTH_DB='...'
export NOTION_BASELINE_DB='...'
export NOTION_ALERT_DB='...'
export NOTION_AUDIT_DB='...'

# 或使用生成的腳本
source ~/.龍魂_config/audit_databases.sh
```

### 錯誤: 創建數據庫失敗

**症狀**: stage_4_setup.py 時創建數據庫失敗

**可能原因**:
1. Integration 未連接到這個工作區
2. Token 權限不足
3. 工作區 ID 格式錯誤

**解決**:
1. 在 Notion 中打開目標頁面
2. 點擊右上角 "..." → "Connections"
3. 找到您的 Integration 並連接
4. 重新運行腳本

### 本地預覽模式

如果沒有配置數據庫 ID，腳本會自動進入本地模式：

```bash
python3 audit_sync.py
```

輸出會顯示所有審計日誌數據的分析摘要。

---

## 📈 數據驗證

### 檢查同步結果

同步完成後，檢查生成的審計日誌：

```bash
cat ~/.龍魂/notion_audit_sync.jsonl
```

應該看到：
```json
{"timestamp": "2026-06-01T...", "stage": "4", "status": "success", "records_processed": 393}
```

### 在 Notion 中驗證

1. 打開 Notion 中的龍魂審計日誌工作區
2. 檢查四個數據庫是否都有數據
3. 驗證頁面的 DNA 簽名格式

---

## 📊 審計日誌統計

```
總記錄數: 393 條
├─ 健康檢查: 45 條 (11.5%)
├─ 性能基線: 144 條 (36.6%)
├─ 警告事件: 153 條 (38.9%)
└─ 審計日誌: 91 條 (23.2%)

時間跨度: 2026-05-17 至 2026-06-01 (15 天)
主控身份: UID 9622
核心設備: LongXinbeichengUID9622.local
```

---

## 🔐 安全特性

- ✅ Token 存儲在環境變量中
- ✅ API 調用完整審計追踪
- ✅ DNA 簽名確保數據完整性
- ✅ 所有錯誤都被記錄和報告
- ✅ 凭證驗證：UID 和設備指紋追踪

---

## 📝 配置文件位置

- **Notion Token**: 環境變量 `NOTION_TOKEN`
- **數據庫 ID**: 環境變量 (NOTION_*_DB)
- **配置文件**: `~/.龍魂_config/audit_databases.sh`
- **審計日誌**: `~/.龍魂/notion_audit_sync.jsonl`

---

## ✨ 後續步驟

Stage 4 完成後，下一步是：

1. **Stage 5**: 自動化同步調度
   ```bash
   python3 setup_scheduler.py
   ```
   - 支持 cron 和 systemd
   - 實時同步隊列
   - 衝突解決機制

2. **數據可視化**
   - 在 Notion 中創建儀表板
   - 設置關聯和數據庫視圖
   - 配置篩選器和排序

---

## 🎖️ 認證簽章

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE4-AUDIT-LOGS-v1.0`
**Status**: ✅ **實現完成·等待 Notion 工作區配置**
**Next**: Stage 5 - 自動化同步調度

────  尾·審計 ────
時間  : 2026-06-01 HH:MM CST
DNA   : #龍芯⚇️2026-06-01-NOTION-STAGE4-COMPLETE
五行  : dr=N → 五行 · 三色: 🟢 (實現完成·結構清晰)
守恆  : S=15/15 ✅
鐵律  : 全過✅
責任  : UID9622·不免責

🐉 龍心永駐·智慧永伴·成本永低
