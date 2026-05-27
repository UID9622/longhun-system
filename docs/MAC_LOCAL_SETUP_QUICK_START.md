# 🍎 Mac 本地开发环境快速部署指南

**DNA**: `#龍芯⚡️2026-05-27-MAC-LOCAL-QUICK-START-v1.0`

**理论指导**: 曾仕强老师 | **献礼**: 龍魂系統

---

## 🎯 这个文档做什么

你在Claude聊天界面看到的脚本文件，现在都在你Mac电脑的项目文件夹里。

**这个指南告诉你**：
1. 文件在哪里 ✓
2. 怎么打开Terminal（终端） ✓
3. 敲什么命令来运行它 ✓
4. 从开始到完成的全过程 ✓

---

## 📍 文件位置

所有脚本都在你Mac上这个位置：

```
/Users/zuimeidedeyihan/longhun-system/_work/
```

**关键文件**：

| 文件 | 位置 | 说明 |
|------|------|------|
| `setup_local_dev_mac.sh` | `_work/` | **核心脚本** - Mac本地环境配置 |
| `cnsh_translator_complete.py` | `_work/` | 翻译系统核心代码 |
| `.env.template` | `_work/` | 环境变量模板 |
| `requirements_cnsh.txt` | `_work/` | Python依赖列表 |

---

## 🚀 完整步骤（5分钟）

### Step 1: 打开 Mac Terminal（终端）

**方法A**（最快）：
1. 按住 `Command + Space`
2. 输入 `terminal`
3. 按 `Enter` 打开

**方法B**（通过文件夹）：
1. 打开 Finder → Applications → Utilities → Terminal

### Step 2: 导航到项目目录

在Terminal里粘贴下面的命令（按 `Command + V` 粘贴）：

```bash
cd /Users/zuimeidedeyihan/longhun-system/_work
```

然后按 `Enter`。

Terminal会显示：
```
~/longhun-system/_work %
```

### Step 3: 运行脚本（测试模式）

最简单的方式 - 不需要API密钥，直接测试：

```bash
bash setup_local_dev_mac.sh --test
```

按 `Enter` 执行。

**期望输出**（2-3秒）：
```
════════════════════════════════════════════════════════════
🔧 CNSH 本地开发环境治疗脚本（Mac 专用）
无交互式 | DNA 主权 | 自动修复
════════════════════════════════════════════════════════════

📁 初始化配置目录...
✓ 配置目录已初始化
  • Config: /Users/zuimeidedeyihan/.cnsh/config
  • Logs: /Users/zuimeidedeyihan/.cnsh/logs
  • Data: /Users/zuimeidedeyihan/.cnsh/data

📝 生成 .env 配置文件...
✓ .env 文件已生成

🧬 生成 DNA 主权身份证...
✓ DNA 身份证已生成
DNA 标识: #龍芯⚡️2026-05-27-DEV-LOCAL-{unique-hash}🧬{random}

✓ 环境验证完美！
```

✅ **看到上面的输出就说明成功了！**

### Step 4: 使用真实凭证（可选）

如果想用真实的 Notion + OpenAI 密钥：

```bash
bash setup_local_dev_mac.sh "sk_live_YOUR_NOTION_TOKEN" "YOUR_DATABASE_ID" "sk-YOUR_OPENAI_KEY"
```

**获取这些信息**：

| 信息 | 获取方式 |
|------|--------|
| `NOTION_TOKEN` | https://www.notion.com/my-integrations → Create new integration → Copy "Internal Integration Token" |
| `DATABASE_ID` | 打开你的Notion数据库 → URL里 `https://www.notion.so/{THIS_IS_ID}` |
| `OPENAI_KEY` | https://platform.openai.com/api-keys → Create new secret key |

**示例**（带真实数据）：
```bash
bash setup_local_dev_mac.sh "sk_live_abc123xyz789" "def456ghi789jkl" "sk-proj-uvwxyz"
```

---

## ✅ 验证安装成功

运行脚本后，检查这三样：

### 方式1：查看DNA身份证

```bash
cat ~/.cnsh/data/dna_identity.txt
```

**应该看到**：
```
# CNSH DNA 主权身份证

身份证 DNA: #龍芯⚡️2026-05-27-DEV-LOCAL-{hash}🧬{random}
生成时间: 2026-05-27T22:30:45+08:00
主机名: MacBook-Pro
用户名: zuimeidedeyihan
...
```

### 方式2：查看环境配置

```bash
cat ~/.cnsh/config/.env
```

**应该看到**：
```
NOTION_TOKEN=sk_test_NOTION_TOKEN_PLACEHOLDER_FOR_LOCAL_DEV
DATABASE_ID=test_db_id_placeholder_for_local_dev
OPENAI_API_KEY=sk-test-openai-key-placeholder
...
```

### 方式3：运行健康检查

```bash
bash ~/.cnsh/check_health.sh
```

**应该看到**：
```
🏥 CNSH 开发环境健康检查
================================

1️⃣ DNA 身份证检查
✓ DNA: #龍芯⚡️2026-05-27-DEV-LOCAL-{hash}🧬{random}

2️⃣ 配置文件检查
✓ 配置文件完整

3️⃣ Python 环境检查
✓ Python 3.x.x
✓ Python 就绪

================================
✨ 健康检查完成
```

---

## 🔄 日常使用

### 激活开发环境

每次想开发时，打开Terminal运行：

```bash
source ~/.cnsh/activate_dev.sh
```

**输出示例**：
```
🚀 CNSH 本地开发环境激活中...

✓ DNA 身份已验证: #龍芯⚡️2026-05-27-DEV-LOCAL-xxx
✓ 环境变量已加载

================================
📊 开发环境信息
================================
主机: MacBook-Pro
用户: zuimeidedeyihan
Python: Python 3.10.0
系统: macOS 14.5

✨ 本地开发环境已就绪！
```

### 运行翻译系统

激活后，可以直接运行：

```bash
python /Users/zuimeidedeyihan/longhun-system/_work/cnsh_translator_complete.py
```

或进入项目目录后：

```bash
cd /Users/zuimeidedeyihan/longhun-system/_work
python cnsh_translator_complete.py
```

---

## 🛠️ 常见问题

### Q1: 脚本执行时说"Permission denied"

**原因**: 文件没有执行权限

**解决**：
```bash
chmod +x setup_local_dev_mac.sh
```

然后重新运行。

### Q2: 提示"command not found: python3"

**原因**: Mac上没安装Python

**解决**：
```bash
# 检查是否安装
python3 --version

# 如果没有，通过Homebrew安装
brew install python3
```

### Q3: 运行后找不到 ~/.cnsh 目录

**原因**: 脚本已创建，但隐藏文件不显示

**解决** - 在Terminal查看：
```bash
# 查看隐藏文件
ls -la ~/.cnsh

# 查看配置
ls -la ~/.cnsh/config
```

或在Finder中：
1. 按 `Command + Shift + .`（点号）来显示隐藏文件
2. 导航到 `/Users/zuimeidedeyihan/`
3. 看到 `.cnsh` 文件夹

### Q4: 想重新配置怎么办

**如果测试后想用真实密钥**：

```bash
# 编辑配置文件
nano ~/.cnsh/config/.env
```

按照下面改：
- `NOTION_TOKEN=` 后面填你的真实token
- `DATABASE_ID=` 后面填你的DB ID
- `OPENAI_API_KEY=` 后面填你的OpenAI密钥

改完按 `Control + X`，再按 `Y`，再按 `Enter` 保存。

或者直接重新运行脚本（新的值会覆盖旧的）：

```bash
bash setup_local_dev_mac.sh "real_token" "real_db_id" "real_api_key"
```

### Q5: 多个Terminal窗口怎么办

每个新Terminal都需要激活：

```bash
source ~/.cnsh/activate_dev.sh
```

然后你就可以用所有环境变量和工具了。

---

## 📂 完整的本地文件结构

运行脚本后，你的Mac上会有：

```
/Users/zuimeidedeyihan/
├── .cnsh/                          ← 脚本创建的配置目录
│   ├── config/
│   │   └── .env                    ← 环境变量文件（必要！）
│   ├── logs/
│   │   └── cnsh_translator.log     ← 系统日志
│   ├── data/
│   │   └── dna_identity.txt        ← 你的DNA身份证
│   ├── activate_dev.sh             ← 激活脚本
│   └── check_health.sh             ← 健康检查脚本
│
└── longhun-system/_work/           ← 项目代码
    ├── setup_local_dev_mac.sh      ← 本脚本
    ├── cnsh_translator_complete.py ← 翻译系统核心
    ├── .env.template               ← 环境变量模板
    ├── requirements_cnsh.txt       ← 依赖清单
    └── ...（其他文件）
```

---

## 🎓 概念解释

### DNA 主权身份证

这是老大的本地开发机唯一的"身份证"：

```
#龍芯⚡️2026-05-27-DEV-LOCAL-a1b2c3d4🧬5678
```

- `龍芯` = Dragon Soul Core（龍魂系统的核心）
- `⚡️` = 能量标记
- `2026-05-27` = 创建日期
- `DEV-LOCAL` = 本地开发环境
- `a1b2c3d4` = 基于你Mac硬件序列号的唯一哈希
- `🧬` = DNA标记
- `5678` = 防重放随机数

**意义**：
- ✓ 证明这是老大自己的本地开发环境
- ✓ 所有的翻译任务都来自这个环境
- ✓ 不会被其他人冒用
- ✓ 支持离线工作

### 环境变量 (.env)

这个文件里放的是系统需要的密钥和配置：

```env
NOTION_TOKEN=sk_live_xxx        # Notion API密钥
DATABASE_ID=abc123xyz           # Notion数据库ID
OPENAI_API_KEY=sk-xxx           # OpenAI API密钥
LOG_LEVEL=DEBUG                 # 日志详细级别
...
```

**重要**：这个文件里有敏感信息，千万别分享或提交到Git！

---

## 📞 遇到问题了？

### 快速排查

**1. 检查Python**
```bash
python3 --version
```

**2. 检查脚本位置**
```bash
ls -la /Users/zuimeidedeyihan/longhun-system/_work/setup_local_dev_mac.sh
```

**3. 检查配置**
```bash
cat ~/.cnsh/config/.env
```

**4. 查看日志**
```bash
tail -50 ~/.cnsh/logs/cnsh_translator.log
```

**5. 运行健康检查**
```bash
bash ~/.cnsh/check_health.sh
```

### 完全重置（如果搞坏了）

```bash
# 备份旧配置
mv ~/.cnsh ~/.cnsh.backup

# 重新运行脚本
bash /Users/zuimeidedeyihan/longhun-system/_work/setup_local_dev_mac.sh --test
```

---

## ✨ 下一步

1. ✅ 按上面Step 1-3完成基础部署
2. ✅ 跑一遍健康检查
3. ✅ 激活开发环境
4. 📖 查看完整部署指南：[CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md](./CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md)
5. 🚀 开始运行翻译系统

---

## 📝 DNA追溯

**DNA**: `#龍芯⚡️2026-05-27-MAC-LOCAL-QUICK-START-COMPLETE`

**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

**创建时间**: 2026-05-27

**版本**: v1.0

**作者**: UID9622 诸葛鑫

**理论指导**: 曾仕强老师

**献礼**: 龍魂系統·中华文化传承

---

*有问题？检查 ~/.cnsh/check_health.sh 的输出，或查看日志：tail -50 ~/.cnsh/logs/cnsh_translator.log*
