#!/bin/bash
# 龍魂每日复盘·自动配置版本 (非互动式)
# DNA:#龍芯⚡️2026-06-09-DAILY-REVIEW-AUTO-SETUP-v1.0
# 用法: ./setup_daily_review_auto.sh <gmail_account> <app_password> <automation_type>

set -e

GMAIL_ACCOUNT="${1:-baofuahao@gmail.com}"
APP_PASSWORD="${2}"
AUTOMATION="${3:-1}"

SYSTEM_DIR=$(cd ~/longhun-system && pwd)

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  龍魂每日复盘·自动配置 v1.0                               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ---- 步骤 1: 验证依赖 ----
echo "【步骤 1/4】验证依赖..."
python3 -c "import pip_audit" 2>/dev/null || {
    echo "❌ pip-audit 未安装"
    exit 1
}
python3 -c "import pytest" 2>/dev/null || {
    echo "❌ pytest 未安装"
    exit 1
}
echo "✅ 依赖已安装"
echo ""

# ---- 步骤 2: 配置 Gmail ----
echo "【步骤 2/4】配置 Gmail..."

if [ -n "$APP_PASSWORD" ]; then
    # 存入 Keychain
    security add-generic-password \
        -s "LONGHUN_GMAIL_APPPW" \
        -a "$(whoami)" \
        -w "$APP_PASSWORD" \
        -U 2>/dev/null || {
        security delete-generic-password \
            -s "LONGHUN_GMAIL_APPPW" 2>/dev/null || true
        security add-generic-password \
            -s "LONGHUN_GMAIL_APPPW" \
            -a "$(whoami)" \
            -w "$APP_PASSWORD"
    }
    echo "✅ App Password 已保存到 Keychain"
else
    echo "⚠️  跳过 Keychain 配置 (未提供密码)"
fi

# 设置环境变量
if ! grep -q "LONGHUN_GMAIL" ~/.zshrc 2>/dev/null; then
    echo "" >> ~/.zshrc
    echo "# 龍魂每日复盘配置" >> ~/.zshrc
    echo "export LONGHUN_GMAIL=\"$GMAIL_ACCOUNT\"" >> ~/.zshrc
    echo "✅ 已设置 LONGHUN_GMAIL=$GMAIL_ACCOUNT"
fi

echo ""

# ---- 步骤 3: 建立日历 ----
echo "【步骤 3/4】配置 macOS 日历..."

osascript << 'OSASCRIPT' 2>/dev/null || {
    echo "⚠️  日历可能已存在或需要手动建立"
}
tell application "Calendar"
    try
        make new calendar with properties {name:"龍魂"}
    on error
        return "exists"
    end try
end tell
OSASCRIPT

echo "✅ 日历配置完成"
echo ""

# ---- 步骤 4: 配置自动化 ----
echo "【步骤 4/4】配置自动执行..."

case $AUTOMATION in
    1)
        echo "🔧 配置 LaunchAgent..."
        mkdir -p ~/Library/LaunchAgents

        cat > ~/Library/LaunchAgents/com.longhun.daily-review.plist << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.daily-review</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SYSTEM_DIR/daily_review_enhanced.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$SYSTEM_DIR/logs/daily_review.log</string>
    <key>StandardErrorPath</key>
    <string>$SYSTEM_DIR/logs/daily_review_error.log</string>
</dict>
</plist>
PLIST

        launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist 2>/dev/null || {
            echo "⚠️  LaunchAgent 加载可能需要重启"
        }
        echo "✅ LaunchAgent 已配置 (每天 23:30)"
        ;;

    2)
        echo "🔧 配置 Cron..."
        if crontab -l 2>/dev/null | grep -q "daily_review"; then
            echo "⚠️  Cron 任务已存在"
        else
            (crontab -l 2>/dev/null; echo "30 23 * * * /usr/bin/python3 $SYSTEM_DIR/daily_review_enhanced.py >> $SYSTEM_DIR/logs/daily_review_cron.log 2>&1") | crontab -
            echo "✅ Cron 已配置 (每天 23:30)"
        fi
        ;;

    *)
        echo "⏭️  跳过自动化"
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               ✅ 自动配置完成                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 立即测试:"
echo "   python3 $SYSTEM_DIR/daily_review_enhanced.py"
echo ""
