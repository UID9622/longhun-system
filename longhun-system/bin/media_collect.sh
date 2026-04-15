#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# media_collect.sh
# 龍魂·个人媒体归集脚本 · 把散落文件收拢到统一媒体库
# DNA: #龍芯⚡️2026-04-06-media-collect-v1.0
# 作者: 诸葛鑫（UID9622）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导: 曾仕强老师（永恒显示）
# 献礼: 乔布斯·曾仕强·历代传递和平与爱的人
# ──────────────────────────────────────────────────────────────

set -euo pipefail

HUB="$HOME/longhun-system/LongHun_Private_Photos_Videos"
LOG="$HOME/longhun-system/logs/media_collect.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# ── 目录结构 ───────────────────────────────────────────────────
mkdir -p "$HUB/图片"          # 个人照片·截图·设计稿
mkdir -p "$HUB/视频"          # mp4·mov·生成视频
mkdir -p "$HUB/音频"          # mp3·m4a·wav·声音素材
mkdir -p "$HUB/生成图"        # AI生成·ComfyUI·midjourney
mkdir -p "$HUB/素材库"        # 性感元素·创意原料·待拆解掰碎

echo "[$TIMESTAMP] ── 龍魂媒体归集开始 ──" | tee -a "$LOG"
echo "目标库: $HUB" | tee -a "$LOG"

COPIED=0
SKIPPED=0

copy_file() {
    local src="$1"
    local dst_dir="$2"
    local filename
    filename=$(basename "$src")
    local dst="$dst_dir/$filename"

    # 同名处理：加哈希前缀避免覆盖
    if [[ -f "$dst" ]]; then
        local hash
        hash=$(md5 -q "$src" 2>/dev/null || md5sum "$src" 2>/dev/null | cut -d' ' -f1)
        local short="${hash:0:6}"
        dst="$dst_dir/${short}_$filename"
    fi

    cp "$src" "$dst"
    echo "  ✅ $(basename "$src") → ${dst_dir##*/}/" | tee -a "$LOG"
    ((COPIED++)) || true
}

# ── 来源1: ~/Pictures/ (散落个人图) ───────────────────────────
echo "" | tee -a "$LOG"
echo "【扫描 ~/Pictures/】" | tee -a "$LOG"
find "$HOME/Pictures" -maxdepth 1 -type f \
    \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \
       -o -iname "*.heic" -o -iname "*.heif" -o -iname "*.gif" \
       -o -iname "*.webp" -o -iname "*.bmp" \) \
    2>/dev/null | while read -r f; do
    copy_file "$f" "$HUB/图片"
done

# ── 来源2: ~/Downloads/ 媒体文件 ──────────────────────────────
echo "" | tee -a "$LOG"
echo "【扫描 ~/Downloads/ 媒体】" | tee -a "$LOG"
find "$HOME/Downloads" -maxdepth 2 -type f \
    \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.heic" \
       -o -iname "*.gif" -o -iname "*.webp" \
       -o -iname "*.mp4" -o -iname "*.mov" -o -iname "*.m4v" -o -iname "*.avi" -o -iname "*.mkv" \
       -o -iname "*.mp3" -o -iname "*.m4a" -o -iname "*.wav" -o -iname "*.flac" -o -iname "*.aac" \) \
    2>/dev/null | while read -r f; do
    ext="${f##*.}"
    ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    case "$ext_lower" in
        mp4|mov|m4v|avi|mkv) copy_file "$f" "$HUB/视频" ;;
        mp3|m4a|wav|flac|aac) copy_file "$f" "$HUB/音频" ;;
        *) copy_file "$f" "$HUB/素材库" ;;
    esac
done

# ── 来源3: longhun-system/video_output/ ──────────────────────
echo "" | tee -a "$LOG"
echo "【扫描 video_output/】" | tee -a "$LOG"
find "$HOME/longhun-system/video_output" -type f \
    \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" \) \
    2>/dev/null | while read -r f; do
    copy_file "$f" "$HUB/视频"
done

# ── 来源4: longhun-system/星辰记忆助手 内的图片 ───────────────
echo "" | tee -a "$LOG"
echo "【扫描 星辰记忆助手 图片】" | tee -a "$LOG"
find "$HOME/longhun-system/星辰记忆助手_CNSH龙魂系统" \
     "$HOME/longhun-system/星辰记忆三端同步" \
     -maxdepth 3 -type f \
    \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" \) \
    2>/dev/null | while read -r f; do
    copy_file "$f" "$HUB/生成图"
done

# ── 来源5: ComfyUI output (AI生成图) ─────────────────────────
echo "" | tee -a "$LOG"
echo "【扫描 ComfyUI/output/ AI生成图】" | tee -a "$LOG"
find "$HOME/ComfyUI/output" -type f \
    \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) \
    2>/dev/null | while read -r f; do
    copy_file "$f" "$HUB/生成图"
done

# ── 来源6: longhun-system/AI有思维/ 散落媒体 ─────────────────
echo "" | tee -a "$LOG"
echo "【扫描 AI有思维/ 媒体】" | tee -a "$LOG"
find "$HOME/longhun-system/AI有思维" -type f \
    \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \
       -o -iname "*.mp4" -o -iname "*.mov" \
       -o -iname "*.mp3" -o -iname "*.m4a" \) \
    2>/dev/null | while read -r f; do
    copy_file "$f" "$HUB/素材库"
done

# ── 来源7: CreativeArchive 音频 ───────────────────────────────
echo "" | tee -a "$LOG"
echo "【扫描 CreativeArchive/音频视频/】" | tee -a "$LOG"
find "$HOME/longhun-system/CreativeArchive/音频视频" -type f \
    \( -iname "*.mp3" -o -iname "*.m4a" -o -iname "*.wav" -o -iname "*.flac" \) \
    2>/dev/null | while read -r f; do
    copy_file "$f" "$HUB/音频"
done

# ── 汇报 ──────────────────────────────────────────────────────
echo "" | tee -a "$LOG"
echo "══════════════════════════════════════" | tee -a "$LOG"
echo "🟢 归集完成 · DNA: #龍芯⚡️2026-04-06-media-collect-v1.0" | tee -a "$LOG"
echo "📁 媒体库: $HUB" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# 统计各分类数量
for d in 图片 视频 音频 生成图 素材库; do
    count=$(find "$HUB/$d" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  $d/: $count 个文件" | tee -a "$LOG"
done

echo "" | tee -a "$LOG"
echo "GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F" | tee -a "$LOG"
echo "[$TIMESTAMP] ── 归集结束 ──" | tee -a "$LOG"
