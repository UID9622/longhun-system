#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 价格透明度审计工具 · 一键安装启动脚本
# DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-PRICE-AUDIT-SETUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
PORT="${1:-8899}"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  价格透明度审计工具 v1.0 - 一键安装启动         ║"
echo "║  Price Audit Tool - Setup & Launch           ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.9+"
    echo "   macOS: brew install python3"
    echo "   Ubuntu: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION"

# 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

# 激活并安装依赖
source "$VENV_DIR/bin/activate"
echo "📦 安装依赖..."
pip install --quiet --upgrade pip
pip install --quiet -r "$SCRIPT_DIR/requirements.txt"

echo "✅ 依赖安装完成"
echo ""

# 运行测试
echo "🧪 运行检测引擎测试..."
if python3 "$SCRIPT_DIR/tests/test_detector.py"; then
    echo ""
else
    echo "⚠️  部分测试未通过，但服务仍可启动"
fi

# 启动
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  🚀 启动服务...                              ║"
echo "║                                               ║"
echo "║  仪表盘: http://localhost:$PORT/dashboard        ║"
echo "║  API文档: http://localhost:$PORT/docs          ║"
echo "║                                               ║"
echo "║  按 Ctrl+C 停止                               ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

cd "$SCRIPT_DIR"
python3 backend/app.py
