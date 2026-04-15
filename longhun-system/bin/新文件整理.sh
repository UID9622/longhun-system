#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 新文件整理 · 扫描桌面和下载 → 对应文件夹
# DNA: #龍芯⚡️2026-03-18-新文件整理-v1.1
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: UID9622 诸葛鑫（龍芯北辰）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE="$HOME/longhun-system"
LOG="$BASE/logs/整理日志.log"
NOW=$(date '+%Y-%m-%d %H:%M:%S')
MONTH=$(date '+%Y-%m')

通知() {
    osascript -e "display notification \"$2\" with title \"📁 文件整理\" subtitle \"$1\"" 2>/dev/null
}

DIR_IMG="$BASE/资源库/图片归档/$MONTH"
DIR_VIDEO="$BASE/资源库/视频归档/$MONTH"
DIR_DOC="$BASE/资源库/文档归档/$MONTH"
DIR_CODE="$BASE/资源库/代码归档/$MONTH"
DIR_ZIP="$BASE/资源库/压缩包归档/$MONTH"
DIR_MISC="$BASE/资源库/待处理"

mkdir -p "$DIR_IMG" "$DIR_VIDEO" "$DIR_DOC" "$DIR_CODE" "$DIR_ZIP" "$DIR_MISC"

moved=0
skipped=0

写日志() { echo "[$NOW] $1" >> "$LOG"; }

move_file() {
    local src="$1"
    local dst_dir="$2"
    local fname
    fname=$(basename "$src")

    if [ -f "$dst_dir/$fname" ]; then
        local ts
        ts=$(date +%H%M%S)
        local base="${fname%.*}"
        local ext="${fname##*.}"
        fname="${base}_${ts}.${ext}"
    fi

    mv "$src" "$dst_dir/$fname"
    echo "  📦 $fname → $(basename "$dst_dir")"
    写日志 "移动: $fname → $dst_dir"
    ((moved++))
}

classify() {
    local f="$1"
    local fname
    fname=$(basename "$f")
    local ext="${fname##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    # 跳过系统文件、隐藏文件、目录
    case "$fname" in
        .DS_Store|.localized|Icon*|desktop.ini) ((skipped++)); return ;;
        .*) ((skipped++)); return ;;
    esac
    [ -d "$f" ] && { ((skipped++)); return; }

    case "$ext" in
        png|jpg|jpeg|gif|webp|heic|bmp|tiff|svg)
            move_file "$f" "$DIR_IMG" ;;
        mp4|mov|avi|mkv|m4v|wmv)
            move_file "$f" "$DIR_VIDEO" ;;
        pdf|doc|docx|xls|xlsx|ppt|pptx)
            move_file "$f" "$DIR_DOC" ;;
        py|js|ts|sh|swift|html|css|json|yaml|toml|cnsh|md)
            move_file "$f" "$DIR_CODE" ;;
        zip|tar|gz|rar|7z)
            move_file "$f" "$DIR_ZIP" ;;
        *)
            local size
            size=$(stat -f%z "$f" 2>/dev/null || echo 0)
            if [ "$size" -gt 1048576 ]; then
                move_file "$f" "$DIR_MISC"
            else
                ((skipped++))
            fi
            ;;
    esac
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📁 新文件整理 · $NOW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "  【扫描桌面】"
for f in "$HOME/Desktop"/*; do
    [ -e "$f" ] && classify "$f"
done

echo ""
echo "  【扫描下载（7天前的文件）】"
if [ -d "$HOME/Downloads" ]; then
    while IFS= read -r f; do
        classify "$f"
    done < <(find "$HOME/Downloads" -maxdepth 1 -mtime +7 -type f)
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  整理完成 · 移动${moved}个 · 跳过${skipped}个"
echo "  图片 → $DIR_IMG"
echo "  文档 → $DIR_DOC"
echo "  视频 → $DIR_VIDEO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

通知 "整理完成" "移动${moved}个文件到对应文件夹"
写日志 "整理完成 移动=${moved} 跳过=${skipped}"
