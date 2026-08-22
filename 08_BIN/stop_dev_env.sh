#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂系统 · 开发环境一键停止
# DNA: #龍芯⚡️丙午·丙申·戊申·巳时·䷄需-DEV-ENV-DOWN-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

stop_by_pid() {
    local pid=$1
    local name=$2
    if kill -0 "$pid" 2>/dev/null; then
        kill "$pid"
        echo "✅ 已停止 $name (PID: $pid)"
    else
        echo "⚠️  $name 进程已不存在"
    fi
}

if [ -f "$PROJECT_ROOT/.dev_env.json" ]; then
    portal_pid=$(python3 -c "import json; print(json.load(open('.dev_env.json'))['portal_pid'])" 2>/dev/null)
    cp_pid=$(python3 -c "import json; print(json.load(open('.dev_env.json'))['control_panel_pid'])" 2>/dev/null)
    stop_by_pid "$portal_pid" "Web 门户"
    stop_by_pid "$cp_pid" "操作台后端"
    rm -f "$PROJECT_ROOT/.dev_env.json"
else
    echo "⚠️  未找到 .dev_env.json，尝试通过端口查找进程..."
    for port in 8777 8778 8779 9630 9631; do
        pid=$(lsof -ti :"$port" 2>/dev/null)
        if [ -n "$pid" ]; then
            kill "$pid" 2>/dev/null && echo "✅ 已停止端口 $port 进程 (PID: $pid)"
        fi
    done
fi

echo "🐉 开发环境已停止"
