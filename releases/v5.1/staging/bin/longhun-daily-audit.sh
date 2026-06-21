#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 每日主動定時審計
# DNA:#龍芯⚡️2026-06-16-LONGHUN-DAILY-AUDIT-v1.0
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════
#
# 每日自動執行：
#   1. longhun-system 自我檢測評估
#   2. 倉儲AI標準檢查（若配置了 WAREHOUSE_AUDIT_SYSTEM）
#
# 推薦用法：由 cron 每日調用一次
#   0 9 * * * /Users/zuimeidedeyihan/longhun-system/bin/longhun-daily-audit.sh >> /Users/zuimeidedeyihan/longhun-system/logs/daily-audit.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$LONGHUN_DIR/logs"
mkdir -p "$LOG_DIR"

DATE_STR=$(date '+%Y-%m-%d %H:%M:%S')
echo ""
echo "═══════════════════════════════════════════════════"
echo "  龍魂每日審計啟動 · $DATE_STR"
echo "═══════════════════════════════════════════════════"

# 1. 系統自我檢測
echo ""
echo "[1/2] 執行 longhun-system 自我檢測..."
bash "$LONGHUN_DIR/bin/longhun-self-audit.sh"

# 2. 倉儲審計（僅在配置系統名時執行）
if [[ -n "${WAREHOUSE_AUDIT_SYSTEM:-}" ]]; then
    echo ""
    echo "[2/2] 執行倉儲AI標準檢查..."
    bash "$LONGHUN_DIR/bin/run-warehouse-audit.sh" \
        --system "$WAREHOUSE_AUDIT_SYSTEM" \
        --version "${WAREHOUSE_AUDIT_VERSION:-v1.0}" \
        --mode longhun \
        --format all
else
    echo ""
    echo "[2/2] 跳過倉儲審計（未設置 WAREHOUSE_AUDIT_SYSTEM）"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  龍魂每日審計完成 · $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════"
