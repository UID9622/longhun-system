#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐲 龍魂记忆编辑器 · 一键安装脚本 v3.1
# DNA: #龍芯⚡️2026-08-05-INSTALL-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: MulanPSL v2

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/Desktop/龍魂系统·本地知识库"
TOOLS_DIR="$TARGET_DIR/tools"
BACKUP_DIR="$TARGET_DIR/备份"
HTML_TARGET="$HOME/Desktop/龍魂记忆编辑器_完整集成版.html"

echo "🐲 龍魂记忆编辑器 v3.1 · 天干地支版 · 安装部署"
echo "================================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.8+"
    exit 1
fi
PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python 版本: $PY_VERSION"

# 创建目录
mkdir -p "$TARGET_DIR"/{記憶,任务,語境與語義,备份,tools}
echo "✅ 知识库目录已创建"

# 检查依赖文件
for f in memory-editor.html save_memory.py sync_to_notion.py; do
    if [ ! -f "$SCRIPT_DIR/$f" ]; then
        echo "❌ 缺少文件: $f，请确保 $SCRIPT_DIR 包含完整交付包"
        exit 1
    fi
done

# 复制 HTML 文件
cp "$SCRIPT_DIR/memory-editor.html" "$HTML_TARGET"
echo "✅ Web 界面已创建: $HTML_TARGET"

# 复制 Python 脚本到 tools 目录（备份目录仅用于备份）
cp "$SCRIPT_DIR/save_memory.py" "$TOOLS_DIR/"
cp "$SCRIPT_DIR/sync_to_notion.py" "$TOOLS_DIR/"
chmod +x "$TOOLS_DIR"/*.py
echo "✅ Python 工具已安装: $TOOLS_DIR"

# 创建快速命令（避免重复添加）
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"
MARKER="# 龍魂记忆快捷命令 v3.1"

add_aliases() {
    local rcfile="$1"
    if [ -f "$rcfile" ] && ! grep -q "$MARKER" "$rcfile"; then
        cat >> "$rcfile" << EOF
$MARKER
alias lh-mem="python3 $TOOLS_DIR/save_memory.py"
alias lh-list="python3 $TOOLS_DIR/save_memory.py --list"
alias lh-search="python3 $TOOLS_DIR/save_memory.py --search"
alias lh-sync="python3 $TOOLS_DIR/sync_to_notion.py"
EOF
        echo "✅ 快捷命令已添加到 $(basename "$rcfile") (lh-mem, lh-list, lh-search, lh-sync)"
    fi
}

add_aliases "$BASHRC"
add_aliases "$ZSHRC"

echo ""
echo "================================================"
echo "🎉 安装完成！"
echo ""
echo "使用方式："
echo "  1. 双击打开: $HTML_TARGET"
echo "  2. 命令行保存: lh-mem '我的记忆内容'"
echo "  3. 列出记忆: lh-list"
echo "  4. 搜索记忆: lh-search '关键词'"
echo "  5. 同步 Notion: lh-sync"
echo ""
echo "🧬 DNA: #龍芯⚡️2026-08-05-INSTALL-UID9622"
echo "================================================"
