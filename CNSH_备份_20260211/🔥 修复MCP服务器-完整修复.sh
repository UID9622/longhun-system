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

# 4. 创建 DragonSoul 目录和数据库
echo "📋 创建 DragonSoul 目录..."
mkdir -p /Users/zuimeidedeyihan/DragonSoul
touch /Users/zuimeidedeyihan/DragonSoul/database.db
echo "✅ DragonSoul 目录创建完成"

# 5. 测试 MCP 服务器
echo "📋 测试 MCP 服务器连接..."
echo "测试 git 服务器..."
npx -y @modelcontextprotocol/server-git --help 2>&1 | head -n 5

echo ""
echo "测试 shell 服务器..."
npx -y @modelcontextprotocol/server-shell --help 2>&1 | head -n 5

echo ""
echo "测试 fetch 服务器..."
npx -y @modelcontextprotocol/server-fetch --help 2>&1 | head -n 5

# 6. 完成
echo ""
echo "🎉 MCP 服务器修复完成！"
echo ""
echo "📋 后续步骤:"
echo "1. 重启 Claude Desktop 应用"
echo "2. 检查 MCP 服务器连接状态"
echo "3. 如仍有问题，请查看日志"
