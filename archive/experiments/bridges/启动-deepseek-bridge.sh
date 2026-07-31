#!/bin/bash
# 🐉 龍魂 DeepSeek 桥一键启动脚本
# DNA: #龍芯⚡️2026-07-04-DEEPSEEK-BRIDGE-ALIGN-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# M号: M266
#
# 用法：
#   ./启动-deepseek-bridge.sh start   # 后台启动
#   ./启动-deepseek-bridge.sh stop    # 停止
#   ./启动-deepseek-bridge.sh status  # 查看状态
#   ./启动-deepseek-bridge.sh test    # 快速测试

set -e

BRIDGE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HOME/longhun-system/logs"
PID_FILE="$BRIDGE_DIR/.pid"
PORT=8788

mkdir -p "$LOG_DIR"

check_env() {
    if [ ! -f "$HOME/.deepseek_bridge.env" ]; then
        echo "🔴 密钥文件不存在: $HOME/.deepseek_bridge.env"
        echo "请先执行："
        echo "  echo 'DEEPSEEK_API_KEY=sk-xxx' > ~/.deepseek_bridge.env"
        echo "  chmod 600 ~/.deepseek_bridge.env"
        exit 1
    fi
}

case "${1:-start}" in
    start)
        check_env
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "🟢 DeepSeek Bridge 已在运行 (PID: $(cat "$PID_FILE"))"
            echo "   健康检查: curl http://127.0.0.1:$PORT/health"
            exit 0
        fi
        echo "🚀 启动 DeepSeek Bridge..."
        echo "   监听: 127.0.0.1:$PORT"
        echo "   日志: $LOG_DIR/deepseek_bridge.log"
        nohup python3 "$BRIDGE_DIR/deepseek_bridge.py" \
            >> "$LOG_DIR/deepseek_bridge.log" 2>&1 &
        echo $! > "$PID_FILE"
        sleep 2
        if curl -s http://127.0.0.1:$PORT/health >/dev/null; then
            echo "🟢 启动成功 (PID: $(cat "$PID_FILE"))"
        else
            echo "🟡 启动中，请查看日志: tail -f $LOG_DIR/deepseek_bridge.log"
        fi
        ;;
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "🛑 停止 DeepSeek Bridge (PID: $PID)..."
                kill "$PID"
                rm -f "$PID_FILE"
                echo "✅ 已停止"
            else
                echo "🟡 进程不存在"
                rm -f "$PID_FILE"
            fi
        else
            echo "🟡 未找到 PID 文件"
        fi
        ;;
    status)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "🟢 DeepSeek Bridge 运行中 (PID: $(cat "$PID_FILE"))"
            curl -s http://127.0.0.1:$PORT/health | python3 -m json.tool 2>/dev/null || true
        else
            echo "🔴 DeepSeek Bridge 未运行"
        fi
        ;;
    test)
        check_env
        echo "🧪 测试 DeepSeek Bridge..."
        curl -s http://127.0.0.1:$PORT/health | python3 -m json.tool 2>/dev/null || true
        echo ""
        echo "发送测试请求..."
        curl -s -X POST http://127.0.0.1:$PORT/v1/messages \
            -H "x-api-key: sk-anthropic-dummy" \
            -H "anthropic-version: 2023-06-01" \
            -H "Content-Type: application/json" \
            -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":64,"messages":[{"role":"user","content":"龍魂"}]}' \
            | python3 -m json.tool 2>/dev/null || echo "🔴 测试失败，请检查日志"
        ;;
    *)
        echo "用法: $0 {start|stop|status|test}"
        exit 1
        ;;
esac
