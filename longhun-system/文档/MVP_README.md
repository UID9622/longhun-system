# 🐉 龍魂MVP自动同步系统

> 《道德经》第六十三章："为无为，事无事，味无味。" —— 自动化就是让系统自己做事，老大只管看结果。

**DNA追溯码：** `#龍芯⚡️2026-04-05-MVP自动化脚本-v1.0`  
**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅`  
**GPG指纹：** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**乔前辈：** P15 · 自动化导师 · 代码补满专线

---

## 🚀 一句话干什么

**开机自动跑 → 拉4个核心页面最新内容 → 判定公开/加密 → 写入对应库 → 草日志留痕**

---

## 📦 第零步：环境准备（只做一次）

```bash
# 1. 确认 Python3 在
python3 --version

# 2. 装依赖
pip3 install requests python-dotenv

# 3. 确认 .env 文件在（已有就跳过）
cat ~/longhun-system/.env
# 应该看到 NOTION_TOKEN=ntn_...
```

---

## 🎯 四个核心页面（已配置完成）

| 页面名称 | Page ID | 用途 |
|---------|---------|------|
| 主控操作台 | `2507125a9c9f80d2b214c07deced0f0f` | 系统总控 |
| 龍魂成果页 | `868fec34e5a24e7e829dc5851a75f6b7` | MVP展示 |
| MVP规范 | `8d377b0869e440139b4026583e86ea5a` | 标准文档 |
| 数字资产总库 | `7ed7d67f0ff940f992f4246a382e2a3d` | 资产管理 |

---

## 🏃 第一步：立即运行（手动测试）

```bash
# 进入项目目录
cd ~/longhun-system

# 运行同步脚本
python3 longhun_auto_sync.py
```

**期望输出：**
```
🐉 龍魂MVP自动同步 · 乔前辈P15 出品
⏰ 2026-04-05 14:30:00 北京时间
🧬 #龍芯⚡️2026-04-05-NOTION-SYNC-v1.0

🏥 孙思邈号脉中...
  🟢 Notion API
  ⚪️ 本地Ollama
  ⚪️ MVP服务

📡 开始同步四个核心页面...

🔄 正在同步: 主控操作台
  📄 标题: AI工作流主控操作台
  ⏰ 最后编辑: 2026-04-05T06:30:00.000Z
  📝 内容长度: 1234 字符
  🎯 判定: 🌐公开
  💾 已保存到: public_knowledge/主控操作台_20260405_143000.json
  📜 草日志写入: 同步页面: 主控操作台

✅ 同步完成 · 成功 4/4 页
📜 草日志: ~/longhun-system/sync_log.jsonl
🌐 公开库: ~/longhun-system/public_knowledge
🔒 加密库: ~/longhun-system/encrypted_vault
```

---

## ⏰ 第二步：设置自动运行

### 方案A：每天早上8点自动跑（推荐）

```bash
# 编辑定时任务
crontab -e

# 添加这行（按 i 进入编辑模式，粘贴后按 ESC，输入 :wq 保存）
0 8 * * * cd ~/longhun-system && /usr/bin/python3 longhun_auto_sync.py >> cron.log 2>&1

# 验证是否添加成功
crontab -l
```

### 方案B：开机自动跑（Mac LaunchAgent）

创建文件 `~/Library/LaunchAgents/com.longhun.autosync.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.autosync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/你的用户名/longhun-system/longhun_auto_sync.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>28800</integer>
    <key>StandardOutPath</key>
    <string>/Users/你的用户名/longhun-system/launchagent.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/longhun-system/launchagent_error.log</string>
</dict>
</plist>
```

加载服务：
```bash
launchctl load ~/Library/LaunchAgents/com.longhun.autosync.plist
launchctl list | grep longhun
```

---

## 📋 验收标准（乔前辈验收三条）

| **验收项** | **期望结果** | **验证方式** |
|----------|------------|------------|
| ✅ 能拉数据 | 四个页面信息成功拉取 | 看终端输出有标题+时间 |
| ✅ 能判定 | 每页有 🌐公开 or 🔒加密 标注 | 看终端「判定:」那行 |
| ✅ 能留痕 | sync_log.jsonl 有新记录 | `cat ~/longhun-system/sync_log.jsonl` |

---

## 🔍 文件结构说明

```
~/longhun-system/
├── .env                        # 敏感凭证（已有）
├── allowed-urls.txt            # URL白名单（已创建）
├── longhun_auto_sync.py        # 主同步脚本（新建）
├── MVP_README.md               # 本说明文档（新建）
├── sync_log.jsonl              # 草日志（自动生成）
├── public_knowledge/           # 公开知识库（自动创建）
│   ├── 主控操作台_20260405_143000.json
│   ├── MVP规范_20260405_143001.json
│   └── ...
└── encrypted_vault/            # 加密保管库（自动创建）
    ├── 龍魂成果页_20260405_143002.json
    └── ...
```

---

## 🚨 常见问题排查

### 问题1：401 Unauthorized

```bash
# 检查 Token 是否正确
cat ~/longhun-system/.env | grep NOTION_TOKEN

# 确认 Token 格式（应该是 ntn_ 或 secret_ 开头）
# 如果过期，去 Notion Settings → Integrations → 重新生成
```

### 问题2：ModuleNotFoundError: No module named 'requests'

```bash
# 安装缺失的依赖
pip3 install requests python-dotenv

# 如果还不行，指定用户安装
pip3 install --user requests python-dotenv
```

### 问题3：Crontab 没有执行

```bash
# 1. 确认 crontab 已添加
crontab -l

# 2. 检查日志（如果有报错会在这里）
cat ~/longhun-system/cron.log

# 3. 使用绝对路径
which python3  # 获取 Python3 完整路径
# 然后编辑 crontab，把 /usr/bin/python3 替换成实际路径
```

### 问题4：Page ID 不对

```bash
# Notion 链接格式：
# https://www.notion.so/workspace/页面标题-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#                                          ↑ 这32位就是 page_id

# 脚本会自动去除连字符，所以这两种格式都支持：
# - 868fec34e5a24e7e829dc5851a75f6b7
# - 868fec34-e5a2-4e7e-829d-c5851a75f6b7
```

---

## 🔒 敏感词黑名单（自动触发加密）

脚本会自动检测以下关键词，一旦命中立即标记为 🔒加密：

- `token=`, `secret_`, `sk-`, `Bearer`, `2FA`
- `私钥`, `密码`, `password`, `api_key`
- `手机`, `身份证`, `住址`, `真实账号`
- `ntn_`, `sk-ant-`, `API_KEY`, `SECRET`

如需添加新关键词，编辑 `longhun_auto_sync.py` 中的 `SENSITIVE_KEYWORDS` 列表。

---

## 📊 查看同步日志

```bash
# 查看最近10条同步记录
tail -n 10 ~/longhun-system/sync_log.jsonl

# 美化显示（需要安装 jq）
tail -n 5 ~/longhun-system/sync_log.jsonl | jq .

# 统计今天同步了多少次
grep "$(date +%Y-%m-%d)" ~/longhun-system/sync_log.jsonl | wc -l
```

---

## 🎨 进阶：集成到 MCP 服务器

如果你的 MCP 服务器需要访问这些同步的数据：

```python
# 在你的 MCP 服务器中引入
import json
from pathlib import Path

def load_synced_knowledge():
    """加载已同步的公开知识"""
    knowledge_dir = Path.home() / 'longhun-system' / 'public_knowledge'
    knowledge = []
    
    for file in knowledge_dir.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            knowledge.append(data)
    
    return knowledge

# 使用示例
pages = load_synced_knowledge()
for page in pages:
    print(f"📄 {page['_metadata']['name']}")
```

---

<aside>
🐉

**DNA追溯码：** #龍芯⚡️2026-04-05-MVP自动化脚本-v1.0

**GPG指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

**三色审计：** 🟢 脚本结构通过·无敏感信息·可公开

**乔前辈签：** P15 · 代码补满 · 复制即用

**龍魂现世！天下无欺·守护普通人 🐉**

</aside>
