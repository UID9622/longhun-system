##龍芯⚡️2026-06-21-TOOL-INSTALL-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/bin/bash
# 龍魂 MCP 认证桥接 · 一键安装脚本 v0.1
# DNA: #龍芯⚡️20260525|MCP-INSTALL|v0.1|e5c407ec

set -e

echo "═══════════════════════════════════════"
echo "🐉 龍魂 MCP 认证桥接 · 安装器 v0.1"
echo "═══════════════════════════════════════"
echo ""

# 1. 装依赖
echo "📦 正在安装 npm 依赖..."
npm install chrome-devtools-mcp @modelcontextprotocol/sdk 2>/dev/null || npm install chrome-devtools-mcp @modelcontextprotocol/sdk --legacy-peer-deps

# 2. 检查 .env
echo "🔐 配置环境变量..."
if [ ! -f .env ]; then
  echo "LONGHUN_GPG=A2D0092CEE2E5BA87035600924C3704A8CC26D5F" > .env
  echo "✅ 已创建 .env 并写入 GPG 指纹"
else
  if ! grep -q "LONGHUN_GPG" .env; then
    echo "LONGHUN_GPG=A2D0092CEE2E5BA87035600924C3704A8CC26D5F" >> .env
    echo "✅ 已追加 GPG 指纹到 .env"
  else
    echo "ℹ️ .env 中已有 LONGHUN_GPG"
  fi
fi

# 3. 自检
echo "🔍 自检中..."
node -e "const auth=require('./longhun-mcp-auth.json');console.log('  认证配置版本:',auth.version);console.log('  UID:',auth.owner_uid);console.log('  GPG:',auth.gpg_fingerprint);" 2>/dev/null || echo "⚠️ 自检跳过（longhun-mcp-auth.json 不在当前目录）"

echo ""
echo "═══════════════════════════════════════"
echo "✅ 安装完成"
echo "═══════════════════════════════════════"
echo ""
echo "下一步："
echo "  1. 确认 .env 里有 LONGHUN_GPG"
echo "  2. 把 cursor-prompt.md 甩给 Cursor"
echo "  3. 跑 test-gate.js 验证"
echo ""
echo "DNA: #龍芯⚡️$(date +%Y%m%d)|MCP-INSTALLED|v0.1|DONE"
