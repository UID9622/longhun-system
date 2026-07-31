#!/usr/bin/env bash
# 🐉 龍魂 · 硬盘备份守护安装脚本
# DNA: #龍芯⚡️2026-07-12-DRIVE-BACKUP-INSTALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -euo pipefail

GREEN='\033[0;32m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
ok() { echo -e "${GREEN}✅${NC} $*"; }

PLIST_SRC="$HOME/longhun-system/launchd/com.longhun.drive-backup.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.longhun.drive-backup.plist"

case "${1:-install}" in
    install)
        echo "🐉 安装龍魂硬盘备份守护..."
        cp "$PLIST_SRC" "$PLIST_DEST"
        launchctl unload "$PLIST_DEST" 2>/dev/null || true
        launchctl load "$PLIST_DEST"
        ok "守护已安装并启动"
        echo ""
        echo "📋 行为说明:"
        echo "   - 系统启动时自动运行"
        echo "   - 每5秒检测 LonghunDisk 是否插入"
        echo "   - 插盘后自动同步冷数据 -> /Volumes/LonghunDisk/longhun-cold-storage/"
        echo "   - 每天只备份一次（同一天不重复）"
        echo "   - 拔盘后待机等下次插入"
        echo ""
        echo "🛑 停止守护: bash $0 stop"
        echo "📊 查看状态: python3 bin/lh_drive_auto_backup.py status"
        ;;
    stop)
        echo "🛑 停止硬盘备份守护..."
        launchctl unload "$PLIST_DEST" 2>/dev/null || true
        ok "守护已停止"
        ;;
    status)
        if launchctl list | grep -q com.longhun.drive-backup; then
            echo "🟢 硬盘备份守护运行中"
            launchctl list com.longhun.drive-backup
        else
            echo "⚪ 硬盘备份守护未运行"
        fi
        ;;
    *)
        echo "用法: $0 {install|stop|status}"
        ;;
esac
