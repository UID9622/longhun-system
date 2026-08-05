#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DeepSeek-V3 一键部署（鲲鹏/Ubuntu适配）
# DNA: #龍芯⚡️丙午·乙未·甲辰-DeepSeek部署-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0

set -e

echo "🐉 龍魂 · DeepSeek-V3 部署脚本"
echo "================================"

# 1. 检测GPU
echo "[1/5] 检测GPU..."
if command -v nvidia-smi &> /dev/null; then
    GPU_COUNT=$(nvidia-smi --list-gpus | wc -l)
    echo "✅ 检测到 $GPU_COUNT 张GPU"
else
    echo "⚠️ 未检测到GPU，将使用CPU模式（极慢）"
    GPU_COUNT=0
fi

# 2. 选择部署模式
echo "[2/5] 选择部署模式:"
echo "  1) vLLM (推荐，高性能)"
echo "  2) SGLang"
echo "  3) 官方API (无需GPU)"
read -p "选择 [1-3]: " MODE

case $MODE in
    1)
        echo "安装 vLLM..."
        pip install vllm
        echo "启动 vLLM 服务..."
        if [ $GPU_COUNT -ge 8 ]; then
            vllm serve deepseek-ai/DeepSeek-V3 \
                --trust-remote-code \
                --tensor-parallel-size $GPU_COUNT \
                --enable-expert-parallel \
                --port 8000 &
        else
            vllm serve deepseek-ai/DeepSeek-V3 \
                --trust-remote-code \
                --port 8000 &
        fi
        echo "✅ vLLM 服务已启动: http://localhost:8000"
        ;;
    2)
        echo "安装 SGLang..."
        pip install sglang
        echo "启动 SGLang 服务..."
        python3 -m sglang.launch_server \
            --model deepseek-ai/DeepSeek-V3 \
            --tp $GPU_COUNT \
            --trust-remote-code \
            --port 30000 &
        echo "✅ SGLang 服务已启动: http://localhost:30000"
        ;;
    3)
        echo "使用官方API模式"
        read -p "请输入你的 DeepSeek API Key: " API_KEY
        export DEEPSEEK_API_KEY=$API_KEY
        echo "export DEEPSEEK_API_KEY=$API_KEY" >> ~/.bashrc
        echo "✅ API Key 已配置"
        ;;
esac

# 3. 安装Python依赖
echo "[3/5] 安装Python依赖..."
pip install requests

# 4. 创建配置
echo "[4/5] 创建配置文件..."
cat > ~/.deepseek_config << EOF
DEEPSEEK_BASE_URL=${DEEPSEEK_BASE_URL:-http://localhost:8000/v1}
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:-}
DEEPSEEK_MODEL=${DEEPSEEK_MODEL:-deepseek-ai/DeepSeek-V3}
EOF

# 5. 验证
echo "[5/5] 验证部署..."
python3 -c "
from deepseek_api import DeepSeekClient
client = DeepSeekClient()
try:
    resp = client.chat([{'role':'user','content':'你好'}])
    print('✅ 部署验证通过')
except Exception as e:
    print(f'❌ 验证失败: {e}')
"

echo "================================"
echo "✅ DeepSeek-V3 部署完成"
echo "配置文件: ~/.deepseek_config"
echo "API地址: ${DEEPSEEK_BASE_URL:-http://localhost:8000/v1}"
