#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龙魂·自愈报告 v1.0 — 自动修复后推送结果                     ║
# ║  Self-Heal Report · 修复了什么 · 修好了没                      ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️2026-07-12-BARK-SELF-HEAL-REPORT-v1.0           ║
# ║  触发: 健康检查发现异常自动修复后执行                             ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

BASE_DIR="/opt/longhun-system"
BARK_SENDER="${BASE_DIR}/executors/bark/bark_send.py"
LOG_DIR="/var/log/longhun"

TS=$(date '+%Y-%m-%d %H:%M:%S')

# ── 读取上次健康检查日志中的修复操作 ──
HEAL_LOG="${LOG_DIR}/health.log"
ALARM_LOG="${LOG_DIR}/alarm.log"

# 最近一次健康检查的告警
RECENT_ALARMS=""
if [ -f "${ALARM_LOG}" ]; then
    RECENT_ALARMS=$(tail -30 "${ALARM_LOG}" | grep "$(date '+%Y-%m-%d')" || echo "")
fi

# 最近一次健康检查的修复操作
RESTART_ACTIONS=""
if [ -f "${HEAL_LOG}" ]; then
    RESTART_ACTIONS=$(tail -50 "${HEAL_LOG}" | grep -E "重启成功|重启失败|挂载成功|挂载失败" | tail -10 || echo "")
fi

# ── 当前服务状态 ──
SERVICES=("longhun-api" "longhun-audit" "longhun-core" "longhun-dashboard"
          "longhun-deepseek-executor" "longhun-gatekeeper" "longhun-local-gateway"
          "longhun-longzhishou" "longhun-orders" "longhun-portal"
          "longhun-sovereignty" "longhun-symbiote" "longhun-wechat" "longhun888")

FAILED_COUNT=0
FAILED_LIST=""
for svc in "${SERVICES[@]}"; do
    if ! systemctl is-active --quiet "${svc}" 2>/dev/null; then
        FAILED_COUNT=$((FAILED_COUNT + 1))
        FAILED_LIST="${FAILED_LIST}\n  ❌ ${svc}"
    fi
done

# ── 构造推送 ──
if [ ${FAILED_COUNT} -eq 0 ]; then
    TITLE="✅ 龙魂自愈 · 全部正常"
    LEVEL="green"
else
    TITLE="⚠️ 龙魂自愈 · ${FAILED_COUNT}个服务异常"
    LEVEL="red"
fi

BODY="🩺 自愈报告 · ${TS}

━━━━ 修复操作 ━━━━"
if [ -n "${RESTART_ACTIONS}" ]; then
    BODY="${BODY}
${RESTART_ACTIONS}"
else
    BODY="${BODY}
无最近修复操作"
fi

BODY="${BODY}

━━━━ 当前状态 ━━━━
运行中: $((${#SERVICES[@]} - FAILED_COUNT))/${#SERVICES[@]}"

if [ -n "${FAILED_LIST}" ]; then
    BODY="${BODY}
异常:${FAILED_LIST}"
fi

BODY="${BODY}

━━━━ 告警日志 ━━━━"
if [ -n "${RECENT_ALARMS}" ]; then
    # 截取最近5条
    RECENT_5=$(echo "${RECENT_ALARMS}" | tail -5)
    BODY="${BODY}
${RECENT_5}"
else
    BODY="${BODY}
今日无告警"
fi

BODY="${BODY}

━━━━━━━━━━━━━━━━━━
${TS} · 鲲鹏 · 自愈引擎"

echo "${BODY}" | python3 "${BARK_SENDER}" "${TITLE}" --stdin --group "龙魂自愈" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 自愈报告已推送 · 异常 ${FAILED_COUNT}" >> "${LOG_DIR}/self_heal.log"
