#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂自动整理器 · Auto Organizer                         ║
# ║  DNA: #龍芯⚡️2026-04-12-ORGANIZER-v1.0                  ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
# ║  理论指导: 曾仕强老师（永恒显示）                          ║
# ╚══════════════════════════════════════════════════════════╝
#
# 功能：
#   1. 读取沙箱容器 → 分类整理到主仓库正确位置
#   2. 去重检测 → 相同内容的文件只保留一份
#   3. 生成整理报告
#
# 规则：
#   - HTML创作 → web/ 或 algorithmic-art/
#   - Python脚本 → core/
#   - Swift文件 → LongHunWidget/
#   - 重复文件 → 标记不移动
#   - 发布操作 → 需要老大确认（本脚本不推送）

SYSTEM_ROOT="$HOME/longhun-system"
SANDBOX_DIR="$SYSTEM_ROOT/sandbox_intake"
ORGANIZED_LOG="$SYSTEM_ROOT/logs/auto_organize.jsonl"
NOW_STR=$(date "+%Y-%m-%d %H:%M:%S")

echo "═══════════════════════════════════════"
echo "🐉 龍魂自动整理器 v1.0"
echo "📅 $NOW_STR"
echo "═══════════════════════════════════════"
echo ""

MOVED=0
SKIPPED=0
DUPES=0

# 检查沙箱是否有东西
total_intake=$(find "$SANDBOX_DIR" -type l 2>/dev/null | wc -l | tr -d ' ')
if [ "$total_intake" -eq 0 ]; then
    echo "✅ 沙箱容器是空的，没有需要整理的文件"
    exit 0
fi

echo "📦 沙箱中有 $total_intake 个文件待整理"
echo ""

# ── HTML 整理 ──
echo "── HTML 创作 ──"
for link in "$SANDBOX_DIR"/html/*; do
    [ ! -e "$link" ] && continue
    real_file=$(readlink -f "$link" 2>/dev/null || readlink "$link")
    basename=$(basename "$link")

    # 检查是否已在 web/ 或 algorithmic-art/
    if [ -f "$SYSTEM_ROOT/web/$basename" ]; then
        echo "  ⏭️  $basename — 已在 web/"
        SKIPPED=$((SKIPPED + 1))
        rm "$link"  # 清理符号链接
        continue
    fi

    if [ -f "$SYSTEM_ROOT/algorithmic-art/$basename" ]; then
        echo "  ⏭️  $basename — 已在 algorithmic-art/"
        SKIPPED=$((SKIPPED + 1))
        rm "$link"
        continue
    fi

    # 检查内容是否重复（md5比较）
    if [ -f "$real_file" ]; then
        file_md5=$(md5 -q "$real_file" 2>/dev/null)
        dupe_found=0
        for existing in "$SYSTEM_ROOT/web/"*.html "$SYSTEM_ROOT/algorithmic-art/"*.html; do
            [ ! -f "$existing" ] && continue
            existing_md5=$(md5 -q "$existing" 2>/dev/null)
            if [ "$file_md5" = "$existing_md5" ]; then
                echo "  🔄 $basename — 内容与 $(basename "$existing") 相同，跳过"
                DUPES=$((DUPES + 1))
                dupe_found=1
                rm "$link"
                break
            fi
        done
        [ "$dupe_found" -eq 1 ] && continue
    fi

    # 分类：流场/算法艺术 → algorithmic-art/, 其他 → web/
    target_dir="$SYSTEM_ROOT/web"
    if echo "$basename" | grep -qE "流场|流場|algorithmic|art"; then
        target_dir="$SYSTEM_ROOT/algorithmic-art"
    fi

    echo "  📥 $basename → $target_dir/"
    cp "$real_file" "$target_dir/" 2>/dev/null && {
        MOVED=$((MOVED + 1))
        rm "$link"
    }
done

# ── Python 整理 ──
echo ""
echo "── Python 脚本 ──"
for link in "$SANDBOX_DIR"/python/*; do
    [ ! -e "$link" ] && continue
    real_file=$(readlink -f "$link" 2>/dev/null || readlink "$link")
    basename=$(basename "$link")

    if [ -f "$SYSTEM_ROOT/core/$basename" ]; then
        echo "  ⏭️  $basename — 已在 core/"
        SKIPPED=$((SKIPPED + 1))
        rm "$link"
        continue
    fi

    echo "  📥 $basename → core/"
    cp "$real_file" "$SYSTEM_ROOT/core/" 2>/dev/null && {
        MOVED=$((MOVED + 1))
        rm "$link"
    }
done

# ── Swift 整理 ──
echo ""
echo "── Swift 文件 ──"
for link in "$SANDBOX_DIR"/swift/*; do
    [ ! -e "$link" ] && continue
    real_file=$(readlink -f "$link" 2>/dev/null || readlink "$link")
    basename=$(basename "$link")

    if [ -f "$SYSTEM_ROOT/LongHunWidget/$basename" ]; then
        echo "  ⏭️  $basename — 已在 LongHunWidget/"
        SKIPPED=$((SKIPPED + 1))
        rm "$link"
        continue
    fi

    echo "  📥 $basename → LongHunWidget/"
    cp "$real_file" "$SYSTEM_ROOT/LongHunWidget/" 2>/dev/null && {
        MOVED=$((MOVED + 1))
        rm "$link"
    }
done

# ── 其他类型 ──
for subdir in config media unknown; do
    for link in "$SANDBOX_DIR/$subdir"/*; do
        [ ! -e "$link" ] && continue
        basename=$(basename "$link")
        echo "  📦 $basename — 留在沙箱 $subdir/ 待老大确认"
        SKIPPED=$((SKIPPED + 1))
    done
done

# 报告
echo ""
echo "═══════════════════════════════════════"
echo "📊 整理结果"
echo "  已整理: $MOVED"
echo "  已跳过: $SKIPPED"
echo "  重复: $DUPES"
echo "═══════════════════════════════════════"

# 日志
echo "{\"时间\":\"$NOW_STR\",\"整理\":$MOVED,\"跳过\":$SKIPPED,\"重复\":$DUPES,\"DNA\":\"#龍芯⚡️ORGANIZE-$(date +%Y%m%d)\"}" >> "$ORGANIZED_LOG"

echo ""
echo "DNA: #龍芯⚡️${NOW_STR}-AUTO-ORGANIZE-v1.0"
