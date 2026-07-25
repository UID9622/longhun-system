#!/bin/bash
# 龍魂系统 · 一键安装脚本
# DNA: #龍芯⚡️2026-07-05-INSTALL-v1.0
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🐉 龍魂系统安装开始..."
echo "   安装路径: $SCRIPT_DIR"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.10+"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python 版本: $PY_VERSION"

# 检查 Python 版本 >= 3.10
PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PY_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    echo "❌ Python 版本过低，需要 3.10+"
    exit 1
fi

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ 虚拟环境已创建"
fi

# 安装依赖
if [ -f "requirements.txt" ]; then
    echo "📦 安装依赖（requirements.txt）..."
    .venv/bin/pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    echo "📦 安装依赖（pyproject.toml）..."
    .venv/bin/pip install -e .
else
    echo "⚠️  未找到 requirements.txt 或 pyproject.toml，跳过依赖安装"
fi

# 确保 bin/lh 可执行
chmod +x bin/lh

# 可选：将 bin/ 加入 PATH（通过 ~/.zshrc 或 ~/.bashrc）
SHELL_RC=""
if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ] && ! grep -q "LONGHUN_ROOT" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# 龍魂系统路径" >> "$SHELL_RC"
    echo "export LONGHUN_ROOT=\"$SCRIPT_DIR\"" >> "$SHELL_RC"
    echo "export PATH=\"\$LONGHUN_ROOT/bin:\$PATH\"" >> "$SHELL_RC"
    echo "✅ 已添加环境变量到 $SHELL_RC"
    echo "   请运行: source $SHELL_RC"
fi

echo ""
echo "✅ 安装完成"
echo ""
echo "🚀 启动系统:"
echo "   python3 bin/龍魂体系v5-一键启动.py"
echo "   或: lh status"
echo ""
echo "📖 快速入门: cat QUICKSTART.md"
echo "🤝 参与贡献: cat CONTRIBUTING.md"
echo "🛡️  行为准则: cat CODE_OF_CONDUCT.md"
