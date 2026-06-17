#!/usr/bin/env bash
# 編譯龍魂桌面主开关 .app 到用戶桌面
# DNA: #龍芯⚡️2026-06-17-LONGHUN-BUILD-DESKTOP-SWITCH-v1.0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/desktop/龍魂主开关.applescript"
DEST="$HOME/Desktop/龍魂主开关.app"

if [ ! -f "$SOURCE" ]; then
    echo "❌ 找不到源碼: $SOURCE"
    exit 1
fi

rm -rf "$DEST"
osacompile -o "$DEST" "$SOURCE"

if [ -d "$DEST" ]; then
    echo "✅ 桌面主开关已生成: $DEST"
    echo "   首次點擊若被 Gatekeeper 攔截，請右鍵 -> 打開"
else
    echo "❌ 編譯失敗"
    exit 1
fi
