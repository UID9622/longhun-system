# 龍魂每日复盘·完全部署指南
**DNA**:#龍芯⚡️2026-06-09-DAILY-REVIEW-SETUP-v1.0
**用途**: 自动审计日志·发送邮件·同步日历

---

## 📋 当前状态分析

### ✅ 已实现
- 三色裁决逻辑（文件·安全·心跳·测试）
- 邮件框架（Gmail SMTP → ProtonMail）
- 日历写入（AppleScript）
- 日志记录机制

### ❌ 待完成
1. **依赖安装** - pip-audit、pytest 未安装
2. **日志审计** - action_log.jsonl 未集成
3. **邮件配置** - LONGHUN_GMAIL 环境变量未设置
4. **日历配置** - 需在 macOS 日历中建立“龍魂”日历
5. **Cron 自动化** - 未配置定时执行

---

## 🚀 部署步骤

### 步骤 1: 安装依赖

```bash
# 安装安全审计工具
pip3 install pip-audit

# 安装测试框架
pip3 install pytest

# 验证
pip-audit --version
pytest --version
```

**预期输出**: 版本信息（无错误）

---

### 步骤 2: 配置邮件

#### 2a. 使用 Gmail App Password

```bash
# 1. 打开 Google Account: https://myaccount.google.com/
# 2. 左侧“安全性”→“应用密码”
# 3. 选择“邮件”和“Windows 电脑”
# 4. 复制生成的 16 字符密码

# 存入 macOS Keychain（加密存储）
security add-generic-password \
  -s "LONGHUN_GMAIL_APPPW" \
  -a "$(whoami)" \
  -w "你的_16字符_APP_密码"

# 验证存储成功
security find-generic-password -s "LONGHUN_GMAIL_APPPW"
```

#### 2b. 设置环境变量（可选备用方案）

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export LONGHUN_GMAIL="your-email@gmail.com"
# export LONGHUN_GMAIL_APPPW="..." # 不推荐，优先用 Keychain

source ~/.zshrc
```

---

### 步骤 3: 配置 macOS 日历

```bash
# 1. 打开 Calendar 应用
# 2. 菜单 → File → New Calendar
# 3. 名称输入：“龍魂”
# 4. 位置选择：“On My Mac”
# 5. 确认建立

# 验证（可选）
osascript -e 'tell application "Calendar" to return name of every calendar'
```

---

### 步骤 4: 配置每日自动执行

#### 4a. 使用 LaunchAgent（推荐）

```bash
# 创建 plist 配置文件
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

# 安装 LaunchAgent
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 验证安装
launchctl list | grep daily-review

# 手动执行一次（测试）
python3 ~/longhun-system/daily_review.py
```

#### 4b. 使用 Cron（备用方案）

```bash
# 编辑 crontab
crontab -e

# 添加行（每天 23:30 执行）
30 23 * * * /usr/bin/python3 /Users/zuimeidedeyihan/longhun-system/daily_review.py >> /Users/zuimeidedeyihan/longhun-system/logs/daily_review_cron.log 2>&1

# 验证
crontab -l
```

---

## 📊 完整日志审计集成

### 改进的 daily_review.py 应包含：

```python
def audit_action_logs():
    """审计 action_log.jsonl 中今天的所有操作"""
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

        return ("🟢", f"今日操作 {count} 笔") if count > 0 else ("🟡", "今日无操作记录")
    except Exception as e:
        return ("🟡", f"日志审计失败:{e}")
```

### 每日复盘应包含的内容：

1. **文件完整性** - 核心文件验证
2. **安全审计** - pip-audit 结果
3. **系统心跳** - KFPP DB 记录数
4. **测试状态** - pytest 通过率
5. **操作日志** - action_log.jsonl 统计 ⭐ 新增
6. **人格调度** - persona_scheduler 执行数
7. **API 状态** - 所有服务端口检查

---

## 🧪 测试执行

### 手动测试

```bash
# 1. 直接执行复盘
cd ~/longhun-system
python3 daily_review.py

# 2. 查看生成的日志
tail -50 操作草日志.log

# 3. 检查邮件发送状态
grep "已发 proton\|邮件发送失败" 操作草日志.log

# 4. 验证日历写入
osascript -e 'tell application "Calendar" to return name of every event in calendar "龍魂"'
```

### 自动化测试

```bash
# 创建测试套件
cat > ~/longhun-system/test_daily_review.sh << 'EOF'
#!/bin/bash
echo "=== Daily Review Test Suite ==="

# 测试 1: 执行复盘
python3 ~/longhun-system/daily_review.py > /tmp/review_output.txt 2>&1
STATUS=$?

# 测试 2: 检查输出
if grep -q "已发\|已发" /tmp/review_output.txt; then
    echo "✅ Email sent successfully"
else
    echo "❌ Email may not have been sent"
fi

# 测试 3: 验证日志
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

## 📈 进阶配置

### 自定义三色裁决规则

编辑 `daily_review.py` 中的 `build_report()` 函数：

```python
checks = {
    "文件完整": check_files(),
    "安全(鲁班)": check_security(),
    "KFPP心跳": check_db_heartbeat(),
    "测试": check_tests(),
    "操作日志": audit_action_logs(),  # 新增
    "人格调度": check_persona_scheduler(),  # 新增
    "API服务": check_api_services(),  # 新增
}
```

### 邮件模板定制

```python
def format_email_body(report, checks):
    """生成格式化的邮件正文"""
    body = f"""
龍魂每日复盘 {datetime.date.today()}

{report}

详细检查项:
"""
    for name, (color, msg) in checks.items():
        body += f"\n  {color} {name}: {msg}"

    return body
```

---

## 🔍 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| pip-audit 未找到 | 未安装 | `pip3 install pip-audit` |
| pytest 未找到 | 未安装 | `pip3 install pytest` |
| 邮件发送失败 | 无 LONGHUN_GMAIL | 设置环境变量或 Keychain |
| 日历写入失败 | 无“龍魂”日历 | 在 Calendar 中手动建立 |
| LaunchAgent 未执行 | plist 路径错误 | 检查 `~/Library/LaunchAgents/` |
| 邮件收不到 | ProtonMail 过滤 | 检查垃圾邮件·添加白名单 |

---

## ✅ 完整检查清单

- [ ] pip-audit 已安装并可执行
- [ ] pytest 已安装并可执行
- [ ] Gmail App Password 已获取
- [ ] Keychain 已存储密码或环境变量已设置
- [ ] macOS 日历“龍魂”已建立
- [ ] daily_review.py 可手动执行
- [ ] LaunchAgent 或 Cron 已配置
- [ ] 邮件已成功发送到 ProtonMail
- [ ] 日历事件已写入
- [ ] 日志正确记录

---

## 📝 每日复盘内容示例

```
⏱️ 2026-06-09 23:30  🧭 P03雯雯·日复盘  🟢三色总评:🟢

  🟢 文件完整: 核心文件齐 2/2
  🟢 安全(鲁班): 无 critical/high
  🟢 KFPP心跳: 今日心跳 42 行
  🟢 测试: pytest 通过
  🟢 操作日志: 今日操作 18 笔
  🟢 人格调度: 已执行 9 个人格

#龍芯⚡️2026-06-09-DAILY-REVIEW
```

---

## 🔏 DNA 签署

```
DNA:#龍芯⚡️2026-06-09-DAILY-REVIEW-SETUP-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2026-06-09-DAILY-REVIEW-OPERATIONAL
```

**状态**: 部署就绪 | **优先级**: 🔴 高 | **推荐行动**: 今日完成配置

---

立即开始：`python3 ~/longhun-system/daily_review.py`
