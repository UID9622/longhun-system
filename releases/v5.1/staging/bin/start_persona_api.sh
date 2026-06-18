#!/bin/bash
# 启动龍魂人格 API 服务
# DNA: #龍芯⚇️2026-06-09-START-PERSONA-API-v1.0

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          龍魂人格 API 服务启动                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "DNA: #龍芯⚇️2026-06-09-START-PERSONA-API-v1.0"
echo ""

cd ~/longhun-system

# 检查依赖
python3 -c "import fastapi" 2>/dev/null || {
    echo "⚠️ 缺少 FastAPI，正在安装..."
    pip install fastapi uvicorn
}

# 启动 API
echo "🚀 启动龍魂人格 API (端口 9001)..."
python3 -m uvicorn cnsh.integrated.flow_decision.persona_api:app --host 0.0.0.0 --port 9001 --reload

