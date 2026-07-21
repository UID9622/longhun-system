#!/bin/bash
# 龍魂API服务启动脚本
# DNA: #龍芯⚡️丙午·辛未·API-START-v1.0
set -e

echo "[龍魂] 启动API服务集群..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

# 加载密钥
if [ -f "config/api_keys.env" ]; then
    set -a
    source config/api_keys.env
    set +a
    echo "[✓] 密钥加载完成"
else
    echo "[!] config/api_keys.env 不存在，请先配置密钥"
fi

# 启动数据库（可选）
# brew services start postgresql 2>/dev/null || true
# brew services start redis 2>/dev/null || true

echo ""
echo "[龍魂] 可用接口:"
echo ""
echo "  🧠 LLM:        python3 bin/lh_llm_api.py --dna '...' --prompt '...'"
echo "  🎤 ASR:        python3 bin/lh_asr_api.py --dna '...' --input audio.wav"
echo "  🔊 TTS:        python3 bin/lh_tts_api.py --dna '...' --text '...'"
echo "  👁️ OCR:        python3 bin/lh_ocr_api.py --dna '...' --input image.png"
echo "  👤 人脸:        python3 bin/lh_face_api.py --dna '...' --input face.jpg"
echo "  💰 支付:        python3 bin/lh_payment_api.py --dna '...' --amount 1.00"
echo "  📱 短信:        python3 bin/lh_sms_api.py --dna '...' --phone 13800138000"
echo "  🗺️ 地图:        python3 bin/lh_map_api.py --dna '...' --geocode '北京'"
echo "  🌤️ 天气:        python3 bin/lh_weather_api.py --dna '...' --city '北京'"
echo ""
echo "  📋 引擎列表:    python3 引擎/launcher.py --list-tools"
echo "  🎬 视频引擎:    python3 引擎/launcher.py video <tool> [args]"
echo "  🎤 语音引擎:    python3 引擎/launcher.py audio <tool> [args]"
echo ""
echo "[龍魂] API集群就绪"
echo "[龍魂] 数据主权在中国 · 本地优先 · 国产模型"
