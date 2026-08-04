#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 launchd 守护一键装载 · P13姜子牙装载 / P03雯雯复盘 / P05上帝之眼督
# DNA:#龍芯⚡️2026-06-05-DAEMON-INSTALL-v1.0
set -euo pipefail

GMAIL="baofuahao@gmail.com"
PYBIN="$(command -v python3)"
SCRIPT="$HOME/longhun-system/daily_review.py"
PLIST="$HOME/Library/LaunchAgents/com.longhun.dailyreview.plist"
LABEL="com.longhun.dailyreview"

echo "🐉 龍魂 launchd 守护一键装载"
echo "DNA:#龍芯⚡️2026-06-05-DAEMON-INSTALL-v1.0"
echo ""

[ -f "$SCRIPT" ] || { echo "🔴 找不到 $SCRIPT,先把 daily_review.py 放好再跑"; exit 1; }

# 1) App 密码 → keychain(只问这一次,不落明文、不进 git)
printf "粘贴 Gmail 16位App专用密码(输入不可见): "
read -rs APPPW; echo
security add-generic-password -U -a "$USER" -s LONGHUN_GMAIL_APPPW -w "$APPPW"
unset APPPW
echo "🟢 密码已存 keychain(条目名 LONGHUN_GMAIL_APPPW)"
echo ""

# 2) 写 plist(注意:里面没有任何密码)
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYBIN</string>
    <string>$SCRIPT</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict><key>LONGHUN_GMAIL</key><string>$GMAIL</string></dict>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>23</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$HOME/longhun-system/launchd.out.log</string>
  <key>StandardErrorPath</key><string>$HOME/longhun-system/launchd.err.log</string>
</dict>
</plist>
PLIST
echo "🟢 已写 $PLIST(无密码)"
echo ""

# 3) 加载守护
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "🟢 守护已加载"
echo ""

# 4) 立即跑一次试水
echo "🚀 立刻跑一次试水..."
launchctl start "$LABEL"
sleep 5
echo ""
echo "—— launchctl 状态 ——"
launchctl list | grep longhun || echo "🟡 没看到进程,查 launchd.err.log"
echo ""
echo "✅ 装完。去 proton 收件箱看自动邮件;以后每天 23:00 自动发,不靠你按任何键。"
echo ""
echo "DNS:#龍芯⚡️2026-06-05-DAEMON-INSTALL-v1.0"
