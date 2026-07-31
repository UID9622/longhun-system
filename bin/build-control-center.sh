#!/usr/bin/env bash
# 编译龍魂控制中心桌面 App
# DNA:#龍芯⚡️2026-06-18-LONGHUN-BUILD-CONTROL-CENTER-FILE1-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/desktop/control-center-launcher.applescript"
DEST="$HOME/Desktop/龍魂控制中心.app"

if [ ! -f "$SOURCE" ]; then
    echo "❌ 找不到启动器源码: $SOURCE"
    exit 1
fi

rm -rf "$DEST"
osacompile -o "$DEST" "$SOURCE"

if [ -d "$DEST" ]; then
    echo "✅ 龍魂控制中心已生成: $DEST"
    echo "   首次点击若被 Gatekeeper 拦截，请右键 -> 打开"
else
    echo "❌ 编译失败"
    exit 1
fi
