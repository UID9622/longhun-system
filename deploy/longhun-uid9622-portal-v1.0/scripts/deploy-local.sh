#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂·本地 Kimi 一键部署
# DNA: #龍芯⚡️丙午·甲申·丁未·丙午·䷝离为火-本地部署-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 功能: 本地启动三入口门户，无需 root，Mac/Linux 直接跑

set -euo pipefail

PORT="${PORT:-8899}"
WEB_ROOT="$(cd "$(dirname "$0")/../portal" && pwd)"
LOG_FILE="/tmp/longhun-portal.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

log_info "=== 龍魂·本地门户部署 ==="
log_info "Web根: $WEB_ROOT"
log_info "端口: $PORT"

# 检查端口占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    log_warn "端口 $PORT 已被占用，尝试关闭..."
    kill $(lsof -t -i:$PORT) 2>/dev/null || true
    sleep 1
fi

# 优先用 Python3 启动
if command -v python3 &> /dev/null; then
    log_info "使用 Python3 HTTP 服务器..."
    cd "$WEB_ROOT"
    nohup python3 -m http.server $PORT > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
elif command -v python &> /dev/null; then
    log_info "使用 Python HTTP 服务器..."
    cd "$WEB_ROOT"
    nohup python -m SimpleHTTPServer $PORT > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
elif command -v node &> /dev/null; then
    log_info "使用 Node.js HTTP 服务器..."
    cd "$WEB_ROOT"
    nohup npx http-server -p $PORT -c-1 > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
else
    log_error "未找到 Python3 或 Node.js，请安装后重试"
    exit 1
fi

echo $SERVER_PID > /tmp/longhun-portal.pid
sleep 2

# 验证
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT | grep -q "200\|301"; then
    log_info "✅ 服务启动成功"
    echo ""
    echo "🐉 龍魂三入口门户:"
    echo "   普通者:   http://localhost:$PORT/index.html"
    echo "   无障碍:   http://localhost:$PORT/accessible.html"
    echo "   开发者:   http://localhost:$PORT/developer.html"
    echo ""
    echo "   日志:     tail -f $LOG_FILE"
    echo "   停止:     kill $(cat /tmp/longhun-portal.pid)"
    echo ""
    # 自动打开浏览器 (Mac)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:$PORT/index.html"
    fi
else
    log_error "服务启动失败，查看日志: $LOG_FILE"
    exit 1
fi

log_info "DNA: #龍芯⚡️丙午·甲申·丁未·丙午·䷝离为火-本地部署完成"
