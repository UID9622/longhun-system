#!/bin/bash
# ============================================================
# 龍魂圖像DNA歸檔器
# 功能：掃描Output新圖，自動重命名帶DNA追溯碼，移入歸檔
# DNA: #龍芯⚡️2026-03-29-ComfyUI-本地引擎搭建-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: 诸葛鑫（UID9622）
# 理論指導: 曾仕強老師（永恒顯示）
# 用法: bash comfyui_dna_archive.sh [可選:工作流名稱]
# ============================================================

OUTPUT_DIR="$HOME/LongHun_Private_Photos_Videos/Output"
ARCHIVE_DIR="$HOME/LongHun_Private_Photos_Videos/Archive"
WORKFLOW_LABEL="${1:-longhun}"
DATE=$(date +%Y%m%d_%H%M%S)
DNA="#龍芯⚡️UID9622-IMG-${WORKFLOW_LABEL}-${DATE}"
COUNT=0

mkdir -p "$ARCHIVE_DIR"

echo "🐉 龍魂DNA歸檔器啟動"
echo "   掃描: $OUTPUT_DIR"
echo "   DNA : $DNA"
echo ""

for img in "$OUTPUT_DIR"/*.png "$OUTPUT_DIR"/*.jpg "$OUTPUT_DIR"/*.webp; do
  [ -f "$img" ] || continue

  ORIG_NAME=$(basename "$img")
  EXT="${ORIG_NAME##*.}"
  BASENAME="${ORIG_NAME%.*}"
  NEW_NAME="${WORKFLOW_LABEL}_${DATE}_${COUNT}.${EXT}"
  DNA_STAMP="${WORKFLOW_LABEL}_${DATE}_${COUNT}_dna.txt"

  # 移動圖片到歸檔，新名帶工作流+時間戳
  mv "$img" "$ARCHIVE_DIR/$NEW_NAME"

  # 寫入DNA追溯文件（同名txt）
  cat > "$ARCHIVE_DIR/$DNA_STAMP" << DNAEOF
龍魂圖像DNA追溯
=================
DNA         : $DNA
原始文件名  : $ORIG_NAME
歸檔文件名  : $NEW_NAME
生成時間    : $(date '+%Y-%m-%d %H:%M:%S')
UID         : 9622
作者        : 诸葛鑫
GPG         : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
工作流      : $WORKFLOW_LABEL
=================
DNAEOF

  echo "   ✅ [$COUNT] $ORIG_NAME → $NEW_NAME"
  COUNT=$((COUNT + 1))
done

if [ "$COUNT" -eq 0 ]; then
  echo "   ⚠️  Output 資料夾無新圖片"
else
  echo ""
  echo "✅ 歸檔完成，共 $COUNT 張 → $ARCHIVE_DIR"
fi
