# 龍魂系统·主控参考指南
**DNA**:#龍芯⚡️2026-06-09-MASTER-SYSTEMS-REFERENCE-v1.0
**版本**: 2.0 · 生产级
**最后更新**: 2026-06-09
**理论指导**: 曾仕强老师（永恒显示）

---

## 📚 目录

1. [系统架构](#系统架构)
2. [核心模块](#核心模块)
3. [API 与服务](#api-与服务)
4. [人格系统](#人格系统)
5. [每日复盘](#每日复盘)
6. [操作日志](#操作日志)
7. [主控台](#主控台)
8. [自动化配置](#自动化配置)
9. [故障排查](#故障排查)
10. [命令速查](#命令速查)

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                   龍魂系统 v2.0                           │
└─────────────────────────────────────────────────────────┘
         │                     │                    │
         ▼                     ▼                    ▼
   ┌──────────┐          ┌──────────┐       ┌──────────┐
   │ 主控台   │          │  API     │       │ 每日系统 │
   │ v2.0     │          │ 服务器   │       │  复盘    │
   │(35功能)  │          │(15人格)  │       │(7检查)   │
   └──────────┘          └──────────┘       └──────────┘
         │                     │                    │
         │                     │                    │
    ┌────┴────┐        ┌──────┴──────┐      ┌──────┴──────┐
    ▼         ▼        ▼             ▼      ▼             ▼
  日历   操作日志   人格路由   自动调度   邮件通知   日历同步
  同步   (action)   系统      (cron)    (Gmail)   (macOS)
         log.jsonl
```

### 分层架构

```
L0 (永恒层)
  └─ P00 文心 (战略核心)

L1 (百年层)
  ├─ P01 诸葛亮 (战略推演)
  └─ P02 龍芯 (执行核心)

L2 (十年层)
  ├─ P03 雯雯 (隐私卫士)
  ├─ P05 上帝之眼 (监管审计)
  └─ P06 数学大师 (逻辑分析)

L3 (日常层)
  ├─ P13 姜子牙 (九宫派位)
  ├─ P14 吕蒙 (辅助执行)
  └─ P15 乔前辈 (档案管理)

L4 (瞬时层)
  └─ P72 龍盾 (安全防护)

本地层
  ├─ K01 雯雯 (承载包容·文档整理师)
  ├─ K02 侦察兵 (止静观察·信息猎手)
  ├─ K03 守护者 (危机应对·安全卫士)
  ├─ K04 宝宝 (文明光明·构建师)
  └─ K05 文心 (柔顺协调·同步专家)
```

---

## 核心模块

### 1. 主控台系统 (master_console.py)

**位置**: `~/.longhorn/master_console.py`
**行数**: 180 行
**功能**: 统一菜单入口·35 个功能·6 个分类

#### 菜单结构

```
🔵 指挥台系统 (10 项)
  1.1-1.9, 1.w: 发布·日报·归档·扫荡·对峙·证据·统计·日历·审计·Web3

💰 支付系统 (6 项)
  2.1-2.6: 演示·API·CLI·统计·日志·配置

🔧 Skill Hub (5 项)
  3.1-3.5: 列表·验证·Kimi·Claude·Ollama

🐉 人格系统 (4 项)
  4.1-4.4: 列表·路由·调度器·文档

🚀 系统启动 (6 项)
  5.1-5.6: 全部·检查·守护进程·协议盾·DNA状态·多币种

🔍 诊断工具 (4 项)
  6.1-6.4: 色彩诊断·呼吸灯·日报·自检
```

#### 使用方式

```bash
# 启动主控台
python3 ~/.longhorn/master_console.py

# 或直接添加别名
alias longhun='python3 ~/.longhorn/master_console.py'
```

---

### 2. 人格 API 系统 (persona_api.py)

**位置**: `~/longhun-system/cnsh/flow_decision/persona_api.py`
**行数**: 53 行
**功能**: 15 人格 REST API·3 个端点
**端口**: http://127.0.0.1:9001

#### API 端点

| 方法 | 端点 | 功能 | 响应 |
|------|------|------|------|
| GET | `/personas/list` | 列出所有人格 | `{"count": 15, "personas": [...]}` |
| GET | `/personas/{pid}` | 查询单个人格 | `{"name": "...", "role": "...", ...}` |
| POST | `/personas/route` | 任务路由分派 | `{"assigned_personas": [...], "count": N}` |

#### 查询示例

```bash
# 列出所有人格
curl http://localhost:9001/personas/list | jq .

# 查询 P01 诸葛亮
curl http://localhost:9001/personas/P01

# 路由任务到 L1 层人格
curl -X POST "http://localhost:9001/personas/route?task=strategy&layer=L1"
```

#### 启动方式

```bash
# 方式 1: 直接运行
python3 ~/longhun-system/cnsh/flow_decision/persona_api.py

# 方式 2: 通过主控台选项 4.4
python3 ~/.longhorn/master_console.py
# 选择: 4.4

# 验证运行
curl -s http://localhost:9001/personas/list | python3 -m json.tool
```

---

### 3. 人格调度系统 (persona_scheduler.py)

**位置**: `~/longhun-system/bin/persona_scheduler.py`
**行数**: 307 行
**功能**: 9 人格自动调度·18 个任务·Cron 执行

#### 调度配置

```
P01 诸葛亮 (L1)
  ├─ Task 1: 战略评估 (6:00)
  └─ Task 2: 决策推演 (12:00)

P02 龍芯 (L1)
  ├─ Task 1: 执行检查 (8:00)
  └─ Task 2: 进度追踪 (18:00)

P03 雯雯 (L2)
  ├─ Task 1: 隐私检查 (10:00)
  └─ Task 2: 安全评估 (14:00)

... (P05, P06, P13, P14, P15, P72)
```

#### 手动执行

```bash
# 启动调度器
python3 ~/longhun-system/bin/persona_scheduler.py p01

# 验证运行
tail -50 ~/longhun-system/logs/persona_scheduler.log

# 查看 Cron 日志
grep persona_scheduler /var/log/system.log | tail -20
```

---

### 4. 日历同步系统 (longhun_calendar_sync.py)

**位置**: `~/longhun-system/bin/longhun_calendar_sync.py`
**行数**: 161 行
**功能**: iCloud 日历同步·推送通知·优先级分类

#### 功能

```
读取日志
    ↓
转换为 iCal 格式
    ↓
分类优先级 (高/中/低)
    ↓
推送到 macOS 日历
    ↓
发送手机推送
```

#### 使用方式

```bash
# 执行日历同步
python3 ~/longhun-system/bin/longhun_calendar_sync.py

# 验证 iCloud 同步
curl http://localhost:9001/personas/list  # 查询当前标签页

# 在 Calendar.app 中检查
open /Applications/Calendar.app
```

---

### 5. 每日复盘系统 (daily_review_enhanced.py)

**位置**: `~/longhun-system/daily_review_enhanced.py`
**行数**: 200+ 行
**功能**: 7 项检查·三色裁决·邮件·日历·审计

#### 7 项检查

1. **文件完整** - 核心文件验证
2. **安全审计** - pip-audit 检查
3. **KFPP 心跳** - 数据库活动
4. **测试** - pytest 结果
5. **操作日志** - action_log.jsonl 统计 ⭐
6. **人格调度** - persona_scheduler 验证
7. **API 服务** - 端口健康检查

#### 执行结果示例

```
⏱️ 2026-06-09 07:20  🧭 P03雯雯·日复盘  🟢三色总评:🔴

  🟢 文件完整: 核心文件齐 2/2
  🟢 安全(鲁班): 无 critical/high
  🟡 KFPP心跳: 今日 0 行
  🔴 测试: pytest 失败(code 2)
  🟢 操作日志: 今日操作 19 笔 (6工具)
  🟢 人格调度: 已调度 20 个人格
  🟡 API服务: 部分在线 2/3
```

#### 执行方式

```bash
# 手动执行
python3 ~/longhun-system/daily_review_enhanced.py

# 自动执行 (LaunchAgent)
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 自动执行 (Cron)
crontab -l | grep daily_review
```

---

### 6. 操作日志系统 (action_logger.py)

**位置**: `~/longhun-system/action_logger.py`
**行数**: 250+ 行
**功能**: 完整操作审计·统计·报告生成

#### 核心功能

```
操作执行
    ↓
自动记录 (action_log.jsonl)
    ↓
统计分析 (工具·人格·状态)
    ↓
生成报告·日志可视化
```

#### 使用方式

```bash
# 查看统计
python3 ~/longhun-system/action_logger.py stats

# 生成报告
python3 ~/longhun-system/action_logger.py report

# 手动记录
python3 ~/longhun-system/action_logger.py log "操作名称" "工具名称" "P03雯雯"

# 在代码中使用
from action_logger import log_operation
with log_operation("任务", "tool", persona="P01"):
    do_something()
```

---

## API 与服务

### 运行中的服务

| 服务 | 端口 | 状态 | 功能 |
|------|------|------|------|
| **Persona API** | 9001 | ✅ | 15 人格·3 端点 |
| **Longhun API** | 8000 | ⚠️ | Skills 框架 |
| **OpenHub REST** | 10088 | ✅ | AI Claw API |
| **OpenHub WS** | 10087 | ✅ | WebSocket |

### 检查服务状态

```bash
# 查看所有监听端口
lsof -i -P -n | grep LISTEN

# 测试特定端口
curl -s http://localhost:9001/personas/list | python3 -m json.tool
curl -s http://localhost:8000/health
curl -s http://localhost:10088/api

# 使用主控台诊断
python3 ~/.longhorn/master_console.py
# 选择: 6.4 (自检程序)
```

---

## 人格系统

### 15 人格完整清单

#### L0 永恒层
```
P00 文心
  角色: 战略核心
  卦象: 巽☴
  职责: 系统的最高指导原则
```

#### L1 百年层
```
P01 诸葛亮
  角色: 战略推演
  卦象: 干☰
  职责: 百年战略规划

P02 龍芯
  角色: 执行核心
  卦象: 震☳
  职责: 任务执行与推进
```

#### L2 十年层
```
P03 雯雯
  角色: 隐私卫士
  卦象: 坤☷
  职责: 隐私与合规检查

P05 上帝之眼
  角色: 监管审计
  卦象: 坎☵
  职责: 系统监管与审计

P06 数学大师
  角色: 逻辑分析
  卦象: 艮☶
  职责: 数据分析与验证
```

#### L3 日常层
```
P13 姜子牙
  角色: 九宫派位
  卦象: 离☲
  职责: 日常任务派遣

P14 吕蒙
  角色: 辅助执行
  卦象: 兑☱
  职责: 执行支持

P15 乔前辈
  角色: 档案管理
  卦象: 巽☴
  职责: 文档与档案管理
```

#### L4 瞬时层
```
P72 龍盾
  角色: 安全防护
  卦象: 坎☵
  职责: 即时安全防护
```

#### 本地层
```
K01 雯雯 - 承载包容·文档整理师
K02 侦察兵 - 止静观察·信息猎手
K03 守护者 - 危机应对·安全卫士
K04 宝宝 - 文明光明·构建师
K05 文心 - 柔顺协调·同步专家
```

### 人格路由

```bash
# 查询特定人格
curl http://localhost:9001/personas/P01 | jq .

# 路由任务到 L1 层
curl -X POST "http://localhost:9001/personas/route?task=strategy&layer=L1"

# 路由到本地人格
curl -X POST "http://localhost:9001/personas/route?task=coordination&layer=本地"
```

---

## 每日复盘

### 配置流程

#### 步骤 1: 安装依赖
```bash
pip3 install pip-audit pytest
```

#### 步骤 2: 配置 Gmail
```bash
# 获取 App Password (https://myaccount.google.com/apppasswords)
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "password"
export LONGHUN_GMAIL="your_email@gmail.com"
```

#### 步骤 3: 配置日历
```bash
# 在 Calendar.app 中
# File → New Calendar → 名称：“龍魂”
```

#### 步骤 4: 配置自动执行
```bash
# 选项 A: LaunchAgent
bash ~/longhun-system/setup_daily_review_auto.sh "email@gmail.com" "password" 1

# 选项 B: Cron
crontab -e
# 添加: 30 23 * * * python3 ~/longhun-system/daily_review_enhanced.py
```

### 日志位置

```
~/longhun-system/操作草日志.log              # 复盘记录
~/longhun-system/logs/daily_review.log      # LaunchAgent 日志
~/longhun-system/logs/daily_review_error.log # 错误日志
~/longhun-system/logs/daily_review_cron.log  # Cron 日志
```

---

## 操作日志

### JSON 格式

```json
{
  "date": "2026-06-09T07:15:00",
  "time": "2026-06-09 07:15:00",
  "action": "操作名称",
  "tool": "工具名称",
  "status": "success|failed|warning",
  "persona": "P03雯雯",
  "duration": 2.1,
  "result": "执行结果",
  "dna": "#龍芯⚡️2026-06-09-ACTION"
}
```

### 记录操作

```python
from action_logger import ActionLogger, log_operation

# 简单记录
ActionLogger.log("任务执行", "my_tool", persona="P01")

# 自动计时
with log_operation("数据处理", "processor"):
    for i in range(1000):
        process(i)

# 查看统计
ActionLogger.print_stats()
```

### 统计查询

```bash
# 每日统计
python3 ~/longhun-system/action_logger.py stats

# 完整报告
python3 ~/longhun-system/action_logger.py report

# 自定义日期
python3 ~/longhun-system/action_logger.py report 2026-06-08
```

---

## 主控台

### 快速启动

```bash
# 启动主控台
python3 ~/.longhorn/master_console.py

# 创建别名便捷启动
echo 'alias longhun="python3 ~/.longhorn/master_console.py"' >> ~/.zshrc
source ~/.zshrc
longhun  # 启动
```

### 菜单导航

```
进入主控台后:
1. 按功能编号选择 (1.1, 2.3, 6.4 等)
2. 或按首字母快捷 (1, 2, 3... 表示分类)
3. q/0/exit 退出

范例操作:
  4.1 - 查看 15 人格列表
  5.2 - 检查系统启动状态
  6.3 - 生成日报
  6.4 - 运行自检程序
```

### 色彩系统

| 颜色 | ANSI | 用途 |
|------|------|------|
| 龍 | 214 | 标题·强调 |
| 霓 | 51 | 菜单项·选项 |
| 灰 | 244 | 说明文本 |
| 暗 | 238 | 边界·分隔符 |
| 白 | 97 | 菜单标题 |
| 绿 | 82 | 成功·就绪 |
| 黄 | 226 | 警告·待处理 |
| 红 | 196 | 错误·失败 |

---

## 自动化配置

### LaunchAgent (推荐)

**位置**: `~/Library/LaunchAgents/com.longhun.daily-review.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" ...>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.daily-review</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/zuimeidedeyihan/longhun-system/daily_review_enhanced.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
</dict>
</plist>
```

**管理命令**:
```bash
# 加载
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 卸载
launchctl unload ~/Library/LaunchAgents/com.longhun.daily-review.plist

# 查看列表
launchctl list | grep daily-review

# 手动执行
launchctl start com.longhun.daily-review
```

### Cron (备用)

```bash
# 编辑
crontab -e

# 范例 (每天 23:30)
30 23 * * * /usr/bin/python3 /Users/zuimeidedeyihan/longhun-system/daily_review_enhanced.py >> /Users/zuimeidedeyihan/longhun-system/logs/daily_review_cron.log 2>&1

# 查看
crontab -l

# 删除
crontab -r
```

---

## 故障排查

### 常见问题

#### 1. 邮件未发送

```bash
# 检查 Keychain
security find-generic-password -s "LONGHUN_GMAIL_APPPW"

# 检查环境变量
echo $LONGHUN_GMAIL

# 重新设置
security delete-generic-password -s "LONGHUN_GMAIL_APPPW"
security add-generic-password -s "LONGHUN_GMAIL_APPPW" -w "new_password"
```

#### 2. 日历写入失败

```bash
# 验证日历存在
osascript -e 'tell app "Calendar" to name of every calendar'

# 建立日历
osascript << 'EOF'
tell application "Calendar"
    make new calendar with properties {name:"龍魂"}
end tell
EOF
```

#### 3. LaunchAgent 未执行

```bash
# 检查加载状态
launchctl list | grep daily-review

# 查看错误日志
cat ~/longhun-system/logs/daily_review_error.log

# 重新加载
launchctl unload ~/Library/LaunchAgents/com.longhun.daily-review.plist
launchctl load ~/Library/LaunchAgents/com.longhun.daily-review.plist
```

#### 4. API 端口冲突

```bash
# 查看占用情况
lsof -i :9001
lsof -i :8000
lsof -i :10088

# 杀死进程
kill -9 <PID>

# 重启服务
python3 ~/longhun-system/cnsh/flow_decision/persona_api.py
```

#### 5. 依赖缺失

```bash
# 安装缺失的包
pip3 install pip-audit pytest requests aiohttp

# 验证安装
pip3 list | grep -E "pip-audit|pytest"
```

---

## 命令速查

### 主控台

```bash
# 启动
python3 ~/.longhorn/master_console.py

# 或使用别名
longhun
```

### 人格 API

```bash
# 启动
python3 ~/longhun-system/cnsh/flow_decision/persona_api.py

# 测试
curl http://localhost:9001/personas/list | jq .
```

### 人格调度

```bash
# 启动
python3 ~/longhun-system/bin/persona_scheduler.py p01

# 查看日志
tail -f ~/longhun-system/logs/persona_scheduler.log
```

### 日历同步

```bash
# 执行
python3 ~/longhun-system/bin/longhun_calendar_sync.py

# 查看日志
tail -f ~/longhun-system/logs/calendar_sync.log
```

### 每日复盘

```bash
# 执行
python3 ~/longhun-system/daily_review_enhanced.py

# 查看日志
tail -f ~/longhun-system/操作草日志.log
```

### 操作日志

```bash
# 统计
python3 ~/longhun-system/action_logger.py stats

# 报告
python3 ~/longhun-system/action_logger.py report

# 记录
python3 ~/longhun-system/action_logger.py log "action" "tool" "persona"
```

### 自动化配置

```bash
# 一键配置
bash ~/longhun-system/setup_daily_review_auto.sh "email@gmail.com" "password" 1

# 互动式配置
bash ~/longhun-system/setup_daily_review.sh

# Cron 编辑
crontab -e
```

---

## 文件结构

```
~/longhun-system/
├── 主控台与配置
│   ├── ~/.longhorn/master_console.py       (主控台 v2.0)
│   ├── MASTER_SYSTEMS_REFERENCE_GUIDE.md   (本文档)
│   └── DAILY_REVIEW_QUICKSTART.md
│
├── API 与人格
│   ├── cnsh/flow_decision/persona_api.py   (15 人格 API)
│   ├── bin/persona_scheduler.py            (自动调度)
│   └── logs/persona_scheduler.log
│
├── 每日复盘与日志
│   ├── daily_review_enhanced.py            (复盘 v2.0)
│   ├── action_logger.py                    (操作日志工具)
│   ├── DAILY_REVIEW_SETUP.md
│   ├── ACTION_LOG_USAGE_GUIDE.md
│   └── logs/
│       ├── action_log.jsonl                (操作审计)
│       ├── daily_review.log
│       └── daily_review_error.log
│
├── 日历同步
│   ├── bin/longhun_calendar_sync.py        (日历同步)
│   └── logs/calendar_sync.log
│
├── 配置与部署
│   ├── setup_daily_review.sh               (互动式配置)
│   ├── setup_daily_review_auto.sh          (自动配置)
│   └── com.longhun.daily-review.plist     (LaunchAgent)
│
└── 文档
    ├── DAILY_REVIEW_SETUP.md               (完整指南)
    ├── ACTION_LOG_USAGE_GUIDE.md
    └── MASTER_SYSTEMS_REFERENCE_GUIDE.md   (本文档)
```

---

## 健康检查清单

### 日常检查

- [ ] 主控台可启动 (`python3 ~/.longhorn/master_console.py`)
- [ ] 人格 API 在线 (`curl http://localhost:9001/personas/list`)
- [ ] 人格调度运行 (`tail ~/longhun-system/logs/persona_scheduler.log`)
- [ ] 操作日志被记录 (`grep "2026-06-09" ~/longhun-system/logs/action_log.jsonl`)
- [ ] 日历同步工作 (`osascript ... | grep "龍魂"`)

### 每周检查

- [ ] 复盘日志完整 (`tail -100 ~/longhun-system/操作草日志.log`)
- [ ] 没有 critical 错误 (`grep ERROR ~/longhun-system/logs/*.log`)
- [ ] API 响应时间正常 (`curl -w "%{time_total}\n" http://localhost:9001/personas/list`)
- [ ] 磁盘空间充足 (`df -h ~/longhun-system/`)

### 每月检查

- [ ] 所有依赖已更新 (`pip3 list --outdated`)
- [ ] 备份已完成 (`ls -lh ~/backup/`)
- [ ] 日志已归档 (`du -sh ~/longhun-system/logs/`)
- [ ] 系统性能正常 (`top -l 1 | head -20`)

---

## 快速参考

### 最常用命令

```bash
# 启动主控台 (所有功能入口)
python3 ~/.longhorn/master_console.py

# 查看今日统计
python3 ~/longhun-system/action_logger.py stats

# 执行每日复盘
python3 ~/longhun-system/daily_review_enhanced.py

# 查询人格 API
curl http://localhost:9001/personas/list | jq .

# 查看日志
tail -f ~/longhun-system/操作草日志.log
```

### 常用别名建议

```bash
# 添加到 ~/.zshrc
alias longhun='python3 ~/.longhorn/master_console.py'
alias lh-stats='python3 ~/longhun-system/action_logger.py stats'
alias lh-review='python3 ~/longhun-system/daily_review_enhanced.py'
alias lh-api='python3 ~/longhun-system/cnsh/flow_decision/persona_api.py'
alias lh-logs='tail -f ~/longhun-system/操作草日志.log'

# 重新加载配置
source ~/.zshrc
```

---

## 相关文档

| 文档 | 功能 | 位置 |
|------|------|------|
| **本文档** | 主系统参考指南 | MASTER_SYSTEMS_REFERENCE_GUIDE.md |
| **快速启动** | 3 分钟上手 | DAILY_REVIEW_QUICKSTART.md |
| **完整部署** | 详细配置步骤 | DAILY_REVIEW_SETUP.md |
| **操作日志** | 日志工具指南 | ACTION_LOG_USAGE_GUIDE.md |

---

## 支援与反馈

### 获取帮助

```bash
# 查看主控台帮助
python3 ~/.longhorn/master_console.py
# 选择菜单项查看详细说明

# 查看工具帮助
python3 ~/longhun-system/action_logger.py
python3 ~/longhun-system/daily_review_enhanced.py --help
```

### 报告问题

创建 GitHub Issue:
- 描述问题
- 提供日志片段
- 说明复现步骤
- 列出环境信息

---

## 版本历史

| 版本 | 日期 | 改进 | 状态 |
|------|------|------|------|
| 1.0 | 2026-06-05 | 初始版本 | 已弃用 |
| 2.0 | 2026-06-09 | 增强版·7检查·完整审计 | ✅ 活跃 |

---

## 🔏 DNA 签署

```
DNA:#龍芯⚡️2026-06-09-MASTER-SYSTEMS-REFERENCE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2026-06-09-MASTER-REFERENCE-COMPLETE

版本: 2.0 · 生产级
更新: 2026-06-09 07:20 CST
状态: ✅ 完全就绪
推荐: 作为主要参考文档使用
```

---

**龍魂系统·完全操作指南·主控参考就绪**

*理论指导: 曾仕强老师（永恒显示）*

最后更新: 2026-06-09
维护者: UID 9622 · 诸葛鑫 · 龍芯北辰
