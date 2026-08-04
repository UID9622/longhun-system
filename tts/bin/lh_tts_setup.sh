#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🧬 龍魂 TTS 引擎部署脚本 v1.0
# DNA: #龍芯⚡️丙午·乙未·己卯·巳时·☰乾-TTS-SETUP-v1.0-g1h2i3j4
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 
# 用法: bash tts/bin/lh_tts_setup.sh [--with-models]
#   --with-models  同时下载预训练模型（约3GB，首次需要）

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SOVITS_DIR="$PROJECT_DIR/engines/gpt_sovits"
SOVITS_VENV="$SOVITS_DIR/.venv_gpt_sovits"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "  龍魂 TTS 引擎 v1.0 部署"
echo "  底座: GPT-SoVITS v2 (MIT License)"
echo "  设备: $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Unknown')"
echo "========================================"
echo ""

# ── 1. 虚拟环境 ──
echo -e "${GREEN}[1/5]${NC} 创建虚拟环境..."
if [ ! -d "$SOVITS_VENV" ]; then
    python3 -m venv "$SOVITS_VENV"
    echo "  ✅ venv 已创建: $SOVITS_VENV"
else
    echo "  ⏭️  venv 已存在"
fi

# ── 2. PyTorch (MPS) ──
echo -e "${GREEN}[2/5]${NC} 安装 PyTorch (MPS 后端)..."
"$SOVITS_VENV/bin/pip" install --quiet torch torchaudio 2>&1 | tail -1
echo "  ✅ PyTorch 已安装"

# ── 3. GPT-SoVITS 依赖 ──
echo -e "${GREEN}[3/5]${NC} 安装 GPT-SoVITS 依赖..."
cd "$SOVITS_DIR"
"$SOVITS_VENV/bin/pip" install --quiet -r requirements.txt 2>&1 | tail -3
echo "  ✅ 依赖已安装"

# ── 4. 验证 ──
echo -e "${GREEN}[4/5]${NC} 验证安装..."
VERIFY=$("$SOVITS_VENV/bin/python" -c "
import torch
print(f'PyTorch {torch.__version__}')
print(f'MPS: {torch.backends.mps.is_available()}')
")
echo "  $VERIFY"

# ── 5. 预训练模型（可选） ──
if [ "$1" = "--with-models" ]; then
    echo -e "${GREEN}[5/5]${NC} 下载预训练模型（约3GB）..."
    cd "$SOVITS_DIR"
    mkdir -p pretrained_models
    
    # GPT 权重
    if [ ! -f "pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt" ]; then
        echo "  下载 GPT 权重..."
        "$SOVITS_VENV/bin/python" -c "
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id='lj1995/GPT-SoVITS', filename='s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt', local_dir='pretrained_models')
" || echo "  ⚠️ GPT权重下载失败，稍后手动下载"
    fi
    
    # SoVITS 权重
    if [ ! -f "pretrained_models/s2G488k.pth" ]; then
        echo "  下载 SoVITS 权重..."
        "$SOVITS_VENV/bin/python" -c "
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id='lj1995/GPT-SoVITS', filename='s2G488k.pth', local_dir='pretrained_models')
" || echo "  ⚠️ SoVITS权重下载失败，稍后手动下载"
    fi
    
    echo "  ✅ 模型下载完成"
else
    echo -e "${YELLOW}[5/5]${NC} 跳过模型下载（加 --with-models 自动下载）"
fi

echo ""
echo "========================================"
echo "  ✅ 龍魂 TTS 引擎部署完成"
echo ""
echo "  启动 GPT-SoVITS API:"
echo "    cd engines/gpt_sovits"
echo "    .venv_gpt_sovits/bin/python api_v2.py -a 0.0.0.0 -p 9880"
echo ""
echo "  测试语音合成:"
echo "    python3 tts/bin/lh_speak.py --list"
echo "    python3 tts/bin/lh_speak.py --persona P00 --text '数据主权在人民手里'"
echo ""
echo "  检查服务:"
echo "    python3 tts/bin/lh_speak.py --health"
echo "========================================"
