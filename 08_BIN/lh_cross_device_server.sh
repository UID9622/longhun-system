#!/bin/bash
# 🐉 龍魂 · 跨设备互通一键启动 (Mac端) v1.2
# DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CROSS-SERVER-V1.2-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 用途: 启动 Mac 记忆中枢 + 同步服务 + 对话桥接

set -e

# ===== 调优参数 =====
SYNC_PORT=19622
HTTP_PORT=19623
CHAT_PORT=18799
HEALTH_CHECK_INTERVAL=30
SYNC_TIMEOUT=10
RETRY_COUNT=3

# ===== 路径 =====
LONGHUN_HOME="${LONGHUN_HOME:-$HOME/longhun-system}"
# 优先仓库内同步脚本（2026-08-14 已同步 v2.0 全套入库），兼容旧 kimi 路径
XSYNC_SCRIPT="$LONGHUN_HOME/skills/longhun-cross-platform/scripts/xsync_workflow.py"
if [ ! -f "$XSYNC_SCRIPT" ]; then
    XSYNC_SCRIPT="$HOME/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py"
fi
BOOTSTRAP_SCRIPT="$HOME/.longhun/scripts/longhun_memory_bootstrap.py"
BRIDGE_SCRIPT="$LONGHUN_HOME/08_BIN/lh_xiaoyi_bridge_v2.py"
LOG_DIR="/tmp/longhun"

mkdir -p "$LOG_DIR"

echo "🐉 龍魂 · 跨设备互通服务启动 (v1.2)"
echo "========================================"

# 1. 生成记忆摘要
echo "📋 生成记忆摘要..."
if [ -f "$BOOTSTRAP_SCRIPT" ]; then
    python3 "$BOOTSTRAP_SCRIPT" > "$LOG_DIR/bootstrap.log" 2>&1 || {
        echo "⚠️ 记忆归集脚本运行异常，使用空摘要兜底"
        mkdir -p "$HOME/.longhun/memory"
        echo '{"digest":"龍魂系统初始记忆","timestamp":"'"$(date -Iseconds)"'","source":"bootstrap"}' \
            > "$HOME/.longhun/memory/latest_digest.json"
    }
else
    echo "⚠️ 记忆归集脚本不存在，创建空摘要"
    mkdir -p "$HOME/.longhun/memory"
    echo '{"digest":"龍魂系统初始记忆","timestamp":"'"$(date -Iseconds)"'","source":"bootstrap"}' \
        > "$HOME/.longhun/memory/latest_digest.json"
fi

# 2. 清理端口冲突
echo "🔧 清理端口冲突..."
for port in 8799 $SYNC_PORT $HTTP_PORT $CHAT_PORT; do
    pid=$(lsof -ti :$port 2>/dev/null || true)
    if [ -n "$pid" ]; then
        echo "  杀掉端口 $port (PID: $pid)"
        kill -9 $pid 2>/dev/null || true
    fi
done
sleep 0.5

# 3. 启动同步服务（使用 xsync_workflow.py serve）
echo "📡 启动同步服务 (端口 $SYNC_PORT)..."
python3 "$XSYNC_SCRIPT" serve \
    --port "$SYNC_PORT" \
    --timeout "$SYNC_TIMEOUT" \
    > "$LOG_DIR/sync.log" 2>&1 &
SYNC_PID=$!
echo "  同步服务 PID: $SYNC_PID"

# 4. 启动对话桥接
echo "💬 启动对话桥接 (端口 $CHAT_PORT)..."
python3 "$BRIDGE_SCRIPT" \
    --host 0.0.0.0 \
    --port "$CHAT_PORT" \
    > "$LOG_DIR/bridge.log" 2>&1 &
BRIDGE_PID=$!
echo "  桥接服务 PID: $BRIDGE_PID"

# 5. 启动健康检查
echo "❤️  启动健康检查 (间隔 ${HEALTH_CHECK_INTERVAL}s)..."
(
    while true; do
        sleep "$HEALTH_CHECK_INTERVAL"
        # 检查同步服务（TCP端口）
        if ! nc -z localhost "$SYNC_PORT" 2>/dev/null; then
            echo "$(date -Iseconds) ⚠️ TCP同步服务健康检查失败" >> "$LOG_DIR/health.log"
        fi
        # 检查HTTP同步服务
        if ! curl -s "http://localhost:$HTTP_PORT/health" > /dev/null 2>&1; then
            echo "$(date -Iseconds) ⚠️ HTTP同步服务健康检查失败" >> "$LOG_DIR/health.log"
        fi
        # 检查桥接服务（HTTP /）
        if ! curl -s "http://localhost:$CHAT_PORT/" > /dev/null 2>&1; then
            echo "$(date -Iseconds) ⚠️ 桥接服务健康检查失败" >> "$LOG_DIR/health.log"
        fi
    done
) &
HEALTH_PID=$!
echo "  健康检查 PID: $HEALTH_PID"

# 6. 输出状态
echo ""
echo "✅ 启动完成"
echo "========================================"
LAN_IP=$(ipconfig getifaddr en0 2>/dev/null || ifconfig | grep 'inet ' | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
echo "Mac 局域网 IP: ${LAN_IP:-未知}"
echo "TCP同步端口: $SYNC_PORT"
echo "HTTP同步端口: $HTTP_PORT"
echo "对话端口: $CHAT_PORT"
echo "同步日志: $LOG_DIR/sync.log"
echo "桥接日志: $LOG_DIR/bridge.log"
echo "健康日志: $LOG_DIR/health.log"
echo "========================================"
echo ""
echo "A. TCP加密同步:"
echo "  python3 $XSYNC_SCRIPT sync-memory --host $LAN_IP --port $SYNC_PORT"
echo ""
echo "B. HTTP REST同步 (鸿蒙SDK):"
echo "  GET http://$LAN_IP:$HTTP_PORT/sync/memory"
echo ""
echo "C. SSE流式对话:"
echo "  POST http://$LAN_IP:$CHAT_PORT/api/v1/chat  (stream: true)"
echo ""
echo "对话接口:"
echo "  POST http://$LAN_IP:$CHAT_PORT/api/v1/chat"
echo ""
echo "停止服务: kill $SYNC_PID $BRIDGE_PID $HEALTH_PID"
