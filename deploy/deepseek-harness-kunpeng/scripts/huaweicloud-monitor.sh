#!/usr/bin/env bash
# 🐉 龍魂 · 华为云鲲鹏扣费与资源监控脚本
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-HUAWEI-CLOUD-MONITOR-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 告警默认输出到 stdout; 设置 BARK_KEY 后推送 Bark (与 health_check.sh 一致)

set -euo pipefail

echo "🐉 龍魂 · 华为云监控 $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# ============================================================
# 配置
# ============================================================
ALERT_CPU_THRESHOLD="${ALERT_CPU_THRESHOLD:-85}"
ALERT_MEM_THRESHOLD="${ALERT_MEM_THRESHOLD:-85}"
ALERT_DISK_THRESHOLD="${ALERT_DISK_THRESHOLD:-85}"
AUDIT_FILE="${AUDIT_FILE:-$HOME/.longhun/04_AUDIT/huawei_cloud_monitor.jsonl}"
BARK_KEY="${BARK_KEY:-}"          # 可选: 设置后推送告警到 Bark
BARK_URL="${BARK_URL:-https://api.day.app}"

mkdir -p "$(dirname "$AUDIT_FILE")"

# ============================================================
# 审计函数
# ============================================================
audit() {
    local metric="$1"
    local value="$2"
    local status="$3"
    echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"metric\":\"$metric\",\"value\":\"$value\",\"status\":\"$status\"}" >> "$AUDIT_FILE"
}

# ============================================================
# Bark 告警推送 (可选)
# ============================================================
bark_push() {
    [ -z "$BARK_KEY" ] && return 0
    local msg="$1"
    curl -s --max-time 5 -G "$BARK_URL/$BARK_KEY" \
        --data-urlencode "title=🐉 龍魂鲲鹏监控告警" \
        --data-urlencode "body=$msg" >/dev/null 2>&1 || true
}

# ============================================================
# 1. 系统资源 (兼容 top 各发行版输出; 空值防误报)
# ============================================================
echo "📊 系统资源"
CPU_USAGE="$(top -bn1 2>/dev/null | grep -i "Cpu(s)\|%Cpu" | head -n1 | awk '{for(i=1;i<=NF;i++) if($i ~ /^[0-9.]+$/) {print $i; break}}' || true)"
CPU_USAGE="${CPU_USAGE:-0}"
MEM_USAGE="$(free 2>/dev/null | awk '/Mem:/ {printf("%.1f", $3/$2 * 100.0)}' || echo "0")"
MEM_USAGE="${MEM_USAGE:-0}"
DISK_USAGE="$(df -h / 2>/dev/null | awk 'NR==2 {print $5}' | tr -d '%' || echo "0")"
DISK_USAGE="${DISK_USAGE:-0}"

# 数值化: 去非数字, 保证告警比较安全
cpu_int="${CPU_USAGE%.*}"
mem_int="${MEM_USAGE%.*}"
disk_int="${DISK_USAGE%.*}"
cpu_int="${cpu_int:-0}"; mem_int="${mem_int:-0}"; disk_int="${disk_int:-0}"

echo "  CPU: ${CPU_USAGE}%"
echo "  内存: ${MEM_USAGE}%"
echo "  磁盘: ${DISK_USAGE}%"

audit "cpu_usage" "$CPU_USAGE" "$([ "$cpu_int" -ge "$ALERT_CPU_THRESHOLD" ] && echo "alert" || echo "ok")"
audit "mem_usage" "$MEM_USAGE" "$([ "$mem_int" -ge "$ALERT_MEM_THRESHOLD" ] && echo "alert" || echo "ok")"
audit "disk_usage" "$DISK_USAGE" "$([ "$disk_int" -ge "$ALERT_DISK_THRESHOLD" ] && echo "alert" || echo "ok")"

# ============================================================
# 2. Docker 容器状态
# ============================================================
echo "🐳 Docker 容器"
if command -v docker >/dev/null 2>&1; then
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || true
    FAILED=$(docker ps --filter "health=unhealthy" --format "{{.Names}}" 2>/dev/null || true)
    if [ -n "$FAILED" ]; then
        echo "⚠️ 不健康容器: $FAILED"
        audit "docker_unhealthy" "$FAILED" "alert"
    else
        audit "docker_health" "all_healthy" "ok"
    fi
else
    echo "  未安装 Docker"
fi

# ============================================================
# 3. 华为云账单（优先 hcloud CLI，否则提示）
# ============================================================
echo "☁️ 华为云账单"
if command -v hcloud >/dev/null 2>&1; then
    BILL=$(hcloud bss bill show-monthly --region cn-east-3 2>/dev/null | tail -n 5 || echo "获取失败")
    echo "$BILL"
    audit "huawei_bill" "$BILL" "ok"
else
    echo "  hcloud CLI 未安装，跳过账单查询"
    echo "  如需启用，请安装华为云 CLI 并配置 AK/SK"
    audit "huawei_bill" "hcloud_not_installed" "warning"
fi

# ============================================================
# 4. 告警摘要
# ============================================================
echo ""
ALERTS=0
ALERT_MSG=""
[ "$cpu_int" -ge "$ALERT_CPU_THRESHOLD" ] && { echo "🔴 CPU 使用率过高 (${CPU_USAGE}%)"; ALERT_MSG="${ALERT_MSG}CPU ${CPU_USAGE}% "; ALERTS=$((ALERTS+1)); }
[ "$mem_int" -ge "$ALERT_MEM_THRESHOLD" ] && { echo "🔴 内存使用率过高 (${MEM_USAGE}%)"; ALERT_MSG="${ALERT_MSG}MEM ${MEM_USAGE}% "; ALERTS=$((ALERTS+1)); }
[ "$disk_int" -ge "$ALERT_DISK_THRESHOLD" ] && { echo "🔴 磁盘使用率过高 (${DISK_USAGE}%)"; ALERT_MSG="${ALERT_MSG}DISK ${DISK_USAGE}% "; ALERTS=$((ALERTS+1)); }

if [ "$ALERTS" -gt 0 ]; then
    bark_push "⚠️ $ALERT_MSG"
else
    echo "✅ 资源使用正常"
fi

echo ""
echo "📝 审计日志: $AUDIT_FILE"
