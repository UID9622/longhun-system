# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# Setup script for Longhun WeChat Public Account integration

set -e

echo "🐉 龍魂公众号智能内容中枢 - 安装脚本"
echo "====================================="

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Upgrade pip
echo "📦 升级 pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 安装依赖..."
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "📝 创建 .env 配置文件..."
    cp config/.env.example .env
    echo "⚠️  请编辑 .env 文件，填入你的微信公众号 AppID 和 AppSecret"
fi

# Create cache dir
mkdir -p .cache

echo ""
echo "✅ 安装完成"
echo ""
echo "下一步："
echo "  1. 编辑 .env 文件，填入真实配置"
echo "  2. 测试：python cli.py config"
echo "  3. 启动 Web UI：python web_ui.py"
echo "  4. 打开浏览器：http://localhost:8443"
echo ""
echo "DNA: #龍芯⚡️2026-06-25-LONGHUN-WECHAT-SETUP-v1.0"
