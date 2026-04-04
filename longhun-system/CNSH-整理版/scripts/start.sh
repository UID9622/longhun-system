#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# start.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-start-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH 启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[信息]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

# 检查 Ollama
check_ollama() {
    if command -v ollama >/dev/null 2>&1; then
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            print_success "Ollama 服务正在运行"
            return 0
        else
            print_warning "Ollama 已安装但未运行"
            print_info "正在启动 Ollama..."
            ollama serve &
            sleep 3
            if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
                print_success "Ollama 启动成功"
                return 0
            else
                print_error "Ollama 启动失败"
                return 1
            fi
        fi
    else
        print_warning "Ollama 未安装，AI 功能将不可用"
        return 1
    fi
}

# 启动核心服务
start_core() {
    print_info "启动 CNSH 核心服务..."
    
    if [ -d "packages/cnsh-core" ]; then
        cd packages/cnsh-core
        
        if [ -f "package.json" ]; then
            npm start &
            CNSH_PID=$!
            cd ../..
            
            # 等待服务启动
            sleep 2
            
            if curl -s http://localhost:3000/api/health >/dev/null 2>&1; then
                print_success "CNSH 核心服务已启动 (PID: $CNSH_PID)"
                echo $CNSH_PID > .cnsh.pid
            else
                print_error "CNSH 核心服务启动失败"
                exit 1
            fi
        else
            print_error "未找到 package.json"
            exit 1
        fi
    else
        print_error "未找到 cnsh-core 目录"
        exit 1
    fi
}

# 启动编辑器（可选）
start_editor() {
    print_info "启动字元编辑器..."
    
    if [ -d "packages/cnsh-editor" ]; then
        cd packages/cnsh-editor
        
        # 使用 Python 启动简单服务器
        if command -v python3 >/dev/null 2>&1; then
            python3 -m http.server 8080 &
            EDITOR_PID=$!
            cd ../..
            
            sleep 1
            print_success "字元编辑器已启动: http://localhost:8080"
            echo $EDITOR_PID > .editor.pid
        else
            print_warning "Python3 未安装，无法启动编辑器服务器"
            print_info "你可以直接打开: packages/cnsh-editor/快速启动.html"
        fi
    fi
}

# 打印状态
print_status() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🐉 CNSH 龍魂体系 已启动                                   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "服务地址:"
    echo "  • CNSH API:     http://localhost:3000"
    echo "  • 字元编辑器:   http://localhost:8080"
    echo ""
    echo "常用命令:"
    echo "  • 查看日志:     tail -f logs/cnsh.log"
    echo "  • 停止服务:     ./scripts/stop.sh"
    echo ""
    echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
    echo ""
}

# 清理函数
cleanup() {
    echo ""
    print_info "正在停止服务..."
    
    if [ -f ".cnsh.pid" ]; then
        kill $(cat .cnsh.pid) 2>/dev/null || true
        rm .cnsh.pid
    fi
    
    if [ -f ".editor.pid" ]; then
        kill $(cat .editor.pid) 2>/dev/null || true
        rm .editor.pid
    fi
    
    print_success "服务已停止"
    exit 0
}

# 设置信号处理
trap cleanup INT TERM

# 主函数
main() {
    # 检查是否在项目根目录
    if [ ! -f "README.md" ] || [ ! -d "packages" ]; then
        print_error "请在 CNSH 项目根目录运行此脚本"
        exit 1
    fi
    
    check_ollama || true
    start_core
    start_editor || true
    print_status
    
    # 保持运行
    while true; do
        sleep 1
    done
}

main "$@"
