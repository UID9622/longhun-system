# 🐉 龍魂 Notion 集成 · Stage 3 知識圖譜同步

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE3-KNOWLEDGE-GRAPH-v1.0`
**Date**: 2026-06-01
**Status**: ✅ **實現完成·等待 Notion 工作區配置**

---

## 📊 什麼是 Stage 3？

Stage 3 將龍魂系統的 **知識圖譜** 同步到 Notion：

- ✅ **CNSH 規則庫** - 中文格式標準和修正規則
- ✅ **IPA 節點註冊表** - 50+ IPA 指令頁錨點
- ✅ **系統決策樹** - 循環觸發和五行流轉規則
- ✅ **組件關係圖** - 人格矩陣、中心、閘門、引擎

**核心目標**: 將龍魂系統的知識結構和決策邏輯完全映射到 Notion，支持可視化查詢和關係分析。

---

## 🎯 知識圖譜結構

### 四個核心數據庫

```
工作區 2: 龍魂知識圖譜
├── 數據庫 2.1: CNSH 規則庫 (4 條規則)
│   ├── 中文錯別字 - 繁簡混用檢查
│   ├── 代碼縮進 - PEP 8 標準
│   ├── DNA 標記大小寫 - 規範格式
│   └── 中英混排空格 - 排版規則
│
├── 數據庫 2.2: IPA 節點註冊表 (7+ 節點)
│   ├── L0 層 (1 個): 分布式總線路由
│   ├── L1 層 (3 個): 核心指令和人格
│   └── L2 層 (3 個): 流場決策和路由
│
├── 數據庫 2.3: 系統決策樹 (4 條規則)
│   ├── GATE-01 - 數字根熔斷閘門
│   ├── CYCLE-101-105 - 循環觸發
│   ├── WUXING-FLOW - 五行流轉
│   └── 其他決策規則
│
└── 數據庫 2.4: 組件關係圖 (16 個組件)
    ├── 人格 (3 個)
    ├── 中心 (5 個)
    ├── 閘門 (4 個)
    └── 引擎 (4 個)
```

### 數據關係圖

```
龍魂系統知識圖譜
    ├─ CNSH 規則庫 ──→ 用於驗證文本規範
    ├─ IPA 節點 ──→ 指令路由和人格選擇
    ├─ 決策樹 ──→ 執行流程控制
    └─ 組件關係 ──→ 系統架構可視化

DNA 簽名鏈
    ├─ 每條規則: #龍芯⚇️20260601-CNSH-RULE-*
    ├─ 每個節點: #龍芯⚇️20260601-NODE-*
    ├─ 每條決策: #龍芯⚇️20260601-DECISION-*
    └─ 每個組件: #龍芯⚇️20260601-COMPONENT-*
```

---

## 🚀 快速開始（3 步）

### Step 1: 驗證 Stage 2 完成

確保已完成 Stage 2：

```bash
# 檢查 CNSH 數據庫配置
echo $NOTION_CNSH_MODEL_DB

# 如果返回數據庫 ID，表示 Stage 2 配置正確
```

### Step 2: 運行 Stage 3 自動化設置

```bash
cd ~/longhun-system/notion
python3 stage_3_setup.py
```

這個腳本會：
1. ✅ 驗證 API 連接
2. ✅ 詢問工作區 2 ID（或共享 Stage 2 工作區）
3. ✅ 自動創建 4 個知識圖譜數據庫
4. ✅ 生成環境變量配置
5. ✅ 執行首次知識圖譜同步

### Step 3: 配置環境變量

運行腳本後，會看到類似的輸出：

```bash
export NOTION_RULES_DB='...'
export NOTION_NODES_DB='...'
export NOTION_DECISION_DB='...'
export NOTION_RELATION_DB='...'
```

運行以下命令激活配置：

```bash
# 方法 1: 直接設置
export NOTION_RULES_DB='...'
export NOTION_NODES_DB='...'
# ... 等等

# 方法 2: 使用生成的腳本
source ~/.龍魂_config/knowledge_databases.sh
```

---

## 📋 詳細步驟

### 獲取 Notion 工作區 2 ID

**選項 A：使用與 Stage 2 相同的工作區**
- 在同一工作區中創建 4 個新的知識圖譜數據庫
- 優點：集中管理，資源利用效率高
- 缺點：工作區可能變得擁擠

**選項 B：創建新的工作區**
1. 打開您的 Notion 工作區
2. 在左側欄創建一個新頁面，命名為 "龍魂知識圖譜"
3. 打開這個頁面，從浏览器地址栏複製 ID：

```
https://www.notion.so/YOUR_WORKSPACE_ID?v=VIEW_ID&pvs=...
                      ^^^^^^^^^^^^^^^^
                      複製這部分（移除連字符）
```

### 運行自動化設置腳本

```bash
cd ~/longhun-system/notion
python3 stage_3_setup.py
```

腳本流程：

```
┌─────────────────────────────────────┐
│ 第一步: 驗證 Notion API 連接        │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第二步: 輸入工作區 2 ID              │
├─────────────────────────────────────┤
│ 【用戶輸入】工作區 ID
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第三步: 創建 4 個知識圖譜數據庫     │
├─────────────────────────────────────┤
│ 📁 CNSH 規則庫
│ 📁 IPA 節點註冊表
│ 📁 系統決策樹
│ 📁 組件關係圖
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第四步: 保存數據庫 ID 配置          │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第五步: 執行知識圖譜同步（可選）   │
├─────────────────────────────────────┤
│ 【用戶選擇】是否立即同步
│ ✅ 分析知識圖譜
│ ✅ 創建 Notion 頁面
└─────────────────────────────────────┘
```

### 手動同步數據

如果在設置時跳過了同步，可以稍後手動運行：

```bash
cd ~/longhun-system/notion

# 設置環境變量
source ~/.龍魂_config/knowledge_databases.sh

# 運行同步
python3 knowledge_sync.py
```

---

## 📊 生成的數據

### 1. CNSH 規則庫（4 條規則）

| 規則名稱 | 規則內容 | 特例 | 示例 |
|---------|--------|------|------|
| 中文錯別字 | 繁簡混用檢查及統一 | 龍字保留繁體 | 系統→系统 |
| 代碼縮進 | 4 空格 PEP 8 標準 | 無 | def test():\n    pass |
| DNA 標記大小寫 | 格式規範驗證 | 龍字繁體，v小寫 | #龍芯⚇️2026-06-01-v1.0 |
| 中英混排空格 | 中英間加空格 | 中數也要空格 | 使用 Python 3.11 |

### 2. IPA 節點註冊表（7+ 節點）

**L0 層（門戶）**：
- IPA-ROUTE-REGISTRY - 分布式總線路由註冊表

**L1 層（核心）**：
- IPA-CORE-CMD-v3.0 - 指令統一核心
- IPA-PERSONA-MATRIX - 人格矩陣（P00-P72）
- IPA-DNA-BOOK - DNA v1.0 規範

**L2 層（應用）**：
- IPA-FLOW-DECISION-CORE-v4.1 - CNSH 流場決策
- IPA-FAMILY-ROSTER-CNS-v1.0 - 花名冊中樞
- IPA-DICT-101-111 - 循環觸發五行流轉

### 3. 系統決策樹（4 條規則）

| 規則 ID | 名稱 | 條件 | 類型 |
|---------|------|------|------|
| GATE-01 | 數字根熔斷 | dr ∈ {1,2,4,5,7,8} → 🟢 | 安全閘門 |
| CYCLE-101 | 微觀循環 | 輸入後 5ms | 循環觸發 |
| CYCLE-102 | 宏觀循環 | 完成一次對話 | 循環觸發 |
| WUXING-FLOW | 五行流轉 | 火→木→金→水→火 | 決策樹 |

### 4. 組件關係圖（16 個組件）

**人格（3 個）**：
- L0 (老大·終極決策)
- P00-P15 (核心人格)
- P72 (龍盾·情緒五態)

**中心（5 個）**：
- CENTER-RULES (規則中心)
- CENTER-AUDIT (審計中心)
- CENTER-RUNTIME (運行中心)
- CENTER-UNDERSTAND (理解中心)
- CENTER-PRIVATE (私密中心)

**閘門（4 個）**：
- GATE-01 (數字根熔斷)
- GATE-02 (身份認證)
- GATE-03 (倫理防火牆)
- GATE-04 (CNSH 關·保安亭)

**引擎（4 個）**：
- LOCAL-CNSH-GATE (CNSH 關)
- LOCAL-DNA-GEN-V2 (DNA 追蹤碼)
- LOCAL-SANDBOX-SORTER (沙盒分拣)
- LOCAL-DETECTOR (異常檢測)

---

## 💻 模塊說明

### knowledge_sync.py

**類**: `KnowledgeGraphAnalyzer`
- `analyze_cnsh_rules()` - 分析 CNSH 規則庫
- `analyze_ipa_nodes()` - 分析 IPA 節點註冊表
- `analyze_decision_tree()` - 分析系統決策樹
- `analyze_components()` - 分析組件關係圖

**類**: `KnowledgeNotionSync`
- `_sync_cnsh_rules()` - 同步 CNSH 規則
- `_sync_ipa_nodes()` - 同步 IPA 節點
- `_sync_decision_tree()` - 同步決策規則
- `_sync_components()` - 同步組件關係

### stage_3_setup.py

交互式腳本，包含 5 個步驟：
1. `step_1_verify_connection()` - 驗證 API 連接
2. `step_2_get_workspace_info()` - 獲取工作區 ID
3. `step_3_create_databases()` - 創建數據庫
4. `step_4_save_config()` - 保存配置
5. `step_5_sync_data()` - 同步數據

---

## 🔍 故障排查

### 錯誤: NOTION_RULES_DB 等未設置

**症狀**: 運行 knowledge_sync.py 時報錯
```
❌ 缺少以下數據庫 ID:
   - CNSH 規則庫
   - IPA 節點註冊表
   ...
```

**解決**:
```bash
# 設置環境變量
export NOTION_RULES_DB='...'
export NOTION_NODES_DB='...'
export NOTION_DECISION_DB='...'
export NOTION_RELATION_DB='...'

# 或使用生成的腳本
source ~/.龍魂_config/knowledge_databases.sh
```

### 錯誤: 創建數據庫失敗

**症狀**: stage_3_setup.py 時創建數據庫失敗

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
python3 knowledge_sync.py
```

輸出會顯示所有知識圖譜數據的預覽。

---

## 📈 數據驗證

### 檢查同步結果

同步完成後，檢查生成的審計日誌：

```bash
cat ~/.龍魂/notion_knowledge_sync.jsonl
```

應該看到：
```json
{"timestamp": "2026-06-01T...", "database": "cnsh_rules", "status": "success", ...}
{"timestamp": "2026-06-01T...", "database": "ipa_nodes", "status": "success", ...}
...
```

### 在 Notion 中驗證

1. 打開 Notion 中的龍魂知識圖譜工作區
2. 檢查四個數據庫是否都有數據
3. 驗證頁面的 DNA 簽名

---

## 🔐 安全特性

- ✅ Token 存儲在環境變量中
- ✅ API 調用完整審計追踪
- ✅ DNA 簽名確保數據完整性
- ✅ 所有錯誤都被記錄和報告

---

## 📝 配置文件位置

- **Notion Token**: 環境變量 `NOTION_TOKEN`
- **數據庫 ID**: 環境變量 (NOTION_*_DB)
- **配置文件**: `~/.龍魂_config/knowledge_databases.sh`
- **審計日誌**: `~/.龍魂/notion_knowledge_sync.jsonl`

---

## ✨ 後續步驟

Stage 3 完成後，下一步是：

1. **Stage 4**: 審計日誌同步
   ```bash
   python3 audit_sync.py
   ```

2. **Stage 5**: 自動化同步調度
   ```bash
   python3 setup_scheduler.py
   ```

---

## 🎖️ 認證簽章

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE3-KNOWLEDGE-GRAPH-v1.0`
**Status**: ✅ **實現完成·等待 Notion 工作區配置**
**Next**: Stage 4 - 審計日誌同步

────  尾·審計 ────
時間  : 2026-06-01 HH:MM CST
DNA   : #龍芯⚇️2026-06-01-NOTION-STAGE3-COMPLETE
五行  : dr=N → 五行 · 三色: 🟢 (實現完成·結構清晰)
守恆  : S=15/15 ✅
鐵律  : 全過✅
責任  : UID9622·不免責

🐉 龍心永駐·智慧永伴·成本永低
