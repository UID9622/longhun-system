#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂Notion深层提取器 · Deep Extractor                   ║
# ║  DNA: #龍芯⚡️2026-04-13-DEEP-EXTRACT-v1.0              ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
# ║  理论指导: 曾仕强老师（永恒显示）                          ║
# ╚══════════════════════════════════════════════════════════╝
#
# 功能：
#   1. 解压Notion导出ZIP → 展开全部内容
#   2. 深层折叠内容全展开（子页面/嵌套/toggle）
#   3. 提取关键信息生成索引
#   4. UUID文件名 → 人话文件名映射

SYSTEM_ROOT="$HOME/longhun-system"
EXTRACT_DIR="$SYSTEM_ROOT/notion-extracted"
INDEX_FILE="$SYSTEM_ROOT/config/notion_content_index.jsonl"
NOW_STR=$(date "+%Y-%m-%d %H:%M:%S")

mkdir -p "$EXTRACT_DIR"
mkdir -p "$(dirname "$INDEX_FILE")"

echo "═══════════════════════════════════════"
echo "🐉 龍魂Notion深层提取器 v1.0"
echo "📅 $NOW_STR"
echo "═══════════════════════════════════════"
echo ""

EXTRACTED=0
INDEXED=0

# ═══════════════════════════════════════════
# 1. 解压所有Notion导出ZIP
# ═══════════════════════════════════════════
echo "── 1. 解压Notion导出包 ──"

find "$SYSTEM_ROOT" -maxdepth 4 -name "*Export*.zip" -type f 2>/dev/null | while read -r zip_file; do
    zip_name=$(basename "$zip_file" .zip)
    target="$EXTRACT_DIR/$zip_name"

    if [ -d "$target" ]; then
        echo "  ⏭️  已解压: $zip_name"
        continue
    fi

    echo "  📦 解压: $zip_name"
    mkdir -p "$target"
    unzip -q -o "$zip_file" -d "$target" 2>/dev/null && {
        EXTRACTED=$((EXTRACTED + 1))
        echo "     ✅ 完成"
    } || {
        echo "     ❌ 解压失败"
        rmdir "$target" 2>/dev/null
    }
done

# ═══════════════════════════════════════════
# 2. UUID → 人话映射
# ═══════════════════════════════════════════
echo ""
echo "── 2. UUID文件名解码 ──"

# Notion导出的文件名格式：标题 UUID.md
# 提取标题部分
find "$SYSTEM_ROOT" -maxdepth 6 -name "*.md" -type f 2>/dev/null | while read -r md_file; do
    fname=$(basename "$md_file" .md)

    # 检查是否包含UUID尾巴（32位hex或36位带横线）
    if echo "$fname" | grep -qE '[a-f0-9]{32}$'; then
        # 提取标题（去掉末尾UUID）
        title=$(echo "$fname" | sed 's/ [a-f0-9]\{32\}$//')
        if [ -n "$title" ] && [ "$title" != "$fname" ]; then
            echo "{\"UUID文件\":\"$fname.md\",\"标题\":\"$title\",\"路径\":\"$md_file\",\"大小\":$(stat -f %z "$md_file" 2>/dev/null || echo 0)}" >> "$INDEX_FILE.tmp"
            INDEXED=$((INDEXED + 1))
        fi
    fi
done

# ═══════════════════════════════════════════
# 3. 深层内容提取（从md中提取关键信息）
# ═══════════════════════════════════════════
echo ""
echo "── 3. 深层内容索引 ──"

# 扫描已有的Notion导出目录
for notion_dir in "$SYSTEM_ROOT"/19d0a3cc* "$EXTRACT_DIR"/*; do
    [ ! -d "$notion_dir" ] && continue
    dir_name=$(basename "$notion_dir")

    file_count=$(find "$notion_dir" -type f 2>/dev/null | wc -l | tr -d ' ')
    md_count=$(find "$notion_dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    html_count=$(find "$notion_dir" -name "*.html" -type f 2>/dev/null | wc -l | tr -d ' ')
    csv_count=$(find "$notion_dir" -name "*.csv" -type f 2>/dev/null | wc -l | tr -d ' ')

    echo "  📁 $dir_name"
    echo "     文件: $file_count | MD: $md_count | HTML: $html_count | CSV: $csv_count"

    # 提取每个md的标题行
    find "$notion_dir" -name "*.md" -type f 2>/dev/null | head -50 | while read -r md; do
        title=$(head -1 "$md" 2>/dev/null | sed 's/^#* *//')
        if [ -n "$title" ]; then
            fsize=$(stat -f %z "$md" 2>/dev/null || echo 0)
            echo "{\"目录\":\"$dir_name\",\"文件\":\"$(basename "$md")\",\"标题\":\"$title\",\"大小\":$fsize,\"来源\":\"notion_export\"}" >> "$INDEX_FILE.tmp"
        fi
    done
done

# 去重写入索引
if [ -f "$INDEX_FILE.tmp" ]; then
    sort -u "$INDEX_FILE.tmp" > "$INDEX_FILE"
    rm -f "$INDEX_FILE.tmp"
    total_index=$(wc -l < "$INDEX_FILE" | tr -d ' ')
    echo ""
    echo "  📋 内容索引: $total_index 条"
fi

# ═══════════════════════════════════════════
# 4. e7057目录特殊处理（ChatGPT导出）
# ═══════════════════════════════════════════
echo ""
echo "── 4. 对话导出检测 ──"

for chat_dir in "$SYSTEM_ROOT"/e7057*; do
    [ ! -d "$chat_dir" ] && continue
    if [ -f "$chat_dir/conversations.json" ]; then
        conv_count=$(python3 -c "
import json
with open('$chat_dir/conversations.json') as f:
    data = json.load(f)
print(len(data))
" 2>/dev/null || echo "?")
        echo "  💬 ChatGPT导出: $conv_count 条对话"
        echo "     位置: $chat_dir"
        echo "     💡 这些对话可以用通心译重写后存入龍魂记忆"
    fi
done

# 报告
echo ""
echo "═══════════════════════════════════════"
echo "📊 提取结果"
echo "  解压ZIP: $EXTRACTED"
echo "  索引条目: $INDEXED"
echo "  内容索引: $INDEX_FILE"
echo "═══════════════════════════════════════"

echo ""
echo "DNA: #龍芯⚡️${NOW_STR}-DEEP-EXTRACT-v1.0"
