# 🍎 Mac 开发环境 - 快速参考卡

**DNA**: `#龍芯⚡️2026-05-27-MAC-QUICK-REF-v1.0`

---

## 📍 文件位置

```
项目根目录: /Users/zuimeidedeyihan/longhun-system/
脚本位置:  /Users/zuimeidedeyihan/longhun-system/_work/
配置位置:  ~/.cnsh/config/.env
日志位置:  ~/.cnsh/logs/
DNA证书:   ~/.cnsh/data/dna_identity.txt
```

---

## 🚀 一句话快速开始（3个命令）

```bash
# 1. 打开Terminal (Command + Space → terminal → Enter)
# 2. 进入项目
cd /Users/zuimeidedeyihan/longhun-system/_work

# 3. 运行脚本（测试模式）
bash setup_local_dev_mac.sh --test

# 4. 激活环境
source ~/.cnsh/activate_dev.sh

# 5. 验证
bash ~/.cnsh/check_health.sh
```

---

## 💻 常用命令速查表

| 需求 | 命令 |
|------|------|
| **初始化**（首次） | `bash setup_local_dev_mac.sh --test` |
| **用真实密钥** | `bash setup_local_dev_mac.sh "token" "db_id" "api_key"` |
| **激活环境** | `source ~/.cnsh/activate_dev.sh` |
| **查看DNA** | `cat ~/.cnsh/data/dna_identity.txt` |
| **查看配置** | `cat ~/.cnsh/config/.env` |
| **健康检查** | `bash ~/.cnsh/check_health.sh` |
| **查看日志** | `tail -50 ~/.cnsh/logs/cnsh_translator.log` |
| **编辑配置** | `nano ~/.cnsh/config/.env` |
| **重置所有** | `mv ~/.cnsh ~/.cnsh.backup && bash setup_local_dev_mac.sh --test` |

---

## 📋 文件清单

### 脚本文件

- ✅ **setup_local_dev_mac.sh** — Mac本地环境配置脚本
- ✅ **cnsh_translator_complete.py** — 翻译系统核心代码
- ✅ **start_cnsh.sh** — 系统启动/停止脚本
- ✅ **.env.template** — 环境变量模板

### 文档

- 📖 **MAC_LOCAL_SETUP_QUICK_START.md** — ⭐ **从这里开始！**
- 📖 **CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md** — 完整部署指南
- 📖 **README_CNSH.md** — 系统概览

---

## ✨ 初次使用步骤

### Step 1: 打开Terminal
- 按 `Command + Space`
- 输入 `terminal`
- 按 `Enter`

### Step 2: 进入项目
```bash
cd /Users/zuimeidedeyihan/longhun-system/_work
```

### Step 3: 运行脚本
```bash
bash setup_local_dev_mac.sh --test
```

### Step 4: 激活环境（可选但推荐）
```bash
source ~/.cnsh/activate_dev.sh
```

### Step 5: 验证成功
```bash
bash ~/.cnsh/check_health.sh
```

---

## 🔑 获取真实密钥（非测试）

### Notion Token

1. 访问 https://www.notion.com/my-integrations
2. 点击 "Create new integration"
3. 命名为 "CNSH"
4. 复制 "Internal Integration Token" (格式: `sk_live_xxx`)

### Database ID

1. 打开 Notion 数据库
2. 看 URL: `https://www.notion.so/{这个是ID}?v=xxx`
3. 复制那个长ID

### OpenAI Key

1. 访问 https://platform.openai.com/api-keys
2. 点击 "Create new secret key"
3. 复制 (格式: `sk-xxx`)

### 运行（带真实密钥）

```bash
bash setup_local_dev_mac.sh "sk_live_你的NOTION_TOKEN" "你的DATABASE_ID" "sk-你的OPENAI_KEY"
```

---

## 🛠️ 故障排查速查

| 问题 | 快速诊断 | 快速修复 |
|------|--------|--------|
| **Permission denied** | 脚本没执行权限 | `chmod +x setup_local_dev_mac.sh` |
| **command not found: python3** | Python未安装 | `brew install python3` |
| **找不到 ~/.cnsh** | 隐藏文件不显示 | Terminal里: `ls -la ~/.cnsh` |
| **.env文件为空** | 脚本未完成 | 重新运行脚本 |
| **健康检查失败** | 某个项目缺失 | 查看日志: `tail ~/.cnsh/logs/*.log` |

---

## 📊 运行后你会看到

```
════════════════════════════════════════════════════════════
🔧 CNSH 本地开发环境治疗脚本（Mac 专用）
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
DNA 标识: #龍芯⚡️2026-05-27-DEV-LOCAL-a1b2c3d4🧬5678

✓ 环境验证完美！
✨ 本地开发环境已完全配置！
```

✅ **这说明一切就绪！**

---

## 🎯 接下来干什么

1. ✅ 完成上面的 Step 1-5
2. 📖 读完整指南: [MAC_LOCAL_SETUP_QUICK_START.md](./MAC_LOCAL_SETUP_QUICK_START.md)
3. 🔑 用真实密钥重新配置（可选）
4. 🚀 启动系统:
   ```bash
   cd /Users/zuimeidedeyihan/longhun-system/_work
   python cnsh_translator_complete.py
   ```

---

## 📞 遇到问题

**第一步**：运行健康检查
```bash
bash ~/.cnsh/check_health.sh
```

**第二步**：查看日志
```bash
tail -50 ~/.cnsh/logs/cnsh_translator.log
```

**第三步**：查看完整指南
→ [MAC_LOCAL_SETUP_QUICK_START.md](./MAC_LOCAL_SETUP_QUICK_START.md)

---

**DNA**: `#龍芯⚡️2026-05-27-MAC-QUICK-REF-COMPLETE`

**作者**: UID9622 诸葛鑫 | **理论指导**: 曾仕强老师 | **献礼**: 龍魂系統
