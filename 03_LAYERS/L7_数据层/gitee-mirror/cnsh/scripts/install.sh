#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# DNA追溯: #ZHUGEXIN⚡20260302-CNSH-INSTALL-SH-v0.1.0
# 作者: Lucky·UID9622 (諸葛鑫)
# GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 镜像来源: https://gitee.com/uid9622/cnsh/raw/main/scripts/install.sh
# ============================================================
# CNSH 本地部署安装脚本 - Obsidian + Ollama 集成系统

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_command() {
    if command -v "$1" &> /dev/null; then return 0; else return 1; fi
}

install_homebrew() {
    if check_command brew; then
        log_info "Homebrew 已安装"
    else
        log_info "正在安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        log_success "Homebrew 安装完成"
    fi
}

install_nodejs() {
    if check_command node && check_command npm; then
        log_info "Node.js 已安装: $(node --version)"
    else
        log_info "正在安装 Node.js..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_homebrew
            brew install node
        else
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        log_success "Node.js 安装完成"
    fi
}

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
        log_success "Python 3 安装完成"
    fi
    if ! check_command pip3; then
        python3 -m ensurepip --default-pip
    fi
}

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

install_ollama() {
    if check_command ollama; then
        log_info "Ollama 已安装"
    else
        log_info "正在安装 Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        log_success "Ollama 安装完成"
    fi
    log_info "启动 Ollama 服务..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! pgrep -f "ollama serve" > /dev/null; then
            nohup ollama serve > /dev/null 2>&1 &
            sleep 3
        fi
    else
        sudo systemctl enable ollama
        sudo systemctl start ollama
    fi
    sleep 5
    if pgrep -f "ollama serve" > /dev/null; then
        log_success "Ollama 服务已启动"
    else
        log_error "Ollama 服务启动失败"
        exit 1
    fi
}

download_models() {
    log_info "正在下载 Ollama 模型..."
    ollama pull qwen:7b-chat
    ollama pull chatglm3:6b
    log_success "模型下载完成"
    ollama list
}

install_cnsh() {
    log_info "正在安装 CNSH 核心系统..."
    npm install
    pip3 install -r requirements.txt
    mkdir -p data logs uploads temp
    if [ ! -f .env ]; then
        log_info "创建 .env 配置文件..."
        cp .env.example .env
        log_warning "请编辑 .env 文件，配置您的 Obsidian 路径和其他设置"
    fi
    log_success "CNSH 核心系统安装完成"
}

create_start_script() {
    log_info "创建 CNSH 启动脚本..."
    cat > ./start-cnsh.sh << 'EOF'
#!/bin/bash
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
check_ollama() {
    if ! pgrep -f "ollama serve" > /dev/null; then
        log_info "启动 Ollama 服务..."
        nohup ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
    log_success "Ollama 服务已运行"
}
main() {
    log_info "CNSH 系统启动中..."
    check_ollama
    npm start
}
main
EOF
    chmod +x ./start-cnsh.sh
    log_success "启动脚本创建完成: $(pwd)/start-cnsh.sh"
}

main() {
    echo -e "${BLUE}====================================${NC}"
    echo -e "${BLUE}    CNSH 本地部署安装程序${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "检测到 macOS 系统"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_info "检测到 Linux 系统"
    else
        log_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
    
    log_info "正在安装系统依赖..."
    install_git
    install_nodejs
    install_python
    install_ollama
    download_models
    install_cnsh
    create_start_script
    
    echo
    log_success "CNSH 系统安装完成!"
    echo
    log_info "下一步:"
    log_info "1. 编辑 .env 文件，配置您的 Obsidian 路径"
    log_info "2. 运行 ./start-cnsh.sh 启动系统"
    log_info "3. 访问 http://localhost:3000 验证安装"
    echo
}

main
