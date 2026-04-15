#!/bin/bash
# 龍魂系統 · MVP v2.0 快速启动脚本（六核心增强版）
# DNA: #龍芯⚡️2026-04-05-QUICK-START-v2.0

set -e  # 遇到错误立即退出

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   🐉 龍魂MVP自动同步 v2.0 - 六核心页面增强版                    ║"
echo "║                                                               ║"
echo "║   🛡️  护盾v1.3          - P0核心安全系统                       ║"
echo "║   🎛️  AI主控操作台      - P0核心控制中心                       ║"
echo "║   📊  主控操作台        - 系统总控                            ║"
echo "║   🏆  龍魂成果页        - MVP展示                             ║"
echo "║   📋  MVP规范          - 标准文档                             ║"
echo "║   💎  数字资产总库      - 资产管理                            ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"

# 1. 检查依赖
echo ""
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

# 4. 运行同步脚本 v2.0
echo ""
echo "🚀 开始同步六大核心页面..."
echo "════════════════════════════════════════════════════════════════"
python3 longhun_auto_sync_v2.py

# 5. 显示结果
echo ""
echo "📊 同步结果统计："
echo "────────────────────────────────────────────────────────────────"

if [ -f "sync_log.jsonl" ]; then
    echo ""
    echo "📜 草日志最后一条："
    echo "────────────────────────────────────────────────────────────────"
    tail -n 1 sync_log.jsonl | python3 -m json.tool 2>/dev/null || tail -n 1 sync_log.jsonl
fi

echo ""
echo "📁 文件分布："
echo "────────────────────────────────────────────────────────────────"

echo ""
echo "🛡️ 护盾专属库（超级机密）："
if [ -d "shield_vault" ]; then
    file_count=$(ls -1 shield_vault/ 2>/dev/null | wc -l)
    echo "  📂 文件数: $file_count"
    ls -lht shield_vault/ 2>/dev/null | head -n 6 || echo "  (空)"
else
    echo "  📂 (未创建)"
fi

echo ""
echo "🔒 加密保管库（机密）："
if [ -d "encrypted_vault" ]; then
    file_count=$(ls -1 encrypted_vault/ 2>/dev/null | wc -l)
    echo "  📂 文件数: $file_count"
    ls -lht encrypted_vault/ 2>/dev/null | head -n 6 || echo "  (空)"
else
    echo "  📂 (未创建)"
fi

echo ""
echo "🌐 公开知识库（内部公开）："
if [ -d "public_knowledge" ]; then
    file_count=$(ls -1 public_knowledge/ 2>/dev/null | wc -l)
    echo "  📂 文件数: $file_count"
    ls -lht public_knowledge/ 2>/dev/null | head -n 6 || echo "  (空)"
else
    echo "  📂 (未创建)"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ 完成！六核心系统同步成功！"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🐉 龍魂现世！六核齐鸣！天下无欺！"
echo ""
