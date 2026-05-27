#!/bin/bash

# CNSH 翻译系统启动脚本
# DNA: #龍芯⚡️2026-05-27-START-CNSH-v1.0
# 用法: ./start_cnsh.sh [start|stop|status|logs|restart]

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_DIR="$HOME/.cnsh/logs"
PID_FILE="$HOME/.cnsh/cnsh_translator.pid"
ENV_FILE="$HOME/.cnsh/config/.env"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# 函数定义
# ============================================================================

log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}${1}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

check_environment() {
    log_header "🔍 环境检查"

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        return 1
    fi
    log_info "Python: $(python3 --version)"

    # 检查虚拟环境
    if [ ! -d "$SCRIPT_DIR/venv" ]; then
        log_warn "虚拟环境不存在·创建中..."
        python3 -m venv "$SCRIPT_DIR/venv"
        log_info "虚拟环境已创建"
    fi

    # 检查配置文件
    if [ ! -f "$ENV_FILE" ]; then
        log_warn "配置文件 $ENV_FILE 不存在"
        log_info "请复制 .env.template 为 .env 并填入配置"
        return 1
    fi
    log_info "配置文件已找到"

    # 检查日志目录
    mkdir -p "$LOG_DIR"
    log_info "日志目录: $LOG_DIR"

    return 0
}

start_service() {
    log_header "🚀 启动 CNSH 翻译系统"

    # 检查环境
    if ! check_environment; then
        log_error "环境检查失败"
        return 1
    fi

    # 检查是否已经运行
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            log_error "系统已在运行 (PID: $PID)"
            return 1
        else
            log_warn "发现旧的 PID 文件·清理中..."
            rm "$PID_FILE"
        fi
    fi

    # 激活虚拟环境
    source "$SCRIPT_DIR/venv/bin/activate"
    log_info "虚拟环境已激活"

    # 安装依赖（如果需要）
    if [ ! -f "$SCRIPT_DIR/venv/lib/python*/site-packages/dotenv" ]; then
        log_warn "安装依赖中..."
        pip install -q -r "$SCRIPT_DIR/requirements_cnsh.txt"
        log_info "依赖已安装"
    fi

    # 后台启动系统
    log_info "启动后台进程..."
    nohup python3 "$SCRIPT_DIR/cnsh_translator_complete.py" \
        >> "$LOG_DIR/cnsh_translator.log" 2>&1 &

    NEW_PID=$!
    echo $NEW_PID > "$PID_FILE"

    # 等待进程启动
    sleep 2

    if ps -p $NEW_PID > /dev/null 2>&1; then
        log_info "系统已启动 (PID: $NEW_PID)"
        log_info "日志位置: $LOG_DIR/cnsh_translator.log"
        log_info ""
        log_info "实时查看日志: tail -f $LOG_DIR/cnsh_translator.log"
        return 0
    else
        log_error "系统启动失败·检查日志"
        tail -20 "$LOG_DIR/cnsh_translator.log"
        return 1
    fi
}

stop_service() {
    log_header "🛑 停止 CNSH 翻译系统"

    if [ ! -f "$PID_FILE" ]; then
        log_error "系统未运行"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if ! ps -p $PID > /dev/null 2>&1; then
        log_error "进程不存在 (PID: $PID)"
        rm "$PID_FILE"
        return 1
    fi

    log_info "关闭进程 (PID: $PID)..."
    kill $PID

    # 等待进程关闭
    sleep 2

    # 强制关闭（如果仍在运行）
    if ps -p $PID > /dev/null 2>&1; then
        log_warn "正常关闭超时·强制关闭..."
        kill -9 $PID
    fi

    rm "$PID_FILE"
    log_info "系统已停止"
    return 0
}

check_status() {
    log_header "📊 系统状态"

    if [ ! -f "$PID_FILE" ]; then
        log_error "系统未运行"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if ps -p $PID > /dev/null 2>&1; then
        log_info "系统运行正常"
        log_info "PID: $PID"
        log_info ""

        # 显示进程信息
        ps aux | grep -E "PID|$PID" | grep -v grep

        log_info ""
        log_info "最近日志:"
        tail -10 "$LOG_DIR/cnsh_translator.log" | sed 's/^/  /'

        return 0
    else
        log_error "系统已崩溃 (PID: $PID)"
        log_info ""
        log_info "错误日志:"
        tail -20 "$LOG_DIR/cnsh_translator.log" | sed 's/^/  /'
        rm "$PID_FILE"
        return 1
    fi
}

show_logs() {
    log_header "📋 实时日志"

    if [ ! -f "$LOG_DIR/cnsh_translator.log" ]; then
        log_error "日志文件不存在"
        return 1
    fi

    tail -f "$LOG_DIR/cnsh_translator.log"
}

restart_service() {
    log_header "♻️ 重启 CNSH 翻译系统"

    stop_service
    sleep 3
    start_service
}

show_help() {
    cat << EOF
CNSH 翻译系统启动脚本

用法: $0 [命令]

命令:
  start       启动系统
  stop        停止系统
  restart     重启系统
  status      查看状态
  logs        实时日志
  help        显示帮助

示例:
  $0 start              # 启动系统
  $0 status             # 查看运行状态
  $0 logs               # 查看实时日志
  $0 stop               # 停止系统

快速参考:
  检查日志路径: ~/.cnsh/logs/cnsh_translator.log
  配置文件路径: ~/.cnsh/config/.env
  PID 文件路径: ~/.cnsh/cnsh_translator.pid

DNA: #龍芯⚡️2026-05-27-START-CNSH-v1.0
EOF
}

# ============================================================================
# 主逻辑
# ============================================================================

case "${1:-start}" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "未知命令: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

exit $?
