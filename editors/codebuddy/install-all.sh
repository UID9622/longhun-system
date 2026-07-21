#!/bin/bash
# ============================================================
# 龍魂 CodeBuddy 扩展一键安装脚本
# 
# 用法:
#   bash install-all.sh                  # 从 GitHub Release 下载并安装
#   bash install-all.sh --local          # 从本地 dist/ 安装
#
# DNA: #龍芯⚡️丙午·辛未·ONE-CLICK-INSTALL-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ============================================================

set -e

RELEASE_URL="https://github.com/UID9622/longhun-system/releases/download/v1.0.0-extensions"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
TMP_DIR="/tmp/longhun-extensions-$$"

# 检测 CodeBuddy CN 的 code 命令
detect_code_cmd() {
    if [ -f "/Volumes/CodeBuddy CN/CodeBuddy CN.app/Contents/Resources/app/bin/code" ]; then
        echo "/Volumes/CodeBuddy CN/CodeBuddy CN.app/Contents/Resources/app/bin/code"
    elif command -v code &>/dev/null; then
        echo "code"
    else
        echo ""
    fi
}

CODE_CMD=$(detect_code_cmd)

if [ -z "$CODE_CMD" ]; then
    echo "❌ 未找到 CodeBuddy 或 VS Code，请确认已安装"
    exit 1
fi

echo "🐉 龍魂 CodeBuddy 扩展一键安装"
echo "   目标: $CODE_CMD"
echo ""

EXTENSIONS=(
    "longhun-one-click-deploy-1.0.0.vsix"
    "longhun-model-router-1.0.0.vsix"
    "longhun-audit-tracker-1.0.0.vsix"
    "longhun-protocol-checker-1.0.0.vsix"
    "longhun-console-1.0.0.vsix"
    "cnsh-syntax-2.0.0.vsix"
)

if [ "$1" = "--local" ]; then
    echo "📂 从本地 dist/ 安装..."
    SOURCE_DIR="$DIST_DIR"
else
    echo "🌐 从 GitHub Release 下载..."
    mkdir -p "$TMP_DIR"
    SOURCE_DIR="$TMP_DIR"
    for vsix in "${EXTENSIONS[@]}"; do
        echo "   下载 $vsix ..."
        curl -sSL "$RELEASE_URL/$vsix" -o "$TMP_DIR/$vsix"
    done
fi

echo ""
SUCCESS=0
FAILED=0

for vsix in "${EXTENSIONS[@]}"; do
    echo -n "  安装 $(basename "$vsix" .vsix | sed 's/-[0-9].*//') ... "
    if "$CODE_CMD" --install-extension "$SOURCE_DIR/$vsix" --force >/dev/null 2>&1; then
        echo "✅"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "❌"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "========================================"
echo "  安装完成: ✅ $SUCCESS  |  ❌ $FAILED"
echo "========================================"

# 清理临时文件
if [ "$1" != "--local" ]; then
    rm -rf "$TMP_DIR"
fi

echo ""
echo "💡 提示: 按 Cmd+Shift+P → 'Reload Window' 重新加载生效"
