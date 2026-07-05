#!/bin/bash
# 龍魂内核一键启动脚本
# 同时启动：取证内核（8843） + 技能内核（8844）
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HOME/longhun-system/data/forensic_kernel"
mkdir -p "$LOG_DIR"

echo "🐉 启动龍魂内核集群..."

# 1. 启动取证内核（含证据、模块、技能清单）
python3 "$DIR/龍魂取证内核.py" --start > "$LOG_DIR/forensic_kernel.log" 2>&1 &
FORENSIC_PID=$!
echo "   取证内核 PID: $FORENSIC_PID  → http://127.0.0.1:8843/"

# 2. 启动技能内核（统一注册表 / 路由 / 评分 / 自优化）
python3 "$DIR/龍魂技能内核.py" --start --port 8844 > "$LOG_DIR/skill_kernel.log" 2>&1 &
SKILL_PID=$!
echo "   技能内核 PID: $SKILL_PID  → http://127.0.0.1:8844/"

# 保存 PID
echo "$FORENSIC_PID" > "$LOG_DIR/forensic_kernel.pid"
echo "$SKILL_PID" > "$LOG_DIR/skill_kernel.pid"

echo ""
echo "🐉 龍魂内核集群已启动"
echo "   取证面板: http://127.0.0.1:8843/"
echo "   技能面板: http://127.0.0.1:8844/"
echo "   停止命令: pkill -f '龍魂取证内核.py'; pkill -f '龍魂技能内核.py'"
