#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🛑 停止龍魂神经网络路由 · 实时状态总控
# DNA: #龍芯⚡️2026-07-05-LONGHUN-NEURAL-NETWORK-SERVER-STOP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -uo pipefail

PID=$(lsof -ti :9627 2>/dev/null || true)
if [ -z "$PID" ]; then
  echo "⚪ 神经网络状态总控未运行"
  exit 0
fi

echo "🛑 停止神经网络状态总控 (PID: $PID)…"
kill -TERM "$PID" 2>/dev/null || true
sleep 1
if lsof -ti :9627 >/dev/null 2>&1; then
  kill -KILL "$PID" 2>/dev/null || true
fi

if lsof -ti :9627 >/dev/null 2>&1; then
  echo "🔴 停止失败"
  exit 1
else
  echo "✅ 已停止"
fi
