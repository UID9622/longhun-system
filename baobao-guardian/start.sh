#!/bin/bash
# 龍魂宝宝守护助手 · 一键启动脚本
# DNA:#龍芯⚡️2026-06-04-START-SCRIPT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂宝宝守护助手启动器 v1.0                  ║"
echo "║  UID9622 · 诸葛鑫 · 龍芯北辰                     ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo "📁 项目目录: $PROJECT_ROOT"
echo ""

# ═══════════════════════════════════════════════════════════
# 检查依赖
# ═══════════════════════════════════════════════════════════

echo "🔍 检查环境..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js 18+"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3.11+"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"
echo "✅ Python 版本: $(python3 --version)"
echo ""

# ═══════════════════════════════════════════════════════════
# 启动后端
# ═══════════════════════════════════════════════════════════

echo "🚀 启动后端服务..."

cd "$BACKEND_DIR"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 检查 Python 版本 (避免 Python 3.14 兼容性问题)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) and sys.version_info < (3, 15) else 1)" 2>/dev/null; then
    if command -v python3.11 &> /dev/null; then
        alias python3="python3.11"
    fi
fi

# 激活虚拟环境
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# 安装依赖 (只在首次运行时)
if [ ! -f "venv/lib/python*/site-packages/fastapi" ] && [ ! -f "venv/Lib/site-packages/fastapi" ]; then
    echo "📦 安装 Python 依赖..."
    pip install -q -r requirements.txt
fi

echo "✅ 后端环境就绪"
echo ""

# 在后台启动后端
echo "🔥 启动 FastAPI 服务器..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!

echo "✅ 后端 PID: $BACKEND_PID"
echo "   访问地址: http://localhost:8000"
echo "   WebSocket: ws://localhost:8000/ws/overlay"
echo ""

# 等待后端启动
sleep 2

if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ 后端启动失败，查看日志:"
    cat backend.log
    exit 1
fi

echo "✅ 后端已启动"
echo ""

# ═══════════════════════════════════════════════════════════
# 启动前端
# ═══════════════════════════════════════════════════════════

echo "🚀 启动前端开发服务器..."

cd "$FRONTEND_DIR"

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装 npm 依赖..."
    npm install
fi

echo "✅ 前端环境就绪"
echo ""

# 启动前端
echo "🔥 启动 Vite 开发服务器..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "✅ 前端 PID: $FRONTEND_PID"
echo ""

# ═══════════════════════════════════════════════════════════
# 启动完成
# ═══════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ 龍魂宝宝守护助手已启动！                      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📖 快速链接:"
echo "   🌐 前端应用: http://localhost:5173"
echo "   🔗 API 文档: http://localhost:8000/docs"
echo "   📊 健康检查: http://localhost:8000/health"
echo ""
echo "🧹 清理进程:"
echo "   kill $BACKEND_PID  # 关闭后端"
echo "   kill $FRONTEND_PID # 关闭前端"
echo ""
echo "📝 日志文件:"
echo "   $BACKEND_DIR/backend.log  # 后端日志"
echo "   $FRONTEND_DIR/frontend.log # 前端日志"
echo ""
echo "💡 提示: 按 Ctrl+C 可以安全地停止所有服务"
echo ""

# 保持脚本运行
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM

# 等待进程
wait
