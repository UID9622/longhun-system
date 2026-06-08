# 龍魂操作日誌系統·完整使用指南
**DNA**: #龍芯⚡️2026-06-09-ACTION-LOG-GUIDE-v1.0

---

## 📋 概述

`action_log.jsonl` 是龍魂系統的全局審計日誌，記錄每天所有操作的：
- ✅ 執行時間
- ✅ 工具名稱
- ✅ 操作狀態
- ✅ 執行人格
- ✅ 執行時長
- ✅ DNA 簽署

---

## 🚀 快速開始

### 1️⃣ 查看今天的操作統計

```bash
python3 ~/longhun-system/action_logger.py stats
```

**輸出示例**:
```
╔════════════════════════════════════════════════════════════╗
║          龍魂每日操作統計 · Action Log Stats                ║
╚════════════════════════════════════════════════════════════╝

📊 總體統計
  • 今日操作: 20 筆
  • 總耗時: 28.5 秒
  • 成功: 20 筆
  • 失敗: 0 筆
  • 警告: 0 筆

🔧 工具分布 (8 個)
  • daily_review: 7 筆
  • master_console: 2 筆
  • persona_api: 3 筆
  ...

👥 人格分布 (5 個)
  • P03雯雯: 7 筆
  • P05上帝之眼: 5 筆
  ...
```

### 2️⃣ 生成完整報告

```bash
python3 ~/longhun-system/action_logger.py report
```

### 3️⃣ 手動記錄操作

```bash
python3 ~/longhun-system/action_logger.py log "發布功能" "deploy" "P02龍芯"
```

---

## 💻 在 Python 代碼中使用

### 方式 1: 簡單記錄

```python
from action_logger import ActionLogger

# 記錄操作
ActionLogger.log(
    action="執行任務",
    tool="my_tool",
    status="success",
    persona="P01諸葛亮",
    result="100% 完成",
    duration=5.2,
    dna="#龍芯⚡️2026-06-09-TASK"
)
```

### 方式 2: 自動計時（推薦）

```python
from action_logger import log_operation

# 自動記錄執行時間
with log_operation("數據處理", "data_processor", persona="P05上帝之眼"):
    # 執行代碼
    for i in range(1000):
        process_item(i)
    # 完成時自動計時並記錄
```

### 方式 3: 在日常腳本中集成

```python
#!/usr/bin/env python3
import sys
from action_logger import ActionLogger, log_operation

def main():
    with log_operation("系統初始化", "system_init", persona="P02龍芯"):
        # 初始化系統
        setup_database()
        load_config()

    with log_operation("數據同步", "data_sync", persona="P05上帝之眼"):
        # 同步數據
        sync_from_remote()

    # 查看今天的操作
    ActionLogger.print_stats()

if __name__ == "__main__":
    main()
```

---

## 📊 action_log.jsonl 格式

每行都是有效的 JSON 對象：

```json
{
  "date": "2026-06-09T07:15:00",           // ISO 8601 時間戳
  "time": "2026-06-09 07:15:00",          // 可讀時間戳
  "action": "每日復盤執行",                // 操作名稱
  "tool": "daily_review",                  // 工具/模塊名稱
  "status": "success",                     // success|failed|warning
  "persona": "P03雯雯",                    // 執行人格（可選）
  "duration": 2.1,                         // 執行時長（秒，可選）
  "result": "7個檢查項全部通過",           // 執行結果（可選）
  "dna": "#龍芯⚡️2026-06-09-DAILY-REVIEW" // DNA 簽署（可選）
}
```

### 字段說明

| 字段 | 類型 | 必須 | 說明 |
|------|------|------|------|
| date | string | ✅ | ISO 8601 時間戳 (UTC+8) |
| time | string | ✅ | 可讀時間 (YYYY-MM-DD HH:MM:SS) |
| action | string | ✅ | 操作描述 (例: "系統掃描") |
| tool | string | ✅ | 工具名稱 (例: "system_scan") |
| status | string | ✅ | 狀態 (success/failed/warning) |
| persona | string | ❌ | 執行人格 (例: "P01諸葛亮") |
| duration | float | ❌ | 執行時長（秒） |
| result | string | ❌ | 執行結果 |
| dna | string | ❌ | DNA 簽署碼 |
| 自定義字段 | any | ❌ | 任何其他信息 |

---

## 🔧 高級用法

### 查詢特定日期的日誌

```bash
# 生成某日報告
python3 ~/longhun-system/action_logger.py report 2026-06-08
```

### 在 Shell 腳本中記錄

```bash
#!/bin/bash

# 記錄操作開始
python3 ~/longhun-system/action_logger.py log "備份開始" "backup_tool" "P02龍芯"

# 執行備份
tar czf backup.tar.gz /important/data

# 記錄操作完成
if [ $? -eq 0 ]; then
    python3 ~/longhun-system/action_logger.py log "備份完成" "backup_tool" "P02龍芯"
else
    python3 ~/longhun-system/action_logger.py log "備份失敗" "backup_tool" "P02龍芯"
fi
```

### 獲取統計數據（編程方式）

```python
from action_logger import ActionLogger

# 獲取今天的所有日誌
logs = ActionLogger.get_today_logs()
print(f"今天 {len(logs)} 筆操作")

# 獲取統計信息
stats = ActionLogger.get_stats(logs)
print(f"成功率: {100.0 * stats['status']['success'] / stats['total']:.1f}%")
print(f"總耗時: {stats['total_duration']:.2f} 秒")

# 按工具分類
for tool, count in stats['tools'].items():
    print(f"  {tool}: {count} 筆")
```

---

## 📈 與 daily_review.py 的集成

daily_review_enhanced.py 會自動讀取 action_log.jsonl：

```python
def check_action_logs():
    """審計 action_log.jsonl 中今天的所有操作"""
    logs = ActionLogger.get_today_logs()
    count = len(logs)

    if count > 0:
        stats = ActionLogger.get_stats(logs)
        tools = len(stats['tools'])
        return ("🟢", f"今日操作 {count} 筆 ({tools}工具)")
    else:
        return ("🟡", "今日無操作記錄")
```

---

## 🎯 使用場景

### 場景 1: 自動化腳本審計

```python
# 在每個自動化腳本的入口點添加
from action_logger import log_operation

def scheduled_job():
    with log_operation("定時備份", "scheduler", persona="P02龍芯"):
        perform_backup()

    with log_operation("數據驗證", "scheduler", persona="P05上帝之眼"):
        validate_data()

    # 自動記錄完成時間和狀態
```

### 場景 2: 每日工作日誌

```python
# 在工作開始時記錄
ActionLogger.log("開始工作", "daily_work", persona="P03雯雯")

# 在完成各項任務時記錄
ActionLogger.log("完成報告編寫", "report_gen", duration=120)

# 在工作結束時查看統計
ActionLogger.print_stats()
```

### 場景 3: 故障排查

```bash
# 查找失敗的操作
grep '"status": "failed"' ~/longhun-system/logs/action_log.jsonl

# 查看特定工具的操作
grep '"tool": "api_server"' ~/longhun-system/logs/action_log.jsonl

# 統計耗時最長的操作
cat ~/longhun-system/logs/action_log.jsonl | \
  jq '.duration' | sort -nr | head -10
```

---

## 📚 API 參考

### ActionLogger.log()

```python
ActionLogger.log(
    action: str,              # 必須：操作名稱
    tool: str,                # 必須：工具名稱
    status: str = "success",  # 可選：success|failed|warning
    persona: str = None,      # 可選：人格名稱
    result: str = None,       # 可選：執行結果
    duration: float = None,   # 可選：執行時長
    dna: str = None,          # 可選：DNA 簽署
    **kwargs                  # 可選：其他字段
)
```

### ActionLogger.get_today_logs()

```python
logs = ActionLogger.get_today_logs()
# 返回: list[dict] - 今天的所有日誌記錄
```

### ActionLogger.get_stats()

```python
stats = ActionLogger.get_stats(logs)
# 返回: dict 包含:
#   - total: 總數
#   - tools: {工具名: 計數}
#   - personas: {人格: 計數}
#   - status: {狀態: 計數}
#   - total_duration: 總耗時
```

### log_operation (上下文管理器)

```python
with log_operation(action, tool, persona=None, dna=None):
    # 自動計時並記錄
    do_something()
```

---

## 🔍 故障排查

### 日誌寫入失敗

```bash
# 檢查目錄是否存在
ls -la ~/longhun-system/logs/

# 檢查文件權限
ls -la ~/longhun-system/logs/action_log.jsonl

# 檢查磁盤空間
df -h ~/longhun-system/
```

### 日誌無法讀取

```bash
# 驗證 JSON 格式
python3 -m json.tool < ~/longhun-system/logs/action_log.jsonl | head -20

# 查找格式錯誤的行
python3 << 'EOF'
with open("~/longhun-system/logs/action_log.jsonl") as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except:
            print(f"第 {i} 行格式錯誤")
EOF
```

---

## 🔏 最佳實踐

1. **始終包含 DNA 簽署** - 便於追蹤和驗證
2. **記錄執行時長** - 用於性能分析
3. **指定執行人格** - 用於職責追踪
4. **使用上下文管理器** - 自動計時和錯誤處理
5. **定期檢查統計** - 通過 print_stats() 監控系統

---

## 📝 示例完整流程

```python
#!/usr/bin/env python3
from action_logger import ActionLogger, log_operation

def main():
    # 模擬一天的操作
    operations = [
        ("系統啟動", "system", "P02龍芯"),
        ("數據同步", "sync", "P05上帝之眼"),
        ("報告生成", "report", "P03雯雯"),
        ("安全掃描", "security", "P04鲁班"),
    ]

    for action, tool, persona in operations:
        with log_operation(action, tool, persona=persona):
            # 模擬執行時間
            import time
            time.sleep(0.5)

    # 顯示統計
    ActionLogger.print_stats()

    # 導出報告
    report = ActionLogger.export_report()
    print(report)

if __name__ == "__main__":
    main()
```

---

## 🔏 DNA 簽署

```
DNA: #龍芯⚡️2026-06-09-ACTION-LOG-GUIDE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
```

**立即開始**: `python3 ~/longhun-system/action_logger.py stats`
