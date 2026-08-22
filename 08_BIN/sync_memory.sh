#!/bin/bash
# 🐉 龍魂 · 鸿蒙端拉取记忆 v1.2
# DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CROSS-CLIENT-V1.2-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 用途: 从 Mac 记忆中枢拉取最新记忆摘要到鸿蒙本地

set -e

echo "🐉 龍魂 · 鸿蒙端拉取记忆"
echo "========================================"

MAC_IP="${1:-192.168.31.100}"
SYNC_PORT="${2:-19622}"
HTTP_PORT="${3:-19623}"
RETRY_COUNT=3
TIMEOUT=10
OUTPUT_DIR="$HOME/.longhun_memory"
OUTPUT_FILE="$OUTPUT_DIR/latest_digest.json"
# 优先仓库内同步脚本（2026-08-14 已同步 v2.0 全套入库），兼容旧 kimi 路径
LONGHUN_HOME="${LONGHUN_HOME:-$HOME/longhun-system}"
XSYNC_SCRIPT="$LONGHUN_HOME/skills/longhun-cross-platform/scripts/xsync_workflow.py"
if [ ! -f "$XSYNC_SCRIPT" ]; then
    XSYNC_SCRIPT="$HOME/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py"
fi

echo "目标 Mac: $MAC_IP"
echo "TCP同步端口: $SYNC_PORT"
echo "HTTP同步端口: $HTTP_PORT"
echo "重试次数: $RETRY_COUNT"
echo "本地存储: $OUTPUT_FILE"

mkdir -p "$OUTPUT_DIR"

# 1. 发现服务（可选，失败继续）
echo ""
echo "📡 尝试发现 Mac 服务..."
python3 "$XSYNC_SCRIPT" discover --timeout 5 2>/dev/null || {
    echo "🟡 mDNS 发现失败，使用手动 IP: $MAC_IP"
}

# 2. 拉取记忆摘要（A路径：TCP加密同步）
echo ""
echo "📋 使用 TCP+ECDH+SM4 加密同步记忆..."
python3 "$XSYNC_SCRIPT" sync-memory \
    --host "$MAC_IP" \
    --port "$SYNC_PORT" \
    --output "$OUTPUT_FILE" \
    --timeout "$TIMEOUT" \
    --retry "$RETRY_COUNT"

echo ""
echo "✅ 记忆拉取完成 (A路径 TCP加密)"
echo "记忆存储: $OUTPUT_FILE"
echo ""
echo "B路径 HTTP REST同步命令:"
echo "  curl -H 'X-LongHun-Confirm: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z' \\"
echo "       http://$MAC_IP:$HTTP_PORT/sync/memory"
echo ""
echo "C路径 SSE流式对话:"
echo "  curl -N -H 'Accept: text/event-stream' \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"prompt\":\"你好\",\"stream\":true,\"model\":\"qwen2.5:1.5b\"}' \\"
echo "       http://$MAC_IP:18799/api/v1/chat"
echo ""
echo "普通对话接口:"
echo "  POST http://$MAC_IP:18799/api/v1/chat"
