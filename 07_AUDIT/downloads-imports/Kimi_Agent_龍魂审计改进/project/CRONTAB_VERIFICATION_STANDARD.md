# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
DNA 标识: DRAGON-SOUL-CRONTAB-STD-v1.0.0
作者: 龍魂系统运维团队
创建时间: 2024-01-15
审计修复: M2 - Crontab 未验证
-->

# Crontab 验证规范标准

## 1. 概述

本文档定义了龍魂系统中 crontab 定时任务配置的标准验证流程，确保所有定时任务在配置前、配置中、配置后均经过严格验证，防止因配置错误导致的服务中断或数据丢失。

**适用范围**: 所有生产环境、测试环境、预发布环境的 crontab 配置操作。

---

## 2. 验证流程总览

```
┌─────────────────────────────────────────────────────────────┐
│                    Crontab 配置验证流程                       │
├─────────────────────────────────────────────────────────────┤
│  阶段1: 配置前  ──▶  阶段2: 配置中  ──▶  阶段3: 配置后       │
│  (备份现有)          (编辑配置)          (验证写入)            │
│      │                                     │                │
│      ▼                                     ▼                │
│  阶段4: 验证检查  ──▶  阶段5: 测试执行  ──▶  完成            │
│  (grep检查)          (手动/自动测试)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 详细验证步骤

### 阶段1: 配置前 — 备份现有配置

**目的**: 在修改前保存当前配置，确保出现问题时可以快速回滚。

**必须执行的操作**:

```bash
# 1.1 显示当前 crontab 配置
crontab -l

# 1.2 备份当前配置到带时间戳的文件
BACKUP_FILE="$HOME/.crontab.backup.$(date '+%Y%m%d_%H%M%S')"
crontab -l > "${BACKUP_FILE}"
chmod 600 "${BACKUP_FILE}"

# 1.3 验证备份文件内容
echo "备份文件: ${BACKUP_FILE}"
wc -l "${BACKUP_FILE}"
ls -la "${BACKUP_FILE}"
```

**检查清单**:
- [ ] `crontab -l` 命令执行成功（或确认当前无配置）
- [ ] 备份文件已创建且大小大于 0 字节
- [ ] 备份文件权限为 600
- [ ] 备份文件路径已记录到变更日志

---

### 阶段2: 配置中 — 编辑 crontab

**方式A**: 使用 `crontab -e` 交互式编辑（推荐用于少量修改）

```bash
# 设置编辑器（如需要）
export EDITOR=vim

# 打开 crontab 编辑器
crontab -e
```

**方式B**: 使用临时文件方式（推荐用于批量部署/自动化）

```bash
# 2.1 创建临时编辑文件
CRON_TEMP=$(mktemp)
crontab -l > "${CRON_TEMP}" 2>/dev/null || true

# 2.2 追加新条目（示例: 每5分钟执行一次健康检查）
cat >> "${CRON_TEMP}" << 'EOF'

# ==== 龍魂系统健康检查任务 [DNA: DRAGON-SOUL-HEALTH-CHECK] ====
*/5 * * * * /opt/dragon_soul/scripts/health_check.sh >> /var/log/dragon_soul/health.log 2>&1
# ==== 龍魂系统健康检查任务结束 ====
EOF

# 2.3 语法预检查
# 使用 crontab 文件的语法检查（如果可用）
if command -v crontab &> /dev/null; then
    # 尝试加载检查（部分系统支持）
    crontab "${CRON_TEMP}" 2>&1 | head -20
fi

# 2.4 应用配置
crontab "${CRON_TEMP}"

# 2.5 清理临时文件
rm -f "${CRON_TEMP}"
```

**检查清单**:
- [ ] 新条目包含 DNA 标识注释
- [ ] 命令路径使用绝对路径
- [ ] 输出重定向到日志文件（避免邮件风暴）
- [ ] 语法格式正确（5个时间字段 + 命令）

---

### 阶段3: 配置后 — 验证新条目已写入

```bash
# 3.1 重新列出 crontab 配置
crontab -l

# 3.2 确认新条目存在
crontab -l | grep -i "DRAGON-SOUL"

# 3.3 显示新条目的行号
crontab -l | grep -n "DRAGON-SOUL"
```

**检查清单**:
- [ ] `crontab -l` 执行成功
- [ ] 新条目在输出中可见
- [ ] DNA 标识注释完整保留
- [ ] 条目内容与预期一致

---

### 阶段4: 验证检查 — grep 检查关键字段

```bash
# 4.1 检查 DNA 标识完整性
crontab -l | grep -E "^#.*DNA: DRAGON-SOUL"

# 4.2 检查命令路径有效性（示例）
CRON_CMD="/opt/dragon_soul/scripts/health_check.sh"
if crontab -l | grep -q "${CRON_CMD}"; then
    echo "命令路径已找到: ${CRON_CMD}"
    # 验证命令文件存在且可执行
    if [[ -x "${CRON_CMD}" ]]; then
        echo "命令文件存在且可执行: ✓"
    else
        echo "WARNING: 命令文件不存在或不可执行: ${CRON_CMD}"
    fi
fi

# 4.3 检查日志目录可写性
LOG_DIR="/var/log/dragon_soul"
if [[ -d "${LOG_DIR}" && -w "${LOG_DIR}" ]]; then
    echo "日志目录可写: ✓"
else
    echo "WARNING: 日志目录可能不可写: ${LOG_DIR}"
fi

# 4.4 检查是否有重复条目
DUPLICATE_COUNT=$(crontab -l | grep -c "DRAGON-SOUL")
echo "DNA 标识条目数量: ${DUPLICATE_COUNT}"
if [[ "${DUPLICATE_COUNT}" -gt 1 ]]; then
    echo "WARNING: 发现可能的重复条目"
fi
```

**检查清单**:
- [ ] DNA 标识注释完整
- [ ] 命令路径存在且可执行
- [ ] 日志目录可写
- [ ] 无重复条目
- [ ] 无语法错误提示

---

### 阶段5: 测试执行

**方式A**: 使用 `run-parts --test`（适用于 run-parts 管理的目录）

```bash
# 测试 /etc/cron.d 目录下的配置
if [[ -d /etc/cron.d ]]; then
    run-parts --test /etc/cron.d 2>&1 | grep -i "dragon" || true
fi
```

**方式B**: 手动触发测试（推荐）

```bash
# 5.1 提取要测试的命令
TEST_CMD=$(crontab -l | grep "DRAGON-SOUL" | grep -v "^#" | tail -1 | sed 's/^[^ ]* [^ ]* [^ ]* [^ ]* [^ ]* //')

# 5.2 在测试模式下执行（添加 --dry-run 或 TEST_MODE 标志）
echo "将要执行的命令: ${TEST_CMD}"

# 5.3 实际执行一次（注意环境变量差异）
# env -i HOME="$HOME" PATH="/usr/local/bin:/usr/bin:/bin" bash -c "${TEST_CMD}"
```

**方式C**: 等待下次执行时间并检查日志

```bash
# 5.4 记录当前时间，等待下次调度
echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "下次执行时间参考 crontab 表达式"

# 5.5 检查日志文件（执行后）
LOG_FILE="/var/log/dragon_soul/health.log"
if [[ -f "${LOG_FILE}" ]]; then
    tail -20 "${LOG_FILE}"
fi
```

**检查清单**:
- [ ] 手动测试执行成功
- [ ] 日志文件有正常输出
- [ ] 无权限错误
- [ ] 无路径找不到错误

---

## 4. 标准验证脚本模板

```bash
#!/bin/bash
# =============================================================================
# Crontab 验证脚本模板
# DNA: DRAGON-SOUL-CRONTAB-VERIFY-v1.0.0
# =============================================================================
set -euo pipefail

readonly DNA_MARKER="DRAGON-SOUL"
readonly LOG_DIR="/var/log/dragon_soul"
readonly SCRIPT_DIR="/opt/dragon_soul/scripts"

# 颜色定义
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

pass() { echo -e "${GREEN}[PASS]${NC} $*"; }
fail() { echo -e "${RED}[FAIL]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

# 阶段1: 备份
verify_backup() {
    echo "=== 阶段1: 备份验证 ==="
    if crontab -l &>/dev/null; then
        pass "当前 crontab 可读取"
    else
        warn "当前无 crontab 配置（可能是首次配置）"
    fi
}

# 阶段2: 配置写入验证
verify_write() {
    echo "=== 阶段2: 配置写入验证 ==="
    if crontab -l | grep -q "${DNA_MARKER}"; then
        pass "DNA 标识条目已写入 crontab"
    else
        fail "未找到 DNA 标识条目"
        return 1
    fi
}

# 阶段3: 关键字段验证
verify_fields() {
    echo "=== 阶段3: 关键字段验证 ==="
    local issues=0

    # 检查命令路径
    while IFS= read -r line; do
        if [[ "$line" =~ ^#.*DNA.*${DNA_MARKER} ]]; then
            continue
        fi
        if [[ "$line" =~ ${SCRIPT_DIR} ]]; then
            local cmd
            cmd=$(echo "$line" | awk '{for(i=6;i<=NF;i++) printf "%s ", $i; print ""}')
            cmd=$(echo "$cmd" | awk '{print $1}')
            if [[ -x "$cmd" ]]; then
                pass "命令可执行: ${cmd}"
            else
                fail "命令不存在或不可执行: ${cmd}"
                ((issues++)) || true
            fi
        fi
    done < <(crontab -l | grep "${DNA_MARKER}" | grep -v "^#")

    return $issues
}

# 阶段4: 日志目录验证
verify_logs() {
    echo "=== 阶段4: 日志目录验证 ==="
    if [[ -d "${LOG_DIR}" ]]; then
        if [[ -w "${LOG_DIR}" ]]; then
            pass "日志目录存在且可写: ${LOG_DIR}"
        else
            fail "日志目录不可写: ${LOG_DIR}"
        fi
    else
        warn "日志目录不存在: ${LOG_DIR}"
    fi
}

# 主函数
main() {
    echo "================================================"
    echo "Crontab 验证脚本"
    echo "DNA: DRAGON-SOUL-CRONTAB-VERIFY-v1.0.0"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "================================================"

    verify_backup
    verify_write
    verify_fields
    verify_logs

    echo "================================================"
    echo "验证完成"
    echo "================================================"
}

main "$@"
```

---

## 5. 常见问题排查

### 问题1: `crontab -e` 无法保存

**症状**: 编辑器提示保存失败或权限不足。

**排查步骤**:
```bash
# 检查用户是否有 crontab 权限
cat /etc/cron.allow 2>/dev/null || echo "无 allow 文件"
cat /etc/cron.deny 2>/dev/null || echo "无 deny 文件"

# 检查 SELinux 状态（如适用）
sestatus 2>/dev/null || true

# 使用临时文件方式替代
CRON_TMP=$(mktemp)
crontab -l > "${CRON_TMP}" 2>/dev/null || true
# 编辑 ${CRON_TMP}
crontab "${CRON_TMP}"
rm -f "${CRON_TMP}"
```

**解决方案**:
- 确保用户在 `/etc/cron.allow` 中（如果存在该文件）
- 检查文件系统是否只读: `mount | grep " $(dirname $(which crontab)) "`
- 检查磁盘空间: `df -h /tmp /var`

---

### 问题2: 任务不执行

**症状**: crontab 配置正确但任务未按预期执行。

**排查步骤**:
```bash
# 1. 检查 cron 服务状态
systemctl status crond 2>/dev/null || service cron status 2>/dev/null

# 2. 检查系统日志
grep CRON /var/log/syslog 2>/dev/null | tail -20
grep CRON /var/log/cron 2>/dev/null | tail -20
journalctl -u cron 2>/dev/null | tail -20

# 3. 检查环境变量差异
echo "SHELL=$SHELL"
echo "PATH=$PATH"
echo "HOME=$HOME"
# crontab 中的环境变量可能不同！
```

**解决方案**:
- 在 crontab 中显式设置 PATH: `PATH=/usr/local/bin:/usr/bin:/bin`
- 使用绝对路径
- 检查命令权限: `ls -la <命令路径>`

---

### 问题3: 邮件风暴（大量邮件输出）

**症状**: 系统产生大量 cron 邮件。

**排查步骤**:
```bash
# 检查邮件队列
mailq 2>/dev/null | head -10

# 检查 cron 输出是否重定向
crontab -l | grep -v ">/dev/null" | grep -v "2>&1"
```

**解决方案**:
- 所有 cron 命令必须重定向输出:
  ```
  * * * * * /path/to/script.sh >> /var/log/script.log 2>&1
  ```
- 或设置 MAILTO="" 禁用邮件

---

### 问题4: 权限被拒绝

**症状**: 日志中出现 "Permission denied" 错误。

**排查步骤**:
```bash
# 检查脚本权限
ls -la /opt/dragon_soul/scripts/

# 检查日志目录权限
ls -la /var/log/dragon_soul/

# 检查 crontab 运行用户
ps aux | grep cron
```

**解决方案**:
- 确保脚本有执行权限: `chmod +x /path/to/script.sh`
- 确保日志目录可写: `chmod 755 /var/log/dragon_soul`
- 考虑使用 `sudo` 或调整目录所有者

---

### 问题5: 时区问题

**症状**: 任务执行时间与预期不一致。

**排查步骤**:
```bash
# 检查系统时区
date
cat /etc/timezone 2>/dev/null
timedatectl 2>/dev/null | grep "Time zone"

# 检查 cron 守护进程时区
cat /etc/sysconfig/clock 2>/dev/null
```

**解决方案**:
- 在 crontab 中设置 TZ 变量: `TZ=Asia/Shanghai`
- 确保系统时区配置正确

---

## 6. 变更记录

| 版本   | 日期       | 修改人     | 修改内容               |
|--------|------------|------------|------------------------|
| 1.0.0  | 2024-01-15 | 龍魂运维团队 | 初始版本，修复 M2      |
