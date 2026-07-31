#!/bin/bash
# 龍魂 IDE 扩展 · 智能安装脚本
# 三层降级: code CLI → CodeBuddy直装 → 手动指南
# DNA: #龍芯⚡️丙午·辛未·VSCODE-EXT-INSTALL-v3.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
EXT_IDS=(longhun-audit-tracker longhun-console longhun-model-router longhun-one-click-deploy longhun-protocol-checker)

echo "🐉 龍魂 IDE 扩展安装"
echo "====================="
echo ""

# ── L1: code CLI ──
if command -v code &>/dev/null; then
    echo "✅ code CLI 检测到，自动安装..."
    echo ""
    echo "[1/3] 卸载旧版..."
    for ext in "${EXT_IDS[@]}"; do
        code --list-extensions 2>/dev/null | grep -q "uid9622.$ext" && \
            code --uninstall-extension "uid9622.$ext" 2>/dev/null && echo "  卸: $ext" || true
    done
    echo ""
    echo "[2/3] 安装新版..."
    for vsix in "$DIST_DIR"/longhun-*.vsix; do
        code --install-extension "$vsix" 2>&1 && echo "  装: $(basename $vsix)"
    done
    echo ""
    echo "[3/3] 验证..."
    code --list-extensions 2>/dev/null | grep uid9622 | sort
    echo ""
    echo "✅ 完成！Cmd+Shift+P → 输入「龍魂」验证。"
    exit 0
fi

# ── L2: CodeBuddy 目录直装 ──
CB_EXT_DIR="$HOME/.codebuddycn/extensions"
if [ -d "$CB_EXT_DIR" ]; then
    echo "✅ 检测到 CodeBuddy 扩展目录，直接安装..."
    echo ""
    for vsix in "$DIST_DIR"/longhun-*.vsix; do
        vsix_name=$(basename "$vsix")
        ext_name="uid9622.$(echo "$vsix_name" | sed 's/-1.0.0.vsix//')-1.0.0"
        ext_dir="$CB_EXT_DIR/$ext_name"
        echo "  📦 $vsix_name"
        rm -rf "$ext_dir"
        mkdir -p "$ext_dir"
        python3 -c "
import zipfile, os, sys
vsix = '$vsix'
target = '$ext_dir'
with zipfile.ZipFile(vsix, 'r') as z:
    for f in z.namelist():
        if f.startswith('extension/'):
            out = target + '/' + f[len('extension/'):]
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, 'wb') as w:
                w.write(z.read(f))
print('    ✅ 已安装')
"
    done
    echo ""
    echo "=== 验证 ==="
    for d in "$CB_EXT_DIR"/uid9622.longhun-*; do
        name=$(basename "$d")
        has_icon=$(python3 -c "import os; print('✅' if os.path.exists('$d/icon.png') else '❌')")
        has_readme=$(python3 -c "import os; print('✅' if os.path.exists('$d/README.md') else '❌')")
        echo "  $name  icon=$has_icon  readme=$has_readme"
    done
    echo ""
    echo "✅ 5个扩展已安装到 CodeBuddy！"
    echo "   Cmd+Shift+X 查看扩展面板"
    echo "   Cmd+Shift+P → 输入「龍魂」使用命令"
    exit 0
fi

# ── L3: 手动指南 ──
echo "⚠️  未找到 code CLI 或 CodeBuddy 目录"
echo ""
echo "   手动安装：Cmd+Shift+X → ... → 从 VSIX 安装"
echo "   路径：$DIST_DIR"
echo ""
open "$DIST_DIR" 2>/dev/null
