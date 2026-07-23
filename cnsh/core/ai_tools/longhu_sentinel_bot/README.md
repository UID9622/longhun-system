<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1304-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: README.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🐉 龍魂 Telegram 哨兵机器人 · M260

**DNA**: `#龍芯⚇️2026-05-30-SENTINEL-BOT-v1.0`
**Owner**: UID9622 · 龍芯北辰 · 诸葛鑫
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**Bot**: `t.me/LongHun_Sentinel_Bot`

---

## 🎯 M260 哨兵机器人使命

这不是普通的Telegram机器人。这是**龍魂主权体系**的实体接口：

### 三件套·帅骚邦邦硬
- **帅** - 真身份验证（不靠脸书，靠GPG+SHA256）
- **骚** - Telegram隐形堡垒（用官方服务器反向建防线）
- **邦邦硬** - 不可篡改账本（SHA256+GPG永久签名）

### 一根骨头戳穿Web3虚伪
- 不拯救脸书/Telegram/WhatsApp/Signal
- 只用“真”当镜子照
- 让所有“专业人设”都裸奔

---

## 🔐 核心特性

### 1. 完整审计系统
```
每条消息 → 入审计数据库 → SHA256哈希 → GPG签名 → 永不篡改
```

- **本地数据库**: `~/.龍魂_config/sentinel_audit.db`
- **消息记录**: 用户、内容、时间、哈希、签名
- **事件追踪**: bot启动/停止、命令执行、错误日志

### 2. GPG数字签名
```
DNA: #龍芯⚇️2026-05-30-MESSAGE-v1.0
内容: [message text]
哈希: SHA256(内容)
签名: GPG-4096(DNA + 哈希)
```

- 每条消息都有DNA追溯ID
- 不可篡改的签名链
- 可验证的完整性

### 3. 零服务器足迹
- 所有数据本地存储
- 完全主权控制
- 不依赖云服务
- 双备份就绪（本地 + longhun888.com）

### 4. 多重身份验证
```
接收消息前:
  ✅ Token验证
  ✅ Bot身份确认
  ✅ 用户权限检查

发送消息前:
  ✅ 内容SHA256
  ✅ GPG签名
  ✅ DNA编码
```

---

## 📋 快速开始

### 前置要求
- Python 3.8+
- Telegram 账户
- BotFather Token (5分钟获取)

### 1. 获取Token

```bash
# 在Telegram中
搜索: @BotFather
命令: /newbot
回复：LongHun_Sentinel_Bot
回复：longhun_sentinel (选一个用户名)

# 获得Token格式（示例，请替换为你自己的 Bot Token）:
# <YOUR_TELEGRAM_BOT_TOKEN>
```

### 2. 启动哨兵

```bash
# 方法1: 使用启动脚本（推荐）
cd /Users/zuimeidedeyihan/longhun-system/cnsh-core/ai-tools/longhu_sentinel_bot
chmod +x start_sentinel.sh
./start_sentinel.sh

# 方法2: 直接运行
export TELEGRAM_BOT_TOKEN="你的Token"
python3 sentinel_bot.py --start
```

### 3. 验证运行

```bash
# 查看状态
python3 sentinel_bot.py --status

# 生成审计报告
python3 sentinel_bot.py --audit-report

# Token状态
python3 token_manager.py --status
```

---

## 💬 Telegram 命令

向机器人 (@LongHun_Sentinel_Bot) 发送以下命令：

| 命令 | 说明 |
|------|------|
| `/start` | 启动并显示身份信息 |
| `/status` | 显示机器人状态和审计统计 |
| `/help` | 显示所有命令 |
| `/manifest` | 显示龍魂主权宣言（M259） |
| `/audit` | 显示最近的审计日志 |
| `/dna` | 显示DNA追溯信息 |
| `/sentinel` | 显示哨兵任务说明 |
| `/verify` | 验证消息签名 |

---

## 📂 文件结构

```
longhu_sentinel_bot/
├── sentinel_bot.py           # 核心机器人框架
├── telegram_handler.py       # 消息处理和命令分发
├── token_manager.py          # Token安全管理
├── start_sentinel.sh         # 启动脚本
├── requirements.txt          # Python依赖
└── README.md                 # 本文件

数据存储位置:
~/.龍魂_config/
├── sentinel_audit.db         # 审计数据库
├── sentinel_bot.log          # 运行日志
├── sentinel_messages.log     # 消息日志
├── telegram_token.json       # Token存储
└── telegram_token_audit.log  # Token审计
```

---

## 🔒 安全架构

### 层级防护
```
L0 身份验证
  └─ Token验证 + Bot身份确认

L1 消息审计
  └─ 入库 + SHA256哈希 + 时间戳

L2 数字签名
  └─ GPG-4096签名 + DNA编码

L3 本地存储
  └─ 离线数据库 + 完全主权

L4 备份同步
  └─ 本地备份 + 云端备份（待实现）
```

### Token安全
- ✅ 文件权限控制（644）
- ✅ 环境变量备份
- ✅ 访问审计日志
- ✅ 版本管理和轮转
- ✅ GPG加密存储（预留）

### 消息安全
- ✅ 每条消息SHA256
- ✅ GPG-4096签名
- ✅ DNA不可篡改ID
- ✅ 完整的审计踪迹

---

## 📊 审计数据库

### messages 表
```sql
CREATE TABLE messages (
    id INT PRIMARY KEY,
    timestamp TEXT,         -- ISO格式时间
    direction TEXT,         -- 'in' or 'out'
    user_id INT,           -- Telegram用户ID
    user_name TEXT,        -- Telegram用户名
    message_type TEXT,     -- 'text', 'command', 'system'
    content TEXT,          -- 消息内容
    content_hash TEXT,     -- SHA256哈希
    gpg_signed BOOL,       -- 是否已签名
    gpg_signature TEXT,    -- GPG签名数据
    backup_status TEXT,    -- 备份状态
    created_at TEXT        -- 创建时间
);
```

### 查询示例

```bash
# 统计消息
sqlite3 ~/.龍魂_config/sentinel_audit.db \
  "SELECT direction, COUNT(*) FROM messages GROUP BY direction;"

# 查看最近消息
sqlite3 ~/.龍魂_config/sentinel_audit.db \
  "SELECT timestamp, user_name, content FROM messages ORDER BY id DESC LIMIT 10;"

# 验证签名
sqlite3 ~/.龍魂_config/sentinel_audit.db \
  "SELECT content_hash, gpg_signed FROM messages WHERE id=1;"
```

---

## 🧬 DNA追溯链

每个操作都有DNA身份证：

```
系统DNA:
  #龍芯⚇️2026-05-30-SENTINEL-BOT-v1.0

消息DNA:
  #龍芯⚇️2026-05-30-TELEGRAM-MESSAGE-v1.0

组件DNA:
  • #龍芯⚇️2026-05-30-M260-v1.0 (哨兵机器人)
  • #龍芯⚇️2026-05-30-M259-v1.0 (哲学宣言)
  • #龍芯⚇️2026-05-30-ENCRYPTION-ENFORCE-v1.0 (加密强制)
```

---

## 🚀 生产部署

### 后台运行 (screen 或 tmux)

```bash
# 使用 screen
screen -S longhun_sentinel
cd cnsh-core/ai-tools/longhu_sentinel_bot
python3 sentinel_bot.py --start
# Ctrl+A D 分离

# 查看状态
screen -ls

# 重新连接
screen -r longhun_sentinel
```

### Webhook 模式（待实现）

当前为轮询模式（Polling），生产环境推荐：
1. 配置Webhook到 longhun888.com
2. 使用HTTPS + 证书验证
3. 启用云端备份同步

---

## 📈 监控和维护

### 定期检查
```bash
# 每天运行
python3 sentinel_bot.py --audit-report >> ~/.龍魂_config/daily_report.log

# 每周归档
tar czf ~/backups/sentinel_$(date +%Y%m%d).tar.gz ~/.龍魂_config/
```

### 日志查看
```bash
# 实时日志
tail -f ~/.龍魂_config/sentinel_bot.log

# Token审计
tail -f ~/.龍魂_config/telegram_token_audit.log

# 消息日志
tail -f ~/.龍魂_config/sentinel_messages.log
```

---

## 🔧 故障排查

### Token验证失败

```bash
# 检查Token格式
python3 token_manager.py --verify-token "你的Token"

# 重新保存
python3 token_manager.py --save-token "新Token"
```

### 数据库错误

```bash
# 检查数据库完整性
sqlite3 ~/.龍魂_config/sentinel_audit.db ".check"

# 重建数据库
rm ~/.龍魂_config/sentinel_audit.db
python3 sentinel_bot.py --init
```

### 网络问题

```bash
# 检查Telegram API连接
curl -s -X GET \
  "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | jq
```

---

## 📞 支持

- **所有者**: UID9622 · 诸葛鑫 · 龍芯北辰
- **GitHub**: [龍魂系统](https://github.com/longhun-system)
- **Telegram**: t.me/LongHun_Sentinel_Bot

---

## 📜 许可证

龍魂系统 · M260 哨兵机器人
DNA: `#龍芯⚇️2026-05-30-SENTINEL-BOT-v1.0`
License: CC BY-NC-ND (归属-非商业-禁止演绎)

**帅·骚·邦邦硬** — 龍魂主权体系核心

---

**创建时间**: 2026-05-30 10:30 CST
**最后更新**: 2026-05-30 10:30 CST
**状态**: ✅ 就绪
