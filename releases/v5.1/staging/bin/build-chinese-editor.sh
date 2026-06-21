#!/usr/bin/env bash
# 編譯龍碼中文編輯器桌面 App
# DNA:#龍芯⚡️2026-06-18-LONGHUN-BUILD-CHINESE-EDITOR-v1.0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/editor/launcher.applescript"
DEST="$HOME/Desktop/龍碼中文編輯器.app"

if [ ! -f "$SOURCE" ]; then
    echo "❌ 找不到啟動器源碼: $SOURCE"
    exit 1
fi

rm -rf "$DEST"
osacompile -o "$DEST" "$SOURCE"

if [ -d "$DEST" ]; then
    echo "✅ 龍碼中文編輯器已生成: $DEST"
    echo "   首次點擊若被 Gatekeeper 攔截，請右鍵 -> 打開"
else
    echo "❌ 編譯失敗"
    exit 1
fi
