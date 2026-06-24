#!/usr/bin/env bash
# 安装龍魂系统 macOS 开机自启动（LaunchAgent）
# DNA:#龍芯⚡️2026-06-17-LONGHUN-INSTALL-AUTOSTART-v1.0

PLIST_NAME="com.uid9622.longhun.autostart.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.uid9622.longhun.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$ROOT/bin/longhun-autostart.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>$ROOT/logs/autostart-launchd.log</string>
    <key>StandardErrorPath</key>
    <string>$ROOT/logs/autostart-launchd.error.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load -w "$PLIST_PATH"

echo "✅ 开机自启动已安装"
echo "   Plist: $PLIST_PATH"
echo "   启动脚本: $ROOT/bin/longhun-autostart.sh"
echo ""
echo "测试立即执行："
echo "   bash $ROOT/bin/longhun-autostart.sh"
