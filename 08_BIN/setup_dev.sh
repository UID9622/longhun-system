#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂系统 · 开发环境一键搭建
# DNA: #龍芯⚡️丙午·丙申·丙辰·巳时·需-SETUP-DEV-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════
# 用法: bash bin/setup_dev.sh
# 功能: 创建 venv → 安装依赖 → 初始化数据目录 → 验证环境
# ═══════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "🐉 ========================================"
echo "   龍魂系统 · 开发环境搭建 v2.0"
echo "   UID9622 · longhun888.com"
echo "🐉 ========================================"
echo ""

# ── 检查 Python ──
PYTHON="python3"
if ! command -v $PYTHON &>/dev/null; then
    echo "🔴 未找到 python3，请先安装 Python 3.11+"
    exit 1
fi
echo "✅ Python: $($PYTHON --version)"

# ── 创建虚拟环境（如果不存在） ──
VENV_DIR="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    $PYTHON -m venv "$VENV_DIR"
    echo "✅ 虚拟环境: $VENV_DIR"
else
    echo "✅ 虚拟环境已存在: $VENV_DIR"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"
echo "✅ 已激活虚拟环境"

# ── 升级 pip ──
echo ""
echo "📦 升级 pip..."
pip install --upgrade pip -q

# ── 安装依赖 ──
echo ""
echo "📦 安装基础依赖..."
pip install -r requirements-base.txt -q 2>&1 | tail -1

echo "📦 安装统一依赖..."
pip install -r requirements.txt -q 2>&1 | tail -1

echo "✅ 依赖安装完成"

# ── 创建必要目录 ──
echo ""
echo "📂 创建数据目录..."
mkdir -p L7_数据层/data
mkdir -p backend/logs
mkdir -p logs
mkdir -p config
mkdir -p .codebuddy/memory

echo "✅ 目录结构就绪"

# ── 创建 .env（如果不存在） ──
ENV_FILE="$PROJECT_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo "📝 创建 .env 配置文件..."
    cat > "$ENV_FILE" << 'EOF'
# 龍魂系统 · 开发环境配置
# 生产环境请覆盖这些值

LONGHUN_API_HOST=127.0.0.1
LONGHUN_API_PORT=9622
LONGHUN_WEB_PORT=8777
LONGHUN_LOG_LEVEL=INFO
LONGHUN_DATA=./L7_数据层
LONGHUN_JWT_SECRET=dev-secret-change-in-production
EOF
    echo "✅ .env 已创建"
else
    echo "✅ .env 已存在"
fi

# ── 验证 ──
echo ""
echo "🧪 验证环境..."
echo ""

# 检查关键模块是否可导入
python3 -c "
import fastapi; print(f'  ✅ FastAPI {fastapi.__version__}')
import uvicorn; print(f'  ✅ Uvicorn {uvicorn.__version__}')
import pydantic; print(f'  ✅ Pydantic {pydantic.__version__}')
import jwt; print(f'  ✅ PyJWT {jwt.__version__}')
import httpx; print(f'  ✅ HTTPX {httpx.__version__}')
import websockets; print(f'  ✅ websockets {websockets.__version__}')
"

# 检查关键脚本是否存在
echo ""
SCRIPTS=(
    "bin/lh_memory_load.py"
    "bin/lh_anti_tamper.py"
    "bin/hetu_luoshu_dna.py"
    "08_BIN/web_server.py"
    "control-panel/main.py"
)
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "  ✅ $script"
    else
        echo "  ⚠️  $script (未找到)"
    fi
done

echo ""
echo "🐉 ========================================"
echo "   🟢 开发环境搭建完成！"
echo ""
echo "   启动门户:   python3 08_BIN/web_server.py"
echo "   启动控制台: python3 control-panel/main.py"
echo "   一键启动:   bash bin/start_dev_env.sh"
echo "   全量启动:   bash bin/start_all.sh"
echo ""
echo "   门户:       http://127.0.0.1:8777"
echo "   控制台:     http://127.0.0.1:9630"
echo "   健康检查:   http://127.0.0.1:8777/health"
echo "🐉 ========================================"
