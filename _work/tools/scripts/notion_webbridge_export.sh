#!/bin/bash
# 龍魂 Notion 自动导出脚本 (webbridge版)
# DNA: #龍芯⚡️2026-05-24-NOTION-WEBBRIDGE-EXPORT-v1.0
# 用途: 一键导出所有Notion公开页面到Git

set -e

NOTION_PAGES=(
    "DNA:https://www.notion.so/uid9622/DNA-34d7125a9c9f81d2be91d1e3e3be34eb"
    "BAOBAO-COLLAB-v1:https://www.notion.so/uid9622/UID9622-24618c23ac3247a19e652de6ab09f82c"
    "FLOW-DECISION-v3:https://www.notion.so/uid9622/UID9622-3427125a9c9f80449e88f4f2170b7940"
    "AI-COLLABORATION:https://www.notion.so/uid9622/AI-868fec34e5a24e7e829dc5851a75f6b7"
    "SYSTEMS-v1:https://www.notion.so/uid9622/UID9622-v1-0-33d7125a9c9f81818d40de9b63c86203"
    "UNIFIED-FRAMEWORK:https://www.notion.so/uid9622/b35faf462bc042aa9de5192520180728"
)

SYNC_DIR="$HOME/longhun-system/notion_sync"
EXPORT_DIR="$SYNC_DIR/latest"
LONGHUN_ROOT="$HOME/longhun-system"

echo "========================================="
echo "🐉 龍魂 Notion 自动导出"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S CST')"
echo "========================================="

# 创建目录
mkdir -p "$EXPORT_DIR"

echo "✅ 目录就绪: $SYNC_DIR"
echo ""
echo "📌 待导出页面:"
for entry in "${NOTION_PAGES[@]}"; do
    name="${entry%%:*}"
    echo "   - $name"
done

echo ""
echo "⚠️  注意: 当前还需要手动操作"
echo "========================================="
echo ""
echo "📝 导出步骤:"
echo "   1. 打开 Notion 页面"
echo "   2. 右上角 '⋯' → 'Export' → 'Markdown & CSV'"
echo "   3. 选择: 'Markdown & CSV'"
echo "   4. 下载后，文件应该在 ~/Downloads"
echo "   5. 移动到: $EXPORT_DIR"
echo "   6. 重命名为对应的 page_name.md"
echo ""
echo "例如:"
echo "   mv ~/Downloads/DNA.md $EXPORT_DIR/DNA.md"
echo "   mv ~/Downloads/UID9622\ 24618c23ac3247a19e652de6ab09f82c.md $EXPORT_DIR/BAOBAO-COLLAB-v1.md"
echo ""
echo "然后运行:"
echo "   python3 $LONGHUN_ROOT/scripts/notion_auto_sync.py"
echo ""
echo "========================================="

# 检查文件
file_count=$(find "$EXPORT_DIR" -name "*.md" 2>/dev/null | wc -l)
echo "📊 当前导出文件: $file_count 个"

if [ $file_count -gt 0 ]; then
    echo ""
    echo "✅ 检测到markdown文件，运行同步..."
    python3 "$LONGHUN_ROOT/scripts/notion_auto_sync.py"
else
    echo "⚠️  还没有导出文件"
fi
