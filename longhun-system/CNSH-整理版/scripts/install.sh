#!/bin/bash

# CNSH 安装脚本
# 支持 macOS、Linux 系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
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

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 打印 banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║   🐉 CNSH 龙魂体系 - 安装脚本                              ║"
    echo "║   Chinese-native Scripting & Heritage                      ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 检查系统要求
check_requirements() {
    print_info "检查系统要求..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
    else
        print_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
    
    print_success "检测到操作系统: $OS"
    
    # 检查 Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version | cut -d'v' -f2)
        print_success "Node.js 已安装: v$NODE_VERSION"
    else
        print_warning "Node.js 未安装，请先安装 Node.js v18+"
        echo "  macOS: brew install node"
        echo "  Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs"
        exit 1
    fi
    
    # 检查 Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python 已安装: v$PYTHON_VERSION"
    else
        print_warning "Python3 未安装，请先安装 Python 3.8+"
        exit 1
    fi
    
    # 检查 Ollama
    if command_exists ollama; then
        OLLAMA_VERSION=$(ollama --version 2>/dev/null || echo "未知")
        print_success "Ollama 已安装: $OLLAMA_VERSION"
    else
        print_warning "Ollama 未安装，建议安装以获得完整功能"
        echo "  安装命令: curl -fsSL https://ollama.ai/install.sh | sh"
    fi
    
    echo ""
}

# 安装 Node.js 依赖
install_node_deps() {
    print_info "安装 Node.js 依赖..."
    
    if [ -d "packages/cnsh-core" ]; then
        cd packages/cnsh-core
        
        if [ -f "package.json" ]; then
            npm install
            print_success "Node.js 依赖安装完成"
        else
            print_warning "未找到 package.json，跳过 Node.js 依赖安装"
        fi
        
        cd ../..
    else
        print_warning "未找到 cnsh-core 目录，跳过 Node.js 依赖安装"
    fi
    
    echo ""
}

# 安装 Python 依赖
install_python_deps() {
    print_info "安装 Python 依赖..."
    
    if [ -d "packages/cnsh-core" ]; then
        cd packages/cnsh-core
        
        if [ -f "requirements.txt" ]; then
            pip3 install -r requirements.txt
            print_success "Python 依赖安装完成"
        else
            print_warning "未找到 requirements.txt，跳过 Python 依赖安装"
        fi
        
        cd ../..
    else
        print_warning "未找到 cnsh-core 目录，跳过 Python 依赖安装"
    fi
    
    echo ""
}

# 创建必要目录
create_directories() {
    print_info "创建必要目录..."
    
    mkdir -p data
    mkdir -p logs
    mkdir -p examples/glyphs
    
    print_success "目录创建完成"
    echo ""
}

# 设置环境变量
setup_env() {
    print_info "设置环境变量..."
    
    if [ -d "packages/cnsh-core" ]; then
        cd packages/cnsh-core
        
        if [ ! -f ".env" ] && [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "环境变量文件已创建 (.env)"
            print_info "请编辑 .env 文件配置你的设置"
        fi
        
        cd ../..
    fi
    
    echo ""
}

# 下载推荐模型
download_models() {
    print_info "检查 Ollama 模型..."
    
    if command_exists ollama; then
        # 检查 qwen 模型
        if ollama list | grep -q "qwen"; then
            print_success "qwen 模型已安装"
        else
            print_info "正在下载 qwen:7b-chat 模型（可能需要几分钟）..."
            ollama pull qwen:7b-chat || print_warning "模型下载失败，请稍后手动运行: ollama pull qwen:7b-chat"
        fi
    else
        print_warning "Ollama 未安装，跳过模型下载"
    fi
    
    echo ""
}

# 打印完成信息
print_completion() {
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║   🎉 CNSH 安装完成！                                        ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "使用方法:"
    echo "  1. 启动服务:    ./scripts/start.sh"
    echo "  2. 打开编辑器:  open packages/cnsh-editor/快速启动.html"
    echo "  3. 查看文档:    open docs/使用手册.md"
    echo ""
    echo "更多信息请参阅:"
    echo "  - docs/安装指南.md"
    echo "  - docs/使用手册.md"
    echo ""
    echo -e "${YELLOW}DNA追溯: #龍芯⚡️-CNSH-CORE-0001${NC}"
    echo ""
}

# 主函数
main() {
    print_banner
    
    # 检查是否在项目根目录
    if [ ! -f "README.md" ] || [ ! -d "packages" ]; then
        print_error "请在 CNSH 项目根目录运行此脚本"
        exit 1
    fi
    
    check_requirements
    create_directories
    install_node_deps
    install_python_deps
    setup_env
    download_models
    print_completion
}

# 运行主函数
main "$@"
