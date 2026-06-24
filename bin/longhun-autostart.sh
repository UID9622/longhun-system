#!/usr/bin/env bash
# 🐉 龍魂系统开机自启动脚本
# 统一启动常驻服务 + 认知压缩 + 分层治理自愈
#
# DNA:#龍芯⚡️2026-06-24-LONGHUN-AUTOSTART-v3.0

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/autostart.log"

echo "🐉 龍魂系统开机自启动 · $(date)" >> "$LOG_FILE"
echo "   统一启动器: bin/longhun-launcher.py" >> "$LOG_FILE"
echo "   治理自愈: bin/longhun-governance.py" >> "$LOG_FILE"

# 1) 调用统一启动器，开机自动模式
python3 "$ROOT/bin/longhun-launcher.py" start --autostart >> "$LOG_FILE" 2>&1

# 2) 自动压缩所有技能（一次性任务，不是常驻服务）
echo "   启动认知压缩引擎..." >> "$LOG_FILE"
python3 "$ROOT/scripts/longhun_compression_engine.py" --compress-all-skills >> "$LOG_FILE" 2>&1

# 3) 分层治理自愈：巡检 + 自动修复 + 报警
echo "   启动分层治理自愈..." >> "$LOG_FILE"
python3 "$ROOT/bin/longhun-governance.py" heal --json >> "$LOG_DIR/governance-autostart.json" 2>&1

# 4) 生成状态看板快照
python3 "$ROOT/bin/longhun-status.py" >> "$LOG_DIR/autostart-status.log" 2>&1

echo "✅ 开机自启动流程结束 · $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
