#!/bin/bash
# ═══════════════════════════════════════════════
# 龍魂·记忆API一键部署脚本
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-MEMORY-API-DEPLOY-v1.0
# ═══════════════════════════════════════════════
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "══════════════════════════════════════════════"
echo "🐉 龍魂·统一记忆 API 部署脚本 v1.0"
echo "   CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo "══════════════════════════════════════════════"

# 检测平台
PLATFORM="unknown"
if [[ "$(uname)" == "Darwin" ]]; then
    PLATFORM="mac"
elif [[ "$(uname)" == "Linux" ]]; then
    PLATFORM="linux"
fi

echo ""
echo "📍 检测到平台: $PLATFORM"
echo "📍 项目路径: $PROJECT_ROOT"

# 确保依赖
echo ""
echo "📦 检查 Python 依赖..."
PYTHON=""
if [ "$PLATFORM" == "mac" ]; then
    PYTHON="python3"
else
    PYTHON="$PROJECT_ROOT/.venv/bin/python3"
    if [ ! -f "$PYTHON" ]; then
        PYTHON="/root/longhun-system/.venv/bin/python3"
    fi
fi

if [ ! -f "$PYTHON" ]; then
    echo "🔴 Python 虚拟环境不存在: $PYTHON"
    echo "   请先创建: python3 -m venv .venv"
    exit 1
fi

echo "✅ Python: $PYTHON"

# 安装依赖
$PYTHON -m pip install fastapi uvicorn pydantic -q 2>/dev/null || true
echo "✅ FastAPI + Uvicorn 已就绪"

# 确保日志目录
mkdir -p "$PROJECT_ROOT/logs"
echo "✅ 日志目录已创建"

# 生成 API Token（如未存在）
TOKEN_FILE="$PROJECT_ROOT/.codebuddy/memory/.api_token"
if [ ! -f "$TOKEN_FILE" ]; then
    python3 -c "
import hashlib, time
seed = f'longhun-memory-$(date +%s)-UID9622'
print(hashlib.sha256(seed.encode()).hexdigest()[:32])
" > "$TOKEN_FILE"
    chmod 600 "$TOKEN_FILE"
    echo "✅ API Token 已生成"
else
    echo "✅ API Token 已存在"
fi

TOKEN=$(cat "$TOKEN_FILE")
echo "   Token: ${TOKEN:0:8}...（完整Token已存于 $TOKEN_FILE）"

# ═══════════════════════════════════════════════
# Mac 部署 (launchd)
# ═══════════════════════════════════════════════
if [ "$PLATFORM" == "mac" ]; then
    echo ""
    echo "🍎 Mac 部署 → launchd (端口 8769, 127.0.0.1)"

    PLIST_SRC="$PROJECT_ROOT/deploy/com.longhun.memory-api.plist"
    PLIST_DST="$HOME/Library/LaunchAgents/com.longhun.memory-api.plist"

    if [ ! -f "$PLIST_SRC" ]; then
        echo "🔴 plist 文件不存在: $PLIST_SRC"
        exit 1
    fi

    # 停止旧服务
    launchctl unload "$PLIST_DST" 2>/dev/null || true
    sleep 1

    # 复制并加载
    cp "$PLIST_SRC" "$PLIST_DST"
    launchctl load "$PLIST_DST"

    sleep 2

    # 验证
    if curl -s http://127.0.0.1:8769/v1/memory/health > /dev/null 2>&1; then
        echo "✅ 记忆 API 已在 :8769 运行"
        curl -s http://127.0.0.1:8769/v1/memory/health | python3 -m json.tool 2>/dev/null || true
    else
        echo "🔴 记忆 API 启动失败，检查日志:"
        echo "   tail -f $PROJECT_ROOT/logs/memory_api.log"
        echo "   tail -f $PROJECT_ROOT/logs/memory_api_error.log"
    fi

# ═══════════════════════════════════════════════
# Linux/鲲鹏 部署 (systemd)
# ═══════════════════════════════════════════════
elif [ "$PLATFORM" == "linux" ]; then
    echo ""
    echo "🐧 鲲鹏部署 → systemd (端口 8770, 0.0.0.0)"

    SERVICE_SRC="$PROJECT_ROOT/deploy/longhun-memory-api.service"
    SERVICE_DST="/etc/systemd/system/longhun-memory-api.service"

    if [ ! -f "$SERVICE_SRC" ]; then
        echo "🔴 service 文件不存在: $SERVICE_SRC"
        exit 1
    fi

    cp "$SERVICE_SRC" "$SERVICE_DST"
    systemctl daemon-reload
    systemctl enable longhun-memory-api
    systemctl restart longhun-memory-api

    sleep 3

    if systemctl is-active --quiet longhun-memory-api; then
        echo "✅ 记忆 API 已运行 (端口 8770)"
        curl -s http://127.0.0.1:8770/v1/memory/health | python3 -m json.tool 2>/dev/null || true
        echo ""
        echo "🔐 远程 Token: ${TOKEN}"
        echo "   使用: curl -H 'X-API-Token: $TOKEN' http://119.13.90.27:8770/v1/memory"
    else
        echo "🔴 记忆 API 启动失败:"
        journalctl -u longhun-memory-api --no-pager -n 20
    fi
fi

echo ""
echo "══════════════════════════════════════════════"
echo "🐉 部署完成"
echo ""
echo "   📍 本机访问: http://127.0.0.1:8769/v1/memory/health"
echo "   📍 鲲鹏访问: http://119.13.90.27:8770/v1/memory/health"
echo "   🔑 Token:     ${TOKEN:0:8}..."
echo ""
echo "   AI 加载命令:"
echo "   python3 bin/lh_memory_load.py           # 本机"
echo "   python3 bin/lh_memory_client.py         # 完整客户端"
echo "   source bin/lh_memory_load.sh            # Shell版"
echo "══════════════════════════════════════════════"
