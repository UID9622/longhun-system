#!/bin/bash
# 🧠 启动龍魂神经网络路由 · 实时状态总控
# DNA: #龍芯⚡️2026-07-05-LONGHUN-NEURAL-NETWORK-SERVER-START-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -uo pipefail

ROOT="$HOME/longhun-system"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

PID=$(lsof -ti :9627 2>/dev/null || true)
if [ -n "$PID" ]; then
  echo "🟡 神经网络状态总控已在运行 (PID: $PID)"
  echo "   访问: http://127.0.0.1:9627/"
  exit 0
fi

echo "🧠 启动龍魂神经网络路由 · 实时状态总控…"
nohup python3 "$ROOT/tools/longhun_neural_network_server.py" \
  > "$LOG_DIR/neural-network-server.out.log" \
  2> "$LOG_DIR/neural-network-server.err.log" &

sleep 2
PID=$(lsof -ti :9627 2>/dev/null || true)
if [ -n "$PID" ]; then
  echo "✅ 已启动 (PID: $PID)"
  echo "   访问: http://127.0.0.1:9627/"
else
  echo "🔴 启动失败，查看日志: $LOG_DIR/neural-network-server.err.log"
  exit 1
fi
