#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 每日主动定时审计
# DNA:#龍芯⚡️2026-06-16-LONGHUN-DAILY-AUDIT-FILE1-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════
#
# 每日自动执行：
#   1. longhun-system 自我检测评估
#   2. 仓储AI标准检查（若配置了 WAREHOUSE_AUDIT_SYSTEM）
#
# 推荐用法：由 cron 每日调用一次
#   0 9 * * * /Users/zuimeidedeyihan/longhun-system/bin/longhun-daily-audit.sh >> /Users/zuimeidedeyihan/longhun-system/logs/daily-audit.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$LONGHUN_DIR/logs"
mkdir -p "$LOG_DIR"

DATE_STR=$(date '+%Y-%m-%d %H:%M:%S')
echo ""
echo "═══════════════════════════════════════════════════"
echo "  龍魂每日审计启动 · $DATE_STR"
echo "═══════════════════════════════════════════════════"

# 1. 系统自我检测
echo ""
echo "[1/2] 执行 longhun-system 自我检测..."
bash "$LONGHUN_DIR/bin/longhun-self-audit.sh"

# 2. 仓储审计（仅在配置系统名时执行）
if [[ -n "${WAREHOUSE_AUDIT_SYSTEM:-}" ]]; then
    echo ""
    echo "[2/2] 执行仓储AI标准检查..."
    bash "$LONGHUN_DIR/bin/run-warehouse-audit.sh" \
        --system "$WAREHOUSE_AUDIT_SYSTEM" \
        --version "${WAREHOUSE_AUDIT_VERSION:-v1.0}" \
        --mode longhun \
        --format all
else
    echo ""
    echo "[2/2] 跳过仓储审计（未设置 WAREHOUSE_AUDIT_SYSTEM）"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  龍魂每日审计完成 · $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════"
