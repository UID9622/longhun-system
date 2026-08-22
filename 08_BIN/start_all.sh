#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂系统 · 一键启动所有服务
# DNA: #龍芯⚡️丙午·丙申·丙辰·巳时·䷄需-START-ALL-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════
# 用法: bash bin/start_all.sh [dev|docker]
# ═══════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

MODE="${1:-dev}"

echo "🐉 龍魂系统 · 一键启动"
echo "   模式: $MODE"
echo ""

case "$MODE" in
    docker)
        echo "🐳 Docker 模式启动..."
        if ! command -v docker &>/dev/null; then
            echo "🔴 未安装 Docker，请先安装"
            exit 1
        fi
        docker compose up -d --build
        echo ""
        echo "🟢 Docker 服务已启动"
        echo "   查看状态: docker compose ps"
        echo "   查看日志: docker compose logs -f"
        echo "   停止:     docker compose down"
        ;;

    dev|*)
        echo "💻 本地开发模式启动..."

        # 检查虚拟环境
        VENV="$PROJECT_ROOT/.venv"
        if [ -d "$VENV" ]; then
            source "$VENV/bin/activate"
        fi

        # 启动 API 后端
        echo "   🚀 启动 API 后端 (端口 9622)..."
        python3 backend/main.py > backend/logs/api.log 2>&1 &
        API_PID=$!
        echo "   ✅ API 后端 PID: $API_PID"

        sleep 2

        # 启动 Web 门户
        echo "   🚀 启动 Web 门户 (端口 8777)..."
        python3 web_server.py > logs/web.log 2>&1 &
        WEB_PID=$!
        echo "   ✅ Web 门户 PID: $WEB_PID"

        sleep 1

        echo ""
        echo "🐉 ========================================"
        echo "   🟢 龍魂系统已启动！"
        echo ""
        echo "   🌐 Web 门户:  http://127.0.0.1:8777"
        echo "   📡 API 文档:  http://127.0.0.1:9622/api/docs"
        echo "   ❤️  健康检查:  http://127.0.0.1:9622/api/system/health"
        echo ""
        echo "   停止: kill $API_PID $WEB_PID"
        echo "   日志: tail -f backend/logs/api.log"
        echo "         tail -f logs/web.log"
        echo "🐉 ========================================"

        # 保存 PID
        echo "$API_PID" > /tmp/longhun-api.pid
        echo "$WEB_PID" > /tmp/longhun-web.pid

        # 等待 Ctrl+C
        trap "echo ''; echo '🛑 停止龍魂系统...'; kill $API_PID $WEB_PID 2>/dev/null; echo '✅ 已停止'; exit 0" INT TERM

        echo ""
        echo "   按 Ctrl+C 停止所有服务..."
        wait
        ;;
esac
