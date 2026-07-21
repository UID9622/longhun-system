#!/usr/bin/env bash
# 🐉 龍魂操作台 MVP v1.1 启动脚本
# DNA:#龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-LAUNCHER-FILE1-v1.0

set -e

cd "$(dirname "$0")"
echo "🐉 启动龍魂操作台 MVP v1.1"
echo "=================================================="

# 可选：安装依赖
if [ "$1" == "--install" ]; then
    echo "📦 安装依赖..."
    pip3 install -r requirements.txt
fi

echo "🌐 访问地址："
echo "   操作台 UI : http://127.0.0.1:9622/static/index.html"
echo "   API 根节点 : http://127.0.0.1:9622/"
echo "   健康检查  : http://127.0.0.1:9622/api/health"
echo ""
echo "🚀 启动服务..."
python3 main.py
