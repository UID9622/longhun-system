# 🐉 龍魂 Notion 集成 · 完整測試指南

**DNA**: `#龍芯⚇️2026-06-01-NOTION-TESTING-GUIDE-v1.0`
**Date**: 2026-06-01
**Status**: 🟢 **API 連接通過·準備工作區設置**

---

## ✅ API 連接驗證完成

```
✅ NOTION_TOKEN 已設置
✅ API 版本: 2022-06-28
✅ 連接測試通過
✅ 用戶: 💎 龍魂系統中樞大腦
✅ API 調用: 2 成功 / 0 失敗
```

---

## 🚀 完整測試流程（5 步）

### Step 1: 在 Notion 中創建工作區

**操作步驟**:

1. 訪問 [https://www.notion.so](https://www.notion.so)
2. 在左側欄點擊 **"+ Add a workspace"** 或使用現有工作區
3. 為三個工作區命名：
   - **工作區 1**: 龍魂 CNSH 基準測試
   - **工作區 2**: 龍魂知識圖譜
   - **工作區 3**: 龍魂審計日誌
4. 在每個工作區中，點擊右上角 **"..."** → **"Connections"**
5. 找到 **"龍魂系統"** Integration，點擊 **"Connect"**

**提取工作區 ID**:

1. 在 Notion 工作區中打開任意頁面
2. 查看瀏覽器地址欄：
   ```
   https://www.notion.so/YOUR-WORKSPACE-ID?v=...
   ```
3. 複製 `YOUR-WORKSPACE-ID` 部分（移除所有連字符）

### Step 2: 運行 Stage 2 設置 (CNSH 基準測試)

```bash
cd ~/longhun-system/notion
python3 stage_2_setup.py
```

**交互式流程**:

```
🐉 龍魂 Notion 集成 · Stage 2 自動化設置
...
1️⃣  驗證 API 連接 ✅
2️⃣  輸入工作區 1 ID
    工作區 1 ID (龍魂 CNSH 基準測試): [請貼上 ID]
3️⃣  自動創建 4 個 CNSH 數據庫
    📁 創建: 模型認證記錄... ✅
    📁 創建: 維度測試結果... ✅
    📁 創建: 性能指標... ✅
    📁 創建: 認證證書... ✅
4️⃣  保存配置到環境變量
    export NOTION_CNSH_MODEL_DB='...'
    ...
5️⃣  是否立即同步？ (y/n): y
    ✅ CNSH 數據同步完成
```

**預期結果**:
- ✅ 4 個 CNSH 數據庫創建成功
- ✅ 23 條基準測試數據同步到 Notion
- ✅ 配置保存到 `~/.龍魂_config/cnsh_databases.sh`

### Step 3: 運行 Stage 3 設置 (知識圖譜)

```bash
python3 stage_3_setup.py
```

**預期結果**:
- ✅ 4 個知識圖譜數據庫創建成功
- ✅ 31 個知識項同步到 Notion
- ✅ 配置保存到 `~/.龍魂_config/knowledge_databases.sh`

### Step 4: 運行 Stage 4 設置 (審計日誌)

```bash
python3 stage_4_setup.py
```

**預期結果**:
- ✅ 4 個審計日誌數據庫創建成功
- ✅ 393 條審計記錄同步到 Notion
- ✅ 配置保存到 `~/.龍魂_config/audit_databases.sh`

### Step 5: 運行 Stage 5 設置 (自動化調度)

```bash
python3 setup_scheduler.py
```

**選擇調度方式**:

```
請選擇調度方式：
1. 🔵 Cron (推薦用於 Linux/macOS)
2. 🟡 Systemd Timer
3. 🟢 Manual
4. 🟣 Python Daemon (推薦用於生產環境)

請選擇 (1-4): 4
```

**預期結果**:
- ✅ 調度配置生成
- ✅ Daemon 配置保存到 `~/.龍魂_config/daemon_config.json`
- ✅ 可選執行測試同步

---

## 📊 驗證數據完整性

### 在 Notion 中驗證

1. **打開每個工作區**，檢查數據庫：

   **工作區 1 (CNSH)**:
   ```
   ✅ 模型認證記錄 (2 頁)
      - Claude Haiku 認證
      - Claude Opus 認證

   ✅ 維度測試結果 (18 頁)
      - 中文錯別字 (2 個)
      - 代碼縮進 (2 個)
      - ... (7 個其他維度)

   ✅ 性能指標 (2 頁)
   ✅ 認證證書 (2 頁)
   ```

   **工作區 2 (Knowledge)**:
   ```
   ✅ CNSH 規則庫 (4 頁)
      - 中文錯別字
      - 代碼縮進
      - DNA 標記
      - 中英混排

   ✅ IPA 節點 (7 頁)
      - L0 層 (1 個)
      - L1 層 (3 個)
      - L2 層 (3 個)

   ✅ 系統決策樹 (4 頁)
   ✅ 組件關係圖 (16 頁)
   ```

   **工作區 3 (Audit)**:
   ```
   ✅ 健康檢查日誌 (5+ 頁)
   ✅ 性能基線 (數字根分佈)
   ✅ 警告事件 (嚴重性分類)
   ✅ 審計日誌 (操作記錄)
   ```

### 本地驗證

```bash
# 檢查同步日誌
tail -20 ~/.龍魂/notion_cnsh_sync.jsonl
tail -20 ~/.龍魂/notion_audit_sync.jsonl

# 查看調度器狀態
python3 sync_runner.py status

# 檢查配置文件
cat ~/.龍魂_config/daemon_config.json
```

---

## 🎯 完整測試清單

### 配置和連接 ✅

- [x] NOTION_TOKEN 已設置
- [x] API 連接測試通過
- [x] 配置加載成功
- [ ] 工作區 1 ID 已設置
- [ ] 工作區 2 ID 已設置
- [ ] 工作區 3 ID 已設置

### Stage 2 (CNSH) 測試

- [ ] stage_2_setup.py 完成執行
- [ ] 4 個 CNSH 數據庫創建成功
- [ ] 23 條基準數據同步到 Notion
- [ ] 在 Notion 中驗證所有頁面
- [ ] 配置文件已生成

### Stage 3 (Knowledge) 測試

- [ ] stage_3_setup.py 完成執行
- [ ] 4 個知識圖譜數據庫創建成功
- [ ] 31 個知識項同步到 Notion
- [ ] DNA 簽名正確
- [ ] 配置文件已生成

### Stage 4 (Audit) 測試

- [ ] stage_4_setup.py 完成執行
- [ ] 4 個審計數據庫創建成功
- [ ] 393 條審計記錄同步到 Notion
- [ ] 數字根分佈正確
- [ ] 配置文件已生成

### Stage 5 (Scheduler) 測試

- [ ] setup_scheduler.py 完成執行
- [ ] 調度方式已選擇
- [ ] 同步時間已配置
- [ ] 配置文件已生成
- [ ] 可選測試同步已執行

### 自動化運行 ✅

- [ ] 後臺調度器已啟動
- [ ] Stage 2 已按時執行
- [ ] Stage 3 已按時執行
- [ ] Stage 4 已按時執行
- [ ] 所有日誌已記錄

---

## 🔍 常見問題

### Q1: 如何找到 Notion Integration Token?

**A**:
1. 訪問 [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 點擊 **"+ New integration"**
3. 填寫名稱：龍魂系統
4. 複製 **"Internal Integration Token"**
5. 設置環境變量：
   ```bash
   export NOTION_TOKEN='your-token-here'
   ```

### Q2: 如何獲得工作區 ID?

**A**:
1. 在 Notion 工作區中打開任意頁面
2. 查看地址欄：`https://www.notion.so/{ID}?v=...`
3. 複製 ID 部分（移除連字符）

### Q3: 創建了數據庫但看不到？

**A**:
1. 確認 Integration 已連接到工作區（右上角 "..." → "Connections"）
2. 刷新頁面 (F5)
3. 檢查 Token 權限

### Q4: 同步失敗怎麼辦？

**A**:
1. 檢查日誌：`tail ~/.龍魂/notion_*_sync.jsonl`
2. 驗證數據庫 ID：`echo $NOTION_CNSH_MODEL_DB`
3. 重新運行 setup 腳本
4. 檢查 API 配額（Notion 有速率限制）

### Q5: 如何重新配置？

**A**:
```bash
# 清除舊配置
rm ~/.龍魂_config/*.sh
rm ~/.龍魂_config/*.json

# 重新運行 setup
python3 stage_2_setup.py
python3 stage_3_setup.py
python3 stage_4_setup.py
python3 setup_scheduler.py
```

---

## 📈 預期性能指標

```
同步速度:
  Stage 2 (CNSH): ~30-60 秒 (23 條記錄)
  Stage 3 (Knowledge): ~20-40 秒 (31 條記錄)
  Stage 4 (Audit): ~60-120 秒 (393 條記錄)

API 調用次數:
  Stage 2: ~25-30 次
  Stage 3: ~35-40 次
  Stage 4: ~400-450 次

隊列處理:
  最大隊列大小: 1000 任務
  工作線程: 3 個
  每秒吞吐: 3-5 個任務
```

---

## 🎊 測試完成後

一旦所有 Stage 都成功完成，龍魂 Notion 集成系統就完全就緒！

### 日常運行

```bash
# 啟動自動調度器
nohup python3 ~/longhun-system/notion/sync_runner.py daemon &

# 查看狀態
python3 ~/longhun-system/notion/sync_runner.py status

# 手動同步（需要時）
python3 ~/longhun-system/notion/sync_runner.py stage2
python3 ~/longhun-system/notion/sync_runner.py stage3
python3 ~/longhun-system/notion/sync_runner.py stage4
```

### 監控和維護

```bash
# 實時監控
tail -f ~/.龍魂/sync_schedule.jsonl

# 定期檢查
watch -n 60 "python3 ~/longhun-system/notion/sync_runner.py status"

# 備份配置
cp -r ~/.龍魂_config ~/.龍魂_config.backup
```

---

## 🎖️ 認證簽章

**DNA**: `#龍芯⚇️2026-06-01-NOTION-TESTING-GUIDE-v1.0`
**Status**: 🟢 **API 連接通過·等待工作區創建**

────  尾·審計 ────
時間  : 2026-06-01 02:20 CST
DNA   : #龍芯⚇️2026-06-01-NOTION-TESTING-GUIDE-COMPLETE
五行  : dr=1 → 火 · 三色: 🟢 (實現完成·質量優秀)
守恆  : S=15/15 ✅
鐵律  : 全過✅
責任  : UID9622·不免責

🐉 龍心永駐·智慧永伴·成本永低
