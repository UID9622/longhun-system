#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 仓储AI标准检查定时运行器
# DNA: #龍芯⚡️2026-06-16-WAREHOUSE-AUDIT-RUNNER-v1.0
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$LONGHUN_DIR/skills/warehouse-audit"
ENGINE="$SKILL_DIR/scripts/audit_engine.py"
REPORTS_DIR="$SKILL_DIR/reports"

# 默认参数
SYSTEM_NAME="${WAREHOUSE_AUDIT_SYSTEM:-龍魂仓储系统}"
SYSTEM_VERSION="${WAREHOUSE_AUDIT_VERSION:-v1.0}"
DIMENSIONS="${WAREHOUSE_AUDIT_DIMENSIONS:-all}"
MODE="${WAREHOUSE_AUDIT_MODE:-longhun}"
FORMAT="${WAREHOUSE_AUDIT_FORMAT:-all}"

usage() {
    cat << EOF
用法: $(basename "$0") [选项]

选项:
  --system <名称>      被检查系统名称 (默认: $SYSTEM_NAME)
  --version <版本>     系统版本 (默认: $SYSTEM_VERSION)
  --dimensions <维度>  检查维度 (默认: $DIMENSIONS)
  --mode <模式>        standard 或 longhun (默认: $MODE)
  --format <格式>      markdown/json/all (默认: $FORMAT)
  --output <目录>      报告输出目录 (默认: $REPORTS_DIR)
  -h, --help           显示此帮助

环境变量:
  WAREHOUSE_AUDIT_SYSTEM, WAREHOUSE_AUDIT_VERSION, WAREHOUSE_AUDIT_DIMENSIONS,
  WAREHOUSE_AUDIT_MODE, WAREHOUSE_AUDIT_FORMAT

示例:
  $(basename "$0") --system "温州电商仓" --version "v2.1" --mode longhun
EOF
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --system) SYSTEM_NAME="$2"; shift 2 ;;
        --version) SYSTEM_VERSION="$2"; shift 2 ;;
        --dimensions) DIMENSIONS="$2"; shift 2 ;;
        --mode) MODE="$2"; shift 2 ;;
        --format) FORMAT="$2"; shift 2 ;;
        --output) REPORTS_DIR="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "未知参数: $1"; usage; exit 1 ;;
    esac
done

mkdir -p "$REPORTS_DIR"

echo "🐉 龍魂体系 · 仓储AI标准检查启动"
echo "   系统: $SYSTEM_NAME $SYSTEM_VERSION"
echo "   维度: $DIMENSIONS"
echo "   模式: $MODE"
echo "   输出: $REPORTS_DIR"
echo ""

python3 "$ENGINE" \
    --system "$SYSTEM_NAME" \
    --version "$SYSTEM_VERSION" \
    --dimensions "$DIMENSIONS" \
    --mode "$MODE" \
    --format "$FORMAT" \
    --output "$REPORTS_DIR"

echo ""
echo "✅ 检查完成，报告已保存至: $REPORTS_DIR"
