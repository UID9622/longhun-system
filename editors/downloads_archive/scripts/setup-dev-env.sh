#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂中文编辑开发环境 - 一键搭建脚本
# DNA: #龍芯⚡️2026-06-26-DEVENV-SETUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬SETUP-001
# 创建者: UID9622（诸葛鑫）
# 三色审计状态: 🟢
# ═══════════════════════════════════════════

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${GREEN}[🟢 INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[🟡 WARN]${NC} $1"; }
log_error() { echo -e "${RED}[🔴 ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
log_dna() { echo -e "${CYAN}[🧬 DNA]${NC} $1"; }

# DNA追溯
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════╗"
echo "║     龍魂中文编辑开发环境搭建工具         ║"
echo "║     DNA: #龍芯⚡️2026-06-26-DEVENV-v1.0   ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# 检测操作系统
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    log_error "不支持的操作系统: $OSTYPE"
    exit 1
fi
log_info "检测到操作系统: $OS"

# 检查命令是否存在
check_command() {
    if command -v "$1" &> /dev/null; then
        log_info "$1 已安装: $(command -v $1)"
        return 0
    else
        log_warn "$1 未安装"
        return 1
    fi
}

# ═══════════════════════════════════════════
# 步骤1: 安装基础工具
# ═══════════════════════════════════════════
log_step "步骤 1/10: 安装基础工具"

if [[ "$OS" == "linux" ]]; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq curl wget git vim build-essential \
        libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
        libsqlite3-dev llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
elif [[ "$OS" == "macos" ]]; then
    if ! check_command brew; then
        log_info "安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install curl wget git vim openssl readline sqlite3 xz zlib
fi

log_info "基础工具安装完成 🟢"

# ═══════════════════════════════════════════
# 步骤2: 安装/更新 Git
# ═══════════════════════════════════════════
log_step "步骤 2/10: 配置 Git"

if ! check_command git; then
    if [[ "$OS" == "linux" ]]; then
        sudo apt-get install -y -qq git
    elif [[ "$OS" == "macos" ]]; then
        brew install git
    fi
fi

# 配置 Git
git config --global init.defaultBranch main
git config --global core.editor "code --wait" 2>/dev/null || git config --global core.editor "vim"
git config --global pull.rebase true
git config --global core.autocrlf input
git config --global core.safecrlf true

git config --global color.ui auto
git config --global color.diff.meta "yellow bold"
git config --global color.diff.frag "magenta bold"
git config --global color.diff.old "red bold"
git config --global color.diff.new "green bold"

log_info "Git 配置完成 🟢"

# ═══════════════════════════════════════════
# 步骤3: 安装/更新 VS Code
# ═══════════════════════════════════════════
log_step "步骤 3/10: 安装 VS Code"

if ! check_command code; then
    log_info "正在安装 VS Code..."
    if [[ "$OS" == "linux" ]]; then
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
        sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
        sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
        rm -f packages.microsoft.gpg
        sudo apt-get update -qq
        sudo apt-get install -y -qq code
    elif [[ "$OS" == "macos" ]]; then
        brew install --cask visual-studio-code
    fi
    log_info "VS Code 安装完成 🟢"
else
    log_info "VS Code 已安装 🟢"
fi

# ═══════════════════════════════════════════
# 步骤4: 安装 Python 3.11+
# ═══════════════════════════════════════════
log_step "步骤 4/10: 安装 Python 3.11+"

if ! check_command python3; then
    log_info "正在安装 Python..."
    if [[ "$OS" == "linux" ]]; then
        sudo apt-get install -y -qq python3 python3-pip python3-venv
    elif [[ "$OS" == "macos" ]]; then
        brew install python@3.11
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
log_info "Python 版本: $PYTHON_VERSION"

# 创建虚拟环境
VENV_DIR="$HOME/.longhun/venv"
if [[ ! -d "$VENV_DIR" ]]; then
    log_info "创建虚拟环境..."
    mkdir -p "$HOME/.longhun"
    python3 -m venv "$VENV_DIR"
fi
log_info "虚拟环境: $VENV_DIR 🟢"

# ═══════════════════════════════════════════
# 步骤5: 安装 Node.js 20+
# ═══════════════════════════════════════════
log_step "步骤 5/10: 安装 Node.js 20+"

if ! check_command node; then
    log_info "正在安装 Node.js..."
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y -qq nodejs
    elif [[ "$OS" == "macos" ]]; then
        brew install node@20
    fi
fi

NODE_VERSION=$(node --version 2>/dev/null || echo "未安装")
log_info "Node.js 版本: $NODE_VERSION 🟢"

# ═══════════════════════════════════════════
# 步骤6: 安装 Python 依赖
# ═══════════════════════════════════════════
log_step "步骤 6/10: 安装 Python 依赖"

PIP_CMD="$VENV_DIR/bin/pip"
$PIP_CMD install --upgrade pip -q

# 安装核心依赖
$PIP_CMD install -q \
    python-dotenv requests pydantic \
    fastapi uvicorn[standard] \
    cryptography \
    rich typer python-dateutil

# 安装开发依赖
$PIP_CMD install -q \
    black flake8 mypy isort \
    pytest pytest-cov

log_info "Python 依赖安装完成 🟢"

# ═══════════════════════════════════════════
# 步骤7: 复制配置文件
# ═══════════════════════════════════════════
log_step "步骤 7/10: 复制配置文件"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")"
DEST_DIR="$HOME/.longhun/dev-env"

mkdir -p "$DEST_DIR"

# 复制 VS Code 配置
if [[ -d "$CONFIG_DIR/vscode" ]]; then
    mkdir -p "$HOME/.config/Code/User"
    cp "$CONFIG_DIR/vscode/settings.json" "$HOME/.config/Code/User/" 2>/dev/null || \
    cp "$CONFIG_DIR/vscode/settings.json" "$HOME/Library/Application Support/Code/User/" 2>/dev/null || true
    log_info "VS Code 配置已复制 🟢"
fi

# 复制 Git 配置
if [[ -f "$CONFIG_DIR/git/.gitconfig" ]]; then
    cp "$CONFIG_DIR/git/.gitconfig" "$HOME/.gitconfig-longhun"
    log_info "Git 配置已复制到 ~/.gitconfig-longhun 🟢"
    log_warn "请手动执行: cat ~/.gitconfig-longhun >> ~/.gitconfig"
fi

log_info "配置文件复制完成 🟢"

# ═══════════════════════════════════════════
# 步骤8: 验证安装
# ═══════════════════════════════════════════
log_step "步骤 8/10: 验证安装"

echo ""
echo "═══════════════════════════════════════════"
echo "  安装验证报告"
echo "═══════════════════════════════════════════"

check_command git && echo "  ✅ Git" || echo "  ❌ Git"
check_command code && echo "  ✅ VS Code" || echo "  ❌ VS Code"
check_command python3 && echo "  ✅ Python" || echo "  ❌ Python"
check_command node && echo "  ✅ Node.js" || echo "  ❌ Node.js"
check_command pip && echo "  ✅ pip" || echo "  ❌ pip"
check_command npm && echo "  ✅ npm" || echo "  ❌ npm"

echo ""
echo "  Python版本: $(python3 --version 2>/dev/null || echo 'N/A')"
echo "  Node版本: $(node --version 2>/dev/null || echo 'N/A')"
echo "  npm版本: $(npm --version 2>/dev/null || echo 'N/A')"
echo "═══════════════════════════════════════════"

# ═══════════════════════════════════════════
# 步骤9: 创建快捷命令
# ═══════════════════════════════════════════
log_step "步骤 9/10: 创建快捷命令"

SHELL_RC=""
if [[ "$SHELL" == */zsh ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == */bash ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" && -f "$SHELL_RC" ]]; then
    # 检查是否已添加
    if ! grep -q "# 龍魂开发环境" "$SHELL_RC" 2>/dev/null; then
        cat >> "$SHELL_RC" << 'EOF'

# ═══════════════════════════════════════════
# 龍魂开发环境快捷命令
# DNA: #龍芯⚡️2026-06-26-DEVENV-ALIAS-v1.0
# ═══════════════════════════════════════════

# 虚拟环境
alias lh-venv='source $HOME/.longhun/venv/bin/activate'

# 常用目录
alias lh-cd='cd $HOME/.longhun'
alias lh-config='code $HOME/.longhun/dev-env'

# DNA生成
alias lh-dna='echo "#龍芯⚡️$(date +%Y-%m-%d)-"'

# 审计状态
alias lh-audit='echo "🟢 通过 / 🟡 警告 / 🔴 阻断"'

# CNSH规范检查
alias lh-cnsh='echo "CNSH中文编程规范: 中文命名优先 | 繁体龍字 | DNA追溯 | 三色审计"'
EOF
        log_info "快捷命令已添加到 $SHELL_RC 🟢"
        log_warn "请执行: source $SHELL_RC"
    else
        log_info "快捷命令已存在 🟢"
    fi
fi

# ═══════════════════════════════════════════
# 步骤10: 完成
# ═══════════════════════════════════════════
log_step "步骤 10/10: 完成"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ✅ 龍魂中文编辑开发环境搭建完成       ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║  DNA: #龍芯⚡️2026-06-26-DEVENV-v1.0     ║${NC}"
echo -e "${GREEN}║  状态: 🟢 通过                           ║${NC}"
echo -e "${GREEN}║  环境: $(printf '%-28s' "$OS")          ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║  下一步操作:                              ║${NC}"
echo -e "${GREEN}║  1. source ~/.bashrc (或 .zshrc)          ║${NC}"
echo -e "${GREEN}║  2. lh-venv  (激活虚拟环境)               ║${NC}"
echo -e "${GREEN}║  3. code .   (打开VS Code)                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""

log_dna "#龍芯⚡️2026-06-26-DEVENV-SETUP-COMPLETE-v1.0"
