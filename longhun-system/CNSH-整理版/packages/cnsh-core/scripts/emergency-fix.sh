#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# emergency-fix.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-emergency-fix-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CNSH 紧急修复脚本 - 傻瓜式操作
# 使用方法：复制粘贴，一键执行，无需理解

echo "🔧 CNSH 紧急修复启动..."
echo "⚠️  此脚本会自动修复常见问题，无需人工判断"

# 1. 重置所有服务到安全状态
echo "🔄 步骤1: 重置服务状态..."
pkill -f "node.*server.js" 2>/dev/null || true
pkill -f "notion-monitor" 2>/dev/null || true
pkill -f "ollama" 2>/dev/null || true

# 2. 清理可能的锁定文件
echo "🧹 步骤2: 清理锁定文件..."
rm -f .notion-monitor.pid
rm -f .notion-hash

# 3. 重新安装依赖（如果需要）
echo "📦 步骤3: 检查依赖..."
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo "重新安装依赖..."
    npm install --silent
fi

# 4. 启动核心服务
echo "🚀 步骤4: 启动核心服务..."
nohup node src/server.js > server.log 2>&1 &
nohup node notion-monitor.js > notion.log 2>&1 &

# 5. 等待服务启动
echo "⏳ 步骤5: 等待服务就绪..."
sleep 5

# 6. 简单状态检查
echo "✅ 步骤6: 状态检查..."
if pgrep -f "node.*server.js" > /dev/null; then
    echo "✅ 主服务器运行正常"
else
    echo "❌ 主服务器启动失败"
fi

if pgrep -f "notion-monitor" > /dev/null; then
    echo "✅ Notion监控运行正常"
else
    echo "❌ Notion监控启动失败"
fi

echo ""
echo "🎯 紧急修复完成！"
echo "📋 如需详细管理，请运行: ./cnsh-unified.sh"
echo "🔄 如需再次修复，请重新粘贴执行此脚本"