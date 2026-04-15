#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂MCP服务器启动脚本                                    ║
# ║  DNA: #龍芯⚡️2026-04-13-MCP-START-v1.0                  ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ╚══════════════════════════════════════════════════════════╝

PYTHON="/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"
SERVER="$HOME/longhun-system/core/mcp_server.py"
PID_FILE="$HOME/longhun-system/logs/mcp_server.pid"
LOG_FILE="$HOME/longhun-system/logs/mcp_server.log"

mkdir -p "$HOME/longhun-system/logs"

case "${1:-start}" in
    start)
        # 检查是否已运行
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "🐉 MCP服务器已在运行 (PID: $(cat "$PID_FILE"))"
            echo "📡 http://localhost:9623/sse"
            exit 0
        fi

        echo "🐉 启动龍魂MCP服务器..."
        nohup "$PYTHON" "$SERVER" --sse > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        sleep 2

        if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "✅ MCP服务器已启动"
            echo "   PID: $(cat "$PID_FILE")"
            echo "   端口: 9623"
            echo "   SSE: http://localhost:9623/sse"
            echo "   日志: $LOG_FILE"
        else
            echo "❌ 启动失败，查看日志: $LOG_FILE"
            cat "$LOG_FILE"
            exit 1
        fi
        ;;

    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                echo "✅ MCP服务器已停止 (PID: $PID)"
            else
                echo "⚠️  进程不存在"
            fi
            rm -f "$PID_FILE"
        else
            echo "⚠️  PID文件不存在"
            # 尝试通过端口找
            PID=$(lsof -ti:9623)
            if [ -n "$PID" ]; then
                kill "$PID"
                echo "✅ 已通过端口关闭 (PID: $PID)"
            fi
        fi
        ;;

    restart)
        "$0" stop
        sleep 1
        "$0" start
        ;;

    status)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "🟢 运行中 (PID: $(cat "$PID_FILE"))"
            echo "📡 http://localhost:9623/sse"
        else
            echo "🔴 未运行"
        fi
        ;;

    *)
        echo "用法: mcp_start.sh [start|stop|restart|status]"
        ;;
esac
