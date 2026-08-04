#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂磁盘守护 · 安装/管理脚本
# DNA: #龍芯⚡️2026-07-12-DISK-GUARD-INSTALL-v1.0

set -e

PLIST_NAME="com.longhun.disk-guard"
PLIST_SRC="$(cd "$(dirname "$0")" && pwd)/../launchd/${PLIST_NAME}.plist"
PLIST_DST="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

usage() {
    echo "🐉 龍魂磁盘守护 v1.0"
    echo ""
    echo "用法: $0 {install|stop|start|status|uninstall}"
    echo ""
    echo "  install   安装/重装守护 (开机自启)"
    echo "  stop      停止守护"
    echo "  start     启动守护"
    echo "  status    查看守护状态"
    echo "  uninstall 卸载守护"
}

case "${1:-}" in
    install)
        echo "🐉 安装龍魂磁盘守护..."

        # 复制 plist
        mkdir -p "$HOME/Library/LaunchAgents"
        cp "$PLIST_SRC" "$PLIST_DST"
        echo "  ✅ plist 已复制到 $PLIST_DST"

        # 确保日志目录
        mkdir -p "$HOME/longhun-system/logs"

        # 先卸载旧的
        launchctl bootout gui/$(id -u)/"$PLIST_NAME" 2>/dev/null || true

        # 加载
        launchctl bootstrap gui/$(id -u) "$PLIST_DST"
        echo "  ✅ 守护已加载并启动"

        echo "  📋 定时检查: 每30秒"
        echo "  📋 清理阈值: 剩余 <20GB 警告, <10GB 紧急"
        echo "  📋 开机自启: 是"
        ;;

    stop)
        launchctl bootout gui/$(id -u)/"$PLIST_NAME" 2>/dev/null || echo "守护未运行"
        echo "✅ 已停止"
        ;;

    start)
        launchctl bootstrap gui/$(id -u) "$PLIST_DST" 2>/dev/null || {
            echo "⚠️  已在运行，重载..."
            launchctl bootout gui/$(id -u)/"$PLIST_NAME" 2>/dev/null
            launchctl bootstrap gui/$(id -u) "$PLIST_DST"
        }
        echo "✅ 已启动"
        ;;

    status)
        if launchctl print gui/$(id -u)/"$PLIST_NAME" &>/dev/null; then
            echo "🟢 守护运行中"
            launchctl print gui/$(id -u)/"$PLIST_NAME" | grep -E "state|last exit" || true
        else
            echo "🔴 守护未运行"
        fi
        echo ""
        df -h /System/Volumes/Data 2>/dev/null | tail -1
        ;;

    uninstall)
        launchctl bootout gui/$(id -u)/"$PLIST_NAME" 2>/dev/null || true
        rm -f "$PLIST_DST"
        echo "✅ 已卸载"
        ;;

    *)
        usage
        exit 1
        ;;
esac
