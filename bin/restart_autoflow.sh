#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂·AutoFlow 后端服务 重启脚本                           ║
# ║  DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-AUTOFLOW-RESTART        ║
# ╚═══════════════════════════════════════════════════════════════╝

PORT=${1:-8766}
HOST=${2:-127.0.0.1}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🐉 龍魂·AutoFlow 后端服务重启"
echo "   项目: $PROJECT_ROOT"
echo "   端口: $HOST:$PORT"
echo ""

# 1. 停止旧进程
OLD_PID=$(lsof -tiTCP:$PORT -sTCP:LISTEN 2>/dev/null)
if [ -n "$OLD_PID" ]; then
    echo "⏹  停止旧进程 (PID: $OLD_PID)..."
    kill $OLD_PID 2>/dev/null
    sleep 1
    # 如果还在，强杀
    if kill -0 $OLD_PID 2>/dev/null; then
        kill -9 $OLD_PID 2>/dev/null
        echo "   强杀完成"
    fi
fi

# 2. 启动新进程
echo "▶️  启动 AutoFlow 后端..."
cd "$PROJECT_ROOT"
nohup python3 bin/lh_autoflow.py --serve --port $PORT --host $HOST \
    > logs/autoflow_server.log 2>&1 &
NEW_PID=$!
echo "   PID: $NEW_PID"
echo "   API: http://$HOST:$PORT"
echo "   Docs: http://$HOST:$PORT/docs"

# 3. 等2秒验证健康
sleep 2
if curl -s http://$HOST:$PORT/health > /dev/null 2>&1; then
    echo ""
    echo "✅ 后端启动成功！"
    curl -s http://$HOST:$PORT/health | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'   引擎: {d[\"engine\"]} v{d[\"version\"]}')
print(f'   模式: {d[\"mode\"]}')
print(f'   路由: {d[\"routes_count\"]} | 闸口: {d[\"gates_count\"]}')
print(f'   否决词: {d[\"veto_words_count\"]} | GPG: {\"可用\" if d[\"gpg_available\"] else \"离线\"}')
"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  快速测试:"
    echo "  curl -X POST http://$HOST:$PORT/api/dry-run \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"task\":\"帮我写个脚本\"}'"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo ""
    echo "❌ 启动失败，查看日志:"
    tail -20 logs/autoflow_server.log
fi
