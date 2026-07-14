#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龙魂·知识图谱变更通知 v1.0                                 ║
# ║  Knowledge Graph Change Notify · 规则入库/降级/封存推送        ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️2026-07-12-BARK-KG-CHANGE-v1.0                 ║
# ║  触发: 知识图谱变更脚本执行后调用                                ║
# ║  用法: bash executors/bark/kg_change_notify.sh "操作" "规则名" "详情" ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

BASE_DIR="/opt/longhun-system"
BARK_SENDER="${BASE_DIR}/executors/bark/bark_send.py"
ACTION="${1:-更新}"
RULE_NAME="${2:-未知规则}"
DETAIL="${3:-}"

TS=$(date '+%Y-%m-%d %H:%M:%S')

# 操作类型图标
case "${ACTION}" in
    入库|新增|CREATE)     ICON="📥"; TYPE="入库" ;;
    降级|DOWNGRADE)      ICON="⬇️"; TYPE="降级" ;;
    封存|ARCHIVE)        ICON="📦"; TYPE="封存" ;;
    升级|UPGRADE|PROMOTE) ICON="⬆️"; TYPE="升级" ;;
    删除|DELETE)          ICON="🗑️"; TYPE="删除" ;;
    *)                   ICON="📝"; TYPE="${ACTION}" ;;
esac

TITLE="${ICON} 知识图谱${TYPE} · ${RULE_NAME}"

BODY="知识图谱变更 · ${TS}

操作: ${TYPE}
规则: ${RULE_NAME}"

if [ -n "${DETAIL}" ]; then
    BODY="${BODY}
详情: ${DETAIL}"
fi

# ── 知识图谱统计 ──
KG_DIR="${BASE_DIR}/03_知識圖譜"
if [ -d "${KG_DIR}" ]; then
    KG_FILES=$(find "${KG_DIR}" -name "*.json" -o -name "*.md" 2>/dev/null | wc -l | xargs)
    KG_SIZE=$(du -sh "${KG_DIR}" 2>/dev/null | cut -f1)
    BODY="${BODY}

知识图谱状态:
文件数: ${KG_FILES}
大小: ${KG_SIZE}"
fi

BODY="${BODY}

━━━━━━━━━━━━━━━━━━
${TS} · 龙魂知识矩阵"

echo "${BODY}" | python3 "${BARK_SENDER}" "${TITLE}" --stdin --group "龙魂知识" 2>&1
