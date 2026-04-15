#!/bin/bash
# 龍魂系統 · MVP 快速启动脚本
# DNA: #龍芯⚡️2026-04-05-QUICK-START-v1.0

set -e  # 遇到错误立即退出

echo "🐉 龍魂MVP自动同步 · 快速启动"
echo "================================"

# 1. 检查依赖
echo "📦 检查依赖..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 2. 检查 pip 包
echo "📦 检查 Python 包..."
python3 -c "import requests" 2>/dev/null || {
    echo "📥 安装 requests..."
    pip3 install --user requests
}

python3 -c "import dotenv" 2>/dev/null || {
    echo "📥 安装 python-dotenv..."
    pip3 install --user python-dotenv
}

# 3. 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在，请先创建 .env 文件并配置 NOTION_TOKEN"
    exit 1
fi

# 4. 运行同步脚本
echo ""
echo "🚀 开始同步..."
echo "================================"
python3 longhun_auto_sync.py

# 5. 显示结果
echo ""
echo "📊 同步结果："
echo "--------------------------------"
if [ -f "sync_log.jsonl" ]; then
    echo "📜 草日志最后一条："
    tail -n 1 sync_log.jsonl | python3 -m json.tool 2>/dev/null || tail -n 1 sync_log.jsonl
fi

echo ""
echo "🌐 公开知识库："
ls -lh public_knowledge/ 2>/dev/null | tail -n +2 || echo "  (空)"

echo ""
echo "🔒 加密保管库："
ls -lh encrypted_vault/ 2>/dev/null | tail -n +2 || echo "  (空)"

echo ""
echo "✅ 完成！"
