#!/bin/bash
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午-乙巳-2026-07-29-VOICE-CLONE-SETUP-v2.0-init
# 创建者: 诸葛鑫（UID9622）
# 功能: 一键搭建 XTTS v2 真声克隆环境（venv + torch + coqui-tts）
# 输出: .venv_tts/ → 可被 lh_voice_clone.py 调用
# 参考音频: docs/reference_optimized.wav（31分钟口语样本，已清洗优化）

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv_tts"
PYTHON_BIN="/opt/homebrew/opt/python@3.12/bin/python3.12"

echo "╔══════════════════════════════════════════╗"
echo "║  龍魂 · XTTS v2 真声克隆环境搭建        ║"
echo "║  DNA: #龍芯⚡️2026-07-29-VOICE-CLONE-v2.0 ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Step 1: 检查 Python 3.12
if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ 需要 Python 3.12: brew install python@3.12"
    exit 1
fi
echo "✅ Python: $($PYTHON_BIN --version)"

# Step 2: 创建 venv
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 创建虚拟环境..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi
echo "✅ venv: $VENV_DIR"

# Step 3: 升级 pip
"$VENV_DIR/bin/pip" install --upgrade pip -q

# Step 4: 安装 PyTorch (MPS for Apple Silicon) — 稳定版，避开 torch 2.9+ 需要 torchcodec
echo "📦 安装 PyTorch (Apple Silicon MPS)..."
"$VENV_DIR/bin/pip" install "torch>=2.5.0,<2.6.0" "torchaudio>=2.5.0,<2.6.0" --quiet

# Step 5: 安装 Coqui TTS (XTTS v2) — transformers 4.57.x 兼容版本
echo "📦 安装 Coqui TTS (XTTS v2)..."
"$VENV_DIR/bin/pip" install "coqui-tts==0.27.5" "transformers>=4.57.0,<5.0.0" --quiet

# Step 5.5: 安装中文依赖
echo "📦 安装中文依赖 (pypinyin)..."
"$VENV_DIR/bin/pip" install pypinyin --quiet

# Step 6: 验证
echo ""
echo "🔍 验证安装..."
"$VENV_DIR/bin/python3" -c "
import os
os.environ['COQUI_TOS_AGREED'] = '1'
from TTS.api import TTS
print('✅ TTS + XTTS v2 安装成功')
" 2>&1

echo ""
echo "🎙️ 首次使用时，XTTS v2 模型会自动下载（约 1.8GB）"
echo "   参考音频: docs/reference_optimized.wav"
echo ""
echo "✅ 环境搭建完成！运行: python3 bin/lh_voice_clone.py --test"
