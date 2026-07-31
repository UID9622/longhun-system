#!/bin/bash
# DNA: #龍芯⚡️2026-07-30-网络限流应对-模型镜像-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 龍魂网络限流应对方案 · 模型下载镜像
# 解决：HuggingFace/模型下载被限流/断连

echo "[龍魂] 配置模型下载国内镜像..."

# ===== 3.1 HuggingFace国内镜像 =====
export HF_ENDPOINT="https://hf-mirror.com"
export HF_HUB_ENABLE_HF_TRANSFER="1"

# 写入永久配置
mkdir -p ~/.config/huggingface
cat > ~/.config/huggingface/hub_config.yml << EOF
endpoint: https://hf-mirror.com
EOF

# ===== 3.2 模型下载脚本（带断点续传+代理） =====
cat > ~/longhun-system/bin/lh_model_download.sh << 'EOF'
#!/bin/bash
MODEL_ID=$1
OUTPUT_DIR=${2:-"~/longhun-system/models"}

# 优先走代理（如果可用）
if [ -n "$ALL_PROXY" ]; then
    echo "[龍魂] 使用代理下载: $MODEL_ID"
    huggingface-cli download $MODEL_ID --local-dir $OUTPUT_DIR/$MODEL_ID --resume-download
else
    # 直连国内镜像
    echo "[龍魂] 使用国内镜像下载: $MODEL_ID"
    HF_ENDPOINT=https://hf-mirror.com huggingface-cli download $MODEL_ID --local-dir $OUTPUT_DIR/$MODEL_ID --resume-download
fi
EOF
chmod +x ~/longhun-system/bin/lh_model_download.sh

# ===== 3.3 常用模型国内镜像地址 =====
cat > ~/longhun-system/config/model_mirrors.json << 'EOF'
{
  "llama-3.1-8b": {
    "hf": "mlx-community/Llama-3.1-8B-Instruct-4bit",
    "mirror": "https://hf-mirror.com/mlx-community/Llama-3.1-8B-Instruct-4bit",
    "modelscope": "https://modelscope.cn/models/llm-research/Llama-3.1-8B"
  },
  "fish-speech": {
    "hf": "fishaudio/fish-speech-1.4",
    "mirror": "https://hf-mirror.com/fishaudio/fish-speech-1.4",
    "modelscope": "https://modelscope.cn/models/fishaudio/fish-speech-1.4"
  },
  "liveportrait": {
    "hf": "KwaiVGI/LivePortrait",
    "mirror": "https://hf-mirror.com/KwaiVGI/LivePortrait"
  }
}
EOF

echo "[龍魂] 镜像配置完成"
echo "[龍魂] 下载示例: lh_model_download.sh mlx-community/Llama-3.1-8B-Instruct-4bit"
