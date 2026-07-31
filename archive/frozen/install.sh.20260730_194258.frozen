#!/usr/bin/env bash
# ============================================================
# 🐉 龍魂体系v4.0 - 一键安装脚本
# DNA签名: #龍芯⚡️2026-06-09-INSTALL-SH-v1.0
# 所属者: UID9622 | 龍芯北辰·诸葛鑫
# 功能: 环境检查、依赖安装、目录初始化、安全配置
# 用法: bash install.sh
# ============================================================

# ------------------------------------------------------------
# 彩色输出定义
# ------------------------------------------------------------
CLR_GREEN='\033[0;32m'
CLR_RED='\033[0;31m'
CLR_YELLOW='\033[1;33m'
CLR_BLUE='\033[0;34m'
CLR_CYAN='\033[0;36m'
CLR_PURPLE='\033[0;35m'
CLR_RESET='\033[0m'
CLR_BOLD='\033[1m'

_print_success() { echo -e "${CLR_GREEN}✅ $1${CLR_RESET}"; }
_print_error() { echo -e "${CLR_RED}❌ $1${CLR_RESET}"; }
_print_warn()  { echo -e "${CLR_YELLOW}⚠️  $1${CLR_RESET}"; }
_print_info()  { echo -e "${CLR_BLUE}ℹ️  $1${CLR_RESET}"; }
_print_title() { echo -e "${CLR_CYAN}${CLR_BOLD}$1${CLR_RESET}"; }
_print_emph()  { echo -e "${CLR_PURPLE}${CLR_BOLD}$1${CLR_RESET}"; }

# ------------------------------------------------------------
# DNA签名
# ------------------------------------------------------------
DNA_HEAD="#龍芯⚡️2026-06-09-INSTALL-SH-v1.0"
DNA_CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅"
DNA_SEAL="#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅"

# ------------------------------------------------------------
# 全局状态
# ------------------------------------------------------------
SUCCESS_COUNT=0
FAIL_COUNT=0
STEP_NUM=0

_step() {
    STEP_NUM=$((STEP_NUM + 1))
    echo ""
    _print_title "════════════════════════════════════════════════════════════"
    _print_title "  步骤 ${STEP_NUM}: $1"
    _print_title "════════════════════════════════════════════════════════════"
}

# ------------------------------------------------------------
# 步骤1: 欢迎界面
# ------------------------------------------------------------
clear
_print_title "╔════════════════════════════════════════════════════════════╗"
_print_title "║          🐉 龍魂体系v4.0 - 一键安装程序                    ║"
_print_title "║          UID9622 | 龍芯北辰·诸葛鑫                        ║"
_print_title "╚════════════════════════════════════════════════════════════╝"
echo ""
_print_info "即将执行以下操作:"
_print_info "  1. 检查 Python 3.8+ 环境"
_print_info "  2. 安装 Python 依赖包"
_print_info "  3. 创建 ~/.longhun/ 配置目录"
_print_info "  4. 初始化五层目录结构"
_print_info "  5. 设置安全权限"
echo ""
_print_warn "按 [Enter] 开始安装，或按 [Ctrl+C] 取消..."
read -r

# ------------------------------------------------------------
# 步骤2: 检查 Python 版本
# ------------------------------------------------------------
_step "检查 Python 3.8+ 环境"

if ! command -v python3 &> /dev/null; then
    _print_error "未找到 python3 命令，请先安装 Python 3.8 或更高版本"
    _print_warn "安装方式:"
    _print_warn "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    _print_warn "  macOS: brew install python3"
    _print_warn "  官网: https://www.python.org/downloads/"
    exit 1
fi

PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
_print_info "检测到 Python 版本: ${PY_VERSION}"

PY_MAJOR=$(echo "${PY_VERSION}" | cut -d. -f1)
PY_MINOR=$(echo "${PY_VERSION}" | cut -d. -f2)

if [ "${PY_MAJOR}" -lt 3 ] || ([ "${PY_MAJOR}" -eq 3 ] && [ "${PY_MINOR}" -lt 8 ]); then
    _print_error "Python 版本 ${PY_VERSION} 不满足要求，需要 3.8 或更高版本"
    exit 1
fi

_print_success "Python ${PY_VERSION} 版本检查通过 ✓"
SUCCESS_COUNT=$((SUCCESS_COUNT + 1))

# ------------------------------------------------------------
# 步骤3: 检查 pip
# ------------------------------------------------------------
_step "检查 pip 包管理器"

if ! command -v pip3 &> /dev/null; then
    _print_warn "未找到 pip3，正在尝试安装..."
    python3 -m ensurepip --upgrade 2>/dev/null || {
        _print_error "无法安装 pip，请手动安装: python3 -m ensurepip"
        exit 1
    }
fi

PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
_print_info "检测到 pip 版本: ${PIP_VERSION}"
_print_success "pip 检查通过 ✓"
SUCCESS_COUNT=$((SUCCESS_COUNT + 1))

# ------------------------------------------------------------
# 步骤4: 安装依赖包
# ------------------------------------------------------------
_step "安装 Python 依赖包"

DEPS=(
    "watchdog>=3.0"
    "requests>=2.28"
    "python-dotenv>=1.0"
    "mcp>=1.0"
)

_print_info "需要安装的依赖:"
for dep in "${DEPS[@]}"; do
    _print_info "  • ${dep}"
done
echo ""

for dep in "${DEPS[@]}"; do
    pkg=$(echo "${dep}" | cut -d'>' -f1 | cut -d'=' -f1)
    _print_info "正在安装 ${pkg} ..."
    if pip3 install "${dep}" --quiet 2>/dev/null; then
        _print_success "${pkg} 安装成功 ✓"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        _print_error "${pkg} 安装失败"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        _print_warn "尝试使用 --user 模式重新安装..."
        if pip3 install "${dep}" --user --quiet 2>/dev/null; then
            _print_success "${pkg} 使用 --user 模式安装成功 ✓"
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            FAIL_COUNT=$((FAIL_COUNT - 1))
        else
            _print_error "${pkg} 所有安装方式均失败"
        fi
    fi
done

# ------------------------------------------------------------
# 步骤5: 创建 ~/.longhun/ 配置目录
# ------------------------------------------------------------
_step "创建 ~/.longhun/ 配置目录"

CONFIG_DIR="${HOME}/.longhun"
TEMPLATE_SRC="$(cd "$(dirname "$0")" && pwd)/secrets.env.template"

if [ -d "${CONFIG_DIR}" ]; then
    _print_warn "配置目录已存在: ${CONFIG_DIR}"
else
    mkdir -p "${CONFIG_DIR}" && _print_success "创建配置目录: ${CONFIG_DIR} ✓"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
fi

# 复制模板文件
if [ -f "${TEMPLATE_SRC}" ]; then
    _print_info "复制密钥模板到配置目录..."
    cp "${TEMPLATE_SRC}" "${CONFIG_DIR}/secrets.env.template"
    _print_success "模板已复制: ${CONFIG_DIR}/secrets.env.template ✓"
else
    _print_warn "未找到模板文件 secrets.env.template"
    _print_warn "请确保 install.sh 和 secrets.env.template 在同一目录下"
fi

# ------------------------------------------------------------
# 步骤6: 提示用户配置密钥
# ------------------------------------------------------------
_step "密钥配置提示"

echo ""
_print_emph "┌────────────────────────────────────────────────────────────┐"
_print_emph "│                   ⚠️  重要：密钥配置                        │"
_print_emph "└────────────────────────────────────────────────────────────┘"
echo ""
_print_warn "你需要完成以下配置步骤:"
echo ""
_print_info "1. 复制模板文件:"
echo ""
_print_emph "     cp ~/.longhun/secrets.env.template ~/.longhun/secrets.env"
echo ""
_print_info "2. 编辑 ~/.longhun/secrets.env，填入你的真实密钥值:"
echo ""
_print_info "   • NOTION_TOKEN    - Notion Integration Token"
_print_info "   • DB_LU           - L0干·主权层数据库ID"
_print_info "   • DB_JQ           - L1离·继承层数据库ID"
_print_info "   • DB_AL           - L2震·战友层数据库ID"
_print_info "   • DB_PUB          - L3巽·公开层数据库ID"
_print_info "   • DB_CLOUD        - L4坎·云端层数据库ID"
_print_info "   • GPG_FINGERPRINT - GPG密钥指纹（可选替换）"
echo ""
_print_info "3. 模板文件中有每个变量的详细说明和获取方式"
echo ""

# ------------------------------------------------------------
# 步骤7: 运行五层目录初始化脚本
# ------------------------------------------------------------
_step "初始化五层目录结构"

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/init_directories.py"

if [ -f "${SCRIPT_PATH}" ]; then
    _print_info "运行目录初始化脚本..."
    python3 "${SCRIPT_PATH}"
    INIT_RESULT=$?
    if [ ${INIT_RESULT} -eq 0 ]; then
        _print_success "五层目录初始化完成 ✓"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        _print_error "目录初始化失败 (退出码: ${INIT_RESULT})"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    _print_error "未找到初始化脚本: ${SCRIPT_PATH}"
    _print_warn "请确保 install.sh 和 init_directories.py 在同一目录下"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# ------------------------------------------------------------
# 步骤8: 设置安全权限
# ------------------------------------------------------------
_step "设置安全权限"

# 设置 secrets.env 权限（如果已存在）
SECRETS_FILE="${HOME}/.longhun/secrets.env"
if [ -f "${SECRETS_FILE}" ]; then
    chmod 600 "${SECRETS_FILE}"
    _print_success "已设置 ~/.longhun/secrets.env 权限为 600 (仅所有者可读写) ✓"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
else
    _print_warn "密钥文件尚未创建，请按上述步骤创建后手动执行:"
    _print_emph "     chmod 600 ~/.longhun/secrets.env"
fi

# 设置配置目录权限
chmod 700 "${CONFIG_DIR}"
_print_success "已设置 ~/.longhun/ 目录权限为 700 (仅所有者可访问) ✓"
SUCCESS_COUNT=$((SUCCESS_COUNT + 1))

# 设置各层目录权限
HOME_DIR="${HOME}"
LAYER_DIRS=("longhun-lu" "longhun-jq" "longhun-al" "longhun-pub" "longhun-cloud")

_print_info "设置五层目录权限..."
for LAYER_DIR in "${LAYER_DIRS[@]}"; do
    FULL_PATH="${HOME_DIR}/${LAYER_DIR}"
    if [ -d "${FULL_PATH}" ]; then
        chmod 755 "${FULL_PATH}"
    fi
done
_print_success "五层目录权限设置完成 ✓"

# ------------------------------------------------------------
# 步骤9: 安装完成报告
# ------------------------------------------------------------
echo ""
_print_title "╔════════════════════════════════════════════════════════════╗"
_print_title "║                 🎉 安装完成总结报告                         ║"
_print_title "╚════════════════════════════════════════════════════════════╝"
echo ""

# 显示已创建的目录
echo ""
_print_title "📁 已创建/验证的五层目录:"
echo ""

LAYER_NAMES=(
    "☰ L0干·主权层  (longhun-lu)   - 老大个人主权"
    "☲ L1离·继承层  (longhun-jq)   - 佳琪UID9622-JQ001"
    "☳ L2震·战友层  (longhun-al)   - 核心战友协作"
    "☴ L3巽·公开层  (longhun-pub)  - 公开发布"
    "☵ L4坎·云端层  (longhun-cloud)- 云端备份"
)

for LAYER in "${LAYER_NAMES[@]}"; do
    _print_success "  ${LAYER}"
done

echo ""
_print_title "📊 安装统计:"
_print_success "  成功: ${SUCCESS_COUNT} 项"
if [ ${FAIL_COUNT} -gt 0 ]; then
    _print_error "  失败: ${FAIL_COUNT} 项"
else
    _print_info "  失败: 0 项"
fi

echo ""
_print_title "📝 后续步骤:"
_print_info "  1. 编辑密钥文件: vim ~/.longhun/secrets.env"
_print_info "  2. 设置权限:     chmod 600 ~/.longhun/secrets.env"
_print_info "  3. 验证Python:    python3 -c 'import dotenv,requests,watchdog,mcp'"
_print_info "  4. 开始使用龍魂体系v4.0！"

echo ""
_print_emph "${DNA_CONFIRM}"
_print_emph "${DNA_SEAL}"
echo ""

if [ ${FAIL_COUNT} -gt 0 ]; then
    _print_warn "⚠️  存在 ${FAIL_COUNT} 项安装失败，请检查上方错误信息"
    exit 1
else
    _print_success "🐉 龍魂体系v4.0 安装全部成功！体系已就绪，等待你的密钥..."
    exit 0
fi
