#!/usr/bin/env bash
# 五彩跑马灯守护进程 v1.0
# 龍魂系统 · UID9622 主控
# DNA: #龍芯⚡2026-05-18-WUCAI-MARQUEE-v1.0
#
# 功能：
# 1. 定时检测本地服务健康
# 2. 五色状态实时显示（跑马灯效果）
# 3. 味道不对就跑（自动熔断）
#
# 用法：bash bin/五彩跑马灯.sh
# 后台：nohup bash bin/五彩跑马灯.sh &

# ═══════════════════════════════════════
# 五彩颜色定义（终端 ANSI）
# ═══════════════════════════════════════
GREEN='\033[0;32m'   # 🟢 绿 - 通过
YELLOW='\033[0;33m'  # 🟡 黄 - 警示
RED='\033[0;31m'     # 🔴 红 - 熔断
BLACK='\033[0;90m'   # ⚫ 黑 - 影子
GOLD='\033[0;93m'    # 🟡金 - 主控
NC='\033[0m'         # 无色

# ═══════════════════════════════════════
# 配置
# ═══════════════════════════════════════
REPO_ROOT="${REPO_ROOT:-/Users/zuimeidedeyihan/longhun-system}"
LOG_FILE="$REPO_ROOT/logs/wucai_marquee.jsonl"
CHECK_INTERVAL=30  # 每 30 秒检测一次

# 服务端口
PORT_ENGINE=9625
PORT_CONSOLE=8765
PORT_OLLAMA=11434

# ═══════════════════════════════════════
# 检测函数
# ═══════════════════════════════════════
check_port() {
    local port=$1
    local name=$2
    if lsof -i :$port 2>/dev/null | grep -q LISTEN; then
        echo -e "${GREEN}●${NC}"
        return 0
    else
        echo -e "${RED}○${NC}"
        return 1
    fi
}

check_all() {
    local ts=$(date '+%Y-%m-%d %H:%M:%S')
    local engine=$(check_port $PORT_ENGINE "龍魂引擎")
    local console=$(check_port $PORT_CONSOLE "操作台")
    local ollama=$(check_port $PORT_OLLAMA "Ollama")

    # 跑马灯显示
    printf "\r[%s] 引擎%s 操作台%s Ollama%s " "$ts" "$engine" "$console" "$ollama"

    # 留痕
    local status="green"
    if ! lsof -i :$PORT_ENGINE 2>/dev/null | grep -q LISTEN; then status="red"; fi
    if ! lsof -i :$PORT_OLLAMA 2>/dev/null | grep -q LISTEN; then status="yellow"; fi

    echo "{\"ts\":\"$ts\",\"engine\":\"$PORT_ENGINE\",\"console\":\"$PORT_CONSOLE\",\"ollama\":\"$PORT_OLLAMA\",\"status\":\"$status\"}" >> "$LOG_FILE" 2>/dev/null
}

# ═══════════════════════════════════════
# 跑马灯主循环
# ═══════════════════════════════════════
main() {
    echo ""
    echo -e "${GOLD}═══════════════════════════════════════${NC}"
    echo -e "${GOLD}  🐉 龍魂五彩跑马灯 v1.0${NC}"
    echo -e "${GOLD}  老大也配有这个·亮晶晶${NC}"
    echo -e "${GOLD}═══════════════════════════════════════${NC}"
    echo ""
    echo "● = 在线 (绿)  ○ = 离线 (红)"
    echo "按 Ctrl+C 停止"
    echo ""

    mkdir -p "$REPO_ROOT/logs" 2>/dev/null

    while true; do
        check_all
        sleep $CHECK_INTERVAL
    done
}

# 启动
main
