> #龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-DRAGONSOULPACK-INSTALL-v1.0

#!/bin/bash
# DragonSoulPack 一键安装脚本
# 支持：macOS / Linux (含 openEuler / 麒麟 / 统信)
# 用法：bash scripts/install.sh

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "🐉 DragonSoulPack 安装目录：$ROOT_DIR"

# 1. 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️ 未检测到 Node.js，请手动安装 >= 18.0"
    exit 1
fi

# 2. 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "⚠️ 未检测到 python3，请手动安装 >= 3.10"
    exit 1
fi

# 3. 安装 CNSH 编译器依赖
if [ -d "$ROOT_DIR/CNSH编译器" ]; then
    echo "📦 安装 CNSH 编译器..."
    cd "$ROOT_DIR/CNSH编译器"
    npm install 2>/dev/null || true
fi

# 4. 安装 VS Code 插件依赖
if [ -d "$ROOT_DIR/CNSH编辑器避坑插件" ]; then
    echo "🔌 安装 VS Code 插件依赖..."
    cd "$ROOT_DIR/CNSH编辑器避坑插件"
    npm install 2>/dev/null || true
fi

# 5. 安装本地服务器依赖
if [ -d "$ROOT_DIR/UID9622本地服务器" ]; then
    echo "🌐 安装本地服务器依赖..."
    cd "$ROOT_DIR/UID9622本地服务器"
    pip3 install -r requirements.txt 2>/dev/null || true
fi

# 6. 安装字体（macOS 示例）
if [[ "$OSTYPE" == "darwin"* ]] && [ -d "$ROOT_DIR/字体支持" ]; then
    echo "🖋️ 安装龍魂字体..."
    cp -R "$ROOT_DIR/字体支持/assets/"*.otf "$HOME/Library/Fonts/" 2>/dev/null || true
fi

echo "✅ DragonSoulPack 安装完成"
echo "👉 运行：bash scripts/start_all.sh"
