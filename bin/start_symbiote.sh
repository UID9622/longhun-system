#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂共生体 · 启动脚本 v2.0                                 ║
# ║  DNA: #龍芯⚡️2026-07-06-SYMBIOTE-LAUNCHER-v2.0            ║
# ║                                                            ║
# ║  启动端口 9627 — 知识矩阵+神经网络融合服务器                ║
# ║  仪表盘: http://127.0.0.1:9627/symbiote                    ║
# ║  3D网络: http://127.0.0.1:9627/                             ║
# ║                                                            ║
# ║  fallback机制: launchctl失败时自动调用本脚本                ║
# ╚══════════════════════════════════════════════════════════════╝
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER_SCRIPT="$ROOT/tools/longhun_symbiote_server.py"
PORT=9627
LOG_DIR="$ROOT/logs"
FALLBACK_LOG="$LOG_DIR/fallback.log"
mkdir -p "$LOG_DIR"

log_fallback() {
    echo "[$(date '+%Y-%m-%dT%H:%M:%SZ')] $*" >> "$FALLBACK_LOG"
}

# ── Fallback 机制 ──
log_fallback "symbiote_launcher_started via=${1:-manual}"

# 先停旧版
echo "🧹 清理旧版服务..."
if /usr/sbin/lsof -ti:$PORT >/dev/null 2>&1; then
    /usr/sbin/lsof -ti:$PORT 2>/dev/null | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# ── 启动共生体（主路径）──
echo "🧬 启动龍魂共生体服务器..."
cd "$ROOT"
nohup /usr/bin/python3 "$SERVER_SCRIPT" > "$LOG_DIR/symbiote_server.log" 2>&1 &
PID=$!
echo "   PID: $PID"
sleep 2

# ── 验证 & Fallback ──
if kill -0 $PID 2>/dev/null; then
    echo "🟢 共生体已启动"
    echo "   仪表盘: http://127.0.0.1:$PORT/symbiote"
    echo "   3D网络: http://127.0.0.1:$PORT/"
    echo "   日志:   $LOG_DIR/symbiote_server.log"
    log_fallback "symbiote_started pid=$PID port=$PORT health=OK"
else
    echo "🔴 启动失败，尝试 fallback 恢复..."
    log_fallback "symbiote_start_failed pid=$PID attempting_fallback"

    # Fallback 1: 检查 Python 可用性
    if ! /usr/bin/python3 -c "import http.server" 2>/dev/null; then
        echo "   ⚠️  Python3 http.server 不可用"
        log_fallback "fallback_failed python3_unavailable"
        exit 1
    fi

    # Fallback 2: 再次尝试启动
    sleep 2
    nohup /usr/bin/python3 "$SERVER_SCRIPT" > "$LOG_DIR/symbiote_server.log" 2>&1 &
    PID=$!
    sleep 3

    if kill -0 $PID 2>/dev/null; then
        echo "🟢 共生体已通过 fallback 恢复启动"
        log_fallback "symbiote_fallback_success pid=$PID"
    else
        echo "🔴 Fallback 也失败了，查看日志: $FALLBACK_LOG"
        log_fallback "symbiote_fallback_failed"
        exit 1
    fi
fi
