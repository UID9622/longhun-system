#!/bin/bash
# 🐉 个人开发者快速起步·30秒从零到跑起来
# 原则：零门槛·零费用·本地跑通再说
# DNA: #龍芯⚡️2026-08-31-DEV-QUICKSTART-V1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: MulanPSL v2（工程实现层）
set -e
cd "$(dirname "$0")/.."

echo "🐉 欢迎使用龍魂主权技术栈！"
echo "🎯 个人开发者版：本地免费·无需云账号·无需信用卡"
echo ""

# 检查 Python
if ! command -v python3 &>/dev/null; then
    echo "📥 请先安装 Python 3.11: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ 依赖检查通过"
echo ""

# 安装最小依赖
pip3 install flask flask-cors requests beautifulsoup4 PyYAML -q

# 启动最小化本地环境（只用 Python，不需要 Docker）
echo "🚀 启动最小化本地环境..."
mkdir -p ~/.longhun/logs

# 搜索服务
nohup python3 search-engine/search.py --server > ~/.longhun/logs/search.log 2>&1 &
SEARCH_PID=$!

# 计量服务
nohup python3 pricing/meter.py > ~/.longhun/logs/meter.log 2>&1 &
METER_PID=$!

# 配额服务
nohup python3 free-tier/quota_manager.py > ~/.longhun/logs/quota.log 2>&1 &
QUOTA_PID=$!

sleep 2

# 注册测试账号
python3 -c "
import requests, json
r = requests.post('http://localhost:8895/quota/register',
    json={'phone': '13800138000', 'nickname': '测试开发者'})
print('👤 账号注册:', r.json().get('welcome', '已注册'))
" 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  🎉 个人开发者环境启动完成！             ║"
echo "║                                          ║"
echo "║  🔍 搜索:  curl 'localhost:8890/search?q=你好'"
echo "║  💰 用量:  curl localhost:8897/meter/usage/13800138000"
echo "║  📊 配额:  curl localhost:8895/quota/status/13800138000"
echo "║                                          ║"
echo "║  每月免费：10000次API + 1000次搜索       ║"
echo "║  超出后：0.0001元/次（1分钱/100次）      ║"
echo "║  无包月！不用不花钱！                    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 运行验证
echo "🧪 运行基础验证..."
curl -s "http://localhost:8890/health" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print('🔍 搜索服务:', d.get('tricolor','🟢'), d.get('status',''))
" 2>/dev/null || echo "🔍 搜索服务: 启动中..."

curl -s "http://localhost:8897/meter/health" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print('💰 计量服务:', '🟢', d.get('status',''))
" 2>/dev/null || echo "💰 计量服务: 启动中..."

curl -s "http://localhost:8895/quota/status/13800138000" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print('👤 配额服务:', '🟢', d.get('month',''))
" 2>/dev/null || echo "👤 配额服务: 启动中..."

echo ""
echo "🧬 DNA: #龍芯⚡️$(date +%Y-%m-%d)-DEV-QUICKSTART-DONE-UID9622"
