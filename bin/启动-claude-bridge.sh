#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║     龍魂 Claude 国内中继桥 · 启动脚本                                       ║
# ║     数据在中国 · 本地中继 · Claude当工具 · 龍魂当主人                          ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️丙午·丙申·乙卯·亥时·需-CLAUDE-BRIDGE-START-v1.0                ║
# ║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

cd "$(dirname "$0")"

# 端口
PORT="${CLAUDE_BRIDGE_PORT:-8789}"
HOST="${CLAUDE_BRIDGE_HOST:-127.0.0.1}"

echo ""
echo "🐉 龍魂 Claude 国内中继桥"
echo "   数据在中国 · 本地中继"
echo "   Claude当工具 · 龍魂当主人"
echo ""
echo "   监听: $HOST:$PORT"
echo "   日志: ~/longhun-system/logs/claude_bridge.log"
echo ""

# 启动
python3 bin/lh_claude_bridge.py
