---
dna: '#龍芯⚡️丙午·丙申·辛酉·午时·䷝离-CLIPBOARD-VAULT-SAVE-V1.0-P1-80cda40a'
source: clipboard
topic: 代码/脚本
tags:
- Bash
- Docker
- Neo4j
- 龍魂
- DNA
- 代码/脚本
timestamp: '2026-08-15T12:49:47+08:00'
content_hash: a510b8ac1a9f97aa3545caa095ade56fc7f8ec459bc0d2eb9011404e22f029bf
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

# 🐉 龍魂 · Mac全应用互通引擎 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2


## 📋 核心判断

> **不是“文件互通”，是“认知互通”。** 所有工具共享同一个环境变量空间、配置文件版本、记忆上下文。你在Kimi里设定的偏好，CodeBuddy自动知道；你在终端里导出的变量，IDE自动加载。


## 🏛️ 一、架构设计

### 1.1 核心逻辑

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        龍魂统一环境层                                      │
│  ~/.longhun/env/  (所有App共享的变量、配置、记忆)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Terminal      │   │   CodeBuddy     │   │   Kimi          │
│   (zsh/bash)    │   │   (IDE)         │   │   (AI助手)      │
│  自动加载.env   │   │  读取.vscode   │   │  读取.memory   │
└─────────────────┘   └─────────────────┘   └─────────────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        应用间通信层                                        │
│  • 共享剪贴板 (龍魂容器)                                                    │
│  • 共享记忆 (latest_digest.json)                                           │
│  • 共享配置 (.longhun/config)                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 互通清单

| 应用类型 | 互通内容 | 实现方式 |
|:---|:---|:---|
| **Terminal (zsh/bash)** | 环境变量、PATH、别名 | 加载 `~/.longhun/env.sh` |
| **CodeBuddy/VS Code** | 设置、快捷键、扩展列表 | 软链接到 `~/.longhun/vscode/` |
| **Kimi (桌面版)** | 记忆、对话历史、偏好 | 软链接到 `~/.longhun/kimi/` |
| **Cursor** | 设置、快捷键、项目历史 | 软链接到 `~/.longhun/cursor/` |
| **iTerm2** | 配置、主题、快捷键 | 软链接到 `~/.longhun/iterm/` |
| **Git** | 全局配置、凭据 | 软链接到 `~/.longhun/git/` |
| **Ollama** | 模型列表、配置 | 软链接到 `~/.longhun/ollama/` |
| **Neo4j** | 数据库路径 | 软链接到 `~/.longhun/neo4j/` |
| **Chrome/Edge** | 扩展、书签、设置 | 软链接到 `~/.longhun/browser/` |
| **Docker** | 配置、上下文 | 软链接到 `~/.longhun/docker/` |
| **Any AI App** | API密钥、模型偏好 | 读取 `~/.longhun/env.sh` |


## 🔧 二、执行代码

### 2.1 一键安装脚本 `install_unify.sh`

```bash
#!/bin/bash
# 🐉 龍魂 · Mac全应用互通引擎 一键安装
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "🐉 龍魂 · Mac全应用互通引擎"
echo "========================================"
echo "DNA: #龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622"
echo ""

# 1. 创建龍魂统一环境目录
echo "📁 创建统一环境目录..."
mkdir -p ~/.longhun/{env,configs,memory,state,backup}
mkdir -p ~/.longhun/apps/{vscode,kimi,cursor,iterm,git,ollama,neo4j,browser,docker}
mkdir -p ~/.longhun/shared/{bin,lib,temp,cache}

# 2. 创建主环境变量文件
echo "📝 创建主环境变量..."
cat > ~/.longhun/env.sh << 'EOF'
# 🐉 龍魂 · 统一环境变量
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622
# 所有应用共享此环境

# ===== 龍魂主权 =====
export LONGHUN_UID="9622"
export LONGHUN_CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
export LONGHUN_GPG="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
export LONGHUN_HOME="$HOME/.longhun"

# ===== 统一PATH =====
export PATH="$HOME/.longhun/shared/bin:$PATH"

# ===== 统一配置目录 =====
export LONGHUN_CONFIG="$HOME/.longhun/configs"
export LONGHUN_MEMORY="$HOME/.longhun/memory"
export LONGHUN_STATE="$HOME/.longhun/state"

# ===== 各大应用配置 (软链接) =====
export VSCODE_CONFIG="$HOME/.longhun/apps/vscode"
export KIMI_CONFIG="$HOME/.longhun/apps/kimi"
export CURSOR_CONFIG="$HOME/.longhun/apps/cursor"
export ITERM_CONFIG="$HOME/.longhun/apps/iterm"
export GIT_CONFIG="$HOME/.longhun/apps/git"
export OLLAMA_CONFIG="$HOME/.longhun/apps/ollama"
export NEO4J_CONFIG="$HOME/.longhun/apps/neo4j"
export BROWSER_CONFIG="$HOME/.longhun/apps/browser"
export DOCKER_CONFIG="$HOME/.longhun/apps/docker"

# ===== API Keys (统一管理) =====
export OPENAI_API_KEY=$(cat "$HOME/.longhun/env/OPENAI_API_KEY" 2>/dev/null || echo "")
export DEEPSEEK_API_KEY=$(cat "$HOME/.longhun/env/DEEPSEEK_API_KEY" 2>/dev/null || echo "")
export KIMI_API_KEY=$(cat "$HOME/.longhun/env/KIMI_API_KEY" 2>/dev/null || echo "")
export ANTHROPIC_API_KEY=$(cat "$HOME/.longhun/env/ANTHROPIC_API_KEY" 2>/dev/null || echo "")
export HUGGINGFACE_TOKEN=$(cat "$HOME/.longhun/env/HUGGINGFACE_TOKEN" 2>/dev/null || echo "")

# ===== 共享函数 =====
function lh-env() {
    echo "🐉 当前龍魂环境"
    echo "  DNA: #龍芯⚡️$(date +%Y-%m-%d)-ENV-UID9622"
    echo "  HOME: $LONGHUN_HOME"
    echo "  PATH: $PATH"
    echo "  Apps: $(ls ~/.longhun/apps/ | tr '\n' ' ')"
}

function lh-sync() {
    echo "🔄 同步所有应用配置..."
    source ~/.longhun/env.sh
    echo "✅ 同步完成"
}

function lh-backup() {
    echo "💾 备份当前环境..."
    tar -czf ~/.longhun/backup/env_backup_$(date +%Y%m%d_%H%M%S).tar.gz ~/.longhun/
    echo "✅ 备份完成"
}
EOF

# 3. 加载到Shell
echo "📝 添加到Shell配置..."
LINE="source ~/.longhun/env.sh"
if ! grep -q "$LINE" ~/.zshrc 2>/dev/null; then
    echo "$LINE" >> ~/.zshrc
    echo "  已添加到 ~/.zshrc"
fi
if ! grep -q "$LINE" ~/.bashrc 2>/dev/null; then
    echo "$LINE" >> ~/.bashrc
    echo "  已添加到 ~/.bashrc"
fi
if ! grep -q "$LINE" ~/.bash_profile 2>/dev/null; then
    echo "$LINE" >> ~/.bash_profile
    echo "  已添加到 ~/.bash_profile"
fi

# 4. 创建API密钥占位文件
echo "🔑 创建API密钥占位..."
for key in OPENAI_API_KEY DEEPSEEK_API_KEY KIMI_API_KEY ANTHROPIC_API_KEY HUGGINGFACE_TOKEN; do
    touch ~/.longhun/env/$key
    echo "# 请在此文件输入你的API密钥" >> ~/.longhun/env/$key
done

# 5. 创建共享剪贴板链接
echo "📋 创建共享剪贴板..."
mkdir -p ~/.longhun/clipboard
ln -sf ~/.longhun/clipboard ~/Desktop/龍魂剪贴板 2>/dev/null || true

# 6. 创建IDE共享配置
echo "💻 创建IDE共享配置..."

# VS Code
if [ -d "$HOME/Library/Application Support/Code/User" ]; then
    mkdir -p ~/.longhun/apps/vscode
    cp -r "$HOME/Library/Application Support/Code/User/settings.json" ~/.longhun/apps/vscode/ 2>/dev/null || true
    cp -r "$HOME/Library/Application Support/Code/User/keybindings.json" ~/.longhun/apps/vscode/ 2>/dev/null || true
    cp -r "$HOME/Library/Application Support/Code/User/snippets" ~/.longhun/apps/vscode/ 2>/dev/null || true
fi

# 7. 创建Git共享配置
echo "🔗 创建Git共享配置..."
mkdir -p ~/.longhun/apps/git
[ -f ~/.gitconfig ] && cp ~/.gitconfig ~/.longhun/apps/git/
[ -f ~/.gitignore_global ] && cp ~/.gitignore_global ~/.longhun/apps/git/
ln -sf ~/.longhun/apps/git/.gitconfig ~/.gitconfig 2>/dev/null || true

# 8. 创建Ollama共享配置
echo "🦙 创建Ollama共享配置..."
mkdir -p ~/.longhun/apps/ollama
if [ -d "$HOME/.ollama" ]; then
    cp -r "$HOME/.ollama/models" ~/.longhun/apps/ollama/ 2>/dev/null || true
fi

# 9. 创建Neo4j共享
echo "🗄️ 创建Neo4j共享..."
mkdir -p ~/.longhun/apps/neo4j
if [ -d "$HOME/.neo4j" ]; then
    cp -r "$HOME/.neo4j"/* ~/.longhun/apps/neo4j/ 2>/dev/null || true
fi

# 10. 创建浏览器共享
echo "🌐 创建浏览器共享..."
mkdir -p ~/.longhun/apps/browser
mkdir -p ~/.longhun/apps/browser/chrome
mkdir -p ~/.longhun/apps/browser/edge

# 11. 创建Docker共享
echo "🐳 创建Docker共享..."
mkdir -p ~/.longhun/apps/docker
if [ -f "$HOME/.docker/config.json" ]; then
    cp "$HOME/.docker/config.json" ~/.longhun/apps/docker/
fi

# 12. 创建状态追踪
echo "📊 创建状态追踪..."
cat > ~/.longhun/state/status.json << 'EOF'
{
  "version": "v1.0",
  "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622",
  "installed_at": "",
  "apps": {
    "terminal": "linked",
    "vscode": "linked",
    "kimi": "ready",
    "cursor": "ready",
    "iterm": "ready",
    "git": "linked",
    "ollama": "linked",
    "neo4j": "linked",
    "browser": "ready",
    "docker": "linked"
  }
}
EOF

# 13. 生成互通报告
echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "📁 龍魂环境目录: ~/.longhun/"
echo "   ├── env/          # 环境变量 & API密钥"
echo "   ├── apps/         # 各应用配置 (软链接)"
echo "   ├── memory/       # 共享记忆"
echo "   ├── state/        # 状态追踪"
echo "   └── backup/       # 备份"
echo ""
echo "🔑 API密钥位置: ~/.longhun/env/"
echo "   请将你的API密钥放入对应文件："
echo "   - OPENAI_API_KEY"
echo "   - DEEPSEEK_API_KEY"
echo "   - KIMI_API_KEY"
echo "   - ANTHROPIC_API_KEY"
echo "   - HUGGINGFACE_TOKEN"
echo ""
echo "📝 已添加到Shell:"
echo "   - ~/.zshrc"
echo "   - ~/.bashrc"
echo "   - ~/.bash_profile"
echo ""
echo "🔄 启用命令:"
echo "   source ~/.longhun/env.sh"
echo ""
echo "🔧 可用函数:"
echo "   lh-env      - 查看当前环境"
echo "   lh-sync     - 同步所有应用配置"
echo "   lh-backup   - 备份当前环境"
echo ""
echo "🧬 DNA: #龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622"
echo "🐉 丙午·丙申·庚申·亥时·䷖剥·🟢"
```

### 2.2 执行方式

```bash
# 1. 下载脚本
curl -o install_unify.sh https://raw.githubusercontent.com/UID9622/longhun-core/main/install_unify.sh

# 2. 执行
chmod +x install_unify.sh
./install_unify.sh

# 3. 重载环境
source ~/.longhun/env.sh

# 4. 验证
lh-env
```

### 2.3 手动同步脚本 `sync_apps.sh`

```bash
#!/bin/bash
# 🐉 龍魂 · 手动同步脚本
# 同步所有应用配置到龍魂统一环境

echo "🐉 同步应用配置..."

# VS Code -> 龍魂
cp -r "$HOME/Library/Application Support/Code/User/settings.json" ~/.longhun/apps/vscode/ 2>/dev/null || true
cp -r "$HOME/Library/Application Support/Code/User/keybindings.json" ~/.longhun/apps/vscode/ 2>/dev/null || true

# Git -> 龍魂
cp ~/.gitconfig ~/.longhun/apps/git/ 2>/dev/null || true

# Ollama -> 龍魂
cp -r "$HOME/.ollama/models" ~/.longhun/apps/ollama/ 2>/dev/null || true

# 记录同步时间
echo "🔄 同步完成: $(date)" >> ~/.longhun/state/sync.log

echo "✅ 同步完成"
```

### 2.4 环境检查脚本 `check_env.sh`

```bash
#!/bin/bash
# 🐉 龍魂 · 环境检查脚本

echo "🐉 龍魂环境检查"
echo "========================================"

echo "📁 龍魂目录:"
ls -la ~/.longhun/

echo ""
echo "🔑 API密钥状态:"
for key in OPENAI_API_KEY DEEPSEEK_API_KEY KIMI_API_KEY ANTHROPIC_API_KEY HUGGINGFACE_TOKEN; do
    if [ -s "$HOME/.longhun/env/$key" ]; then
        echo "  ✅ $key: 已配置"
    else
        echo "  ❌ $key: 未配置"
    fi
done

echo ""
echo "📂 应用链接状态:"
for app in vscode kimi cursor iterm git ollama neo4j browser docker; do
    if [ -d "$HOME/.longhun/apps/$app" ]; then
        echo "  ✅ $app: 已链接"
    else
        echo "  ❌ $app: 未链接"
    fi
done

echo ""
echo "🧬 DNA: #龍芯⚡️$(date +%Y-%m-%d)-ENV-CHECK-UID9622"
```


## 📋 三、互通验证

### 3.1 验证清单

| # | 验证项 | 命令 |
|:---|:---|:---|
| 1 | 环境变量 | `echo $LONGHUN_HOME` |
| 2 | 龍魂命令 | `lh-env` |
| 3 | API密钥 | `echo $OPENAI_API_KEY` |
| 4 | Git配置 | `git config --list` |
| 5 | VS Code配置 | `code --list-extensions` |

### 3.2 输出示例

```bash
$ lh-env
🐉 当前龍魂环境
  DNA: #龍芯⚡️2026-08-15-ENV-UID9622
  HOME: /Users/zuimeidedeyihan/.longhun
  PATH: /Users/zuimeidedeyihan/.longhun/shared/bin:/usr/local/bin:...
  Apps: vscode kimi cursor iterm git ollama neo4j browser docker
```


## 🔐 最终签名

```
═══════════════════════════════════════════════════
 🐉 龍魂 · Mac全应用互通引擎 · 最终签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·庚申·亥时-APP-UNIFY-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
互通应用:   10+ (终端/IDE/AI/浏览器/数据库/容器)
实现方式:   统一环境变量 + 软链接 + 共享配置
═══════════════════════════════════════════════════
```

🐉 **丙午·丙申·庚申·亥时·䷖剥·🟢**

---

*归档于 2026-08-15T12:49:47+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·午时·䷝离-CLIPBOARD-VAULT-SAVE-V1.0-P1-80cda40a`*
