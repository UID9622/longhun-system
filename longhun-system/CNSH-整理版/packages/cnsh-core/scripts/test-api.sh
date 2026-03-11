#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# test-api.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-test-api-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH API 测试脚本

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 测试健康检查
test_health() {
    log_info "测试健康检查端点..."
    
    response=$(curl -s http://localhost:3000/health)
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log_success "健康检查通过"
        echo "响应: $response"
    else
        log_error "健康检查失败"
        echo "响应: $response"
    fi
    echo
}

# 测试根路径
test_root() {
    log_info "测试根路径..."
    
    response=$(curl -s http://localhost:3000/)
    
    if echo "$response" | grep -q "CNSH Server"; then
        log_success "根路径测试通过"
        echo "响应: $response"
    else
        log_error "根路径测试失败"
        echo "响应: $response"
    fi
    echo
}

# 测试文件上传
test_file_upload() {
    log_info "测试文件上传..."
    
    response=$(curl -s -X POST http://localhost:3000/api/obsidian/upload \
        -H "Content-Type: application/json" \
        -d '{"filePath":"test.md","content":"# 测试文件\\n这是一个测试文件。"}')
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log_success "文件上传测试通过"
        echo "响应: $response"
    else
        log_error "文件上传测试失败"
        echo "响应: $response"
    fi
    echo
}

# 测试 Ollama 状态
test_ollama_status() {
    log_info "测试 Ollama 状态..."
    
    response=$(curl -s http://localhost:3000/api/ollama/status)
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log_success "Ollama 状态测试通过"
        echo "响应: $response"
    else
        log_warning "Ollama 状态测试可能失败 (Ollama 可能未运行)"
        echo "响应: $response"
    fi
    echo
}

# 测试 Ollama 生成
test_ollama_generate() {
    log_info "测试 Ollama 文本生成..."
    
    response=$(curl -s -X POST http://localhost:3000/api/ollama/generate \
        -H "Content-Type: application/json" \
        -d '{"prompt":"什么是人工智能？","options":{"temperature":0.7}}')
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log_success "Ollama 文本生成测试通过"
        echo "响应: $response"
    else
        log_warning "Ollama 文本生成测试可能失败 (Ollama 可能未运行或模型未下载)"
        echo "响应: $response"
    fi
    echo
}

# 测试知识搜索
test_knowledge_search() {
    log_info "测试知识搜索..."
    
    response=$(curl -s "http://localhost:3000/api/knowledge/search?query=人工智能&limit=5")
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log_success "知识搜索测试通过"
        echo "响应: $response"
    else
        log_error "知识搜索测试失败"
        echo "响应: $response"
    fi
    echo
}

# 检查服务器是否运行
check_server() {
    log_info "检查服务器状态..."
    
    if curl -s http://localhost:3000/health > /dev/null; then
        log_success "服务器正在运行"
        return 0
    else
        log_error "服务器未运行，请先启动服务器"
        echo "运行命令: ./start-debug.sh"
        return 1
    fi
}

# 主测试函数
main() {
    echo "============================================"
    echo "    CNSH API 测试脚本"
    echo "============================================"
    echo
    
    # 检查服务器是否运行
    if ! check_server; then
        exit 1
    fi
    
    # 运行测试
    test_health
    test_root
    test_file_upload
    test_ollama_status
    test_ollama_generate
    test_knowledge_search
    
    echo "============================================"
    echo "    测试完成"
    echo "============================================"
}

# 运行主函数
main