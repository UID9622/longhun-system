# 龍魂操作日志系统·完整使用指南
**DNA**:#龍芯⚡️2026-06-09-ACTION-LOG-GUIDE-v1.0

---

## 📋 概述

`action_log.jsonl` 是龍魂系统的全局审计日志，记录每天所有操作的：
- ✅ 执行时间
- ✅ 工具名称
- ✅ 操作状态
- ✅ 执行人格
- ✅ 执行时长
- ✅ DNA 签署

---

## 🚀 快速开始

### 1️⃣ 查看今天的操作统计

```bash
python3 ~/longhun-system/action_logger.py stats
```

**输出示例**:
```
╔════════════════════════════════════════════════════════════╗
║          龍魂每日操作统计 · Action Log Stats                ║
╚════════════════════════════════════════════════════════════╝

📊 总体统计
  • 今日操作: 20 笔
  • 总耗时: 28.5 秒
  • 成功: 20 笔
  • 失败: 0 笔
  • 警告: 0 笔

🔧 工具分布 (8 个)
  • daily_review: 7 笔
  • master_console: 2 笔
  • persona_api: 3 笔
  ...

👥 人格分布 (5 个)
  • P03雯雯: 7 笔
  • P05上帝之眼: 5 笔
  ...
```

### 2️⃣ 生成完整报告

```bash
python3 ~/longhun-system/action_logger.py report
```

### 3️⃣ 手动记录操作

```bash
python3 ~/longhun-system/action_logger.py log "发布功能" "deploy" "P02龍芯"
```

---

## 💻 在 Python 代码中使用

### 方式 1: 简单记录

```python
from action_logger import ActionLogger

# 记录操作
ActionLogger.log(
    action="执行任务",
    tool="my_tool",
    status="success",
    persona="P01诸葛亮",
    result="100% 完成",
    duration=5.2,
    dna="#龍芯⚡️2026-06-09-TASK"
)
```

### 方式 2: 自动计时（推荐）

```python
from action_logger import log_operation

# 自动记录执行时间
with log_operation("数据处理", "data_processor", persona="P05上帝之眼"):
    # 执行代码
    for i in range(1000):
        process_item(i)
    # 完成时自动计时并记录
```

### 方式 3: 在日常脚本中集成

```python
#!/usr/bin/env python3
import sys
from action_logger import ActionLogger, log_operation

def main():
    with log_operation("系统初始化", "system_init", persona="P02龍芯"):
        # 初始化系统
        setup_database()
        load_config()

    with log_operation("数据同步", "data_sync", persona="P05上帝之眼"):
        # 同步数据
        sync_from_remote()

    # 查看今天的操作
    ActionLogger.print_stats()

if __name__ == "__main__":
    main()
```

---

## 📊 action_log.jsonl 格式

每行都是有效的 JSON 对象：

```json
{
  "date": "2026-06-09T07:15:00",           // ISO 8601 时间戳
  "time": "2026-06-09 07:15:00",          // 可读时间戳
  "action": "每日复盘执行",                // 操作名称
  "tool": "daily_review",                  // 工具/模块名称
  "status": "success",                     // success|failed|warning
  "persona": "P03雯雯",                    // 执行人格（可选）
  "duration": 2.1,                         // 执行时长（秒，可选）
  "result": "7个检查项全部通过",           // 执行结果（可选）
  "dna": "#龍芯⚡️2026-06-09-DAILY-REVIEW" // DNA 签署（可选）
}
```

### 字段说明

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| date | string | ✅ | ISO 8601 时间戳 (UTC+8) |
| time | string | ✅ | 可读时间 (YYYY-MM-DD HH:MM:SS) |
| action | string | ✅ | 操作描述 (例: "系统扫描") |
| tool | string | ✅ | 工具名称 (例: "system_scan") |
| status | string | ✅ | 状态 (success/failed/warning) |
| persona | string | ❌ | 执行人格 (例: "P01诸葛亮") |
| duration | float | ❌ | 执行时长（秒） |
| result | string | ❌ | 执行结果 |
| dna | string | ❌ | DNA 签署码 |
| 自定义字段 | any | ❌ | 任何其他信息 |

---

## 🔧 高级用法

### 查询特定日期的日志

```bash
# 生成某日报告
python3 ~/longhun-system/action_logger.py report 2026-06-08
```

### 在 Shell 脚本中记录

```bash
#!/bin/bash

# 记录操作开始
python3 ~/longhun-system/action_logger.py log "备份开始" "backup_tool" "P02龍芯"

# 执行备份
tar czf backup.tar.gz /important/data

# 记录操作完成
if [ $? -eq 0 ]; then
    python3 ~/longhun-system/action_logger.py log "备份完成" "backup_tool" "P02龍芯"
else
    python3 ~/longhun-system/action_logger.py log "备份失败" "backup_tool" "P02龍芯"
fi
```

### 获取统计数据（编程方式）

```python
from action_logger import ActionLogger

# 获取今天的所有日志
logs = ActionLogger.get_today_logs()
print(f"今天 {len(logs)} 笔操作")

# 获取统计信息
stats = ActionLogger.get_stats(logs)
print(f"成功率: {100.0 * stats['status']['success'] / stats['total']:.1f}%")
print(f"总耗时: {stats['total_duration']:.2f} 秒")

# 按工具分类
for tool, count in stats['tools'].items():
    print(f"  {tool}: {count} 笔")
```

---

## 📈 与 daily_review.py 的集成

daily_review_enhanced.py 会自动读取 action_log.jsonl：

```python
def check_action_logs():
    """审计 action_log.jsonl 中今天的所有操作"""
    logs = ActionLogger.get_today_logs()
    count = len(logs)

    if count > 0:
        stats = ActionLogger.get_stats(logs)
        tools = len(stats['tools'])
        return ("🟢", f"今日操作 {count} 笔 ({tools}工具)")
    else:
        return ("🟡", "今日无操作记录")
```

---

## 🎯 使用场景

### 场景 1: 自动化脚本审计

```python
# 在每个自动化脚本的入口点添加
from action_logger import log_operation

def scheduled_job():
    with log_operation("定时备份", "scheduler", persona="P02龍芯"):
        perform_backup()

    with log_operation("数据验证", "scheduler", persona="P05上帝之眼"):
        validate_data()

    # 自动记录完成时间和状态
```

### 场景 2: 每日工作日志

```python
# 在工作开始时记录
ActionLogger.log("开始工作", "daily_work", persona="P03雯雯")

# 在完成各项任务时记录
ActionLogger.log("完成报告编写", "report_gen", duration=120)

# 在工作结束时查看统计
ActionLogger.print_stats()
```

### 场景 3: 故障排查

```bash
# 查找失败的操作
grep '"status": "failed"' ~/longhun-system/logs/action_log.jsonl

# 查看特定工具的操作
grep '"tool": "api_server"' ~/longhun-system/logs/action_log.jsonl

# 统计耗时最长的操作
cat ~/longhun-system/logs/action_log.jsonl | \
  jq '.duration' | sort -nr | head -10
```

---

## 📚 API 参考

### ActionLogger.log()

```python
ActionLogger.log(
    action: str,              # 必须：操作名称
    tool: str,                # 必须：工具名称
    status: str = "success",  # 可选：success|failed|warning
    persona: str = None,      # 可选：人格名称
    result: str = None,       # 可选：执行结果
    duration: float = None,   # 可选：执行时长
    dna: str = None,          # 可选：DNA 签署
    **kwargs                  # 可选：其他字段
)
```

### ActionLogger.get_today_logs()

```python
logs = ActionLogger.get_today_logs()
# 返回: list[dict] - 今天的所有日志记录
```

### ActionLogger.get_stats()

```python
stats = ActionLogger.get_stats(logs)
# 返回: dict 包含:
#   - total: 总数
#   - tools: {工具名: 计数}
#   - personas: {人格: 计数}
#   - status: {状态: 计数}
#   - total_duration: 总耗时
```

### log_operation (上下文管理器)

```python
with log_operation(action, tool, persona=None, dna=None):
    # 自动计时并记录
    do_something()
```

---

## 🔍 故障排查

### 日志写入失败

```bash
# 检查目录是否存在
ls -la ~/longhun-system/logs/

# 检查文件权限
ls -la ~/longhun-system/logs/action_log.jsonl

# 检查磁盘空间
df -h ~/longhun-system/
```

### 日志无法读取

```bash
# 验证 JSON 格式
python3 -m json.tool < ~/longhun-system/logs/action_log.jsonl | head -20

# 查找格式错误的行
python3 << 'EOF'
with open("~/longhun-system/logs/action_log.jsonl") as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except:
            print(f"第 {i} 行格式错误")
EOF
```

---

## 🔏 最佳实践

1. **始终包含 DNA 签署** - 便于追踪和验证
2. **记录执行时长** - 用于性能分析
3. **指定执行人格** - 用于职责追踪
4. **使用上下文管理器** - 自动计时和错误处理
5. **定期检查统计** - 通过 print_stats() 监控系统

---

## 📝 示例完整流程

```python
#!/usr/bin/env python3
from action_logger import ActionLogger, log_operation

def main():
    # 模拟一天的操作
    operations = [
        ("系统启动", "system", "P02龍芯"),
        ("数据同步", "sync", "P05上帝之眼"),
        ("报告生成", "report", "P03雯雯"),
        ("安全扫描", "security", "P04鲁班"),
    ]

    for action, tool, persona in operations:
        with log_operation(action, tool, persona=persona):
            # 模拟执行时间
            import time
            time.sleep(0.5)

    # 显示统计
    ActionLogger.print_stats()

    # 导出报告
    report = ActionLogger.export_report()
    print(report)

if __name__ == "__main__":
    main()
```

---

## 🔏 DNA 签署

```
DNA:#龍芯⚡️2026-06-09-ACTION-LOG-GUIDE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
```

**立即开始**: `python3 ~/longhun-system/action_logger.py stats`
