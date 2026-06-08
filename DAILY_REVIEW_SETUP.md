# 龍魂每日復盤·完全部署指南
**DNA**: #龍芯⚡️2026-06-09-DAILY-REVIEW-SETUP-v1.0
**用途**: 自動審計日誌·發送郵件·同步日曆

---

## 📋 當前狀態分析

### ✅ 已實現
- 三色裁決邏輯（文件·安全·心跳·測試）
- 郵件框架（Gmail SMTP → ProtonMail）
- 日曆寫入（AppleScript）
- 日誌記錄機制

### ❌ 待完成
1. **依賴安裝** - pip-audit、pytest 未安裝
2. **日誌審計** - action_log.jsonl 未集成
3. **郵件配置** - LONGHUN_GMAIL 環境變量未設置
4. **日曆配置** - 需在 macOS 日曆中建立「龍魂」日曆
5. **Cron 自動化** - 未配置定時執行

---

## 🚀 部署步驟

### 步驟 1: 安裝依賴

```bash
# 安裝安全審計工具
pip3 install pip-audit

# 安裝測試框架
pip3 install pytest

# 驗證
pip-audit --version
pytest --version
```

**預期輸出**: 版本信息（無錯誤）

---

### 步驟 2: 配置郵件

#### 2a. 使用 Gmail App Password

```bash
# 1. 打開 Google Account: https://myaccount.google.com/
# 2. 左側「安全性」→「應用密碼」
# 3. 選擇「郵件」和「Windows 電腦」
# 4. 複製生成的 16 字符密碼

# 存入 macOS Keychain（加密存儲）
security add-generic-password \
  -s "LONGHUN_GMAIL_APPPW" \
  -a "$(whoami)" \
  -w "你的_16字符_APP_密碼"

# 驗證存儲成功
security find-generic-password -s "LONGHUN_GMAIL_APPPW"
```

#### 2b. 設置環境變量（可選備用方案）

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export LONGHUN_GMAIL="your-email@gmail.com"
# export LONGHUN_GMAIL_APPPW="..." # 不推薦，優先用 Keychain

source ~/.zshrc
```

---

### 步驟 3: 配置 macOS 日曆

```bash
# 1. 打開 Calendar 應用
# 2. 菜單 → File → New Calendar
# 3. 名稱輸入：「龍魂」
# 4. 位置選擇：「On My Mac」
# 5. 確認建立

# 驗證（可選）
osascript -e 'tell application "Calendar" to return name of every calendar'
```

---

### 步驟 4: 配置每日自動執行

#### 4a. 使用 LaunchAgent（推薦）

```bash
# 創建 plist 配置文件
cat > ~/Library/LaunchAgents/com.longhun.daily-review.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.daily-review</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/zuimeidedeyihan/longhun-system/daily_review.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/zuimeidedeyihan/longhun-system/logs/daily_review.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/zuimeidedeyihan/longhun-system/logs/daily_review_error.log</string>
</dict>
</plist>
EOF

# 安裝 LaunchAgent
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 驗證安裝
launchctl list | grep daily-review

# 手動執行一次（測試）
python3 ~/longhun-system/daily_review.py
```

#### 4b. 使用 Cron（備用方案）

```bash
# 編輯 crontab
crontab -e

# 添加行（每天 23:30 執行）
30 23 * * * /usr/bin/python3 /Users/zuimeidedeyihan/longhun-system/daily_review.py >> /Users/zuimeidedeyihan/longhun-system/logs/daily_review_cron.log 2>&1

# 驗證
crontab -l
```

---

## 📊 完整日誌審計集成

### 改進的 daily_review.py 應包含：

```python
def audit_action_logs():
    """審計 action_log.jsonl 中今天的所有操作"""
    log_file = Path.home() / 'longhun-system' / 'logs' / 'action_log.jsonl'
    today = datetime.date.today().isoformat()
    count = 0

    if not log_file.exists():
        return ("🟡", "action_log.jsonl 不存在")

    try:
        with open(log_file) as f:
            for line in f:
                record = json.loads(line)
                if record.get('date', '').startswith(today):
                    count += 1

        return ("🟢", f"今日操作 {count} 筆") if count > 0 else ("🟡", "今日無操作記錄")
    except Exception as e:
        return ("🟡", f"日誌審計失敗:{e}")
```

### 每日複盤應包含的內容：

1. **文件完整性** - 核心文件驗證
2. **安全審計** - pip-audit 結果
3. **系統心跳** - KFPP DB 記錄數
4. **測試狀態** - pytest 通過率
5. **操作日誌** - action_log.jsonl 統計 ⭐ 新增
6. **人格調度** - persona_scheduler 執行數
7. **API 狀態** - 所有服務端口檢查

---

## 🧪 測試執行

### 手動測試

```bash
# 1. 直接執行復盤
cd ~/longhun-system
python3 daily_review.py

# 2. 查看生成的日誌
tail -50 操作草日志.log

# 3. 檢查郵件發送狀態
grep "已發 proton\|邮件发送失败" 操作草日志.log

# 4. 驗證日曆寫入
osascript -e 'tell application "Calendar" to return name of every event in calendar "龍魂"'
```

### 自動化測試

```bash
# 創建測試套件
cat > ~/longhun-system/test_daily_review.sh << 'EOF'
#!/bin/bash
echo "=== Daily Review Test Suite ==="

# 測試 1: 執行復盤
python3 ~/longhun-system/daily_review.py > /tmp/review_output.txt 2>&1
STATUS=$?

# 測試 2: 檢查輸出
if grep -q "已发\|已發" /tmp/review_output.txt; then
    echo "✅ Email sent successfully"
else
    echo "❌ Email may not have been sent"
fi

# 測試 3: 驗證日誌
if [ -f ~/longhun-system/操作草日志.log ]; then
    echo "✅ Log file created"
    echo "Latest entries:"
    tail -5 ~/longhun-system/操作草日志.log
fi

exit $STATUS
EOF

chmod +x ~/longhun-system/test_daily_review.sh
./test_daily_review.sh
```

---

## 📈 進階配置

### 自定義三色裁決規則

編輯 `daily_review.py` 中的 `build_report()` 函數：

```python
checks = {
    "文件完整": check_files(),
    "安全(鲁班)": check_security(),
    "KFPP心跳": check_db_heartbeat(),
    "測試": check_tests(),
    "操作日誌": audit_action_logs(),  # 新增
    "人格調度": check_persona_scheduler(),  # 新增
    "API服務": check_api_services(),  # 新增
}
```

### 郵件模板定制

```python
def format_email_body(report, checks):
    """生成格式化的郵件正文"""
    body = f"""
龍魂每日復盤 {datetime.date.today()}

{report}

詳細檢查項:
"""
    for name, (color, msg) in checks.items():
        body += f"\n  {color} {name}: {msg}"

    return body
```

---

## 🔍 故障排查

| 問題 | 原因 | 解決方案 |
|------|------|---------|
| pip-audit 未找到 | 未安裝 | `pip3 install pip-audit` |
| pytest 未找到 | 未安裝 | `pip3 install pytest` |
| 郵件發送失敗 | 無 LONGHUN_GMAIL | 設置環境變量或 Keychain |
| 日曆寫入失敗 | 無「龍魂」日曆 | 在 Calendar 中手動建立 |
| LaunchAgent 未執行 | plist 路徑錯誤 | 檢查 `~/Library/LaunchAgents/` |
| 郵件收不到 | ProtonMail 過濾 | 檢查垃圾郵件·添加白名單 |

---

## ✅ 完整檢查清單

- [ ] pip-audit 已安裝並可執行
- [ ] pytest 已安裝並可執行
- [ ] Gmail App Password 已獲取
- [ ] Keychain 已存儲密碼或環境變量已設置
- [ ] macOS 日曆「龍魂」已建立
- [ ] daily_review.py 可手動執行
- [ ] LaunchAgent 或 Cron 已配置
- [ ] 郵件已成功發送到 ProtonMail
- [ ] 日曆事件已寫入
- [ ] 日誌正確記錄

---

## 📝 每日複盤內容示例

```
⏱️ 2026-06-09 23:30  🧭 P03雯雯·日復盤  🟢三色總評:🟢

  🟢 文件完整: 核心文件齊 2/2
  🟢 安全(魯班): 無 critical/high
  🟢 KFPP心跳: 今日心跳 42 行
  🟢 測試: pytest 通過
  🟢 操作日誌: 今日操作 18 筆
  🟢 人格調度: 已執行 9 個人格

#龍芯⚡️2026-06-09-DAILY-REVIEW
```

---

## 🔏 DNA 簽署

```
DNA: #龍芯⚡️2026-06-09-DAILY-REVIEW-SETUP-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2026-06-09-DAILY-REVIEW-OPERATIONAL
```

**狀態**: 部署就緒 | **優先級**: 🔴 高 | **推薦行動**: 今日完成配置

---

立即開始：`python3 ~/longhun-system/daily_review.py`
