# 龍魂每日复盘·快速启动指南 ⚡️
**DNA**:#龍芯⚡️2026-06-09-DAILY-REVIEW-QUICKSTART-v1.0

---

## 🚀 3 分钟快速启动

### 方案 A: 完全自动 (推荐)

```bash
# 准备 Gmail App Password (从 https://myaccount.google.com/apppasswords 获取)
GMAIL="baofuahao@gmail.com"
APP_PASS="你的_16字符_APP_密码"

# 一行命令配置所有
bash ~/longhun-system/setup_daily_review_auto.sh "$GMAIL" "$APP_PASS" 1

# 测试执行
python3 ~/longhun-system/daily_review_enhanced.py
```

### 方案 B: 互动式配置

```bash
# 执行互动式脚本（会提示输入各项信息）
bash ~/longhun-system/setup_daily_review.sh
```

### 方案 C: 手动配置

```bash
# 1. 安装依赖
pip3 install pip-audit pytest

# 2. 设置 Keychain
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "your_app_password"

# 3. 设置环境变量
export LONGHUN_GMAIL="your_email@gmail.com"

# 4. 创建日历
# 打开 Calendar.app → File → New Calendar → 名称：“龍魂”

# 5. 配置自动执行 (LaunchAgent)
mkdir -p ~/Library/LaunchAgents
cp ~/longhun-system/com.longhun.daily-review.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 6. 测试
python3 ~/longhun-system/daily_review_enhanced.py
```

---

## 📊 实时监看

```bash
# 查看最新复盘结果
tail -30 ~/longhun-system/操作草日志.log

# 监控自动执行日志
tail -f ~/longhun-system/logs/daily_review.log

# 查看 Cron 执行状况（如选择 Cron）
tail -f ~/longhun-system/logs/daily_review_cron.log

# 验证 LaunchAgent 运行
launchctl list | grep daily-review
```

---

## 🔧 故障快速修复

### 邮件发送失败

```bash
# 验证 Keychain 配置
security find-generic-password -s "LONGHUN_GMAIL_APPPW"

# 验证环境变量
echo $LONGHUN_GMAIL

# 重新设置密码
security delete-generic-password -s "LONGHUN_GMAIL_APPPW"
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "新密码"
```

### 日历写入失败

```bash
# 在 Calendar.app 中确认“龍魂”日历存在
# 或手动建立：Calendar → File → New Calendar

# 重新执行
python3 ~/longhun-system/daily_review_enhanced.py
```

### LaunchAgent 未执行

```bash
# 重新加载
launchctl unload ~/Library/LaunchAgents/com.longhun.daily-review.plist
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 验证
launchctl list | grep daily-review

# 手动执行一次
launchctl start com.longhun.daily-review
```

### pytest 找不到

```bash
# 安装或重新安装
pip3 install --upgrade pytest

# 验证
pytest --version
```

---

## 📋 执行时间设置

### 修改每日执行时间

编辑 `com.longhun.daily-review.plist` 中的：

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>23</integer>        <!-- 23 = 晚上 11 点 -->
    <key>Minute</key>
    <integer>30</integer>        <!-- 30 分钟 -->
</dict>
```

范例：
- 早上 8:00 → Hour=8, Minute=0
- 下午 14:30 → Hour=14, Minute=30
- 晚上 21:00 → Hour=21, Minute=0

---

## ✅ 配置完成检查清单

执行此脚本验证所有配置：

```bash
#!/bin/bash
echo "=== 龍魂每日复盘配置检查 ==="

echo "✓ 依赖"
pip-audit --version 2>&1 | head -1
pytest --version 2>&1 | head -1

echo ""
echo "✓ Keychain"
security find-generic-password -s "LONGHUN_GMAIL_APPPW" >/dev/null && echo "  Gmail 密码已保存" || echo "  ❌ 密码未保存"

echo ""
echo "✓ 环境变量"
echo "  LONGHUN_GMAIL=$LONGHUN_GMAIL"

echo ""
echo "✓ 日历"
osascript -e 'tell app "Calendar" to name of every calendar' | grep -q "龍魂" && echo "  “龍魂”日历已建立" || echo "  ❌ 日历不存在"

echo ""
echo "✓ LaunchAgent"
launchctl list | grep -q daily-review && echo "  LaunchAgent 已加载" || echo "  ⚠️  未加载（可选）"

echo ""
echo "✓ 执行测试"
cd ~/longhun-system
python3 daily_review_enhanced.py 2>&1 | head -15
```

---

## 📞 支援资源

| 资源 | 位置 |
|------|------|
| **完整文档** | `~/longhun-system/DAILY_REVIEW_SETUP.md` |
| **增强版代码** | `~/longhun-system/daily_review_enhanced.py` |
| **执行日志** | `~/longhun-system/操作草日志.log` |
| **自动化日志** | `~/longhun-system/logs/daily_review.log` |

---

## 🎯 下一步

1. **今日启用** - 执行配置脚本
2. **验证执行** - 运行 daily_review_enhanced.py
3. **监控邮件** - 确认 ProtonMail 收到复盘
4. **检查日历** - Calendar.app 中确认事件写入

---

## 🆘 需要帮助？

```bash
# 查看详细文档
cat ~/longhun-system/DAILY_REVIEW_SETUP.md

# 查看原始日复盘程序
cat ~/longhun-system/daily_review.py

# 查看增强版程序
cat ~/longhun-system/daily_review_enhanced.py

# 检查所有相关文件
ls -lah ~/longhun-system/ | grep -i review
```

---

## 🔏 DNA 签署

```
DNA:#龍芯⚡️2026-06-09-DAILY-REVIEW-QUICKSTART-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
```

**立即开始**: `bash ~/longhun-system/setup_daily_review_auto.sh`
