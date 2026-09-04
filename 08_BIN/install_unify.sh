#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · Mac全应用互通引擎 v2.0 · 一键安装
# DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-INSTALL-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: bash bin/install_unify.sh

set -e

LONGHUN_SYSTEM="${HOME}/longhun-system"
UNIFY_ENGINE="${LONGHUN_SYSTEM}/08_BIN/lh_unify.py"
LONGHUN_HOME="${HOME}/.longhun"

echo "🐉 龍魂 · Mac全应用互通引擎 v2.0"
echo "========================================"
echo "DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-APP-UNIFY-v2.0-UID9622"
echo "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo ""

# 1. 检测Python3
echo "📦 检测Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装: brew install python3"
    exit 1
fi
echo "   ✅ Python3: $(python3 --version)"

# 2. 定位核心引擎
echo "📥 定位核心引擎..."
if [ ! -f "${UNIFY_ENGINE}" ]; then
    echo "❌ 未找到核心引擎: ${UNIFY_ENGINE}"
    echo "   （引擎应位于 longhun-system/08_BIN/lh_unify.py）"
    exit 1
fi
echo "   ✅ 引擎: ${UNIFY_ENGINE}"

# 3. 执行安装（引擎自复制到 ~/.longhun/apps/python/）
echo "🚀 执行安装..."
python3 "${UNIFY_ENGINE}" --install

# 4. 添加到Shell配置
echo "📝 添加到Shell配置..."
SHELL_CONFIG="${HOME}/.zshrc"
if [ -f "${HOME}/.bashrc" ]; then
    SHELL_CONFIG="${HOME}/.bashrc"
fi
if [ -f "${HOME}/.bash_profile" ]; then
    SHELL_CONFIG="${HOME}/.bash_profile"
fi

LINE="source ~/.longhun/env.sh"
if ! grep -q "$LINE" "$SHELL_CONFIG" 2>/dev/null; then
    echo "$LINE" >> "$SHELL_CONFIG"
    echo "   ✅ 已添加到 $SHELL_CONFIG"
else
    echo "   ⏭️ 已存在 $SHELL_CONFIG"
fi

echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "📁 龍魂环境: ~/.longhun/"
echo ""
echo "🔧 可用命令:"
echo "   source ~/.longhun/env.sh   # 加载环境"
echo "   lh env                     # 查看环境"
echo "   lh sync                    # 同步配置"
echo "   lh backup                  # 备份环境"
echo "   lh status                  # 查看状态"
echo ""
echo "🧬 DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-APP-UNIFY-v2.0-UID9622"
echo "🐉丙午·亥时·䷖剥·🟢"
