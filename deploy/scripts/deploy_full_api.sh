#!/bin/bash
# 龍魂全接口/数据库/API一键部署脚本
# DNA: #龍芯⚡️丙午·辛未·FULL-API-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -e

echo "========================================"
echo "  龍魂系统 · 全接口/数据库/API部署"
echo "  数据主权在中国 · 本地优先"
echo "========================================"
echo ""

# 1. 创建目录结构
echo "[1/6] 创建目录结构..."
mkdir -p {data/sqlite,data/postgres,data/redis,data/cache/weather,config,logs}
echo "[✓] 目录就绪"

# 2. 检查Python依赖
echo ""
echo "[2/6] 检查Python依赖..."
python3 -c "import sqlite3" 2>/dev/null && echo "[✓] sqlite3" || echo "[!] sqlite3 缺失"
python3 -c "import requests" 2>/dev/null && echo "[✓] requests" || echo "[!] pip3 install requests"
python3 -c "import hashlib" 2>/dev/null && echo "[✓] hashlib" || echo "[!] hashlib 缺失"
python3 -c "import json" 2>/dev/null && echo "[✓] json" || echo "[!] json 缺失"

# 3. 数据库检查
echo ""
echo "[3/6] 检查数据库..."

# SQLite（内置）
echo "[✓] SQLite (内置Python)"

# PostgreSQL
if command -v psql &> /dev/null; then
    echo "[✓] PostgreSQL ($(psql --version 2>&1 | head -1))"
else
    echo "[!] PostgreSQL 未安装 (brew install postgresql)"
fi

# Redis
if command -v redis-server &> /dev/null; then
    echo "[✓] Redis ($(redis-server --version 2>&1 | head -1))"
else
    echo "[!] Redis 未安装 (brew install redis)"
fi

# Milvus
if docker ps 2>/dev/null | grep -q milvus; then
    echo "[✓] Milvus (Docker运行中)"
else
    echo "[!] Milvus 未运行 (docker run -d --name milvus-standalone -p 19530:19530 milvusdb/milvus:latest)"
fi

# Neo4j
if docker ps 2>/dev/null | grep -q neo4j; then
    echo "[✓] Neo4j (Docker运行中)"
else
    echo "[!] Neo4j 未运行 (docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/longhun123 neo4j:latest)"
fi

# 4. 验证API文件
echo ""
echo "[4/6] 验证API接口文件..."
API_FILES=(
    "bin/lh_llm_api.py:大模型统一接口"
    "bin/lh_asr_api.py:ASR语音识别"
    "bin/lh_tts_api.py:TTS语音合成"
    "bin/lh_ocr_api.py:OCR图像识别"
    "bin/lh_face_api.py:人脸识别"
    "bin/lh_payment_api.py:支付接口"
    "bin/lh_sms_api.py:短信推送"
    "bin/lh_map_api.py:地图/位置"
    "bin/lh_weather_api.py:天气/环境"
    "bin/lh_bark_dispatcher.py:Bark推送"
    "bin/lh_asr_engine.py:ASR引擎"
    "bin/lh_tts_engine.py:TTS引擎"
    "bin/lh_video_generator.py:视频生成引擎"
    "bin/lh_video_analyzer.py:视频分析引擎"
    "bin/lh_video_dna_embedder.py:视频DNA嵌入引擎"
    "bin/lh_voice_clone.py:语音克隆引擎"
    "bin/lh_voice_chat.py:语音对话引擎"
)

ALL_OK=true
for entry in "${API_FILES[@]}"; do
    file="${entry%%:*}"
    desc="${entry##*:}"
    if [ -f "$file" ]; then
        echo "[✓] $desc ($file)"
    else
        echo "[✗] $desc ($file) 缺失!"
        ALL_OK=false
    fi
done

# 5. 配置文件检查
echo ""
echo "[5/6] 检查配置文件..."
if [ -f "config/api_keys.env" ]; then
    echo "[✓] config/api_keys.env"
else
    echo "[✗] config/api_keys.env 缺失!"
    ALL_OK=false
fi

# 6. 可执行权限
echo ""
echo "[6/6] 设置可执行权限..."
chmod +x bin/lh_llm_api.py
chmod +x bin/lh_asr_api.py
chmod +x bin/lh_tts_api.py
chmod +x bin/lh_ocr_api.py
chmod +x bin/lh_face_api.py
chmod +x bin/lh_payment_api.py
chmod +x bin/lh_sms_api.py
chmod +x bin/lh_map_api.py
chmod +x bin/lh_weather_api.py
echo "[✓] 权限设置完成"

# 总结
echo ""
echo "========================================"
if [ "$ALL_OK" = true ]; then
    echo "  ✅ 龍魂全接口部署验证通过"
else
    echo "  ⚠️ 部分组件缺失，请检查"
fi
echo "========================================"
echo ""
echo "📋 可用接口列表:"
echo ""
echo "  🧠 LLM大模型:    python3 bin/lh_llm_api.py --dna '#龍芯⚡️...' --prompt '你好' --list"
echo "  🎤 语音识别:     python3 bin/lh_asr_api.py --dna '#龍芯⚡️...' --list"
echo "  🔊 语音合成:     python3 bin/lh_tts_api.py --dna '#龍芯⚡️...' --list"
echo "  👁️ OCR识别:      python3 bin/lh_ocr_api.py --dna '#龍芯⚡️...' --list"
echo "  👤 人脸识别:     python3 bin/lh_face_api.py --dna '#龍芯⚡️...' --list"
echo "  💰 支付接口:     python3 bin/lh_payment_api.py --dna '#龍芯⚡️...' --list"
echo "  📱 短信推送:     python3 bin/lh_sms_api.py --dna '#龍芯⚡️...' --list"
echo "  🗺️ 地图/位置:    python3 bin/lh_map_api.py --dna '#龍芯⚡️...' --list"
echo "  🌤️ 天气/环境:    python3 bin/lh_weather_api.py --dna '#龍芯⚡️...' --list"
echo ""
echo "  📋 视频/音频引擎: python3 引擎/launcher.py --list-tools"
echo ""
echo "  数据主权在中国 · 本地优先 · 国产模型"
echo ""
echo "  下一步: 编辑 config/api_keys.env 填入API密钥"
echo ""
