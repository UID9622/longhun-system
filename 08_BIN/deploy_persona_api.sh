#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-TOOL-DEPLOY_PERSONA_API-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/bin/bash

# 龍魂人格 API 生产部署脚本
# DNA: #龍芯⚇️2026-06-09-PERSONA-API-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

PORT=${1:-9001}
WORKERS=${2:-2}
PERSONA_DIR=$(dirname "$(readlink -f "$0")")

echo "╔════════════════════════════════════════════════════════════╗"
echo "║      龍魂人格 API 生产部署 / Persona API Production Deploy ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 步骤 1: 环境检查
echo "[1/4] 环境检查"
echo "─────────────────────────────────────────────────────────────"

echo "   检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "   ❌ Python 3 未安装"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   ✅ Python $PYTHON_VERSION"

echo "   检查 FastAPI..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "   ⚠️  FastAPI 未安装，正在安装..."
    pip install fastapi uvicorn[standard] --quiet
fi
echo "   ✅ FastAPI 已安装"

echo "   检查 Uvicorn..."
if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "   ⚠️  Uvicorn 未安装，正在安装..."
    pip install uvicorn --quiet
fi
echo "   ✅ Uvicorn 已安装"

echo ""

# 步骤 2: 停止现有进程
echo "[2/4] 清理现有进程"
echo "─────────────────────────────────────────────────────────────"

PID_FILE="$PERSONA_DIR/.persona_api.pid"
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "   停止进程 $OLD_PID..."
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            kill -9 "$OLD_PID" 2>/dev/null || true
        fi
    fi
    rm "$PID_FILE"
fi
echo "   ✅ 清理完成"
echo ""

# 步骤 3: 启动新实例
echo "[3/4] 启动 API 服务"
echo "─────────────────────────────────────────────────────────────"
echo "   配置:"
echo "      • 端口: $PORT"
echo "      • 工作进程: $WORKERS"
echo "      • 模式: 生产 (--no-reload)"
echo "      • 主机: 0.0.0.0"

cd "$PERSONA_DIR"
nohup python3 -m uvicorn \
    cnsh.flow_decision.persona_api:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers "$WORKERS" \
    --no-reload \
    > logs/persona_api_deploy.log 2>&1 &

NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

# 等待启动
sleep 2

# 验证启动
if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo "   ✅ 进程 $NEW_PID 已启动"
else
    echo "   ❌ 启动失败"
    cat logs/persona_api_deploy.log
    exit 1
fi
echo ""

# 步骤 4: 健康检查
echo "[4/4] 健康检查"
echo "─────────────────────────────────────────────────────────────"

MAX_ATTEMPTS=10
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    if curl -s "http://localhost:$PORT/personas/list" > /dev/null 2>&1; then
        echo "   ✅ API 健康检查通过 (尝试 $ATTEMPT/$MAX_ATTEMPTS)"
        break
    fi
    echo "   ⏳ 等待 API 启动... ($ATTEMPT/$MAX_ATTEMPTS)"
    sleep 1
    ((ATTEMPT++))
done

if [ $ATTEMPT -gt $MAX_ATTEMPTS ]; then
    echo "   ❌ 健康检查失败"
    cat logs/persona_api_deploy.log
    kill "$NEW_PID" 2>/dev/null || true
    rm "$PID_FILE"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    部署完成                                 ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ 🚀 API 已启动"
echo "║    地址: http://localhost:$PORT"
echo "║    PID: $NEW_PID"
echo "║    PID 文件: $PID_FILE"
echo "║"
echo "║ 📚 API 文档"
echo "║    Swagger: http://localhost:$PORT/docs"
echo "║    ReDoc: http://localhost:$PORT/redoc"
echo "║"
echo "║ 🧪 测试命令"
echo "║    curl http://localhost:$PORT/personas/list"
echo "║    curl http://localhost:$PORT/personas/P01"
echo "║"
echo "║ 📋 日志文件"
echo "║    logs/persona_api_deploy.log"
echo "╚════════════════════════════════════════════════════════════╝"
