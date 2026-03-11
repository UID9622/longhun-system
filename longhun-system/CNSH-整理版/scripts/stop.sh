#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# stop.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-stop-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH 停止脚本

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[信息]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_info "正在停止 CNSH 服务..."

# 停止核心服务
if [ -f ".cnsh.pid" ]; then
    PID=$(cat .cnsh.pid)
    if kill $PID 2>/dev/null; then
        print_success "CNSH 核心服务已停止 (PID: $PID)"
    fi
    rm .cnsh.pid
fi

# 停止编辑器服务
if [ -f ".editor.pid" ]; then
    PID=$(cat .editor.pid)
    if kill $PID 2>/dev/null; then
        print_success "字元编辑器服务已停止 (PID: $PID)"
    fi
    rm .editor.pid
fi

# 停止 Ollama (可选，通常保持运行)
# pkill -f "ollama serve" 2>/dev/null || true

print_success "所有服务已停止"
