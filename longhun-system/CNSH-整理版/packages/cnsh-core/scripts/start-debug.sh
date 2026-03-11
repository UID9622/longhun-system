#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# start-debug.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-start-debug-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH 调试启动脚本

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Ollama 服务
check_ollama() {
    if ! pgrep -f "ollama serve" > /dev/null; then
        log_info "启动 Ollama 服务..."
        nohup ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
    
    if pgrep -f "ollama serve" > /dev/null; then
        log_success "Ollama 服务已运行"
    else
        log_error "Ollama 服务启动失败，请手动启动: ollama serve"
    fi
}

# 启动 CNSH 服务
start_cnsh() {
    log_info "启动 CNSH 调试模式服务..."
    
    # 设置环境变量
    export NODE_ENV=development
    export DEBUG=*
    
    # 使用修复版本的 server
    node src/server-fixed.js
}

# 主函数
main() {
    log_info "CNSH 调试模式启动中..."
    check_ollama
    start_cnsh
}

main