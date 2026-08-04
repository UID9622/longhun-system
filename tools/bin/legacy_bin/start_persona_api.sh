#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
##龍芯⚡️2026-06-21-TOOL-START_PERSONA_API-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色审计: 🟢 通过

#!/bin/bash
# 启动龍魂人格 API 服务
# DNA: #龍芯⚡️2026-06-09-START-PERSONA-API-v1.0

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          龍魂人格 API 服务启动                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "DNA: #龍芯⚡️2026-06-09-START-PERSONA-API-v1.0"
echo ""

cd ~/longhun-system

# 检查依赖
python3 -c "import fastapi" 2>/dev/null || {
    echo "⚠️ 缺少 FastAPI，正在安装..."
    pip install fastapi uvicorn
}

# 启动 API
# 注意：目录名含 '.'，不能作为 Python 包名导入，直接运行文件
echo "🚀 启动龍魂人格 API (端口 9001)..."
python3 cnsh.integrated/flow_decision/persona_api.py

