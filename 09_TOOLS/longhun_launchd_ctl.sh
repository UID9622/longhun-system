#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 longhun888.com 服务 LaunchAgent 控制脚本
# DNA: #龍芯⚡️2026-07-05-LONGHUN-LAUNCHD-CTL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法：bash longhun_launchd_ctl.sh [load|unload|reload|status]

PLIST="com.longhun.services"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST}.plist"
ROOT="$HOME/longhun-system"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

ACTION="${1:-status}"

case "$ACTION" in
    load)
        echo "🚀 加载 LaunchAgent: $PLIST"
        launchctl load "$PLIST_FILE" 2>&1 | tee "$LOG_DIR/launchd-load.log"
        launchctl start "$PLIST" 2>&1 | tee -a "$LOG_DIR/launchd-load.log"
        echo "✅ 已加载并启动（开机自动运行）"
        ;;
    unload)
        echo "🛑 卸载 LaunchAgent: $PLIST"
        launchctl stop "$PLIST" 2>/dev/null || true
        launchctl unload "$PLIST_FILE" 2>&1 | tee "$LOG_DIR/launchd-unload.log"
        echo "✅ 已卸载（不再开机自动运行）"
        ;;
    reload)
        echo "🔄 重载 LaunchAgent: $PLIST"
        launchctl stop "$PLIST" 2>/dev/null || true
        launchctl unload "$PLIST_FILE" 2>/dev/null || true
        sleep 1
        launchctl load "$PLIST_FILE" 2>&1 | tee "$LOG_DIR/launchd-reload.log"
        launchctl start "$PLIST" 2>&1 | tee -a "$LOG_DIR/launchd-reload.log"
        echo "✅ 已重载"
        ;;
    status)
        echo "📊 LaunchAgent 状态: $PLIST"
        if launchctl list "$PLIST" >/dev/null 2>&1; then
            echo "  状态: ✅ 已加载"
            launchctl list "$PLIST" 2>&1 | sed 's/^/  /'
        else
            echo "  状态: 🔴 未加载"
        fi
        echo ""
        echo "📊 核心端口监听状态"
        for port in 8777 18000 9630 9635 18100 9622 9623 9624 9625; do
            pid=$(lsof -Pi :$port -sTCP:LISTEN -t 2>/dev/null | head -1)
            if [ -n "$pid" ]; then
                cmd=$(ps -p $pid -o comm= 2>/dev/null | head -c 40)
                echo "  :$port ✅ PID $pid ($cmd)"
            else
                echo "  :$port 🔴 未运行"
            fi
        done
        ;;
    *)
        echo "用法: $0 {load|unload|reload|status}"
        exit 1
        ;;
esac
