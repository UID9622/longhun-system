# 龍魂每日復盤·快速啟動指南 ⚡️
**DNA**:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-DAILY-REVIEW-QUICKSTART-v1.0

---

## 🚀 3 分鐘快速啟動

### 方案 A: 完全自動 (推薦)

```bash
# 準備 Gmail App Password (從 https://myaccount.google.com/apppasswords 獲取)
GMAIL="baofuahao@gmail.com"
APP_PASS="你的_16字符_APP_密碼"

# 一行命令配置所有
bash ~/longhun-system/setup_daily_review_auto.sh "$GMAIL" "$APP_PASS" 1

# 測試執行
python3 ~/longhun-system/daily_review_enhanced.py
```

### 方案 B: 互動式配置

```bash
# 執行互動式腳本（會提示輸入各項信息）
bash ~/longhun-system/setup_daily_review.sh
```

### 方案 C: 手動配置

```bash
# 1. 安裝依賴
pip3 install pip-audit pytest

# 2. 設置 Keychain
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "your_app_password"

# 3. 設置環境變量
export LONGHUN_GMAIL="your_email@gmail.com"

# 4. 創建日曆
# 打開 Calendar.app → File → New Calendar → 名稱：「龍魂」

# 5. 配置自動執行 (LaunchAgent)
mkdir -p ~/Library/LaunchAgents
cp ~/longhun-system/com.longhun.daily-review.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 6. 測試
python3 ~/longhun-system/daily_review_enhanced.py
```

---

## 📊 實時監看

```bash
# 查看最新復盤結果
tail -30 ~/longhun-system/操作草日誌.log

# 監控自動執行日誌
tail -f ~/longhun-system/logs/daily_review.log

# 查看 Cron 執行狀況（如選擇 Cron）
tail -f ~/longhun-system/logs/daily_review_cron.log

# 驗證 LaunchAgent 運行
launchctl list | grep daily-review
```

---

## 🔧 故障快速修復

### 郵件發送失敗

```bash
# 驗證 Keychain 配置
security find-generic-password -s "LONGHUN_GMAIL_APPPW"

# 驗證環境變量
echo $LONGHUN_GMAIL

# 重新設置密碼
security delete-generic-password -s "LONGHUN_GMAIL_APPPW"
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "新密碼"
```

### 日曆寫入失敗

```bash
# 在 Calendar.app 中確認「龍魂」日曆存在
# 或手動建立：Calendar → File → New Calendar

# 重新執行
python3 ~/longhun-system/daily_review_enhanced.py
```

### LaunchAgent 未執行

```bash
# 重新加載
launchctl unload ~/Library/LaunchAgents/com.longhun.daily-review.plist
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 驗證
launchctl list | grep daily-review

# 手動執行一次
launchctl start com.longhun.daily-review
```

### pytest 找不到

```bash
# 安裝或重新安裝
pip3 install --upgrade pytest

# 驗證
pytest --version
```

---

## 📋 執行時間設置

### 修改每日執行時間

編輯 `com.longhun.daily-review.plist` 中的：

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>23</integer>        <!-- 23 = 晚上 11 點 -->
    <key>Minute</key>
    <integer>30</integer>        <!-- 30 分鐘 -->
</dict>
```

範例：
- 早上 8:00 → Hour=8, Minute=0
- 下午 14:30 → Hour=14, Minute=30
- 晚上 21:00 → Hour=21, Minute=0

---

## ✅ 配置完成檢查清單

執行此腳本驗證所有配置：

```bash
#!/bin/bash
echo "=== 龍魂每日復盤配置檢查 ==="

echo "✓ 依賴"
pip-audit --version 2>&1 | head -1
pytest --version 2>&1 | head -1

echo ""
echo "✓ Keychain"
security find-generic-password -s "LONGHUN_GMAIL_APPPW" >/dev/null && echo "  Gmail 密碼已保存" || echo "  ❌ 密碼未保存"

echo ""
echo "✓ 環境變量"
echo "  LONGHUN_GMAIL=$LONGHUN_GMAIL"

echo ""
echo "✓ 日曆"
osascript -e 'tell app "Calendar" to name of every calendar' | grep -q "龍魂" && echo "  「龍魂」日曆已建立" || echo "  ❌ 日曆不存在"

echo ""
echo "✓ LaunchAgent"
launchctl list | grep -q daily-review && echo "  LaunchAgent 已加載" || echo "  ⚠️  未加載（可選）"

echo ""
echo "✓ 執行測試"
cd ~/longhun-system
python3 daily_review_enhanced.py 2>&1 | head -15
```

---

## 📞 支援資源

| 資源 | 位置 |
|------|------|
| **完整文檔** | `~/longhun-system/DAILY_REVIEW_SETUP.md` |
| **增強版代碼** | `~/longhun-system/daily_review_enhanced.py` |
| **執行日誌** | `~/longhun-system/操作草日誌.log` |
| **自動化日誌** | `~/longhun-system/logs/daily_review.log` |

---

## 🎯 下一步

1. **今日啟用** - 執行配置腳本
2. **驗證執行** - 運行 daily_review_enhanced.py
3. **監控郵件** - 確認 ProtonMail 收到復盤
4. **檢查日曆** - Calendar.app 中確認事件寫入

---

## 🆘 需要幫助？

```bash
# 查看詳細文檔
cat ~/longhun-system/DAILY_REVIEW_SETUP.md

# 查看原始日複盤程序
cat ~/longhun-system/daily_review.py

# 查看增強版程序
cat ~/longhun-system/daily_review_enhanced.py

# 檢查所有相關文件
ls -lah ~/longhun-system/ | grep -i review
```

---

## 🔏 DNA 簽署

```
DNA:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-DAILY-REVIEW-QUICKSTART-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
```

**立即開始**: `bash ~/longhun-system/setup_daily_review_auto.sh`
