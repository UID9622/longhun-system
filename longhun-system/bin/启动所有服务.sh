#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 启动所有服务 · 后台静默运行
# DNA: #龍芯⚡️2026-03-31-启动所有服务-v3.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师
# 触发词：龍 / 龍吟 / 籠吟
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOG_DIR="$HOME/longhun-system/运行日志"
SCAN_REPORT="$LOG_DIR/服务扫描报告.log"
mkdir -p "$LOG_DIR"

通知() {
    osascript -e "display notification \"$2\" with title \"🐉 龍魂\" subtitle \"$1\"" 2>/dev/null
}

# ══════════════════════════════════════════
# 预扫描：检测所有已知端口状态 + 识别新进程
# ══════════════════════════════════════════
预扫描() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🔍 预扫描 · $(date '+%Y-%m-%d %H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # 已知端口表（端口:服务名:是否受管理）
    declare -A KNOWN_PORTS
    KNOWN_PORTS[9622]="CNSH-64 Governance Engine:managed"
    KNOWN_PORTS[8000]="CNSH MVP v2.0:managed"
    KNOWN_PORTS[8080]="Open WebUI:managed"
    KNOWN_PORTS[11434]="Ollama:managed"
    KNOWN_PORTS[8765]="龍魂本地服务:managed"
    KNOWN_PORTS[9623]="龍魂MCP服务器:managed"
    KNOWN_PORTS[8089]="Locust压测:zombie"   # 这个是僵尸，要杀

    WARN_COUNT=0
    ZOMBIE_COUNT=0

    # 扫描所有当前监听端口
    while IFS= read -r PORT; do
        [ -z "$PORT" ] && continue
        if [[ -n "${KNOWN_PORTS[$PORT]}" ]]; then
            TYPE="${KNOWN_PORTS[$PORT]##*:}"
            NAME="${KNOWN_PORTS[$PORT]%%:*}"
            if [ "$TYPE" = "zombie" ]; then
                echo "  🔴 :$PORT  $NAME → 僵尸，将清理"
                ((ZOMBIE_COUNT++))
            fi
        else
            # 未知端口，获取进程名
            PROC=$(lsof -i :$PORT -sTCP:LISTEN 2>/dev/null | awk 'NR==2{print $1}')
            echo "  🟡 :$PORT  未登记端口 (进程: ${PROC:-未知}) → 不干预，仅报告"
            echo "$(date '+%Y-%m-%d %H:%M:%S') 未知端口 :$PORT 进程:${PROC:-?}" >> "$SCAN_REPORT"
            ((WARN_COUNT++))
        fi
    done < <(lsof -iTCP -sTCP:LISTEN -P -n 2>/dev/null | awk 'NR>1{match($9, /:([0-9]+)$/, a); if(a[1]!="") print a[1]}' | sort -nu)

    if [ $WARN_COUNT -gt 0 ]; then
        echo ""
        echo "  ⚠️  发现 $WARN_COUNT 个未登记端口，已记录到:"
        echo "       $SCAN_REPORT"
    fi
    if [ $ZOMBIE_COUNT -eq 0 ] && [ $WARN_COUNT -eq 0 ]; then
        echo "  ✅ 环境干净，无异常"
    fi
    echo ""
}

预扫描

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 启动所有服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 0. 清理僵尸进程 ──
for ZOMBIE_PORT in 8089; do
    if lsof -ti :$ZOMBIE_PORT > /dev/null 2>&1; then
        kill $(lsof -ti :$ZOMBIE_PORT) 2>/dev/null
        echo "  🧹 清理僵尸端口 :$ZOMBIE_PORT"
    fi
done

# ── 1. 龍魂本地服务 (8765) ──
if lsof -i :8765 > /dev/null 2>&1; then
    echo "  ✅ 龍魂本地服务 · 已在运行"
else
    SERVICE="$HOME/longhun-system/longhun_local_service.py"
    if [ -f "$SERVICE" ]; then
        nohup python3 "$SERVICE" > "$LOG_DIR/服务输出.log" 2>&1 &
        sleep 3
        if lsof -i :8765 > /dev/null 2>&1; then
            echo "  ✅ 龍魂本地服务 · 启动成功 (8765)"
        else
            echo "  🟡 龍魂本地服务 · 启动中，稍等..."
        fi
    else
        echo "  ⚪ longhun_local_service.py 不存在，跳过"
    fi
fi

# ── 2. Ollama 模型服务 ──
if lsof -i :11434 > /dev/null 2>&1; then
    echo "  ✅ Ollama · 已在运行"
else
    if command -v ollama &>/dev/null; then
        nohup ollama serve > "$LOG_DIR/ollama输出.log" 2>&1 &
        sleep 2
        echo "  ✅ Ollama · 已启动"
    else
        echo "  ⚠️  Ollama 未安装，跳过"
    fi
fi

# ── 3. CNSH-64 Governance Engine (9622) ──
CNSH_CORE="$HOME/longhun-system/cnsh-core"
if lsof -i :9622 > /dev/null 2>&1; then
    if curl -s --max-time 2 http://127.0.0.1:9622/persona/stats > /dev/null 2>&1; then
        echo "  ✅ CNSH-64 Governance · 已在运行 (9622)"
    else
        echo "  🔄 CNSH-64 端口占用但无响应，重启..."
        kill $(lsof -ti :9622) 2>/dev/null
        sleep 1
        cd "$CNSH_CORE" && nohup python3 -m uvicorn api.main:app --host 127.0.0.1 --port 9622 --log-level warning > "$LOG_DIR/cnsh9622.log" 2>&1 &
        sleep 2
        echo "  ✅ CNSH-64 Governance · 重启完成 (9622)"
    fi
elif [ -d "$CNSH_CORE" ]; then
    cd "$CNSH_CORE" && nohup python3 -m uvicorn api.main:app --host 127.0.0.1 --port 9622 --log-level warning > "$LOG_DIR/cnsh9622.log" 2>&1 &
    sleep 2
    if lsof -i :9622 > /dev/null 2>&1; then
        echo "  ✅ CNSH-64 Governance · 启动成功 (9622)"
    else
        echo "  🔴 CNSH-64 启动失败 · 查看 logs/cnsh9622.log"
    fi
else
    echo "  ⚪ cnsh-core 目录不存在，跳过"
fi

# ── 4. Open WebUI ──
OPENWEBUI="/Library/Frameworks/Python.framework/Versions/3.11/bin/open-webui"
if lsof -i :8080 > /dev/null 2>&1; then
    echo "  ✅ Open WebUI · 已在运行 (8080)"
elif [ -f "$OPENWEBUI" ]; then
    nohup "$OPENWEBUI" serve > "$LOG_DIR/openwebui输出.log" 2>&1 &
    sleep 3
    if lsof -i :8080 > /dev/null 2>&1; then
        echo "  ✅ Open WebUI · 启动成功 (8080)"
    else
        echo "  🟡 Open WebUI · 启动中，稍等..."
    fi
else
    echo "  ⚪ open-webui 未找到，跳过"
fi

# ── 5. 龍魂MCP服务器 (9623) ──
if lsof -i :9623 > /dev/null 2>&1; then
    echo "  ✅ 龍魂MCP服务器 · 已在运行 (9623)"
else
    PYTHON311="/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"
    MCP_SERVER="$HOME/longhun-system/core/mcp_server.py"
    if [ -f "$MCP_SERVER" ] && [ -f "$PYTHON311" ]; then
        nohup "$PYTHON311" "$MCP_SERVER" --sse > "$LOG_DIR/mcp_server.log" 2>&1 &
        echo $! > "$LOG_DIR/mcp_server.pid"
        sleep 2
        if lsof -i :9623 > /dev/null 2>&1; then
            echo "  ✅ 龍魂MCP服务器 · 启动成功 (9623)"
        else
            echo "  🟡 龍魂MCP服务器 · 启动中，稍等..."
        fi
    else
        echo "  ⚪ MCP服务器文件不完整，跳过"
    fi
fi

# ══════════════════════════════════════════
# 最终状态汇总
# ══════════════════════════════════════════
echo ""
echo "  ┌─────────────────────────────────────┐"
echo "  │         龍魂服务状态一览             │"
echo "  ├──────────┬──────────────────────────┤"

状态行() {
    local PORT=$1 NAME=$2
    if lsof -i :$PORT > /dev/null 2>&1; then
        printf "  │  🟢 %-6s│ %-24s │\n" ":$PORT" "$NAME"
    else
        printf "  │  🔴 %-6s│ %-24s │\n" ":$PORT" "$NAME (未运行)"
    fi
}

状态行 9622 "CNSH-64 主API"
状态行 8000 "CNSH MVP v2.0"
状态行 8080 "Open WebUI"
状态行 11434 "Ollama"
状态行 8765 "龍魂本地服务"
状态行 9623 "龍魂MCP服务器"

echo "  └──────────┴──────────────────────────┘"

通知 "服务启动完成" "龍魂服务已在后台运行"
echo ""
echo "  ✅ 完成 · DNA: #龍芯⚡️$(date +%Y%m%d)-启动-UID9622"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
