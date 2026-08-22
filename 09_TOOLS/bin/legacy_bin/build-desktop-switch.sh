#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 根据 desktop/menu-registry.json 与各模块 desktop-menu.json 动态生成并编译桌面主开关 .app
# DNA:#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-LONGHUN-BUILD-DESKTOP-SWITCH-FILE1-FILE1-v1.1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/desktop/龍魂主开关.applescript"
DEST="$HOME/Desktop/龍魂主开关.app"

echo "🔄 生成最新主开关菜单..."
cd "$ROOT"
python3 bin/generate-desktop-switch.py

if [ ! -f "$SOURCE" ]; then
    echo "❌ 找不到源码: $SOURCE"
    exit 1
fi

echo "🛠️  编译桌面 App..."
rm -rf "$DEST"
osacompile -o "$DEST" "$SOURCE"

if [ -d "$DEST" ]; then
    echo "✅ 桌面主开关已生成: $DEST"
    echo "   首次点击若被 Gatekeeper 拦截，请右键 -> 打开"
else
    echo "❌ 编译失败"
    exit 1
fi
