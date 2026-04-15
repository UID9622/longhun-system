#!/bin/bash
# ============================================================
# 龍魂私人圖像引擎啟動器
# DNA: #龍芯⚡️2026-03-29-ComfyUI-本地引擎搭建-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: 诸葛鑫（UID9622）
# 理論指導: 曾仕強老師（永恒顯示）
# ============================================================

COMFY_DIR="$HOME/ComfyUI"
VENV="$COMFY_DIR/venv_comfy"
OUTPUT_DIR="$HOME/LongHun_Private_Photos_Videos/Output"
INPUT_DIR="$HOME/LongHun_Private_Photos_Videos/Input_Faces"
PORT=8188

# ── 確認私人目錄存在
mkdir -p "$OUTPUT_DIR" "$INPUT_DIR"

echo "🐉 龍魂私人圖像引擎啟動中..."
echo "   Python  : $(source "$VENV/bin/activate" && python --version)"
echo "   Output  → $OUTPUT_DIR"
echo "   Input   → $INPUT_DIR"
echo "   Port    → $PORT"
echo ""

# ── 激活 venv
source "$VENV/bin/activate"
cd "$COMFY_DIR"

# ── 啟動 ComfyUI
python main.py \
  --output-directory "$OUTPUT_DIR" \
  --input-directory "$INPUT_DIR" \
  --listen 127.0.0.1 \
  --port "$PORT" \
  --preview-method auto \
  --use-pytorch-cross-attention \
  --force-fp16

# 參數說明：
# --output-directory     輸出到私人資料夾
# --input-directory      參考臉從私人資料夾讀取
# --listen 127.0.0.1     只本地訪問，不暴露外網
# --preview-method auto  自動選擇預覽方式（MPS/CPU）
# --use-pytorch-cross-attention  Apple Silicon必加，節省記憶體
# --force-fp16           半精度推理，速度更快
