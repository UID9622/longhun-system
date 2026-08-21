#!/bin/bash
# =============================================================
# 🐉 龍魂审计全套流水线 v1.0
# DNA: #龍芯⚡️2026-08-21-AUDIT-FULL-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法:  bash scripts/audit_full.sh [--verbose] [--no-report]
# =============================================================

set -euo pipefail

# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/08_BIN"
SCRIPTS="$ROOT/scripts"
DOCS_AUDIT="$ROOT/docs/audit"
LOG_FILE="$ROOT/audit_run.log"

VERBOSE=false
SKIP_REPORT=false

for arg in "$@"; do
  case $arg in
    --verbose|-v) VERBOSE=true ;;
    --no-report)  SKIP_REPORT=true ;;
    --help|-h)
      echo "Usage: bash scripts/audit_full.sh [--verbose] [--no-report]"
      exit 0
      ;;
  esac
done

VERBOSE_FLAG=""
[ "$VERBOSE" = true ] && VERBOSE_FLAG="--verbose"

# 报告序号（用日期+秒生成唯一序号）
SEQ=$(date +"%H%M%S")
REPORT_FILE="$DOCS_AUDIT/audit_report_$(date +%Y%m%d)_${SEQ}.md"
LATEST_LINK="$DOCS_AUDIT/audit_report_latest.md"

# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────

STEP=0
FAILED_STEPS=()

step_header() {
  STEP=$((STEP + 1))
  echo ""
  echo "╬═══════════════════════════════════════════════════════════╬"
  echo "║  [$STEP] $1"
  echo "╬═══════════════════════════════════════════════════════════╬"
}

run_step() {
  local label="$1"
  shift
  if "$@" 2>&1 | tee -a "$LOG_FILE"; then
    echo "  ✅ $label 通过"
  else
    echo "  ❌ $label 失败"
    FAILED_STEPS+=("$label")
  fi
}

# ──────────────────────────────────────────────
# 启动
# ──────────────────────────────────────────────

cd "$ROOT"
mkdir -p "$DOCS_AUDIT"
> "$LOG_FILE"   # 清空日志

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂审计全套流水线 v1.0                             ║"
echo "║  时间: $(date '+%Y-%m-%d %H:%M:%S')                          ║"
echo "║  工作目录: $ROOT"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║  DNA: #龍芯⚡️$(date '+%Y-%m-%d')-AUDIT-FULL-PIPELINE              ║"
echo "║  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅             ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# ──────────────────────────────────────────────
# STEP 1 · DNA 引擎自测
# ──────────────────────────────────────────────

step_header "DNA 引擎自测（6 个锚点用例）"
run_step "DNA引擎自测" \
  python3 "$BIN/lh_dna_ref_impl.py" --selftest

# ──────────────────────────────────────────────
# STEP 2 · 代码审计节点
# ──────────────────────────────────────────────

step_header "代码审计节点（静态 + 动态）"
run_step "代码审计" \
  python3 "$BIN/audit_code.py" --module all $VERBOSE_FLAG

# ──────────────────────────────────────────────
# STEP 3 · 协议审计节点
# ──────────────────────────────────────────────

step_header "协议审计节点（注册表合规 + DNA格式）"
run_step "协议审计" \
  python3 "$BIN/audit_protocol.py" $VERBOSE_FLAG

# ──────────────────────────────────────────────
# STEP 4 · 红蓝对抗节点
# ──────────────────────────────────────────────

step_header "红蓝对抗节点（6 类攻击向量）"
run_step "红蓝对抗" \
  python3 "$BIN/audit_red_blue.py" --attack all $VERBOSE_FLAG

# ──────────────────────────────────────────────
# STEP 5 · 审计状态汇总
# ──────────────────────────────────────────────

step_header "审计状态汇总（七维度三色）"
run_step "审计状态" \
  python3 "$BIN/audit_status.py" --full

# ──────────────────────────────────────────────
# STEP 6 · 报告生成
# ──────────────────────────────────────────────

if [ "$SKIP_REPORT" = false ]; then
  step_header "审计报告生成（DNA签名 + Markdown）"
  run_step "报告生成" \
    python3 "$BIN/audit_report.py" \
      --output "$REPORT_FILE" \
      --scope "全部核心模块" \
      --auditor "龍魂自动审计引擎" \
      --seq "$SEQ"

  # 更新 latest 链接
  if [ -f "$REPORT_FILE" ]; then
    cp "$REPORT_FILE" "$LATEST_LINK"
    echo "  📎 最新报告: $LATEST_LINK"
  fi
else
  echo "  ⏭️  跳过报告生成 (--no-report)"
fi

# ──────────────────────────────────────────────
# 最终总结
# ──────────────────────────────────────────────

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"

if [ ${#FAILED_STEPS[@]} -eq 0 ]; then
  echo "║  🟢 全套流水线通过！                                        ║"
else
  echo "║  🔴 以下步骤失败:                                        ║"
  for step in "${FAILED_STEPS[@]}"; do
    echo "║    ❌ $step"
  done
fi

echo "║  完成时间: $(date '+%Y-%m-%d %H:%M:%S')                         ║"
echo "║  审计日志: audit_log.jsonl                                 ║"
echo "║  运行日志: audit_run.log                                    ║"
[ "$SKIP_REPORT" = false ] && \
echo "║  最新报告: docs/audit/audit_report_latest.md              ║"
echo "║  DNA: #龍芯⚡️$(date '+%Y-%m-%d')-AUDIT-FULL-DONE                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# 有失败步骤则返回非0退出码
[ ${#FAILED_STEPS[@]} -eq 0 ] || exit 1
