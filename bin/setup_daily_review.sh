#!/bin/bash
# 龍魂每日復盤·一鍵配置腳本
# DNA:#龍芯⚡️2026-06-09-DAILY-REVIEW-SETUP-FILE1-v1.0

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  龍魂每日復盤·快速部署安裝程序 v2.0                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

HOME_DIR=$(eval echo ~${SUDO_USER:-$USER})
SYSTEM_DIR="$HOME_DIR/longhun-system"

# ---- 步驟 1: 安裝依賴 ----
echo "【步驟 1/5】安裝依賴 (pip-audit, pytest)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pip3 install pip-audit pytest -q || {
    echo "❌ pip 安裝失敗，請檢查 Python 環境"
    exit 1
}

echo "✅ 依賴安裝完成"
echo "   • pip-audit $(pip-audit --version 2>&1 | head -1)"
echo "   • pytest $(pytest --version 2>&1 | head -1)"
echo ""

# ---- 步驟 2: 設置 Gmail 應用密碼 ----
echo "【步驟 2/5】配置 Gmail 應用密碼..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 操作步驟："
echo "  1. 訪問 https://myaccount.google.com/security"
echo "  2. 左側「安全性」→「應用密碼」"
echo "  3. 選擇「郵件」和「Mac」"
echo "  4. 複製生成的 16 字符密碼"
echo ""

read -p "📧 Gmail 帳號 (baofuahao@gmail.com): " gmail_account
gmail_account=${gmail_account:-"baofuahao@gmail.com"}

read -sp "🔐 應用密碼 (16 字符，輸入後隱藏): " app_password
echo ""

if [ -z "$app_password" ]; then
    echo "⚠️  跳過 Keychain 配置（可稍後手動設置）"
else
    # 存入 Keychain
    security add-generic-password \
        -s "LONGHUN_GMAIL_APPPW" \
        -a "$(whoami)" \
        -w "$app_password" \
        -U 2>/dev/null || {
        # 如果密碼已存在，先刪除再添加
        security delete-generic-password \
            -s "LONGHUN_GMAIL_APPPW" 2>/dev/null || true
        security add-generic-password \
            -s "LONGHUN_GMAIL_APPPW" \
            -a "$(whoami)" \
            -w "$app_password"
    }
    echo "✅ 已安全存儲到 Keychain"
fi

# 設置環境變量
echo "📝 設置環境變量..."
if ! grep -q "LONGHUN_GMAIL" ~/.zshrc 2>/dev/null; then
    cat >> ~/.zshrc << EOF

# 龍魂每日復盤配置
export LONGHUN_GMAIL="$gmail_account"
EOF
    source ~/.zshrc
    echo "✅ 已添加到 ~/.zshrc"
else
    echo "✅ 環境變量已存在"
fi

echo ""

# ---- 步驟 3: 創建 macOS 日曆 ----
echo "【步驟 3/5】配置 macOS 日曆..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

osascript << 'OSASCRIPT' 2>/dev/null || {
    echo "⚠️  日曆創建失敗（請在 Calendar 應用中手動建立「龍魂」日曆）"
}
tell application "System Events"
    tell application "Calendar"
        try
            make new calendar with properties {name:"龍魂"}
            return "🟢 日曆已創建"
        on error
            return "🟡 日曆可能已存在"
        end try
    end tell
end tell
OSASCRIPT

echo "✅ macOS 日曆設置完成"
echo ""

# ---- 步驟 4: 測試執行 ----
echo "【步驟 4/5】測試執行複盤..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$SYSTEM_DIR"
python3 daily_review_enhanced.py 2>&1 | tee /tmp/review_test.log

echo "✅ 複盤執行完成"
echo ""

# ---- 步驟 5: 配置自動化 ----
echo "【步驟 5/5】配置自動執行..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "選擇自動執行方式："
echo "  1️⃣  LaunchAgent (推薦·可靠)"
echo "  2️⃣  Cron (備用·簡單)"
echo "  3️⃣  跳過 (手動執行)"
echo ""

read -p "請選擇 (1-3, 默認 1): " choice
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

        # 替換佔位符
        sed -i '' "s|SYSTEM_DIR_PLACEHOLDER|$SYSTEM_DIR|g" ~/Library/LaunchAgents/com.longhun.daily-review.plist

        # 加載
        launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist 2>/dev/null || {
            echo "⚠️  LaunchAgent 加載失敗（可能需要重啟 Finder）"
        }

        echo "✅ LaunchAgent 已配置"
        echo "   執行時間: 每天 23:30"
        echo "   日誌位置: $SYSTEM_DIR/logs/daily_review.log"
        ;;

    2)
        echo "配置 Cron..."
        # 檢查是否已有此任務
        if crontab -l 2>/dev/null | grep -q "daily_review"; then
            echo "⚠️  Cron 任務已存在"
        else
            (crontab -l 2>/dev/null; echo "30 23 * * * /usr/bin/python3 $SYSTEM_DIR/daily_review_enhanced.py >> $SYSTEM_DIR/logs/daily_review_cron.log 2>&1") | crontab -
            echo "✅ Cron 任務已配置"
            echo "   執行時間: 每天 23:30"
            echo "   日誌位置: $SYSTEM_DIR/logs/daily_review_cron.log"
        fi
        ;;

    3)
        echo "⏭️  跳過自動化配置"
        echo "   手動執行: python3 $SYSTEM_DIR/daily_review_enhanced.py"
        ;;

    *)
        echo "❌ 無效選擇"
        exit 1
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               ✅ 安裝完成·系統就緒                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 安裝摘要："
echo "  ✅ 依賴: pip-audit, pytest"
echo "  ✅ 郵件: Gmail → ProtonMail"
echo "  ✅ 日曆: macOS 日曆同步"
echo "  ✅ 自動化: $([ $choice -eq 1 ] && echo 'LaunchAgent' || [ $choice -eq 2 ] && echo 'Cron' || echo '手動')"
echo ""
echo "🚀 立即測試:"
echo "   python3 $SYSTEM_DIR/daily_review_enhanced.py"
echo ""
echo "📖 詳細文檔:"
echo "   cat $SYSTEM_DIR/DAILY_REVIEW_SETUP.md"
echo ""
