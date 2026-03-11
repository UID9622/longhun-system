#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# install.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-install-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH 本地部署安装脚本
# 自动安装和配置 Obsidian + Ollama 集成系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 安装 Homebrew (macOS)
install_homebrew() {
    if check_command brew; then
        log_info "Homebrew 已安装"
    else
        log_info "正在安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        log_success "Homebrew 安装完成"
    fi
}

# 安装 Node.js
install_nodejs() {
    if check_command node && check_command npm; then
        log_info "Node.js 已安装: $(node --version)"
        log_info "npm 已安装: $(npm --version)"
    else
        log_info "正在安装 Node.js..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_homebrew
            brew install node
        else
            # 下载并安装 Node.js
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        log_success "Node.js 安装完成: $(node --version)"
    fi
}

# 安装 Python 3
install_python() {
    if check_command python3; then
        log_info "Python 3 已安装: $(python3 --version)"
    else
        log_info "正在安装 Python 3..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_homebrew
            brew install python
        else
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
        fi
        log_success "Python 3 安装完成: $(python3 --version)"
    fi

    # 安装 pip3
    if ! check_command pip3; then
        log_info "正在安装 pip3..."
        python3 -m ensurepip --default-pip
        log_success "pip3 安装完成"
    fi
}

# 安装 Git
install_git() {
    if check_command git; then
        log_info "Git 已安装: $(git --version)"
    else
        log_info "正在安装 Git..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_homebrew
            brew install git
        else
            sudo apt-get update
            sudo apt-get install -y git
        fi
        log_success "Git 安装完成"
    fi
}

# 安装 Ollama
install_ollama() {
    if check_command ollama; then
        log_info "Ollama 已安装: $(ollama --version)"
    else
        log_info "正在安装 Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        log_success "Ollama 安装完成"
    fi

    # 启动 Ollama 服务
    log_info "启动 Ollama 服务..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS 使用 launchd
        if ! pgrep -f "ollama serve" > /dev/null; then
            nohup ollama serve > /dev/null 2>&1 &
            sleep 3
        fi
    else
        # Linux 使用 systemd
        sudo systemctl enable ollama
        sudo systemctl start ollama
    fi
    
    # 等待服务启动
    sleep 5
    
    # 检查服务是否运行
    if pgrep -f "ollama serve" > /dev/null; then
        log_success "Ollama 服务已启动"
    else
        log_error "Ollama 服务启动失败"
        exit 1
    fi
}

# 下载 Ollama 模型
download_models() {
    log_info "正在下载 Ollama 模型..."
    
    # 下载中文模型
    log_info "下载 qwen:7b-chat 模型..."
    ollama pull qwen:7b-chat
    
    log_info "下载 chatglm3:6b 模型..."
    ollama pull chatglm3:6b
    
    log_success "模型下载完成"
    
    # 显示已安装的模型
    log_info "已安装的模型:"
    ollama list
}

# 安装 CNSH 核心
install_cnsh() {
    log_info "正在安装 CNSH 核心系统..."
    
    # 安装 Node.js 依赖
    log_info "安装 Node.js 依赖..."
    npm install
    
    # 安装 Python 依赖
    log_info "安装 Python 依赖..."
    pip3 install -r requirements.txt
    
    # 创建数据目录
    mkdir -p data logs uploads temp
    
    # 创建 .env 文件
    if [ ! -f .env ]; then
        log_info "创建 .env 配置文件..."
        cp .env.example .env
        log_warning "请编辑 .env 文件，配置您的 Obsidian 路径和其他设置"
    fi
    
    log_success "CNSH 核心系统安装完成"
}

# 创建启动脚本
create_start_script() {
    log_info "创建 CNSH 启动脚本..."
    
    cat > ./start-cnsh.sh << 'EOF'
#!/bin/bash

# CNSH 启动脚本

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
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
        log_info "Ollama 服务启动失败，请手动启动: ollama serve"
    fi
}

# 启动 CNSH 服务
start_cnsh() {
    log_info "启动 CNSH 服务..."
    npm start
}

# 主函数
main() {
    log_info "CNSH 系统启动中..."
    check_ollama
    start_cnsh
}

main
EOF

    chmod +x ./start-cnsh.sh
    log_success "启动脚本创建完成: $(pwd)/start-cnsh.sh"
}

# 主安装流程
main() {
    echo -e "${BLUE}====================================${NC}"
    echo -e "${BLUE}    CNSH 本地部署安装程序${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo
    
    # 检查操作系统
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "检测到 macOS 系统"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_info "检测到 Linux 系统"
    else
        log_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
    
    # 安装依赖
    log_info "正在安装系统依赖..."
    install_git
    install_nodejs
    install_python
    
    # 安装 Ollama
    install_ollama
    
    # 下载模型
    download_models
    
    # 安装 CNSH
    install_cnsh
    
    # 创建启动脚本
    create_start_script
    
    echo
    log_success "CNSH 系统安装完成!"
    echo
    log_info "下一步:"
    log_info "1. 编辑 .env 文件，配置您的 Obsidian 路径"
    log_info "2. 运行 ./start-cnsh.sh 启动系统"
    log_info "3. 访问 http://localhost:3000 验证安装"
    echo
    log_info "文档: ./README.md"
    log_info "支持: https://github.com/your-username/cnsh-deployment"
}

# 运行主函数
main