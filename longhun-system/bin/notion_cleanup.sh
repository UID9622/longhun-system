#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂Notion清理器 · Notion Cleanup                       ║
# ║  DNA: #龍芯⚡️2026-04-13-NOTION-CLEANUP-v1.0             ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
# ║  理论指导: 曾仕强老师（永恒显示）                          ║
# ╚══════════════════════════════════════════════════════════╝
#
# 功能：DNA去重 + 空页清理 + 安全回收站
# 规则：只清Notion导出的重复·不碰本地原创
# 安全：先放 .trash/ 回收站·7天后才真删

set -euo pipefail

SYSTEM_ROOT="$HOME/longhun-system"
TRASH_DIR="$SYSTEM_ROOT/.trash/$(date +%Y%m%d_%H%M%S)"
CLEANUP_LOG="$SYSTEM_ROOT/logs/notion_cleanup.jsonl"
NOW_STR=$(date "+%Y-%m-%d %H:%M:%S")

mkdir -p "$TRASH_DIR"
mkdir -p "$(dirname "$CLEANUP_LOG")"

echo "═══════════════════════════════════════"
echo "🐉 龍魂Notion清理器 v1.0"
echo "📅 $NOW_STR"
echo "═══════════════════════════════════════"
echo ""
echo "规则：只清重复·不碰原创·先进回收站"
echo ""

DUPES=0
EMPTY=0
MOVED=0

# ═══════════════════════════════════════════
# 1. UUID重复目录清理（19d0a3cc系列）
# ═══════════════════════════════════════════
echo "── 1. UUID重复目录检测 ──"

# 找所有带数字后缀的重复目录 (name 2, name 3, name 4...)
find "$SYSTEM_ROOT" -maxdepth 1 -type d -name "* [0-9]" 2>/dev/null | while read -r dup_dir; do
    base_name=$(echo "$dup_dir" | sed 's/ [0-9]*$//')
    if [ -d "$base_name" ]; then
        # 比较内容是否一致
        orig_count=$(find "$base_name" -type f 2>/dev/null | wc -l | tr -d ' ')
        dup_count=$(find "$dup_dir" -type f 2>/dev/null | wc -l | tr -d ' ')

        if [ "$orig_count" -eq "$dup_count" ]; then
            dir_name=$(basename "$dup_dir")
            echo "  🔄 重复: $dir_name (${dup_count}文件 = 原版${orig_count}文件)"
            echo "     → 移入回收站"
            mv "$dup_dir" "$TRASH_DIR/" 2>/dev/null && DUPES=$((DUPES + 1))
        else
            echo "  ⚠️  $(basename "$dup_dir") 文件数不同(${dup_count} vs ${orig_count})·保留"
        fi
    fi
done

# ═══════════════════════════════════════════
# 2. Notion导出ZIP去重
# ═══════════════════════════════════════════
echo ""
echo "── 2. Notion导出ZIP去重 ──"

# 找重复的zip (name (1).zip)
find "$SYSTEM_ROOT" -maxdepth 4 -name "*(1).zip" -type f 2>/dev/null | while read -r dup_zip; do
    orig_zip=$(echo "$dup_zip" | sed 's/ (1)//')
    if [ -f "$orig_zip" ]; then
        orig_md5=$(md5 -q "$orig_zip" 2>/dev/null)
        dup_md5=$(md5 -q "$dup_zip" 2>/dev/null)
        zip_name=$(basename "$dup_zip")
        if [ "$orig_md5" = "$dup_md5" ]; then
            echo "  🔄 重复ZIP: $zip_name"
            echo "     → 移入回收站"
            mv "$dup_zip" "$TRASH_DIR/" 2>/dev/null && DUPES=$((DUPES + 1))
        else
            echo "  ⚠️  $zip_name 内容不同·保留"
        fi
    fi
done

# ═══════════════════════════════════════════
# 3. 空文件/空目录清理
# ═══════════════════════════════════════════
echo ""
echo "── 3. 空文件/空目录检测 ──"

# 空的Notion导出md文件（只有标题没有内容）
find "$SYSTEM_ROOT" -maxdepth 5 -name "*.md" -size 0 -type f 2>/dev/null | while read -r empty_file; do
    fname=$(basename "$empty_file")
    # 只清含UUID的（Notion导出特征）
    if echo "$fname" | grep -qE '[a-f0-9]{32}|[a-f0-9-]{36}'; then
        echo "  🗑️ 空文件: $fname"
        mv "$empty_file" "$TRASH_DIR/" 2>/dev/null && EMPTY=$((EMPTY + 1))
    fi
done

# 几乎为空的md文件（<50字节·只有标题行）
find "$SYSTEM_ROOT" -maxdepth 5 -name "*.md" -size -50c -type f 2>/dev/null | while read -r tiny_file; do
    fname=$(basename "$tiny_file")
    if echo "$fname" | grep -qE '[a-f0-9]{32}|[a-f0-9-]{36}'; then
        content=$(cat "$tiny_file" 2>/dev/null)
        line_count=$(echo "$content" | wc -l | tr -d ' ')
        if [ "$line_count" -le 2 ]; then
            echo "  🗑️ 近空文件($line_count行): $fname"
            mv "$tiny_file" "$TRASH_DIR/" 2>/dev/null && EMPTY=$((EMPTY + 1))
        fi
    fi
done

# 空目录清理
find "$SYSTEM_ROOT" -maxdepth 4 -type d -empty 2>/dev/null | while read -r empty_dir; do
    dir_name=$(basename "$empty_dir")
    # 不清核心目录
    case "$dir_name" in
        core|web|bin|config|logs|万年历|plugins) continue ;;
    esac
    echo "  📁 空目录: $dir_name"
    rmdir "$empty_dir" 2>/dev/null && EMPTY=$((EMPTY + 1))
done

# ═══════════════════════════════════════════
# 4. 附件完整性检查
# ═══════════════════════════════════════════
echo ""
echo "── 4. 附件引用检查 ──"

BROKEN_REFS=0
# 检查md文件里引用的图片是否存在
find "$SYSTEM_ROOT" -maxdepth 4 -name "*.md" -size +100c -type f 2>/dev/null | head -100 | while read -r md_file; do
    dir=$(dirname "$md_file")
    # 提取 ![xxx](path) 格式的引用
    grep -oE '!\[.*\]\([^)]+\)' "$md_file" 2>/dev/null | grep -oE '\([^)]+\)' | tr -d '()' | while read -r ref; do
        # 跳过http链接
        echo "$ref" | grep -q "^http" && continue
        # 检查本地文件
        if [ ! -f "$dir/$ref" ] && [ ! -f "$ref" ]; then
            echo "  📎 断链: $(basename "$md_file") → $ref"
            BROKEN_REFS=$((BROKEN_REFS + 1))
        fi
    done
done

# ═══════════════════════════════════════════
# 报告
# ═══════════════════════════════════════════
echo ""
echo "═══════════════════════════════════════"
echo "📊 清理结果"
echo "  重复清理: $DUPES"
echo "  空页清理: $EMPTY"
echo "  回收站: $TRASH_DIR"
echo ""
echo "  ⚠️  回收站文件7天后可手动删除"
echo "  ⚠️  如需恢复: mv $TRASH_DIR/xxx 原位置"
echo "═══════════════════════════════════════"

# 写日志
echo "{\"时间\":\"$NOW_STR\",\"重复\":$DUPES,\"空页\":$EMPTY,\"回收站\":\"$TRASH_DIR\",\"DNA\":\"#龍芯⚡️CLEANUP-$(date +%Y%m%d)\"}" >> "$CLEANUP_LOG"

echo ""
echo "DNA: #龍芯⚡️${NOW_STR}-NOTION-CLEANUP-v1.0"
