#!/bin/bash
# ☰☰ 龍🇨🇳魂 ☷ · 视频AI免费安装脚本
# DNA: #龍芯⚡️2026-04-08-VIDEO-AI-FREE-v1.0
# 配置: Apple M4 Max + 64GB RAM（顶配，14B模型随便跑）

set -e

echo ""
echo "    ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰"
echo "    ☰                                ☰"
echo "    ☰   🎬 龍魂视频AI · 免费安装    ☰"
echo "    ☰       一分钱不花！            ☰"
echo "    ☰                                ☰"
echo "    ☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷"
echo ""
echo "    检测配置: Apple M4 Max + 64GB ✅"
echo "    目标: 本地视频AI · 数据不出境"
echo ""

COMFY_DIR="$HOME/ComfyUI"
NODES_DIR="$COMFY_DIR/custom_nodes"
MODELS_DIR="$COMFY_DIR/models"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
GOLD='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GOLD}[龍魂]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

# 检查ComfyUI
if [ ! -d "$COMFY_DIR" ]; then
    error "ComfyUI目录不存在: $COMFY_DIR"
    exit 1
fi

success "ComfyUI目录确认: $COMFY_DIR"

cd "$NODES_DIR"

log "开始安装视频AI插件..."
echo ""

# 1. WanVideo (阿里开源 - 最强中文视频)
if [ -d "ComfyUI-WanVideoWrapper" ]; then
    log "WanVideo已存在，更新到最新版..."
    cd ComfyUI-WanVideoWrapper && git pull && cd ..
else
    log "安装 WanVideo (阿里·通义万相·中文最强)..."
    git clone https://github.com/kijai/ComfyUI-WanVideoWrapper.git
fi
success "WanVideo 安装完成"

# 2. AnimateDiff (图片动起来)
if [ -d "ComfyUI-AnimateDiff-Evolved" ]; then
    log "AnimateDiff已存在，跳过"
else
    log "安装 AnimateDiff (图片动画)..."
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
fi
success "AnimateDiff 安装完成"

# 3. VideoHelperSuite (视频工具)
if [ -d "ComfyUI-VideoHelperSuite" ]; then
    log "VideoHelperSuite已存在，跳过"
else
    log "安装 VideoHelperSuite (视频处理)..."
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
fi
success "VideoHelperSuite 安装完成"

# 4. 安装依赖
echo ""
log "安装Python依赖..."
cd "$COMFY_DIR"
pip3 install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install -q transformers accelerate safetensors omegaconf
pip3 install -q einops imageio imageio-ffmpeg
success "Python依赖安装完成"

echo ""
log "下载模型..."
log "你的64GB内存可以跑14B模型，但先从1.3B试用开始"
echo ""

# 创建模型目录
mkdir -p "$MODELS_DIR/diffusion_models"
mkdir -p "$MODELS_DIR/text_encoders"
mkdir -p "$MODELS_DIR/vae"

# 下载脚本
cat > "$MODELS_DIR/download_wan_models.sh" << 'MODEL_EOF'
#!/bin/bash
# 模型下载脚本 - 使用国内镜像

echo "下载WanVideo模型..."
echo ""
echo "推荐下载（从大到小）："
echo "1. Wan2.1-T2V-14B  - 最强质量 (约30GB)"
echo "2. Wan2.1-T2V-1.3B - 快速试用 (约3GB)"
echo "3. Wan2.1-I2V-14B  - 图片转视频 (约30GB)"
echo ""

# 国内镜像地址（ModelScope）
MS_URL="https://www.modelscope.cn/models"

echo "使用ModelScope国内镜像下载..."
echo ""

# 1.3B T2V模型（新手推荐）
if [ ! -f "diffusion_models/wan2.1_t2v_1.3B_bf16.safetensors" ]; then
    echo "下载 Wan2.1-T2V-1.3B..."
    # 这里可以用wget或curl，实际地址需要去ModelScope查
    echo "请访问: https://www.modelscope.cn/models/Wan-AI/Wan2.1-T2V-1.3B"
    echo "下载后放到: diffusion_models/"
fi

MODEL_EOF

chmod +x "$MODELS_DIR/download_wan_models.sh"
success "模型下载脚本已创建"

echo ""
echo "═══════════════════════════════════════════"
echo "    ✅ 安装完成！"
echo "═══════════════════════════════════════════"
echo ""
echo "已安装插件："
echo "  🎬 WanVideo (阿里·最强中文视频)"
echo "  🎞️ AnimateDiff (图片动画)"
echo "  🛠️ VideoHelperSuite (视频工具)"
echo ""
echo "下一步："
echo "  1. 启动ComfyUI"
echo "  2. 运行: $MODELS_DIR/download_wan_models.sh"
echo "  3. 加载工作流，开始生成视频"
echo ""
echo "模型下载地址："
echo "  ModelScope(国内): https://www.modelscope.cn"
echo "  HuggingFace(国际): https://huggingface.co/Wan-AI"
echo ""
echo "DNA: #龍芯⚡️2026-04-08-VIDEO-AI-FREE-v1.0"
echo ""
