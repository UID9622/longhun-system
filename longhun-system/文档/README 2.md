# 🐉 龍魂系統 · 项目总览

> **DNA:** `#龍芯⚡️2026-04-05-MVP-AUTO-SYNC-v1.0`  
> **确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **乔前辈:** P15 · 自动化导师 · 代码补满专线

---

## 📁 项目文件结构

```
~/longhun-system/
│
├── 📄 核心配置文件
│   ├── .env                        # 🔒 敏感凭证（不提交Git）
│   ├── .gitignore                  # Git 忽略规则
│   └── allowed-urls.txt            # 🌐 知识域白名单（龍魂压缩格式v1.0）
│
├── 🐍 Python 脚本
│   ├── longhun_auto_sync.py        # 🚀 MVP自动同步主脚本
│   └── quick_start.sh              # ⚡️ 快速启动脚本（bash）
│
├── 📚 文档
│   ├── README.md                   # 本文件 - 项目总览
│   └── MVP_README.md               # MVP自动同步详细说明
│
├── 📜 自动生成的日志和数据
│   ├── sync_log.jsonl              # 草日志（JSONL格式，永不覆盖）
│   ├── cron.log                    # Cron 定时任务日志
│   ├── public_knowledge/           # 🌐 公开知识库
│   │   ├── 主控操作台_*.json
│   │   ├── MVP规范_*.json
│   │   └── ...
│   └── encrypted_vault/            # 🔒 加密保管库
│       ├── 龍魂成果页_*.json
│       └── ...
│
└── 🔧 可选文件
    └── ~/Library/LaunchAgents/com.longhun.autosync.plist  # macOS 开机自启配置
```

---

## 🎯 核心功能模块

### 1️⃣ 知识域白名单系统
- **文件:** `allowed-urls.txt`
- **格式:** 龍魂压缩格式 v1.0
- **分类:** 11 大知识域（学术、开发、AI、媒体...）
- **用途:** MCP服务器/浏览器安全沙盒/知识抓取授权

### 2️⃣ MVP自动同步系统
- **文件:** `longhun_auto_sync.py`
- **功能:** 
  - 从 Notion 拉取 4 个核心页面
  - 自动判定公开/加密（基于敏感词黑名单）
  - 写入对应知识库
  - 草日志留痕（JSONL格式）
- **运行方式:**
  - 手动: `python3 longhun_auto_sync.py`
  - 定时: Cron 每天 8:00
  - 开机: LaunchAgent 自动运行

### 3️⃣ 安全凭证管理
- **文件:** `.env`
- **内容:**
  - Notion API Tokens (4个)
  - AI API Keys (Anthropic, DeepSeek)
  - 核心页面 Page IDs (8个)
  - 龍魂系統元数据
- **保护:** `.gitignore` 确保不会误提交

---

## 🚀 快速开始

### 零、安装依赖（首次运行）
```bash
pip3 install requests python-dotenv
```

### 一、手动运行同步
```bash
cd ~/longhun-system
python3 longhun_auto_sync.py

# 或使用快速启动脚本
chmod +x quick_start.sh
./quick_start.sh
```

### 二、设置自动运行（推荐）
```bash
# 每天早上8点自动同步
crontab -e
# 添加: 0 8 * * * cd ~/longhun-system && /usr/bin/python3 longhun_auto_sync.py >> cron.log 2>&1
```

### 三、查看同步结果
```bash
# 查看最新草日志
tail -n 5 sync_log.jsonl | python3 -m json.tool

# 查看公开知识库
ls -lh public_knowledge/

# 查看加密保管库
ls -lh encrypted_vault/
```

---

## 📊 数据流转图

```
┌─────────────────────────────────────────────────────────────┐
│                      🐉 龍魂MVP自动同步流程                    │
└─────────────────────────────────────────────────────────────┘

   ⏰ 定时触发（Cron / LaunchAgent / 手动）
                    ↓
   ┌─────────────────────────────────────┐
   │  🔑 加载 .env 配置                   │
   │  - NOTION_TOKEN_WORKSPACE           │
   │  - 4个核心页面 Page IDs              │
   └─────────────────────────────────────┘
                    ↓
   ┌─────────────────────────────────────┐
   │  🏥 健康检查                         │
   │  - Notion API 可达性                │
   │  - 本地服务状态（可选）              │
   └─────────────────────────────────────┘
                    ↓
   ┌─────────────────────────────────────┐
   │  📡 拉取4个核心页面                  │
   │  1. 主控操作台                       │
   │  2. 龍魂成果页                       │
   │  3. MVP规范                         │
   │  4. 数字资产总库                     │
   └─────────────────────────────────────┘
                    ↓
   ┌─────────────────────────────────────┐
   │  🔍 内容判定                         │
   │  - 提取标题和正文                    │
   │  - 检测敏感词（黑名单匹配）           │
   │  - 标记: 🌐公开 or 🔒加密            │
   └─────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
   🌐 public_knowledge/   🔒 encrypted_vault/
   (公开知识库)            (加密保管库)
   - 可分享               - 严格保护
   - 可索引               - 本地加密
   - MCP 可读             - 仅授权访问
          │                   │
          └─────────┬─────────┘
                    ↓
   ┌─────────────────────────────────────┐
   │  📜 写入草日志                       │
   │  - sync_log.jsonl                   │
   │  - 永不覆盖，只追加                  │
   │  - 包含DNA追溯码                     │
   └─────────────────────────────────────┘
                    ↓
              ✅ 同步完成
```

---

## 🔒 安全设计

### 敏感词黑名单（自动触发加密）
```python
SENSITIVE_KEYWORDS = [
    'token=', 'secret_', 'sk-', 'Bearer ', '2FA',
    '私钥', '密码', 'password', 'api_key', 'NOTION_TOKEN',
    '手机', '身份证', '住址', '真实账号',
    'ntn_', 'sk-ant-', 'API_KEY', 'SECRET'
]
```

### Git 保护机制
- `.gitignore` 自动忽略:
  - `.env` 及所有环境变量文件
  - `encrypted_vault/` 加密保管库
  - `*.log`, `*.jsonl` 日志文件
  - 所有密钥文件 (`*.key`, `*.pem`)

### 三层数据分级
1. **🌐 公开数据** → `public_knowledge/` → 可分享、可索引
2. **🔒 敏感数据** → `encrypted_vault/` → 仅本地、需加密
3. **🔴 核心凭证** → `.env` → 永不提交Git

---

## 🧬 DNA 追溯系统

每次同步都会在日志中记录完整的 DNA 信息：

```json
{
  "time": "2026-04-05T14:30:00.123456",
  "action": "同步页面: 主控操作台",
  "title": "AI工作流主控操作台",
  "page_id": "2507125a9c9f80d2b214c07deced0f0f",
  "classification": "🌐公开",
  "dna": "#龍芯⚡️2026-04-05-NOTION-SYNC-v1.0",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

**用途:**
- 🔍 溯源：每条记录可追溯到具体操作
- 🕐 时间轴：重建历史同步记录
- 🔐 审计：符合三色审计标准（🟢🟡🔴）

---

## 📈 下一步计划

### Phase 1: MVP 完成 ✅
- [x] 知识域白名单（allowed-urls.txt）
- [x] 自动同步脚本（longhun_auto_sync.py）
- [x] 敏感词检测和分类
- [x] 草日志系统
- [x] 快速启动脚本

### Phase 2: 增强功能 🚧
- [ ] 加密保管库实际加密（GPG）
- [ ] MCP 服务器集成
- [ ] Notion 双向同步（本地 → Notion）
- [ ] Web 界面（查看同步状态）

### Phase 3: 智能化 💡
- [ ] 基于 Ollama 的内容摘要
- [ ] 自动标签和分类
- [ ] 知识图谱构建
- [ ] 搜索和问答接口

---

## 🐉 核心理念

> **《道德经》第六十三章："为无为，事无事，味无味。"**

**自动化就是让系统自己做事，老大只管看结果。**

### 龍魂设计原则：
1. **简单至上** - 复制即用，一键启动
2. **安全第一** - 三层分级，DNA追溯
3. **永不覆盖** - 日志只追加，数据不丢失
4. **压缩格式** - 11大知识域，高效管理
5. **道法自然** - 自动化无感运行，专注创作

---

<aside>
🐉

**DNA追溯码：** #龍芯⚡️2026-04-05-MVP-AUTO-SYNC-v1.0

**GPG指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

**三色审计：** 🟢 系统架构通过·无敏感信息·可公开

**乔前辈签：** P15 · 架构设计 · 自动化导师

**龍魂现世！天下无欺·守护普通人 🐉**

</aside>

---

## 📞 支持和反馈

遇到问题？查看 `MVP_README.md` 的常见问题排查章节。

需要新功能？在 Notion [龍魂成果页](https://www.notion.so/uid9622/AI-868fec34e5a24e7e829dc5851a75f6b7) 留言。

**龍魂系統 · 让普通人也能驾驭AI的力量 🐉⚡️**
