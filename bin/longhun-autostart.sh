#!/usr/bin/env bash
# 🐉 龍魂系统开机自启动脚本 v3.1
# 统一启动常驻服务 + 认知压缩 + 分层治理自愈
# 已集成反熔断守卫：过载检查 → 执行 → 输出契约校验 → 审计日志
#
# DNA:#龍芯⚡️2026-06-25-LONGHUN-AUTOSTART-v3.1
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/autostart.log"
GUARD="python3 $ROOT/persona/anti_blowout_guard.py --json"

echo "🐉 龍魂系统开机自启动 · $(date)" >> "$LOG_FILE"

# 1) 启动核心服务
$GUARD --op deploy --evidence '{"artifact_path":"bin/longhun-launcher.py","mode":"autostart"}' -- python3 "$ROOT/bin/longhun-launcher.py" start --autostart >> "$LOG_FILE" 2>&1 || true

# 2) 自动压缩技能
$GUARD --op compress --evidence '{"artifact_path":"scripts/longhun_compression_engine.py"}' -- python3 "$ROOT/scripts/longhun_compression_engine.py" --compress-all-skills >> "$LOG_FILE" 2>&1 || true

# 3) 分层治理自愈
$GUARD --op audit --evidence '{"artifact_path":"bin/longhun-governance.py"}' -- python3 "$ROOT/bin/longhun-governance.py" heal --json >> "$LOG_DIR/governance-autostart.json" 2>&1 || true

# 4) 生成状态看板快照
$GUARD --op check --evidence '{"artifact_path":"bin/longhun-status.py"}' -- python3 "$ROOT/bin/longhun-status.py" >> "$LOG_DIR/autostart-status.log" 2>&1 || true

# 5) 每日复盘
$GUARD --op daily_review --evidence '{"artifact_path":"daily_review.py"}' -- python3 "$ROOT/daily_review.py" >> "$LOG_FILE" 2>&1 || true

echo "✅ 开机自启动流程结束 · $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
