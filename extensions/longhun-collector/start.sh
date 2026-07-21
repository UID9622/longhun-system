#!/bin/bash
# ============================================================
# 龍魂系统 · 采集服务启动脚本 v2.0
# DNA: #龍芯⚡️丙午·乙申·COLLECTOR-v2.0-LAUNCHER
# UID9622 | 龍芯北辰
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/longhun-system/data/collector/raw"
PID_FILE="/tmp/longhun-collector.pid"
LOG_FILE="$HOME/longhun-system/logs/collector.log"
PORT=9622

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║     🐉 龍魂采集服务 v2.0 · 启动器        ║"
echo "  ║     UID9622 · 龍芯北辰                    ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# ---- 检查 Python ----
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装"
    exit 1
fi

# ---- 检查 Flask ----
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 安装 Flask..."
    pip3 install flask
fi

# ---- 创建必要目录 ----
mkdir -p "$DATA_DIR"
mkdir -p "$HOME/longhun-system/logs"

# ---- 停止旧进程 ----
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "⏹  停止旧进程 (PID: $OLD_PID)..."
        kill "$OLD_PID" 2>/dev/null
        sleep 1
    fi
    rm -f "$PID_FILE"
fi

# ---- 启动服务 ----
cd "$SCRIPT_DIR"
nohup python3 longhun-collector.py >> "$LOG_FILE" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"

sleep 1
if kill -0 "$PID" 2>/dev/null; then
    echo "✅ 龍魂采集服务已启动"
    echo "   PID:        $PID"
    echo "   端口:       $PORT"
    echo "   数据目录:   $DATA_DIR"
    echo "   日志:       $LOG_FILE"
    echo ""
    echo "📊 健康检查: curl http://localhost:$PORT/health"
    echo "📈 统计信息: curl http://localhost:$PORT/stats"
    echo "📤 导出数据: curl http://localhost:$PORT/export"
    echo ""
    echo "🌐 浏览器插件安装:"
    echo "   1. Chrome → chrome://extensions/"
    echo "   2. 开启【开发者模式】"
    echo "   3. 加载已解压 → 选择: $SCRIPT_DIR"
    echo ""
    echo "DNA: #龍芯⚡️丙午·乙申·COLLECTOR-v2.0"
else
    echo "❌ 启动失败，查看日志: tail -20 $LOG_FILE"
    exit 1
fi
