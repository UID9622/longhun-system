#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 longhun888.com + v10 API 服務一鍵啟動腳本
# DNA: #龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN888-SERVICES-STARTER-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法：bash start_longhun888_services.sh [start|stop|status]

set -uo pipefail

HOME_DIR="$HOME"
ROOT="$HOME_DIR/longhun-system"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

ACTION="${1:-start}"

start() {
    echo "🐉 启动 longhun888.com 服务套件 · $(date)"

    # 1. CNSH Editor API :18000、门户服务器 :8777、Cloudflare Tunnel
    if [ -f "$ROOT/tools/补全服务.sh" ]; then
        bash "$ROOT/tools/补全服务.sh" 2>&1 | tee "$LOG_DIR/longhun888-services-start.log"
    else
        echo "🔴 未找到 $ROOT/tools/补全服务.sh"
        return 1
    fi

    # 2. 龍魂 v10.0 API 服务器 :18100
    if [ -f "$ROOT/notion_absorb/v10_api_skill/longhun_v10_api_server.py" ]; then
        pkill -f "longhun_v10_api_server.py" 2>/dev/null || true
        sleep 1
        cd "$ROOT/notion_absorb/v10_api_skill"
        # 显式使用 Python 3.12（Homebrew 已装 fastapi/uvicorn）
        PY3="/opt/homebrew/bin/python3.12"
        if [ ! -x "$PY3" ]; then
            PY3="python3"
        fi
        nohup "$PY3" longhun_v10_api_server.py > "$LOG_DIR/longhun_v10_api_server.out.log" 2>&1 &
        sleep 2
        if lsof -Pi :18100 -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo "✅ v10.0 API 服务器 :18100 已启动"
        else
            echo "🔴 v10.0 API 服务器 :18100 启动失败"
        fi
    fi

    # 3. 龍魂對話系統（L0 倫理錨定）:9635
    if [ -f "$ROOT/tools/dialogue_server_with_ethics.py" ]; then
        pkill -f "dialogue_server_with_ethics.py" 2>/dev/null || true
        sleep 1
        cd "$ROOT"
        PY3="/opt/homebrew/bin/python3.12"
        if [ ! -x "$PY3" ]; then
            PY3="python3"
        fi
        nohup "$PY3" "$ROOT/tools/dialogue_server_with_ethics.py" > "$LOG_DIR/dialogue_server_with_ethics.out.log" 2>&1 &
        sleep 2
        if lsof -Pi :9635 -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo "✅ 龍魂對話系統（L0 錨定）:9635 已启动"
        else
            echo "🔴 龍魂對話系統（L0 錨定）:9635 启动失败"
        fi
    fi

    echo "✅ longhun888.com 服务套件启动完成"

    # 保持脚本运行，让 launchd 能监控；每 30 秒检查一次核心端口
    echo "🛡️ 进入守护循环（按 Ctrl+C 退出）"
    while true; do
        sleep 30
        for port in 9630 9635 18000 8777 18100; do
            if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo "⚠️  端口 $port 未监听，尝试重启对应服务" >&2
                # 让 launchd 重启整个套件
                exit 1
            fi
        done
    done
}

stop() {
    echo "🛑 停止 longhun888.com 服务套件 · $(date)"
    pkill -f "dialogue_server_with_ethics.py" 2>/dev/null || true
    pkill -f "longhun_v10_api_server.py" 2>/dev/null || true
    pkill -f "longhun_portal_server.py" 2>/dev/null || true
    pkill -f "cloudflared tunnel --config.*longhun888.yml" 2>/dev/null || true
    pkill -f "cnsh_editor_api.main" 2>/dev/null || true
    echo "✅ 已停止"
}

status() {
    echo "📊 longhun888.com 服务套件状态 · $(date)"
    for port in 9630 9635 18000 8777 18100; do
        pid=$(lsof -Pi :$port -sTCP:LISTEN -t 2>/dev/null | head -1)
        if [ -n "$pid" ]; then
            cmd=$(ps -p $pid -o comm= 2>/dev/null | head -c 50)
            echo "  :$port ✅ PID $pid ($cmd)"
        else
            echo "  :$port 🔴 未运行"
        fi
    done
    if pgrep -f "cloudflared tunnel --config.*longhun888.yml" >/dev/null 2>&1; then
        echo "  Cloudflare Tunnel ✅ 运行中"
    else
        echo "  Cloudflare Tunnel 🔴 未运行"
    fi
}

case "$ACTION" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    restart) stop; sleep 2; start ;;
    *) echo "用法: $0 {start|stop|status|restart}" ;;
esac
