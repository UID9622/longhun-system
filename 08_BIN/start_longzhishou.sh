#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍智守本地控制接口 · 启动脚本 v2.0
# Flask 服务，监听 127.0.0.1:5001，接收飞书 Webhook 回调
# DNA: #龍芯⚡️2026-07-06-LONGZHISHOU-START-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/longzhishou.out.log"
ERR_FILE="$LOG_DIR/longzhishou.err.log"

SERVER="$ROOT/dist/龍智守_v2.0_20260630_142007/龍智守_本地控制接口_v2.0.py"
PY3="/Users/zuimeidedeyihan/.longhun/bin/python3"
PORT=5001

echo "[$(date)] 🐉 龍智守启动中..." | tee -a "$LOG_FILE"

# 1. 检查服务文件
if [ ! -f "$SERVER" ]; then
    echo "🔴 龍智守服务文件不存在: $SERVER" | tee -a "$ERR_FILE"
    exit 1
fi

# 2. 杀掉旧进程（如果端口已被占用）
OLD_PID=$(lsof -ti:$PORT 2>/dev/null || true)
if [ -n "$OLD_PID" ]; then
    echo "🟡 端口 $PORT 被占用 (PID: $OLD_PID)，先释放..." | tee -a "$LOG_FILE"
    kill -9 $OLD_PID 2>/dev/null || true
    sleep 1
fi

# 3. 启动服务
export PYTHONPATH="$ROOT/scripts:$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONUNBUFFERED=1

cd "$ROOT"
nohup "$PY3" "$SERVER" >> "$LOG_FILE" 2>> "$ERR_FILE" &
PID=$!

sleep 2

# 4. 验证
if kill -0 "$PID" 2>/dev/null && lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ 龍智守已启动 · PID: $PID · 端口: $PORT" | tee -a "$LOG_FILE"
else
    echo "🔴 龍智守启动失败 · PID: $PID" | tee -a "$ERR_FILE"
    exit 1
fi
