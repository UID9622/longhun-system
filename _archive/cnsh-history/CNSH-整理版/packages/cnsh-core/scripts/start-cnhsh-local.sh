#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# start-cnhsh-local.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-start-cnhsh-local-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH 本地系统一键启动脚本
# 让您完全自主控制自己的AI人格系统

echo "🧠 CNSH 本地AI人格系统启动器"
echo "================================"

# 检查是否为首次运行
if [ ! -d "./data" ]; then
    echo "📦 检测到首次运行，正在初始化..."
    ./local-db-setup.sh
    echo ""
fi

# 检查服务状态
echo "🔍 检查系统状态..."

# 检查数据库
if [ -f "./data/databases/sqlite/cnsh.db" ]; then
    echo "✅ 本地数据库已就绪"
else
    echo "❌ 数据库未初始化，请先运行 ./local-db-setup.sh"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."

# Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js 已安装: $(node --version)"
else
    echo "❌ 请先安装 Node.js"
    exit 1
fi

# 检查模块依赖
if [ ! -d "./node_modules" ]; then
    echo "📦 安装Node.js依赖..."
    npm install
fi

# 检查Ollama (可选)
if curl -s "http://localhost:11434/api/tags" &> /dev/null; then
    echo "✅ Ollama 服务已运行"
    OLLAMA_AVAILABLE=true
else
    echo "⚠️ Ollama 未运行，某些AI功能可能受限"
    OLLAMA_AVAILABLE=false
fi

# 加载配置
if [ -f "./data/.env.local" ]; then
    export $(cat ./data/.env.local | grep -v '^#' | xargs)
    echo "✅ 配置已加载"
else
    echo "❌ 配置文件未找到，请先运行 ./local-db-setup.sh"
    exit 1
fi

# 创建启动脚本目录
mkdir -p ./scripts

# 检查是否有现有的启动脚本
if [ ! -f "./scripts/start-local.sh" ]; then
    echo "📝 创建启动脚本..."
    cat > ./scripts/start-local.sh << 'EOF'
#!/bin/bash

# CNSH 本地服务启动脚本
cd "$(dirname "$0")/.."

# 加载环境变量
source ./data/.env.local

echo "🚀 启动 CNSH 本地服务..."

# 检查端口占用
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️ 端口 3000 已被占用，尝试终止现有进程..."
    lsof -ti:3000 | xargs kill -9
    sleep 2
fi

# 启动主服务
echo "🌟 启动 CNSH 主服务器..."
cd src && node server-fixed.js

# 如果上面的命令退出，显示错误信息
echo "❌ CNSH 服务已停止，请检查错误信息"
EOF
    chmod +x ./scripts/start-local.sh
fi

echo ""
echo "🎯 启动选项："
echo "1. 启动 CNSH 主服务 (推荐)"
echo "2. 启动并打开浏览器"
echo "3. 查看系统状态"
echo "4. 手动备份数据"
echo "5. 数据库维护"
echo "6. 退出"

read -p "请选择 (1-6): " choice

case $choice in
    1)
        echo "🚀 启动 CNSH 主服务..."
        ./scripts/start-local.sh
        ;;
    2)
        echo "🚀 启动 CNSH 并打开浏览器..."
        ./scripts/start-local.sh &
        sleep 5
        if command -v open &> /dev/null; then
            open http://localhost:3000
        elif command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:3000
        else
            echo "请手动打开: http://localhost:3000"
        fi
        ;;
    3)
        echo "📊 系统状态检查..."
        ./scripts/monitor.sh
        ;;
    4)
        echo "💾 手动备份数据..."
        ./scripts/backup.sh
        ;;
    5)
        echo "🔧 数据库维护..."
        node -e "
const db = require('./src/services/database-enhanced');
const service = new db();
service.initialize().then(() => {
    console.log('🔧 开始数据库维护...');
    return service.maintenance();
}).then(() => {
    console.log('✅ 数据库维护完成');
    process.exit(0);
}).catch(err => {
    console.error('❌ 维护失败:', err);
    process.exit(1);
});
"
        ;;
    6)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac