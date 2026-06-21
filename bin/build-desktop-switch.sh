#!/usr/bin/env bash
# 根據 desktop/menu-registry.json 與各模塊 desktop-menu.json 動態生成並編譯桌面主开关 .app
# DNA:#龍芯⚡️2026-06-17-LONGHUN-BUILD-DESKTOP-SWITCH-FILE1-v1.1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/desktop/龍魂主开关.applescript"
DEST="$HOME/Desktop/龍魂主开关.app"

echo "🔄 生成最新主开关菜單..."
cd "$ROOT"
python3 bin/generate-desktop-switch.py

if [ ! -f "$SOURCE" ]; then
    echo "❌ 找不到源碼: $SOURCE"
    exit 1
fi

echo "🛠️  編譯桌面 App..."
rm -rf "$DEST"
osacompile -o "$DEST" "$SOURCE"

if [ -d "$DEST" ]; then
    echo "✅ 桌面主开关已生成: $DEST"
    echo "   首次點擊若被 Gatekeeper 攔截，請右鍵 -> 打開"
else
    echo "❌ 編譯失敗"
    exit 1
fi
