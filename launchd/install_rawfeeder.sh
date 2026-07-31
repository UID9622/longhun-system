#!/bin/bash
# 安装龍魂投喂器开机自启服务
# DNA: #龍芯⚡️2026-07-01-LONGHUN-RAW-FEEDER-INSTALL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -e
PLIST_SRC="$(cd "$(dirname "$0")" && pwd)/com.longhun.rawfeeder.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.longhun.rawfeeder.plist"
mkdir -p "$HOME/.longhun/logs"
cp "$PLIST_SRC" "$PLIST_DST"
launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load "$PLIST_DST"
echo "🐉 龍魂投喂器服务已安装并启动。"
echo "📁 plist: $PLIST_DST"
echo "📝 日志: $HOME/.longhun/logs/raw_feeder.{out,err}"
