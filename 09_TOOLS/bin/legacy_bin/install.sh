#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════════════════
#  🐉 龍魂系统 · 一键安装脚本
#  LongHun System · One-Click Install
# ═══════════════════════════════════════════════════════════════════════
# DNA:     #龍芯⚡️丙午·乙未·戊子·戊午·䷙大畜-INSTALL-SCRIPT-v1.0
# SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: CN-SOVEREIGN-LICENSE-v1.0
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# ── 版本 ──
VERSION="v5.0.0"
REQUIRED_PYTHON_MAJOR=3
REQUIRED_PYTHON_MINOR=11

# ── 横幅 ──
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}║        ${BOLD}🐉 龍魂系统 ${VERSION} · 一键安装${NC}${BLUE}                         ║${NC}"
echo -e "${BLUE}║        LongHun System · One-Click Install                       ║${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}║        创始人: UID9622 · 龍芯北辰 · 诸葛鑫                       ║${NC}"
echo -e "${BLUE}║                                                                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Step 1: 检查 Python ──
echo -e "${BOLD}[1/5]${NC} 检查 Python 环境..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} 未找到 python3，请先安装 Python >= ${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt "$REQUIRED_PYTHON_MAJOR" ] || { [ "$PYTHON_MAJOR" -eq "$REQUIRED_PYTHON_MAJOR" ] && [ "$PYTHON_MINOR" -lt "$REQUIRED_PYTHON_MINOR" ]; }; then
    echo -e "${RED}✗${NC} Python ${PYTHON_VERSION} 不满足要求（需要 >= ${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR}）"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION}"

# ── Step 2: 创建虚拟环境 ──
echo -e "${BOLD}[2/5]${NC} 创建虚拟环境..."

VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠${NC} 虚拟环境已存在，跳过创建"
else
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓${NC} 虚拟环境创建完成"
fi

# 激活虚拟环境
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
fi

# ── Step 3: 安装依赖 ──
echo -e "${BOLD}[3/5]${NC} 安装核心依赖..."

# 升级 pip
python3 -m pip install --upgrade pip -q

# 安装核心依赖
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt -q
    echo -e "${GREEN}✓${NC} requirements.txt 安装完成"
fi

# 安装开发依赖（可选）
if [ "${INSTALL_DEV:-0}" = "1" ] && [ -f "requirements-dev.txt" ]; then
    python3 -m pip install -r requirements-dev.txt -q
    echo -e "${GREEN}✓${NC} requirements-dev.txt 安装完成"
fi

# ── Step 4: 验证安装 ──
echo -e "${BOLD}[4/5]${NC} 验证安装..."

# 检查关键模块
python3 -c "
import sys
modules = ['numpy', 'yaml']
missing = []
for m in modules:
    try:
        __import__(m)
        print(f'  ✓ {m}')
    except ImportError:
        print(f'  ✗ {m}')
        missing.append(m)
if missing:
    print(f'警告: 以下模块未安装: {missing}')
    sys.exit(1)
print('核心依赖验证通过')
"

# ── Step 5: 注册 CLI ──
echo -e "${BOLD}[5/5]${NC} 配置 CLI 命令..."

if command -v lh &> /dev/null; then
    echo -e "${GREEN}✓${NC} lh 命令已可用"
else
    # 创建别名脚本
    ALIAS_FILE="$HOME/.longhun_aliases"
    cat > "$ALIAS_FILE" << 'ALIASEOF'
# 龍魂系统 CLI 别名
# 添加到你的 ~/.bashrc 或 ~/.zshrc:
#   source ~/.longhun_aliases

LONGHUN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

alias lh='python3 ${LONGHUN_ROOT}/bin/龍魂体系v5-一键启动.py'
alias lh-status='python3 ${LONGHUN_ROOT}/bin/龍魂体系v5-一键启动.py --status'
alias lh-start='python3 ${LONGHUN_ROOT}/bin/龍魂体系v5-一键启动.py --start'
alias lh-stop='python3 ${LONGHUN_ROOT}/bin/龍魂体系v5-一键启动.py --stop'
alias lh-health='python3 ${LONGHUN_ROOT}/bin/longhun-self-heal.py --quick'
alias lh-audit='python3 ${LONGHUN_ROOT}/bin/longhun-self-heal.py --audit'
ALIASEOF
    echo -e "${YELLOW}⚠${NC} 请将以下行添加到 ~/.zshrc 或 ~/.bashrc:"
    echo ""
    echo -e "  ${BOLD}source ~/.longhun_aliases${NC}"
    echo ""
fi

# ── 完成 ──
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║                   🎉 安装完成！                                   ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║  下一步：                                                        ║${NC}"
echo -e "${GREEN}║    python3 bin/龍魂体系v5-一键启动.py       # 启动系统            ║${NC}"
echo -e "${GREEN}║    cat QUICKSTART.md                        # 查看快速入门        ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# DNA 锚定
echo -e "${BLUE}🧬 DNA: #龍芯⚡️丙午·乙未·戊子·戊午·䷙大畜-INSTALL-COMPLETE-v1.0${NC}"
echo ""
