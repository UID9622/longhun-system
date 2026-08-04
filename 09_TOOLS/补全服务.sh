#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂核心服务补全脚本
# DNA: #龍芯⚡️2026-07-05-LONGHUN-SERVICE-FIX-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 作用：把 lh 状态 里未运行的核心服务补起来，或明确标记为占位

set -euo pipefail

HOME_DIR="$HOME"
LONGHUN_ROOT="$HOME_DIR/longhun-system"
LOG_DIR="$LONGHUN_ROOT/logs"
mkdir -p "$LOG_DIR"

# 優先使用 Homebrew Python 3.12（已裝 fastapi/uvicorn）
PY3="/opt/homebrew/bin/python3.12"
if [ ! -x "$PY3" ]; then
    PY3="python3"
fi

echo "🔧 龍魂核心服务补全开始...（使用 $PY3）"

# 1. 操作台 :9622（用 http.server 托管 web/p0-controls）
if lsof -Pi :9622 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ 操作台 :9622 已在运行"
else
    echo "▶ 启动操作台 :9622（http.server 托管 web/p0-controls）"
    cd "$LONGHUN_ROOT/web/p0-controls"
    nohup python3 -m http.server 9622 --bind 127.0.0.1 > "$LOG_DIR/console-9622.out.log" 2> "$LOG_DIR/console-9622.err.log" &
    sleep 1
    if lsof -Pi :9622 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 操作台 :9622 已启动 (PID: $(lsof -Pi :9622 -sTCP:LISTEN -t))"
    else
        echo "🔴 操作台 :9622 启动失败，查看 $LOG_DIR/console-9622.err.log"
        exit 1
    fi
fi

# 2. 卦象审计 :9623（通过 launchctl 重启）
if lsof -Pi :9623 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ 卦象审计 :9623 已在运行"
else
    echo "▶ 重启卦象审计 :9623"
    # 先杀掉可能卡住的旧进程
    pkill -f "gua_audit_daemon.py" 2>/dev/null || true
    sleep 2
    # 确保端口释放
    for i in {1..10}; do
        if ! lsof -Pi :9623 -sTCP:LISTEN -t >/dev/null 2>&1; then
            break
        fi
        echo "  等待 :9623 端口释放... ($i/10)"
        sleep 1
    done
    # 用 launchctl 启动
    launchctl start com.longhun.gua-audit || true
    sleep 2
    if lsof -Pi :9623 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 卦象审计 :9623 已启动 (PID: $(lsof -Pi :9623 -sTCP:LISTEN -t))"
    else
        echo "🔴 卦象审计 :9623 启动失败，查看 $LOG_DIR/gua_audit_daemon.err.log"
        exit 1
    fi
fi

echo ""
# 3. CNSH Editor API :18000
if lsof -Pi :18000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ CNSH Editor API :18000 已在运行"
else
    echo "▶ 启动 CNSH Editor API :18000"
    pkill -f "cnsh_editor_api.main" 2>/dev/null || true
    sleep 1
    cd "$LONGHUN_ROOT/integrated-modules"
    PYTHONPATH="$LONGHUN_ROOT/integrated-modules:$LONGHUN_ROOT/dev-env/chinese-editor/src" \
        CNSH_API_PORT=18000 CNSH_API_HOST=127.0.0.1 \
        nohup "$PY3" -m cnsh_editor_api.main > "$LOG_DIR/cnsh_editor_api-18000.out.log" 2> "$LOG_DIR/cnsh_editor_api-18000.err.log" &
    sleep 3
    if lsof -Pi :18000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ CNSH Editor API :18000 已启动 (PID: $(lsof -Pi :18000 -sTCP:LISTEN -t))"
    else
        echo "🔴 CNSH Editor API :18000 启动失败，查看 $LOG_DIR/cnsh_editor_api-18000.err.log"
        exit 1
    fi
fi

echo ""
# 4. L0 道德經倫理錨定引擎 :9630
if lsof -Pi :9630 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ L0 道德經倫理錨定引擎 :9630 已在运行"
else
    echo "▶ 启动 L0 道德經倫理錨定引擎 :9630"
    pkill -f "dao_ethics_anchor_v2.py" 2>/dev/null || true
    sleep 1
    cd "$LONGHUN_ROOT"
    nohup "$PY3" "$LONGHUN_ROOT/tools/dao_ethics_anchor_v2.py" --api --api-port 9630 \
        > "$LOG_DIR/dao-ethics-9630.out.log" 2> "$LOG_DIR/dao-ethics-9630.err.log" &
    sleep 2
    if lsof -Pi :9630 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ L0 道德經倫理錨定引擎 :9630 已启动 (PID: $(lsof -Pi :9630 -sTCP:LISTEN -t))"
    else
        echo "🔴 L0 道德經倫理錨定引擎 :9630 启动失败，查看 $LOG_DIR/dao-ethics-9630.err.log"
        exit 1
    fi
fi

echo ""
# 5. 龍魂门户本地预览服务器 :8777（模拟 Nginx，代理 /editor/ /docs 等到 18000）
if lsof -Pi :8777 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ 龍魂门户服务器 :8777 已在运行"
else
    echo "▶ 启动龍魂门户服务器 :8777"
    pkill -f "longhun_portal_server.py" 2>/dev/null || true
    sleep 1
    cd "$LONGHUN_ROOT/portal"
    nohup "$PY3" ../tools/longhun_portal_server.py > "$LOG_DIR/portal-server-8777.out.log" 2> "$LOG_DIR/portal-server-8777.err.log" &
    sleep 3
    if lsof -Pi :8777 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 龍魂门户服务器 :8777 已启动 (PID: $(lsof -Pi :8777 -sTCP:LISTEN -t))"
    else
        echo "🔴 龍魂门户服务器 :8777 启动失败，查看 $LOG_DIR/portal-server-8777.err.log"
        exit 1
    fi
fi

# 6. 龍魂神经网络路由 · 实时状态总控 :9627
if lsof -Pi :9627 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ 神经网络状态总控 :9627 已在运行"
else
    echo "▶ 启动神经网络状态总控 :9627"
    nohup python3 "$LONGHUN_ROOT/tools/longhun_neural_network_server.py" \
        > "$LOG_DIR/neural-network-server.out.log" \
        2> "$LOG_DIR/neural-network-server.err.log" &
    sleep 2
    if lsof -Pi :9627 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 神经网络状态总控 :9627 已启动 (PID: $(lsof -Pi :9627 -sTCP:LISTEN -t))"
    else
        echo "🔴 神经网络状态总控 :9627 启动失败，查看 $LOG_DIR/neural-network-server.err.log"
    fi
fi

echo ""
# 7. Cloudflare Tunnel for longhun888.com（尽力而为，网络波动时不阻断）
if pgrep -f "cloudflared tunnel --config.*longhun888.yml" >/dev/null 2>&1; then
    echo "✅ Cloudflare Tunnel longhun888 已在运行"
else
    echo "▶ 启动 Cloudflare Tunnel longhun888（指向 :8777）"
    nohup cloudflared tunnel --config "$HOME/.cloudflared/longhun888.yml" run > "$LOG_DIR/cloudflared-longhun888.out.log" 2>&1 &
    sleep 8
    if pgrep -f "cloudflared tunnel --config.*longhun888.yml" >/dev/null 2>&1; then
        echo "✅ Cloudflare Tunnel longhun888 已启动（DNS 传播可能需要 1-5 分钟）"
    else
        echo "🟡 Cloudflare Tunnel 启动异常，可能是网络抖动，查看 $LOG_DIR/cloudflared-longhun888.out.log"
    fi
fi

echo ""
echo "✅ 补全完成。访问：https://longhun888.com/（DNS 缓存刷新后）或 http://127.0.0.1:8777/"
echo "🧠 神经网络实时总控：http://127.0.0.1:9627/"
