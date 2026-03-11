# MCP服务器连接问题诊断与修复指南

**DNA追溯码**: `#ZHUGEXIN⚡️2026-02-11-MCP-SERVER-FIX-v1.0`
**创建者**: 龙芯北辰·UID9622（诸葛鑫/Lucky）
**创建日期**: 2026-02-11

---

## 🎯 问题概述

**当前错误信息**:
```
Could not attach to MCP server git
MCP sqlite: Server disconnected
MCP git: Server disconnected
Could not attach to MCP server shell
Could not attach to MCP server fetch
```

**问题分析**:
所有MCP服务器都使用 `npx` 命令启动，但连接失败，可能原因:
1. Node.js/npm 未安装或版本过低
2. MCP服务器包下载失败或网络问题
3. 配置文件中的路径不存在（如 DragonSoul 目录）
4. 环境变量或权限问题

---

## 🔍 诊断步骤

### 步骤1: 检查 Node.js 和 npm 是否安装

```bash
# 检查 Node.js 版本（需要 v18+）
node --version

# 检查 npm 版本（需要 v9+）
npm --version

# 如果未安装或版本过低，请升级:
# macOS: brew install node
# 或从官网下载: https://nodejs.org/
```

### 步骤2: 检查 DragonSoul 目录是否存在

```bash
# 检查配置中引用的目录
ls -la /Users/zuimeidedeyihan/DragonSoul

# 如果不存在，需要创建:
mkdir -p /Users/zuimeidedeyihan/DragonSoul
```

### 步骤3: 手动测试 MCP 服务器

```bash
# 测试 filesystem MCP 服务器
npx -y @modelcontextprotocol/server-filesystem /Users/zuimeidedeyihan/DragonSoul

# 测试 git MCP 服务器
npx -y @modelcontextprotocol/server-git

# 测试 sqlite MCP 服务器
npx -y @modelcontextprotocol/server-sqlite --db-path /Users/zuimeidedeyihan/DragonSoul/database.db

# 测试 shell MCP 服务器
npx -y @modelcontextprotocol/server-shell

# 测试 fetch MCP 服务器
npx -y @modelcontextprotocol/server-fetch
```

### 步骤4: 检查网络连接

```bash
# 测试 npm 源连接
ping registry.npmjs.org

# 如果连接失败，切换到国内镜像:
npm config set registry https://registry.npmmirror.com
npm config set registry https://mirrors.cloud.tencent.com/npm/
```

---

## 🛠️ 修复方案

### 方案A: 创建必需目录（最简单）

```bash
#!/bin/bash
# 一键创建 DragonSoul 目录和空数据库

# 创建目录
mkdir -p /Users/zuimeidedeyihan/DragonSoul

# 创建空数据库（可选）
touch /Users/zuimeidedeyihan/DragonSoul/database.db

# 验证
ls -la /Users/zuimeidedeyihan/DragonSoul

echo "✅ DragonSoul 目录创建完成！"
```

保存为 `🔥 修复MCP服务器-创建目录.sh` 并运行:

```bash
chmod +x "🔥 修复MCP服务器-创建目录.sh"
bash "🔥 修复MCP服务器-创建目录.sh"
```

---

### 方案B: 简化 MCP 配置（推荐）

如果某些服务器不需要，可以暂时禁用:

修改 `.claude.json`:

```json
{
  "globalShortcut": "CommandOrControl+Shift+.",
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "shell": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-shell"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  },
  "preferences": {
    "quickEntryDictationShortcut": "capslock"
  }
}
```

**说明**: 
- 移除了 `filesystem`（因为 DragonSoul 目录不存在）
- 移除了 `sqlite`（因为数据库文件不存在）
- 移除了 `brave-search` 和 `github`（因为需要 API Key）

---

### 方案C: 使用本地安装（避免网络问题）

```bash
#!/bin/bash
# 本地安装所有 MCP 服务器

# 安装到本地项目
cd "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"

# 创建 package.json（如果不存在）
cat > package.json << 'EOF'
{
  "name": "cnsh-mcp-servers",
  "version": "1.0.0",
  "description": "CNSH MCP Servers",
  "scripts": {
    "start": "echo 'MCP servers installed locally'"
  },
  "dependencies": {
    "@modelcontextprotocol/server-git": "^1.0.0",
    "@modelcontextprotocol/server-shell": "^1.0.0",
    "@modelcontextprotocol/server-fetch": "^1.0.0"
  }
}
EOF

# 安装依赖
npm install

echo "✅ MCP 服务器已本地安装！"
echo "📝 请更新 .claude.json 使用本地路径"
```

更新后的 `.claude.json`:

```json
{
  "globalShortcut": "CommandOrControl+Shift+.",
  "mcpServers": {
    "git": {
      "command": "node",
      "args": ["node_modules/@modelcontextprotocol/server-git/dist/index.js"]
    },
    "shell": {
      "command": "node",
      "args": ["node_modules/@modelcontextprotocol/server-shell/dist/index.js"]
    },
    "fetch": {
      "command": "node",
      "args": ["node_modules/@modelcontextprotocol/server-fetch/dist/index.js"]
    }
  },
  "preferences": {
    "quickEntryDictationShortcut": "capslock"
  }
}
```

---

### 方案D: 网络环境优化（如果方案A/B都不行）

```bash
#!/bin/bash
# 网络环境优化脚本

# 1. 切换到腾讯云镜像（速度快，稳定）
npm config set registry https://mirrors.cloud.tencent.com/npm/

# 2. 验证镜像
npm config get registry

# 3. 测试连接
npm ping

# 4. 清理 npm 缓存
npm cache clean --force

# 5. 设置 npx 镜像（可选）
npm config set npx_config_registry https://mirrors.cloud.tencent.com/npm/

echo "✅ 网络环境优化完成！"
```

---

## 📋 完整修复脚本（一键执行）

将以下脚本保存为 `🔥 修复MCP服务器-完整修复.sh`:

```bash
#!/bin/bash

echo "🔧 开始修复 MCP 服务器连接问题..."

# 1. 检查 Node.js
echo "📋 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装！请先安装 Node.js: https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js 版本: $(node --version)"

# 2. 检查 npm
echo "📋 检查 npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装！"
    exit 1
fi
echo "✅ npm 版本: $(npm --version)"

# 3. 切换到国内镜像
echo "📋 配置 npm 镜像..."
npm config set registry https://mirrors.cloud.tencent.com/npm/
npm config set npx_config_registry https://mirrors.cloud.tencent.com/npm/
echo "✅ npm 镜像已配置: $(npm config get registry)"

# 4. 创建 DragonSoul 目录
echo "📋 创建 DragonSoul 目录..."
mkdir -p /Users/zuimeidedeyihan/DragonSoul
touch /Users/zuimeidedeyihan/DragonSoul/database.db
echo "✅ DragonSoul 目录创建完成"

# 5. 测试 MCP 服务器
echo "📋 测试 MCP 服务器连接..."
echo "测试 git 服务器..."
timeout 5 npx -y @modelcontextprotocol/server-git --help 2>&1 | head -n 5

echo ""
echo "测试 shell 服务器..."
timeout 5 npx -y @modelcontextprotocol/server-shell --help 2>&1 | head -n 5

echo ""
echo "测试 fetch 服务器..."
timeout 5 npx -y @modelcontextprotocol/server-fetch --help 2>&1 | head -n 5

# 6. 生成简化配置
echo "📋 生成简化版 .claude.json..."
BACKUP_FILE=".claude.json.backup.$(date +%Y%m%d_%H%M%S)"
cp .claude.json "$BACKUP_FILE"

cat > .claude.json << 'EOF'
{
  "globalShortcut": "CommandOrControl+Shift+.",
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "shell": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-shell"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  },
  "preferences": {
    "quickEntryDictationShortcut": "capslock"
  }
}
EOF

echo "✅ .claude.json 已更新（备份: $BACKUP_FILE）"

# 7. 完成
echo ""
echo "🎉 MCP 服务器修复完成！"
echo ""
echo "📋 后续步骤:"
echo "1. 重启 Claude Desktop 应用"
echo "2. 检查 MCP 服务器连接状态"
echo "3. 如仍有问题，请查看日志"
echo ""
echo "🔍 备份文件位置: $BACKUP_FILE"
```

---

## 📝 执行步骤

### 快速修复（推荐）

```bash
# 1. 进入项目目录
cd "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"

# 2. 创建并执行完整修复脚本
cat > "🔥 修复MCP服务器-完整修复.sh" << 'END_OF_SCRIPT'
#!/bin/bash

echo "🔧 开始修复 MCP 服务器连接问题..."

# 1. 检查 Node.js
echo "📋 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装！请先安装 Node.js: https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js 版本: $(node --version)"

# 2. 检查 npm
echo "📋 检查 npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装！"
    exit 1
fi
echo "✅ npm 版本: $(npm --version)"

# 3. 切换到国内镜像
echo "📋 配置 npm 镜像..."
npm config set registry https://mirrors.cloud.tencent.com/npm/
npm config set npx_config_registry https://mirrors.cloud.tencent.com/npm/
echo "✅ npm 镜像已配置: $(npm config get registry)"

# 4. 创建 DragonSoul 目录
echo "📋 创建 DragonSoul 目录..."
mkdir -p /Users/zuimeidedeyihan/DragonSoul
touch /Users/zuimeidedeyihan/DragonSoul/database.db
echo "✅ DragonSoul 目录创建完成"

# 5. 测试 MCP 服务器
echo "📋 测试 MCP 服务器连接..."
echo "测试 git 服务器..."
timeout 5 npx -y @modelcontextprotocol/server-git --help 2>&1 | head -n 5

echo ""
echo "测试 shell 服务器..."
timeout 5 npx -y @modelcontextprotocol/server-shell --help 2>&1 | head -n 5

echo ""
echo "测试 fetch 服务器..."
timeout 5 npx -y @modelcontextprotocol/server-fetch --help 2>&1 | head -n 5

# 6. 生成简化配置
echo "📋 生成简化版 .claude.json..."
BACKUP_FILE=".claude.json.backup.$(date +%Y%m%d_%H%M%S)"
cp .claude.json "$BACKUP_FILE"

cat > .claude.json << 'EOF'
{
  "globalShortcut": "CommandOrControl+Shift+.",
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "shell": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-shell"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  },
  "preferences": {
    "quickEntryDictationShortcut": "capslock"
  }
}
EOF

echo "✅ .claude.json 已更新（备份: $BACKUP_FILE）"

# 7. 完成
echo ""
echo "🎉 MCP 服务器修复完成！"
echo ""
echo "📋 后续步骤:"
echo "1. 重启 Claude Desktop 应用"
echo "2. 检查 MCP 服务器连接状态"
echo "3. 如仍有问题，请查看日志"
echo ""
echo "🔍 备份文件位置: $BACKUP_FILE"
END_OF_SCRIPT

chmod +x "🔥 修复MCP服务器-完整修复.sh"
bash "🔥 修复MCP服务器-完整修复.sh"
```

---

## 🔧 手动修复（如果脚本失败）

如果脚本执行失败，按以下步骤手动修复:

```bash
# 1. 检查 Node.js
node --version
npm --version

# 2. 配置镜像
npm config set registry https://mirrors.cloud.tencent.com/npm/
npm config set npx_config_registry https://mirrors.cloud.tencent.com/npm/

# 3. 创建目录
mkdir -p /Users/zuimeidedeyihan/DragonSoul
touch /Users/zuimeidedeyihan/DragonSoul/database.db

# 4. 编辑 .claude.json
# 移除不需要的服务器配置，保留基础的 git, shell, fetch
```

---

## ❓ 常见问题

### Q1: Node.js 版本过低怎么办?

```bash
# 使用 Homebrew 升级
brew update
brew upgrade node

# 或从官网下载安装
# https://nodejs.org/
```

### Q2: npx 下载速度慢怎么办?

```bash
# 使用国内镜像
npm config set registry https://mirrors.cloud.tencent.com/npm/
npm config set npx_config_registry https://mirrors.cloud.tencent.com/npm/
```

### Q3: MCP 服务器连接后仍然断开?

可能原因:
- 防火墙阻止连接
- 端口冲突
- 磁盘空间不足

解决方案:
```bash
# 检查磁盘空间
df -h

# 检查防火墙（macOS）
sudo pfctl -sr | grep mcp
```

---

## 📊 验证修复结果

修复完成后，重启 Claude Desktop，检查以下内容:

✅ `git` MCP 服务器正常连接
✅ `shell` MCP 服务器正常连接
✅ `fetch` MCP 服务器正常连接

如果仍有问题，查看 Claude Desktop 日志:
```bash
# macOS 日志位置
~/Library/Logs/Claude/
```

---

## 🔐 DNA追溯码

`#ZHUGEXIN⚡️2026-02-11-MCP-SERVER-FIX-v1.0`

**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

**创建者**: 龙芯北辰·UID9622（诸葛鑫/Lucky）

**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

**技术为人民服务，不是人为技术服务** 🚀
