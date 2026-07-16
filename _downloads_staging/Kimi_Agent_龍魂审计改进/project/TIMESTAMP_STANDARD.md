<!--
DNA 标识: DRAGON-SOUL-TIMESTAMP-STD-v1.0.0
作者: 龙魂系统架构团队
创建时间: 2024-01-15
审计修复: M1 - 时序不一致
-->

# 时序记录标准

## 1. 概述

本文档定义龙魂系统中统一的时序记录标准，解决审计发现的多阶段报告时间戳不一致问题（M1）。所有系统组件、脚本、报告和日志必须遵循此标准。

**核心原则**:
- **唯一时间源**: 所有时间戳必须基于同一时间源生成
- **不可变引用**: 第一阶段的时间戳作为后续所有阶段的引用基准
- **显式时区**: 所有时间戳必须包含时区信息

---

## 2. 时间戳格式规范

### 2.1 标准格式

**唯一合法格式**:

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
```

**输出示例**:
```
2024-01-15 14:30:45 CST
```

### 2.2 格式说明

| 字段       | 格式     | 示例   | 说明                    |
|------------|----------|--------|-------------------------|
| 年         | %Y       | 2024   | 4位年份                 |
| 月         | %m       | 01     | 2位月份 (01-12)         |
| 日         | %d       | 15     | 2位日期 (01-31)         |
| 时         | %H       | 14     | 24小时制 (00-23)        |
| 分         | %M       | 30     | 2位分钟 (00-59)         |
| 秒         | %S       | 45     | 2位秒 (00-59)           |
| 时区       | %Z       | CST    | 时区缩写 (如 CST, UTC)  |

### 2.3 禁止使用的格式

以下格式**严禁**在新代码中使用:

```bash
# 禁止: 无时区信息
date '+%Y-%m-%d %H:%M:%S'        # 错误!

# 禁止: 12小时制（有歧义）
date '+%Y-%m-%d %I:%M:%S %p'     # 错误!

# 禁止: 仅日期
date '+%Y-%m-%d'                  # 错误!（用于日志文件名时除外）

# 禁止: 本地化格式
date                              # 输出不统一，禁止!
```

### 2.4 文件名安全格式

用于日志文件名时（无时区和空格）:

```bash
date '+%Y%m%d_%H%M%S'
# 输出: 20240115_143045
```

---

## 3. 时间源同步机制

### 3.1 唯一时间源定义

```bash
# /opt/dragon_soul/config/time_source.conf
# =============================================================================
# 龙魂系统时间源配置文件
# DNA: DRAGON-SOUL-TIME-SOURCE-v1.0.0
# =============================================================================

# 时间同步服务器
NTP_SERVERS=(
    "ntp1.aliyun.com"
    "ntp2.aliyun.com"
    "pool.ntp.org"
)

# 同步间隔（秒）
SYNC_INTERVAL=300

# 时区设置
SYSTEM_TIMEZONE="Asia/Shanghai"
```

### 3.2 时间同步脚本

```bash
#!/bin/bash
# =============================================================================
# 时间同步脚本
# DNA: DRAGON-SOUL-TIME-SYNC-v1.0.0
# =============================================================================
set -euo pipefail

# 同步时间
sync_time() {
    local ntp_server="${1:-ntp1.aliyun.com}"

    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] 开始时间同步..."

    if command -v chronyc &> /dev/null; then
        chronyc makestep
    elif command -v ntpdate &> /dev/null; then
        ntpdate -u "$ntp_server"
    elif command -v sntp &> /dev/null; then
        sntp -s "$ntp_server"
    else
        echo "WARNING: 无可用的时间同步工具"
        return 1
    fi

    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] 时间同步完成"
}

# 验证时间偏差
verify_time_drift() {
    local max_drift_ms="${1:-1000}"  # 最大允许偏差 1秒

    # 使用ntpdate查询偏差（只查不改）
    if command -v ntpdate &> /dev/null; then
        local drift
        drift=$(ntpdate -q ntp1.aliyun.com 2>/dev/null | awk '/offset/ {print $10}')
        echo "当前时间偏差: ${drift} ms"

        if (( $(echo "${drift} > ${max_drift_ms}" | bc -l) )); then
            echo "WARNING: 时间偏差超过阈值"
            return 1
        fi
    fi
}

sync_time
verify_time_drift
```

### 3.3 时间源健康检查

```bash
# 检查时间同步状态
check_time_sync() {
    echo "=== 时间源健康检查 ==="
    echo "当前系统时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "系统时区: $(timedatectl show --property=Timezone --value 2>/dev/null || cat /etc/timezone 2>/dev/null)"

    # 检查 NTP 同步状态
    if command -v timedatectl &> /dev/null; then
        timedatectl status | grep "NTP enabled\|NTP synchronized\|System clock synchronized"
    fi

    # 检查 chronyd 状态
    if command -v chronyc &> /dev/null; then
        chronyc tracking 2>/dev/null | head -5
    fi
}
```

---

## 4. 多阶段时间戳引用规范

### 4.1 核心规则

**所有阶段报告必须引用第一阶段的时间戳**，确保全链路时序一致性。

```
阶段1 (初始化)          阶段2 (处理)            阶段3 (验证)            阶段4 (报告)
   │                       │                       │                       │
   ▼                       ▼                       ▼                       ▼
T1=2024-01-15            T2引用T1               T3引用T1               T4引用T1
   14:30:45 CST          开始处理:               开始验证:               生成报告:
                         "基于 2024-01-15        "基于 2024-01-15        "基于 2024-01-15
                         14:30:45 CST            14:30:45 CST            14:30:45 CST
                         启动处理"               启动验证"               生成最终报告"
```

### 4.2 环境变量传递

```bash
#!/bin/bash
# =============================================================================
# 多阶段处理示例
# DNA: DRAGON-SOUL-PHASED-PROCESS-v1.0.0
# =============================================================================
set -euo pipefail

# ---- 阶段1: 初始化 ----
# 记录第一阶段时间戳到环境变量
export PHASE1_TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S %Z')"
export PHASE1_EPOCH="$(date +%s)"

log_with_phase1() {
    local message="$1"
    local current_time
    current_time="$(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "[${current_time}] [REF: ${PHASE1_TIMESTAMP}] ${message}"
}

# ---- 阶段2: 处理 ----
phase2_process() {
    log_with_phase1 "阶段2开始: 数据处理"
    # 处理逻辑...
    sleep 1
    log_with_phase1 "阶段2完成: 数据处理结束"
}

# ---- 阶段3: 验证 ----
phase3_verify() {
    log_with_phase1 "阶段3开始: 结果验证"
    # 验证逻辑...
    log_with_phase1 "阶段3完成: 验证通过"
}

# ---- 阶段4: 报告 ----
phase4_report() {
    local current_time
    current_time="$(date '+%Y-%m-%d %H:%M:%S %Z')"

    cat << EOF
===============================================================================
龙魂系统处理报告
===============================================================================
第一阶段时间戳: ${PHASE1_TIMESTAMP}
报告生成时间:   ${current_time}
总耗时:         $(($(date +%s) - PHASE1_EPOCH)) 秒

各阶段引用基准: ${PHASE1_TIMESTAMP}
===============================================================================
EOF
}

# 主流程
phase2_process
phase3_verify
phase4_report
```

### 4.3 跨脚本时间戳传递

当多个独立脚本需要共享时间戳时，使用文件传递:

```bash
# 写入共享时间戳文件
write_shared_timestamp() {
    local timestamp_file="/var/run/dragon_soul/phase1.timestamp"
    mkdir -p "$(dirname "$timestamp_file")"
    date '+%Y-%m-%d %H:%M:%S %Z' > "$timestamp_file"
    chmod 644 "$timestamp_file"
}

# 读取共享时间戳
read_shared_timestamp() {
    local timestamp_file="/var/run/dragon_soul/phase1.timestamp"
    if [[ -f "$timestamp_file" ]]; then
        cat "$timestamp_file"
    else
        date '+%Y-%m-%d %H:%M:%S %Z'
    fi
}
```

---

## 5. 记录位置规范

### 5.1 日志文件路径

| 日志类型         | 路径                                          | 格式要求               |
|------------------|-----------------------------------------------|------------------------|
| 系统主日志       | `/var/log/dragon_soul/system.log`             | 每行包含标准时间戳     |
| 审计日志         | `/var/log/dragon_soul/audit/YYYY/MM/DD.log`   | 不可修改，只追加       |
| 阶段报告         | `/var/log/dragon_soul/reports/`               | 文件名包含阶段1时间戳  |
| 错误日志         | `/var/log/dragon_soul/error.log`              | 包含堆栈和时间戳       |

### 5.2 日志行格式

```
[2024-01-15 14:30:45 CST] [INFO] [module:welding] 焊接点 WP-001 验证通过
└──────── 标准时间戳 ────────┘ └─级别┘ └── 模块 ──┘ └────── 消息 ────────┘
```

### 5.3 数据库记录

```sql
-- 审计表时间戳字段
CREATE TABLE audit_log (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    phase1_timestamp TIMESTAMP NOT NULL,  -- 第一阶段时间戳（引用基准）
    event_timestamp  TIMESTAMP NOT NULL,  -- 事件实际发生时间
    timezone        VARCHAR(10) NOT NULL DEFAULT 'CST',
    event_type      VARCHAR(50) NOT NULL,
    event_data      JSON,
    INDEX idx_phase1 (phase1_timestamp),
    INDEX idx_event  (event_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 6. 一致性验证

### 6.1 自动化验证脚本

```bash
#!/bin/bash
# =============================================================================
# 时间戳一致性验证脚本
# DNA: DRAGON-SOUL-TIMESTAMP-VERIFY-v1.0.0
# =============================================================================
set -euo pipefail

verify_timestamp_format() {
    local file="$1"
    local invalid_count=0

    echo "=== 验证文件: ${file} ==="

    # 检查是否符合标准格式: YYYY-MM-DD HH:MM:SS TZ
    while IFS= read -r line; do
        # 查找可能的时间戳模式
        if echo "$line" | grep -qP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'; then
            # 检查是否包含时区
            if ! echo "$line" | grep -qP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{2,4}'; then
                echo "WARNING: 时间戳缺少时区: ${line:0:100}"
                ((invalid_count++)) || true
            fi
        fi
    done < "$file"

    if [[ $invalid_count -eq 0 ]]; then
        echo "PASS: 所有时间戳格式正确"
        return 0
    else
        echo "FAIL: 发现 ${invalid_count} 个格式问题"
        return 1
    fi
}

# 验证日志目录
verify_log_directory() {
    local log_dir="/var/log/dragon_soul"
    echo "=== 验证日志目录时间戳一致性 ==="

    for logfile in "${log_dir}"/*.log; do
        if [[ -f "$logfile" ]]; then
            verify_timestamp_format "$logfile"
        fi
    done
}

verify_log_directory
```

### 6.2 一致性检查清单

- [ ] 所有日志行的时间戳使用 `+%Y-%m-%d %H:%M:%S %Z` 格式
- [ ] 所有阶段报告引用第一阶段时间戳
- [ ] 跨脚本调用时时间戳通过环境变量或文件传递
- [ ] 数据库记录包含 phase1_timestamp 和 event_timestamp
- [ ] 文件名中的时间戳使用 `%Y%m%d_%H%M%S` 格式
- [ ] 时区设置统一为 `Asia/Shanghai`
- [ ] NTP 同步正常，时间偏差不超过 1 秒

---

## 7. 实施检查表

| 组件类型     | 实施项                                          | 状态 |
|--------------|-------------------------------------------------|------|
| Shell 脚本   | 使用 `date '+%Y-%m-%d %H:%M:%S %Z'` 获取时间戳  | ⬜   |
| Python 代码  | 使用 `datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')` | ⬜   |
| 配置文件     | 包含时区设置和 NTP 服务器配置                    | ⬜   |
| 日志文件     | 每行以标准时间戳开头                             | ⬜   |
| 数据库       | 包含 phase1_timestamp 引用字段                   | ⬜   |
| 报告模板     | 显示第一阶段时间戳作为基准                       | ⬜   |
| CI/CD 流水线 | 构建时间戳与部署时间戳使用同一格式               | ⬜   |
| 监控告警     | 告警时间戳使用标准格式                           | ⬜   |

---

## 8. 变更记录

| 版本   | 日期       | 修改人       | 修改内容                 |
|--------|------------|--------------|--------------------------|
| 1.0.0  | 2024-01-15 | 龙魂架构团队 | 初始版本，修复 M1        |
