#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# 龍魂系统 · 统一采集启动器 v3.0
# 一键拉起：采集服务 + 数据中台 + 打开看板
# DNA: #龍芯⚡️丙午·乙申·LAUNCHER-v3.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# UID9622
# ============================================================
set -e

PROJECT="$HOME/longhun-system"
COLLECTOR="$PROJECT/extensions/longhun-collector/longhun-collector.py"
DASHBOARD_URL="http://localhost:9622/dashboard"
PID_FILE="$PROJECT/var/collector.pid"
LOG_FILE="$PROJECT/logs/collector.log"

mkdir -p "$PROJECT/logs" "$PROJECT/var"

echo "🐉 龍魂统一采集器 v3.0 启动..."
echo ""

# ---- 1. 检查/启动采集服务 ----
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "✅ 采集服务已在运行 (PID: $OLD_PID)"
    else
        rm -f "$PID_FILE"
        START_SERVICE=1
    fi
else
    START_SERVICE=1
fi

if [ -n "$START_SERVICE" ]; then
    echo "🚀 启动采集服务..."
    nohup python3 "$COLLECTOR" >> "$LOG_FILE" 2>&1 &
    NEW_PID=$!
    echo $NEW_PID > "$PID_FILE"
    sleep 2
    
    if kill -0 "$NEW_PID" 2>/dev/null; then
        echo "✅ 采集服务已启动 (PID: $NEW_PID)"
    else
        echo "❌ 采集服务启动失败，查看日志: $LOG_FILE"
        exit 1
    fi
fi

# ---- 2. 健康检查 ----
echo "🔍 健康检查..."
if curl -s http://localhost:9622/health > /dev/null 2>&1; then
    echo "✅ 服务健康"
else
    echo "⚠️ 服务无响应"
fi

echo ""
echo "============================================"
echo "🐉 龍魂统一采集系统 v3.0 就绪"
echo ""
echo "📊 看板:   $DASHBOARD_URL"
echo "📡 中台:   $PROJECT/scripts/龍魂数据中台采集器.py --sync"
echo "🔧 扩展:   extensions/longhun-collector/ → Chrome加载"
echo "📁 数据:   $PROJECT/data/collector/raw/"
echo "============================================"
echo ""

# ---- 3. 自动打开看板 ----
if command -v open &>/dev/null; then
    open "$DASHBOARD_URL"
    echo "🌐 看板已在浏览器中打开"
fi

# ---- 4. 可选：自动运行一次数据中台 ----
if [ "${1:-}" = "--full" ]; then
    echo ""
    echo "📡 运行数据中台采集（首次全量）..."
    python3 "$PROJECT/scripts/龍魂数据中台采集器.py" --sync
    echo "✅ 数据中台采集完成"
fi
