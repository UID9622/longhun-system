---
name: longhun-backup
description: >
  龍魂备份恢复系统 (Longhun Backup & Recovery v5.1)。
  提供三层分级备份策略（L1协议文件 / L2五层脚本 / L3配置文件）、
  全量备份、增量备份、定时备份调度、快照恢复、版本回退、完整性验证等功能。
  适用于龍魂v5技能栈的备份保护与灾难恢复场景。
  当用户需要备份龍魂系统、恢复先前版本、验证备份完整性、
  或设置自动备份策略时使用此技能。
  DNA: #龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1
---

# 龍魂备份恢复系统 (L12)

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1`

## 1. 系统概述

龍魂备份恢复系统是龍魂v5技能栈的L12层组件，负责整个技能栈的数据保护与灾难恢复。系统采用三层分级备份策略，支持全量/增量/定时三种备份模式，并提供完整的恢复、回退、验证能力。

### 1.1 核心指标

| 指标 | 数值 |
|------|------|
| 总备份量 | 516KB |
| L1 协议文件备份 | 41KB |
| L2 五层脚本备份 | 340KB |
| L3 配置文件备份 | 135KB |

### 1.2 架构定位

```
龍魂v5技能栈 (Longhun v5 Skills Stack)
├── L0: 龍芯引擎 (core)
├── L1: 时间处理器 (time)
├── L2: 知识域控制器 (domain)
├── L3: 交互层 (interaction)
├── L4: 生态接口 (ecosystem)
├── L5: 诊断系统 (diagnostics)
├── L6-L11: 扩展技能
└── L12: 备份恢复系统 (backup) ← 本系统
```

## 2. 三层备份策略

### 2.1 策略定义

| 层级 | 名称 | 内容 | 大小 | 保留期 | 优先级 |
|------|------|------|------|--------|--------|
| **L1** | 协议文件备份 | CNSH协议文件v2.0双语版 | 41KB | 90天 | 1 (最高) |
| **L2** | 五层脚本备份 | L0-L4 + common + main.py + setup.sh | 340KB | 60天 | 2 |
| **L3** | 配置文件备份 | 权重·权限·熔断阈值·防护盾规则 | 135KB | 30天 | 3 |

### 2.2 文件分类规则

系统自动按文件路径和扩展名分类到对应层级：

- **L1**: `**/CNSH*`, `**/protocol*`, `**/*协议*`, `**/*.md`
- **L2**: `**/L[0-4]*`, `**/common*`, `**/main.py`, `**/setup.sh`, `**/*.py`, `**/*.sh`
- **L3**: `**/config*`, `**/*.json`, `**/*.yaml`, `**/*.yml`, `**/*.toml`, `**/weight*`, `**/permission*`, `**/fuse*`, `**/shield*`

默认归入L2。

## 3. 备份管理器

### 3.1 脚本位置

`scripts/备份管理器.py`

### 3.2 核心功能

| 功能 | 说明 |
|------|------|
| `full_backup()` | 全量备份 - 完整备份指定层级的所有文件 |
| `incremental_backup()` | 增量备份 - 基于父快照只备份变更文件 |
| `scheduled_backup()` | 定时备份 - 支持daily/hourly/weekly调度 |
| `verify_backup()` | 验证备份 - SHA256校验和 + tar.gz结构验证 |
| `cleanup_old_backups()` | 生命周期管理 - 按层级保留策略自动清理 |

### 3.3 CLI用法

```bash
# 全量备份
python3 scripts/备份管理器.py full /mnt/agents/output/longhun-v5-skills --layers L1 L2 L3 --label "v5.1-release"

# 增量备份
python3 scripts/备份管理器.py incremental /mnt/agents/output/longhun-v5-skills --base BH_20260115_120000_abc12345

# 列出快照
python3 scripts/备份管理器.py list --layer L2 --type full

# 验证备份
python3 scripts/备份管理器.py verify BH_20260115_120000_abc12345

# 清理过期备份
python3 scripts/备份管理器.py cleanup

# 定时备份 (每天2点)
python3 scripts/备份管理器.py schedule /mnt/agents/output/longhun-v5-skills --expr daily@02:00 --type incremental

# 统计信息
python3 scripts/备份管理器.py stats
```

### 3.4 定时备份表达式

| 表达式 | 含义 |
|--------|------|
| `hourly` | 每小时执行 |
| `daily@02:00` | 每天凌晨2点 |
| `weekly@sun@03:00` | 每周日3点 |
| `minute@5` | 每5分钟执行 |

## 4. 恢复系统

### 4.1 脚本位置

`scripts/恢复系统.py`

### 4.2 核心功能

| 功能 | 说明 |
|------|------|
| `restore_snapshot()` | 快照恢复 - 从tar.gz归档完整恢复到指定目录 |
| `rollback()` | 版本回退 - 按快照ID/时间戳/层级智能回退 |
| `rollback_to_last_good()` | 智能回退 - 自动找到最后一个验证通过的版本 |
| `verify_integrity()` | 完整性验证 - 多层验证（归档/校验和/tar/清单/文件级） |
| `diff_against_snapshot()` | 差异对比 - 对比当前目录与备份状态 |
| `selective_restore()` | 选择性恢复 - 按层级或文件模式选择性恢复 |

### 4.3 恢复流程

```
恢复请求
  ├── 1. 验证备份完整性 (verify_integrity)
  │     ├── 归档存在性检查
  │     ├── SHA256校验和验证
  │     ├── tar.gz结构完整性
  │     ├── 清单文件一致性
  │     └── (deep) 逐个文件校验和验证
  ├── 2. 创建恢复点 (备份当前状态)
  ├── 3. 执行恢复
  │     ├── 全量: 清空目标 → 解压归档
  │     └── 增量: 递归恢复父快照 → 应用增量变更
  └── 4. 验证恢复结果
```

### 4.4 CLI用法

```bash
# 完整性验证
python3 scripts/恢复系统.py verify BH_20260115_120000_abc12345 --deep

# 快照恢复
python3 scripts/恢复系统.py restore BH_20260115_120000_abc12345 /mnt/agents/output/longhun-v5-skills

# 版本回退 (指定快照)
python3 scripts/恢复系统.py rollback /mnt/agents/output/longhun-v5-skills --snapshot BH_20260115_120000_abc12345

# 版本回退 (指定时间)
python3 scripts/恢复系统.py rollback /mnt/agents/output/longhun-v5-skills --time "2026-01-15T12:00:00"

# 智能回退到最后可用版本
python3 scripts/恢复系统.py rollback-good /mnt/agents/output/longhun-v5-skills

# 差异对比
python3 scripts/恢复系统.py diff BH_20260115_120000_abc12345 /mnt/agents/output/longhun-v5-skills

# 选择性恢复 (只恢复L1层级)
python3 scripts/恢复系统.py selective BH_20260115_120000_abc12345 /tmp/restore --layer L1

# 选择性恢复 (按文件模式)
python3 scripts/恢复系统.py selective BH_20260115_120000_abc12345 /tmp/restore --pattern "*.py" "*.json"
```

## 5. 完整性验证体系

### 5.1 五层验证模型

| 层级 | 验证项 | 方法 |
|------|--------|------|
| L1-归档 | 归档文件存在性 | `os.path.exists()` |
| L2-校验和 | SHA256哈希匹配 | `hashlib.sha256()` |
| L3-结构 | tar.gz结构完整性 | `tarfile.open()` + 读取测试 |
| L4-清单 | 清单文件一致性 | JSON解析 + snapshot_id比对 |
| L5-深度 | 逐个文件校验和 | 解压后逐文件计算SHA256 |

### 5.2 验证状态

- **ok**: 所有检查通过，备份健康
- **warning**: 部分文件校验和不匹配（<5个），可恢复但需谨慎
- **corrupted**: 严重损坏，不建议恢复

## 6. 备份元数据结构

备份元数据存储在 `backup_meta.json`：

```json
{
  "dna": "#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1",
  "updated_at": "2026-01-15T12:00:00",
  "snapshots": [
    {
      "id": "BH_20260115_120000_abc12345",
      "timestamp": "2026-01-15T12:00:00",
      "type": "full",
      "status": "completed",
      "layers": ["L1", "L2", "L3"],
      "source_path": "/mnt/agents/output/longhun-v5-skills",
      "backup_path": "/mnt/agents/output/longhun-v5-skills/backups/BH_20260115_120000_abc12345/BH_20260115_120000_abc12345.tar.gz",
      "size_bytes": 528384,
      "file_count": 42,
      "checksum": "sha256_hash_here",
      "metadata": {
        "label": "v5.1-release",
        "total_size_human": "516KB",
        "layer_stats": {
          "L1": {"file_count": 5, "size_bytes": 41984, "size_human": "41KB"},
          "L2": {"file_count": 25, "size_bytes": 348160, "size_human": "340KB"},
          "L3": {"file_count": 12, "size_bytes": 138240, "size_human": "135KB"}
        }
      }
    }
  ],
  "policies": {}
}
```

## 7. 增量备份机制

### 7.1 工作原理

增量备份基于父快照的清单进行文件级去重：

1. 扫描源目录所有文件，计算SHA256校验和
2. 与父快照的清单对比
3. 只打包校验和发生变化的文件
4. 恢复时递归应用增量链

### 7.2 增量链

```
Full(BH_001) → Incr(BH_002, parent=BH_001) → Incr(BH_003, parent=BH_002)
                                                    ↓
恢复BH_003: 先恢复BH_001 → 应用BH_002增量 → 应用BH_003增量
```

## 8. 灾难恢复预案

### 8.1 场景矩阵

| 场景 | 响应 | 命令 |
|------|------|------|
| 文件误删除 | 智能回退 | `恢复系统.py rollback-good <target>` |
| 配置错误 | 选择性恢复L3 | `恢复系统.py selective <id> <target> --layer L3` |
| 脚本损坏 | 选择性恢复L2 | `恢复系统.py selective <id> <target> --layer L2` |
| 协议冲突 | 选择性恢复L1 | `恢复系统.py selective <id> <target> --layer L1` |
| 完整崩溃 | 全量恢复 | `恢复系统.py restore <id> <target>` |
| 回滚失败 | 恢复到恢复点 | 自动创建，手动从recovery_points目录恢复 |

### 8.2 恢复优先级

1. 首先尝试 **智能回退** (`rollback-good`)
2. 如果知道具体层级问题，使用 **选择性恢复**
3. 如果系统完全崩溃，使用 **全量快照恢复**
4. 所有恢复操作前自动创建 **恢复点**（当前状态的备份）

## 9. 目录结构

```
longhun-backup/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── 备份管理器.py                  # 备份管理
│   └── 恢复系统.py                    # 恢复系统
└── backups/                          # 默认备份根目录 (运行生成)
    ├── backup_meta.json              # 备份元数据
    ├── BH_xxxx/                      # 快照目录
    │   ├── BH_xxxx.tar.gz            # 备份归档
    │   └── backup_manifest.json      # 备份清单
    └── recovery_points/              # 恢复点
        └── RP_xxxx/
            └── RP_xxxx.tar.gz
```

## 10. 使用工作流

### 10.1 首次备份工作流

```bash
# 1. 执行全量备份
python3 scripts/备份管理器.py full /mnt/agents/output/longhun-v5-skills --layers L1 L2 L3 --label "initial"

# 2. 验证备份完整性
python3 scripts/恢复系统.py verify <snapshot_id> --deep

# 3. 设置定时增量备份
python3 scripts/备份管理器.py schedule /mnt/agents/output/longhun-v5-skills --expr daily@02:00
```

### 10.2 日常恢复工作流

```bash
# 1. 查看可用快照
python3 scripts/备份管理器.py list

# 2. 对比当前状态与备份
python3 scripts/恢复系统.py diff <snapshot_id> /mnt/agents/output/longhun-v5-skills

# 3. 执行恢复 (自动创建恢复点)
python3 scripts/恢复系统.py restore <snapshot_id> /mnt/agents/output/longhun-v5-skills

# 4. 验证恢复结果
python3 scripts/恢复系统.py verify <snapshot_id>
```

### 10.3 灾难恢复工作流

```bash
# 1. 快速智能回退
python3 scripts/恢复系统.py rollback-good /mnt/agents/output/longhun-v5-skills

# 2. 如果失败，查看恢复历史
python3 scripts/恢复系统.py history

# 3. 手动从恢复点恢复
ls backups/recovery_points/
```

## 11. Python API

### 11.1 备份管理器API

```python
from scripts.备份管理器 import BackupManager

# 初始化
bm = BackupManager("/path/to/backup/root")

# 全量备份
snapshot = bm.full_backup("/source/path", layers=["L1", "L2", "L3"], label="release")
print(f"备份ID: {snapshot.id}, 大小: {snapshot.size_bytes}")

# 增量备份
incr = bm.incremental_backup("/source/path", base_snapshot_id=snapshot.id)

# 列出快照
snaps = bm.list_snapshots(layers=["L2"], backup_type="full")

# 验证
result = bm.verify_backup(snapshot.id)

# 清理
bm.cleanup_old_backups()

# 统计
stats = bm.get_stats()
```

### 11.2 恢复系统API

```python
from scripts.恢复系统 import RecoverySystem

# 初始化
rs = RecoverySystem("/path/to/backup/root")

# 完整性验证
report = rs.verify_integrity(snapshot_id, deep_check=True)
print(f"状态: {report.overall_status}")

# 快照恢复
result = rs.restore_snapshot(snapshot_id, "/target/path", verify_before=True)

# 版本回退
result = rs.rollback("/target/path", to_snapshot_id="BH_xxx")
result = rs.rollback("/target/path", to_timestamp="2026-01-15T12:00:00")
result = rs.rollback("/target/path", to_layer_version="L2")

# 智能回退
result = rs.rollback_to_last_good("/target/path")

# 差异对比
diff = rs.diff_against_snapshot(snapshot_id, "/current/path")
print(f"新增: {len(diff.added)}, 删除: {len(diff.removed)}, 修改: {len(diff.modified)}")

# 选择性恢复
result = rs.selective_restore(snapshot_id, "/target/path", layers=["L3"])
result = rs.selective_restore(snapshot_id, "/target/path", file_patterns=["*.py", "*.json"])
```

## 12. 故障排查

### 12.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 备份失败，文件不存在 | 源路径错误 | 检查 `source_path` 是否存在 |
| 校验和不匹配 | 文件在备份过程中被修改 | 停止相关服务后重试 |
| 增量备份无变化 | 文件未变更 | 正常行为，检查文件修改时间 |
| 恢复后文件缺失 | 增量链断裂 | 检查父快照是否存在 |
| tar.gz损坏 | 磁盘故障或传输错误 | 使用 `--deep` 验证，删除损坏备份 |
| 定时备份不执行 | 调度器未启动 | 调用 `start_scheduler()` |
| 恢复点创建失败 | 磁盘空间不足 | 清理旧备份或扩展磁盘 |

### 12.2 日志解读

```
[2026-01-15 12:00:00] INFO | LonghunBackup | [全量备份] 开始 | ID=BH_xxx | 源=/path | 层级=['L1', 'L2', 'L3']
[2026-01-15 12:00:05] INFO | LonghunBackup | [全量备份] 完成 | ID=BH_xxx | 文件=42 | 大小=516KB
[2026-01-15 12:01:00] INFO | LonghunRecovery | [完整性验证] 开始 | ID=BH_xxx | 深度=True
[2026-01-15 12:01:02] INFO | LonghunRecovery | [完整性验证] 完成 | ID=BH_xxx | 状态=ok
```

### 12.3 调试模式

```python
import logging
logging.getLogger("LonghunBackup").setLevel(logging.DEBUG)
logging.getLogger("LonghunRecovery").setLevel(logging.DEBUG)
```

---

**龍魂备份恢复系统 v5.1** | DNA: `#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1`
