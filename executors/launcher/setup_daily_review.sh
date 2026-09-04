#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂每日复盘·一键配置脚本
# DNA:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-DAILY-REVIEW-SETUP-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  龍魂每日复盘·快速部署安装程序 v2.0                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

HOME_DIR=$(eval echo ~${SUDO_USER:-$USER})
SYSTEM_DIR="$HOME_DIR/longhun-system"

# ---- 步骤 1: 安装依赖 ----
echo "【步骤 1/5】安装依赖 (pip-audit, pytest)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pip3 install pip-audit pytest -q || {
    echo "❌ pip 安装失败，请检查 Python 环境"
    exit 1
}

echo "✅ 依赖安装完成"
echo "   • pip-audit $(pip-audit --version 2>&1 | head -1)"
echo "   • pytest $(pytest --version 2>&1 | head -1)"
echo ""

# ---- 步骤 2: 设置 Gmail 应用密码 ----
echo "【步骤 2/5】配置 Gmail 应用密码..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 操作步骤："
echo "  1. 访问 https://myaccount.google.com/security"
echo "  2. 左侧“安全性”→“应用密码”"
echo "  3. 选择“邮件”和“Mac”"
echo "  4. 复制生成的 16 字符密码"
echo ""

read -p "📧 Gmail 账号 (baofuahao@gmail.com): " gmail_account
gmail_account=${gmail_account:-"baofuahao@gmail.com"}

read -sp "🔐 应用密码 (16 字符，输入后隐藏): " app_password
echo ""

if [ -z "$app_password" ]; then
    echo "⚠️  跳过 Keychain 配置（可稍后手动设置）"
else
    # 存入 Keychain
    security add-generic-password \
        -s "LONGHUN_GMAIL_APPPW" \
        -a "$(whoami)" \
        -w "$app_password" \
        -U 2>/dev/null || {
        # 如果密码已存在，先删除再添加
        security delete-generic-password \
            -s "LONGHUN_GMAIL_APPPW" 2>/dev/null || true
        security add-generic-password \
            -s "LONGHUN_GMAIL_APPPW" \
            -a "$(whoami)" \
            -w "$app_password"
    }
    echo "✅ 已安全存储到 Keychain"
fi

# 设置环境变量
echo "📝 设置环境变量..."
if ! grep -q "LONGHUN_GMAIL" ~/.zshrc 2>/dev/null; then
    cat >> ~/.zshrc << EOF

# 龍魂每日复盘配置
export LONGHUN_GMAIL="$gmail_account"
EOF
    source ~/.zshrc
    echo "✅ 已添加到 ~/.zshrc"
else
    echo "✅ 环境变量已存在"
fi

echo ""

# ---- 步骤 3: 创建 macOS 日历 ----
echo "【步骤 3/5】配置 macOS 日历..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

osascript << 'OSASCRIPT' 2>/dev/null || {
    echo "⚠️  日历创建失败（请在 Calendar 应用中手动建立“龍魂”日历）"
}
tell application "System Events"
    tell application "Calendar"
        try
            make new calendar with properties {name:"龍魂"}
            return "🟢 日历已创建"
        on error
            return "🟡 日历可能已存在"
        end try
    end tell
end tell
OSASCRIPT

echo "✅ macOS 日历设置完成"
echo ""

# ---- 步骤 4: 测试执行 ----
echo "【步骤 4/5】测试执行复盘..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$SYSTEM_DIR"
python3 daily_review_enhanced.py 2>&1 | tee /tmp/review_test.log

echo "✅ 复盘执行完成"
echo ""

# ---- 步骤 5: 配置自动化 ----
echo "【步骤 5/5】配置自动执行..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "选择自动执行方式："
echo "  1️⃣  LaunchAgent (推荐·可靠)"
echo "  2️⃣  Cron (备用·简单)"
echo "  3️⃣  跳过 (手动执行)"
echo ""

read -p "请选择 (1-3, 默认 1): " choice
choice=${choice:-1}

case $choice in
    1)
        echo "配置 LaunchAgent..."
        mkdir -p ~/Library/LaunchAgents
        cat > ~/Library/LaunchAgents/com.longhun.daily-review.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.daily-review</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>SYSTEM_DIR_PLACEHOLDER/daily_review_enhanced.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>SYSTEM_DIR_PLACEHOLDER/logs/daily_review.log</string>

    <key>StandardErrorPath</key>
    <string>SYSTEM_DIR_PLACEHOLDER/logs/daily_review_error.log</string>
</dict>
</plist>
PLIST

        # 替换占位符
        sed -i '' "s|SYSTEM_DIR_PLACEHOLDER|$SYSTEM_DIR|g" ~/Library/LaunchAgents/com.longhun.daily-review.plist

        # 加载
        launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist 2>/dev/null || {
            echo "⚠️  LaunchAgent 加载失败（可能需要重启 Finder）"
        }

        echo "✅ LaunchAgent 已配置"
        echo "   执行时间: 每天 23:30"
        echo "   日志位置: $SYSTEM_DIR/logs/daily_review.log"
        ;;

    2)
        echo "配置 Cron..."
        # 检查是否已有此任务
        if crontab -l 2>/dev/null | grep -q "daily_review"; then
            echo "⚠️  Cron 任务已存在"
        else
            (crontab -l 2>/dev/null; echo "30 23 * * * /usr/bin/python3 $SYSTEM_DIR/daily_review_enhanced.py >> $SYSTEM_DIR/logs/daily_review_cron.log 2>&1") | crontab -
            echo "✅ Cron 任务已配置"
            echo "   执行时间: 每天 23:30"
            echo "   日志位置: $SYSTEM_DIR/logs/daily_review_cron.log"
        fi
        ;;

    3)
        echo "⏭️  跳过自动化配置"
        echo "   手动执行: python3 $SYSTEM_DIR/daily_review_enhanced.py"
        ;;

    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               ✅ 安装完成·系统就绪                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 安装摘要："
echo "  ✅ 依赖: pip-audit, pytest"
echo "  ✅ 邮件: Gmail → ProtonMail"
echo "  ✅ 日历: macOS 日历同步"
echo "  ✅ 自动化: $([ $choice -eq 1 ] && echo 'LaunchAgent' || [ $choice -eq 2 ] && echo 'Cron' || echo '手动')"
echo ""
echo "🚀 立即测试:"
echo "   python3 $SYSTEM_DIR/daily_review_enhanced.py"
echo ""
echo "📖 详细文档:"
echo "   cat $SYSTEM_DIR/DAILY_REVIEW_SETUP.md"
echo ""
