# 🐉 龍魂 Notion 集成 · Stage 5 自動化調度

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE5-AUTOMATION-v1.0`
**Date**: 2026-06-01
**Status**: ✅ **實現完成·等待配置激活**

---

## 📊 什麼是 Stage 5？

Stage 5 建立龍魂系統的 **自動化同步調度機制**：

- ✅ **基於時間的調度** - cron-like 定時執行
- ✅ **實時同步隊列** - 事件驅動架構
- ✅ **衝突檢測和解決** - 文件鎖防止並發衝突
- ✅ **多種調度方式** - cron、systemd、daemon、manual
- ✅ **完整的監控和日誌** - 審計追踪和告警

**核心目標**: 實現 Notion 數據與龍魂系統的實時同步，支持生產級別的自動化運維。

---

## 🎯 調度系統架構

### 核心組件

```
┌─────────────────────────────────────────┐
│     龍魂 Notion 自動化同步系統           │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  調度器層 (Scheduler)                    │
├─────────────────────────────────────────┤
│ - 時間計算引擎                          │
│ - 任務隊列管理                          │
│ - 衝突檢測和鎖機制                      │
│ - 監控線程                              │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  同步隊列 (SyncQueue)                    │
├─────────────────────────────────────────┤
│ - 任務入隊/出隊                         │
│ - 隊列持久化                            │
│ - 線程安全                              │
│ - 歷史追踪                              │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  衝突解決器 (ConflictResolver)           │
├─────────────────────────────────────────┤
│ - 獲取/釋放鎖                           │
│ - 鎖超時檢測                            │
│ - 單點執行保證                          │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  同步執行器 (Workers)                    │
├─────────────────────────────────────────┤
│ - Stage 2 (CNSH) 同步                   │
│ - Stage 3 (Knowledge) 同步              │
│ - Stage 4 (Audit) 同步                  │
│ - 結果記錄                              │
└─────────────────────────────────────────┘
```

### 調度方式對比

| 方式 | 優點 | 缺點 | 推薦場景 |
|------|------|------|--------|
| **Cron** | 輕量級·系統原生·簡單 | 功能有限·不可靠 | Linux/macOS 開發環境 |
| **Systemd** | 高級功能·日誌集成·可靠 | 僅限 systemd 系統 | 生產環境 (systemd) |
| **Python Daemon** | 完整控制·靈活配置·跨平台 | 需要 Python 進程 | 生產環境 (推薦) |
| **Manual** | 簡單·靈活·調試方便 | 需要手動執行 | 開發和測試 |

---

## 🚀 快速開始（5 步）

### Step 1: 驗證 Stage 4 完成

確保已完成 Stage 4：

```bash
# 檢查審計日誌數據庫配置
echo $NOTION_AUDIT_DB

# 如果返回數據庫 ID，表示 Stage 4 配置正確
```

### Step 2: 運行調度配置向導

```bash
cd ~/longhun-system/notion
python3 setup_scheduler.py
```

向導會提示您：
1. 驗證 API 連接
2. 選擇調度方式（推薦：Python Daemon）
3. 配置各 Stage 的運行時間
4. 生成配置文件
5. 執行測試同步

### Step 3: 選擇調度方式

根據您的環境選擇：

```
1. Cron (Linux/macOS)
2. Systemd Timer (systemd 系統)
3. Manual (手動執行)
4. Python Daemon (推薦·生產環境)
```

### Step 4: 配置運行時間

系統會為每個 Stage 詢問運行時間：

```
Stage 2 (CNSH): 02:00 (每日)
Stage 3 (Knowledge): 03:00 (每日)
Stage 4 (Audit): 04:00 (每日)
```

### Step 5: 激活調度

根據選擇的方式，執行相應的激活命令

---

## 📋 詳細配置方式

### 方式 1: Python Daemon（推薦）

最簡單、最可靠的生產方案。

**啟動方式**:

```bash
# 前臺運行（用於測試）
python3 ~/longhun-system/notion/sync_runner.py daemon

# 後臺運行（生產環境）
nohup python3 ~/longhun-system/notion/sync_runner.py daemon > ~/.龍魂/daemon.log 2>&1 &
```

**查看狀態**:

```bash
python3 ~/longhun-system/notion/sync_runner.py status
```

**停止服務**:

```bash
pkill -f "sync_runner.py daemon"
```

**配置文件**:
- `~/.龍魂_config/daemon_config.json` - 調度配置

### 方式 2: Cron（Linux/macOS）

輕量級的系統級調度。

**安裝方式**:

```bash
# 生成 cron 配置
python3 ~/longhun-system/notion/setup_scheduler.py

# 查看配置文件
cat ~/.龍魂_config/notion_sync.cron

# 安裝到 crontab
crontab ~/.龍魂_config/notion_sync.cron

# 驗證安裝
crontab -l
```

**配置示例**:

```crontab
# Stage 2: 每天 02:00 執行 CNSH 同步
0 2 * * * python3 ~/longhun-system/notion/sync_runner.py stage2

# Stage 3: 每天 03:00 執行知識圖譜同步
0 3 * * * python3 ~/longhun-system/notion/sync_runner.py stage3

# Stage 4: 每天 04:00 執行審計日誌同步
0 4 * * * python3 ~/longhun-system/notion/sync_runner.py stage4
```

### 方式 3: Systemd Timer（高級 Linux）

高級定時和依賴管理。

**安裝方式**:

```bash
# 生成 systemd 配置
python3 ~/longhun-system/notion/setup_scheduler.py

# 複製服務文件
sudo cp ~/.龍魂_config/systemd/* /etc/systemd/system/

# 重載 systemd
sudo systemctl daemon-reload

# 啟用服務
sudo systemctl enable longhun-notion-sync.service

# 啟動服務
sudo systemctl start longhun-notion-sync.service

# 查看狀態
sudo systemctl status longhun-notion-sync.service
```

**查看日誌**:

```bash
# 實時日誌
sudo journalctl -u longhun-notion-sync -f

# 最近 100 行
sudo journalctl -u longhun-notion-sync -n 100
```

### 方式 4: Manual（開發和測試）

手動執行每次同步。

**執行同步**:

```bash
# 執行 Stage 2
python3 ~/longhun-system/notion/sync_runner.py stage2

# 執行 Stage 3
python3 ~/longhun-system/notion/sync_runner.py stage3

# 執行 Stage 4
python3 ~/longhun-system/notion/sync_runner.py stage4
```

**查看計劃表**:

```bash
cat ~/.龍魂_config/manual_schedule.txt
```

---

## 💻 模塊說明

### scheduler.py (~600 行)

**核心調度引擎**

**類**: `SyncTask`
- 調度任務的數據類
- 包含狀態、時間戳、錯誤信息、記錄計數

**類**: `SyncQueue`
- 實時同步隊列
- 線程安全的任務管理
- JSONL 歷史日誌

**類**: `ConflictResolver`
- 衝突檢測和鎖管理
- 文件系統鎖實現
- 鎖超時檢測

**類**: `SyncScheduler`
- 主調度器
- 支持 daily/hourly/every_6h 頻率
- 多線程工作器架構
- 監控線程

### setup_scheduler.py (~400 行)

**交互式配置向導**

**函數**:
- `step_1_verify_connection()` - 驗證 API
- `step_2_select_scheduler_type()` - 選擇方式
- `step_3_configure_schedules()` - 配置時間
- `step_4_generate_config()` - 生成配置
- `step_5_test_scheduler()` - 執行測試

### sync_runner.py (~300 行)

**命令行同步入口**

**命令**:
- `stage2` - 執行 CNSH 同步
- `stage3` - 執行知識圖譜同步
- `stage4` - 執行審計日誌同步
- `daemon` - 啟動後臺調度器
- `status` - 查看調度器狀態
- `help` - 顯示幫助

---

## 📊 監控和日誌

### 日誌文件位置

```
~/.龍魂/
├── sync_schedule.jsonl          # 調度執行記錄
├── sync_queue_history.jsonl     # 隊列操作歷史
├── sync_runner.jsonl            # 同步運行日誌
├── notion_api_audit.jsonl       # API 審計日誌
├── notion_cnsh_sync.jsonl       # CNSH 同步日誌
├── notion_audit_sync.jsonl      # 審計同步日誌
└── daemon.log                   # 後臺守護進程日誌
```

### 查看日誌

```bash
# 查看最近的調度記錄
tail -f ~/.龍魂/sync_schedule.jsonl

# 查看隊列狀態
cat ~/.龍魂/sync_queue_history.jsonl | tail -20

# 查看同步結果
python3 sync_runner.py status
```

### 日誌格式

```json
{
  "timestamp": "2026-06-01T14:30:00.123456",
  "stage": 2,
  "status": "completed",
  "duration_seconds": 45.2,
  "task_id": "task-2-a1b2c3d4",
  "records_synced": 23
}
```

---

## 🔍 故障排查

### 問題: 同步任務未執行

**檢查清單**:

1. 驗證 Notion Token
   ```bash
   echo $NOTION_TOKEN
   ```

2. 驗證數據庫 ID
   ```bash
   source ~/.龍魂_config/audit_databases.sh
   echo $NOTION_HEALTH_DB
   ```

3. 檢查後臺進程
   ```bash
   ps aux | grep sync_runner
   ```

4. 查看日誌
   ```bash
   tail ~/.龍魂/daemon.log
   ```

### 問題: Cron 任務不執行

**解決方案**:

1. 驗證 crontab 安裝
   ```bash
   crontab -l | grep sync_runner
   ```

2. 檢查郵件日誌
   ```bash
   tail /var/mail/$USER
   ```

3. 重新安裝 crontab
   ```bash
   crontab ~/.龍魂_config/notion_sync.cron
   ```

### 問題: 同步衝突（重複執行）

**症狀**: 同一 Stage 被執行多次

**解決**:

1. 檢查鎖文件
   ```bash
   ls -la ~/.龍魂/sync_locks/
   ```

2. 手動清理鎖（慎用）
   ```bash
   rm ~/.龍魂/sync_locks/stage_*.lock
   ```

3. 驗證沒有多個調度器實例
   ```bash
   ps aux | grep "sync_runner.py daemon"
   ```

### 問題: 內存洩漏

**監控內存使用**:

```bash
# 定期監控進程
watch -n 5 "ps aux | grep sync_runner"

# 查看詳細內存使用
ps aux | grep sync_runner | awk '{print $6}' # RSS in KB
```

**解決方案**:

1. 定期重啟守護進程
   ```bash
   pkill -f "sync_runner.py daemon"
   sleep 5
   nohup python3 ~/longhun-system/notion/sync_runner.py daemon &
   ```

2. 使用 systemd 服務自動重啟
   ```
   Restart=on-failure
   RestartSec=300
   ```

---

## 📈 性能優化

### 隊列大小優化

```python
# 默認隊列大小: 1000 任務
queue = SyncQueue(max_size=1000)

# 根據系統資源調整
# 高頻率: 500-1000
# 低頻率: 100-200
```

### 工作線程數優化

```python
# 啟動 3 個工作線程（默認）
workers, monitor = scheduler.start_scheduler(worker_threads=3)

# 根據 CPU 核心調整
# CPU 核心數 = 最優線程數
```

### 超時設置

```python
# 默認任務超時: 300 秒
resolver.acquire_lock(stage, timeout=300)

# 根據同步時間調整
# 快速同步: 60-180 秒
# 慢速同步: 300-600 秒
```

---

## 🔐 安全考慮

### 權限管理

```bash
# 確保配置文件只有用戶可讀
chmod 700 ~/.龍魂_config
chmod 600 ~/.龍魂_config/*.json

# 鎖文件應該是私有的
chmod 700 ~/.龍魂/sync_locks
```

### 日誌管理

```bash
# 定期清理舊日誌（保留 30 天）
find ~/.龍魂 -name "*.jsonl" -mtime +30 -delete

# 或使用 logrotate
```

### 進程安全

```bash
# 不要以 root 身份運行調度器
# 推薦使用專用用戶
sudo useradd -m -s /bin/false notion-sync
sudo chown notion-sync:notion-sync ~/.龍魂
```

---

## 💡 最佳實踐

### 1. 測試先行

```bash
# 在激活自動化前，先測試每個 Stage
python3 sync_runner.py stage2
python3 sync_runner.py stage3
python3 sync_runner.py stage4
```

### 2. 監控運行

```bash
# 監控調度器狀態
python3 sync_runner.py status

# 定期檢查日誌
tail -f ~/.龍魂/sync_schedule.jsonl
```

### 3. 定期驗證

```bash
# 每週檢查 Notion 中的數據新鮮度
# 確認所有同步都成功執行
# 檢查有無異常和錯誤

# 月度健康檢查
python3 sync_runner.py status
du -sh ~/.龍魂/*
```

### 4. 備份配置

```bash
# 備份調度配置
cp -r ~/.龍魂_config ~/.龍魂_config.backup

# 備份日誌（用於分析）
tar czf ~/longhun-backup-$(date +%Y%m%d).tar.gz ~/.龍魂
```

---

## 🚨 告警和通知

### 設置郵件告警（可選）

對於 cron 任務：

```bash
# 在 crontab 中添加郵件地址
MAILTO="your-email@example.com"
```

### 設置 Slack 通知（可選）

修改 sync_runner.py 以支持 Slack:

```python
def notify_slack(message):
    """發送 Slack 通知"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    # 實現 webhook 調用
    pass
```

---

## ✨ 進階功能

### 自定義同步邏輯

在 scheduler.py 中擴展 `_execute_sync`:

```python
def _execute_sync(self, task: SyncTask):
    """執行同步任務"""
    # 添加自定義邏輯
    # 例: 預同步驗證、後同步清理等
    pass
```

### 添加新的調度頻率

在 `_calculate_next_run` 中添加新頻率:

```python
elif frequency == "weekly":
    # 每週一 02:00 執行
    next_run = ...
```

### 集成外部服務

在 sync_runner.py 中添加回調:

```python
def on_sync_complete(stage: int, success: bool):
    """同步完成後的回調"""
    # 發送通知、更新儀表板等
    pass
```

---

## 📝 配置文件位置

- **調度器配置**: `~/.龍魂_config/daemon_config.json`
- **Cron 配置**: `~/.龍魂_config/notion_sync.cron`
- **Systemd 配置**: `~/.龍魂_config/systemd/`
- **Manual 時間表**: `~/.龍魂_config/manual_schedule.txt`
- **調度日誌**: `~/.龍魂/sync_schedule.jsonl`

---

## 🎖️ 認證簽章

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE5-AUTOMATION-v1.0`
**Status**: ✅ **實現完成·等待配置激活**
**Next**: 全量 Notion 集成系統交付

────  尾·審計 ────
時間  : 2026-06-01 HH:MM CST
DNA   : #龍芯⚇️2026-06-01-NOTION-STAGE5-COMPLETE
五行  : dr=N → 五行 · 三色: 🟢 (實現完成·結構清晰)
守恆  : S=15/15 ✅
鐵律  : 全過✅
責任  : UID9622·不免責

🐉 龍心永駐·智慧永伴·成本永低
