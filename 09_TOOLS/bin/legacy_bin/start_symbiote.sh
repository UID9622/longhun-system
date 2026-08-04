#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ╔══════════════════════════════════════════════════════════════════╗
# ║  龍魂共生体 · 启动脚本 v2.1                                    ║
# ║  DNA: #龍芯⚡️2026-07-06-SYMBIOTE-LAUNCHER-v2.1               ║
# ║  端口 9627 — 知识矩阵+神经网络融合服务器                        ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER_SCRIPT="$ROOT/tools/longhun_symbiote_server.py"
PORT=9627
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

# ── 先清理旧进程 ──
if lsof -ti:$PORT >/dev/null 2>&1; then
    echo "🧹 清理端口 $PORT 上的旧进程..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# ── 确保 HTML 资源就位 ──
WEB_DIR="$ROOT/web"
mkdir -p "$WEB_DIR"

# symbiote-dashboard.html
if [ ! -s "$WEB_DIR/symbiote-dashboard.html" ]; then
    SRC="$ROOT/L5_服务层/services/dashboard/web/symbiote-dashboard.html"
    if [ -f "$SRC" ]; then
        cp "$SRC" "$WEB_DIR/symbiote-dashboard.html"
        echo "📋 复制 symbiote-dashboard.html → web/"
    fi
fi

# 3D 神经网络
if [ ! -f "$WEB_DIR/longhun-neural-network-3d-v2.html" ]; then
    SRC="$ROOT/L5_服务层/services/dashboard/web/longhun-neural-network-3d-v2.html"
    if [ -f "$SRC" ]; then
        ln -sf "$SRC" "$WEB_DIR/longhun-neural-network-3d-v2.html"
        echo "🔗 链接 longhun-neural-network-3d-v2.html → web/"
    fi
fi

# ── 启动共生体 ──
echo "🧬 启动龍魂共生体服务器..."
cd "$ROOT"
nohup python3 "$SERVER_SCRIPT" > "$LOG_DIR/symbiote_server.log" 2>&1 &
PID=$!
disown "$PID" 2>/dev/null || true

# 等待启动
for i in $(seq 1 10); do
    sleep 1
    if curl -s --connect-timeout 1 "http://127.0.0.1:$PORT/api/health" >/dev/null 2>&1; then
        echo "🟢 共生体已启动 (PID=$PID)"
        echo "   仪表盘: http://127.0.0.1:$PORT/symbiote"
        echo "   3D网络: http://127.0.0.1:$PORT/"
        echo "   状态:   http://127.0.0.1:$PORT/api/health"
        exit 0
    fi
    echo "   ⏳ 等待中... ($i/10)"
done

# 超时
echo "🔴 共生体启动超时"
kill $PID 2>/dev/null || true
exit 1
