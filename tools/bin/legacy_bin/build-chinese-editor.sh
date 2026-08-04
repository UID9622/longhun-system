#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 编译龍码中文编辑器桌面 App
# DNA:#龍芯⚡️2026-06-18-LONGHUN-BUILD-CHINESE-EDITOR-FILE1-v1.0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/editor/launcher.applescript"
DEST="$HOME/Desktop/龍码中文编辑器.app"

if [ ! -f "$SOURCE" ]; then
    echo "❌ 找不到启动器源码: $SOURCE"
    exit 1
fi

rm -rf "$DEST"
osacompile -o "$DEST" "$SOURCE"

if [ -d "$DEST" ]; then
    echo "✅ 龍码中文编辑器已生成: $DEST"
    echo "   首次点击若被 Gatekeeper 拦截，请右键 -> 打开"
else
    echo "❌ 编译失败"
    exit 1
fi
