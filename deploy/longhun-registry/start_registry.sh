#!/bin/bash
# 龍魂系统 · 注册中心启动器 v2.0
# DNA: #龍芯⚡️丙午·辛未·乙酉·卯时·讼-REGISTRY-STARTER-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-9623}"

echo "🐉 龍魂注册中心启动器 v2.0"
echo "🐉 #龍芯⚡️丙午·辛未·乙酉·卯时·讼-REGISTRY-v2.0"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python3"
    exit 1
fi

# 检查端口占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口 $PORT 已被占用"
    read -p "是否强制停止并重启? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
        kill $PID 2>/dev/null || true
        sleep 1
        echo "✅ 已释放端口 $PORT"
    else
        echo "❌ 已取消"
        exit 1
    fi
fi

# 启动
LOG_FILE="$SCRIPT_DIR/registry.log"
echo "📡 启动注册中心 (端口: $PORT)..."
nohup python3 "$SCRIPT_DIR/registry_server.py" --port $PORT > "$LOG_FILE" 2>&1 &
PID=$!
sleep 1

# 验证
if kill -0 $PID 2>/dev/null; then
    echo "✅ 注册中心已启动 (PID: $PID)"
    echo "📡 端口: $PORT"
    echo "📋 日志: tail -f $LOG_FILE"
    echo "🔍 测试: curl http://localhost:$PORT/health"
    echo ""
    echo "📊 常用命令:"
    echo "   curl http://localhost:$PORT/health"
    echo "   curl http://localhost:$PORT/nodes"
    echo "   curl http://localhost:$PORT/stats"
else
    echo "❌ 启动失败，查看日志:"
    cat "$LOG_FILE" 2>/dev/null || true
    exit 1
fi
