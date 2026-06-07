#!/bin/bash
# 龍魂宝宝守护助手 · 项目结构验证脚本
# DNA: #龍芯⚡️2026-06-04-VERIFY-v1.0

echo "╔════════════════════════════════════════════════════╗"
echo "║  🔍 龍魂宝宝守护助手 · 项目结构验证              ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASSED=0
FAILED=0

# 检查函数
check_file() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ]; then
        echo "✅ $description"
        ((PASSED++))
    else
        echo "❌ $description (缺失: $file)"
        ((FAILED++))
    fi
}

echo "📝 检查前端文件..."
check_file "$PROJECT_ROOT/frontend/package.json" "npm 配置"
check_file "$PROJECT_ROOT/frontend/tsconfig.json" "TypeScript 配置"
check_file "$PROJECT_ROOT/frontend/vite.config.ts" "Vite 配置"
check_file "$PROJECT_ROOT/frontend/electron-main.ts" "Electron 主进程"
check_file "$PROJECT_ROOT/frontend/index.html" "HTML 入口"
check_file "$PROJECT_ROOT/frontend/src/main.tsx" "React 入口"
check_file "$PROJECT_ROOT/frontend/src/App.tsx" "主应用组件"
check_file "$PROJECT_ROOT/frontend/src/components/Overlay.tsx" "Overlay 组件"
check_file "$PROJECT_ROOT/frontend/src/components/Baobao.tsx" "Baobao 组件"
check_file "$PROJECT_ROOT/frontend/src/components/ParticleContainer.tsx" "粒子系统"
check_file "$PROJECT_ROOT/frontend/src/store/overlay.ts" "Overlay 状态"
check_file "$PROJECT_ROOT/frontend/src/store/baobao.ts" "Baobao 状态"
check_file "$PROJECT_ROOT/frontend/src/services/wsClient.ts" "WebSocket 客户端"
check_file "$PROJECT_ROOT/frontend/src/styles/animations.css" "动画库"
check_file "$PROJECT_ROOT/frontend/src/styles/index.css" "全局样式"

echo ""
echo "📝 检查后端文件..."
check_file "$PROJECT_ROOT/backend/app/main.py" "FastAPI 应用"
check_file "$PROJECT_ROOT/backend/requirements.txt" "Python 依赖"
check_file "$PROJECT_ROOT/backend/.env" "环境变量"

echo ""
echo "📝 检查项目配置..."
check_file "$PROJECT_ROOT/README.md" "项目文档"
check_file "$PROJECT_ROOT/.gitignore" "Git 忽略配置"
check_file "$PROJECT_ROOT/start.sh" "启动脚本 (Linux/macOS)"
check_file "$PROJECT_ROOT/start.bat" "启动脚本 (Windows)"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  📊 验证结果                                       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "✅ 通过: $PASSED"
echo "❌ 失败: $FAILED"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "✨ 所有文件检查完成！项目结构正确。"
    echo ""
    echo "下一步:"
    echo "  1. 进入项目: cd ~/longhun-system/baobao-guardian"
    echo "  2. 启动服务: ./start.sh          (macOS/Linux)"
    echo "  2. 启动服务: start.bat           (Windows)"
    echo "  3. 打开浏览器: http://localhost:5173"
    exit 0
else
    echo ""
    echo "⚠️  发现 $FAILED 个缺失文件，请检查！"
    exit 1
fi
