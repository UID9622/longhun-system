#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂系统 · 开发环境一键启动
# DNA: #龍芯⚡️丙午·丙申·戊申·巳时·需-DEV-ENV-UP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════
# 用法: bash bin/start_dev_env.sh
# 功能: 同时启动门户服务器 + 操作台后端 + 可选静态文件服务
# ═══════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 颜色
GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
info() { log "${CYAN}▶${NC}  $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }

info "🐉 龍魂系统 · 开发环境一键启动"
info "   项目根: $PROJECT_ROOT"

: # set -e 安全占位

# 检查虚拟环境（不强制，全局 Python 也可运行）
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source "$PROJECT_ROOT/.venv/bin/activate" || true
    ok "已激活虚拟环境"
else
    warn "未找到 .venv，将使用全局 Python。建议先做: bash bin/setup_dev.sh"
fi

# 检查依赖
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    warn "缺少 fastapi/uvicorn，尝试安装..."
    pip install -r requirements.txt -q
fi

# 自动寻找可用端口
find_free_port() {
    local start_port=$1
    local port=$start_port
    while lsof -i :"$port" >/dev/null 2>&1 || nc -z 127.0.0.1 "$port" >/dev/null 2>&1; do
        port=$((port + 1))
    done
    echo "$port"
}

PORTAL_PORT=$(find_free_port 8777)
CP_PORT=$(find_free_port 9630)

# 启动门户（后台）
info "启动 Web 门户 :$PORTAL_PORT ..."
LONGHUN_WEB_PORT=$PORTAL_PORT LONGHUN_API_URL=http://127.0.0.1:$CP_PORT \
    python3 08_BIN/web_server.py > logs/portal.log 2>&1 &
PORTAL_PID=$!
ok "门户 PID: $PORTAL_PID → http://127.0.0.1:$PORTAL_PORT"

# 启动控制台（后台）
info "启动操作台后端 :$CP_PORT ..."
CONTROL_PANEL_PORT=$CP_PORT python3 control-panel/main.py > logs/control-panel.log 2>&1 &
CP_PID=$!
ok "控制台 PID: $CP_PID → http://127.0.0.1:$CP_PORT"

# 等待服务就绪
sleep 2

# 健康检查
if curl -s "http://127.0.0.1:$PORTAL_PORT/health" | grep -q '"ok": true'; then
    ok "门户健康检查通过"
else
    warn "门户健康检查未通过，查看 logs/portal.log"
fi

if curl -s "http://127.0.0.1:$CP_PORT/api/health" | grep -q '"status": "ok"'; then
    ok "控制台健康检查通过"
else
    warn "控制台健康检查未通过，查看 logs/control-panel.log"
fi

echo ""
echo "🐉 ========================================"
echo -e "   ${GREEN}🟢 开发环境已启动${NC}"
echo ""
echo "   门户首页:   http://127.0.0.1:$PORTAL_PORT"
echo "   控制台:     http://127.0.0.1:$CP_PORT"
echo "   门户健康:   http://127.0.0.1:$PORTAL_PORT/health"
echo "   控制台健康: http://127.0.0.1:$CP_PORT/api/health"
echo ""
echo "   停止命令:   bash bin/stop_dev_env.sh"
echo "   日志目录:   logs/"
echo "🐉 ========================================"

# 保存 PID 和端口
cat > "$PROJECT_ROOT/.dev_env.json" <<EOF
{
  "portal_pid": $PORTAL_PID,
  "portal_port": $PORTAL_PORT,
  "control_panel_pid": $CP_PID,
  "control_panel_port": $CP_PORT,
  "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
