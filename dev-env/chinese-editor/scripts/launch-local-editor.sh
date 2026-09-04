#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂中文编辑开发环境 · 本地闭环启动器
# DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-LOCAL-LAUNCHER-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 说明: 不依赖外部 VS Code / 浏览器渲染，本地直接启动
# ═══════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVENV_DIR="$(dirname "$SCRIPT_DIR")"

echo "🐉 启动龍魂中文编辑开发环境（本地闭环）"
echo "📁 根目录: $DEVENV_DIR"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.11+"
    exit 1
fi

# 以可编辑模式安装本包（依赖已在 pyproject.toml 声明）
echo "🟢 检查并安装 longhun-chinese-editor..."
pip install -q -e "$DEVENV_DIR" 2>/dev/null || true

# 启动本地中文编辑器
echo "🟢 启动本地中文编辑器..."
longhun-editor editor "$@"
