#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  install.sh - 龙魂知识图谱安装脚本 (UID9622)
# ═══════════════════════════════════════════════════════════════
#  功能:
#    1. 创建目录结构
#    2. 复制 Python 引擎和 kg 命令
#    3. 安装到 /usr/local/bin 或 ~/bin
#    4. 设置环境变量
#    5. 验证安装
#
#  用法:
#    chmod +x install.sh
#    ./install.sh              # 安装到 ~/bin
#    ./install.sh --system     # 安装到 /usr/local/bin (需 sudo)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

# ---- 配置 ----------------------------------------------------
INSTALL_SYSTEM=false
INSTALL_DIR=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 数据目录
KG_DATA_DIR="${LHKG_DIR:-$HOME/.龍魂/knowledge-graph}"

# ANSI 颜色
C_BOLD='\033[1m'
C_DIM='\033[2m'
C_RED='\033[91m'
C_GREEN='\033[92m'
C_YELLOW='\033[93m'
C_BLUE='\033[94m'
C_CYAN='\033[96m'
C_RESET='\033[0m'

# ---- 辅助函数 ------------------------------------------------
info()  { echo -e "${C_BLUE}[INFO]${C_RESET} $*"; }
ok()    { echo -e "${C_GREEN}[OK]${C_RESET}   $*"; }
warn()  { echo -e "${C_YELLOW}[WARN]${C_RESET} $*"; }
err()   { echo -e "${C_RED}[ERROR]${C_RESET} $*"; }

banner() {
    echo -e "${C_CYAN}╔══════════════════════════════════════════════════════════════╗${C_RESET}"
    echo -e "${C_CYAN}║         龙魂知识图谱安装程序  v1.0  (UID9622)               ║${C_RESET}"
    echo -e "${C_CYAN}╚══════════════════════════════════════════════════════════════╝${C_RESET}"
    echo ""
}

detect_install_dir() {
    if [[ "$INSTALL_SYSTEM" == true ]]; then
        INSTALL_DIR="/usr/local/bin"
        if [[ ! -w "$INSTALL_DIR" ]]; then
            err "需要 root 权限安装到 $INSTALL_DIR"
            err "请使用: sudo ./install.sh --system"
            exit 1
        fi
    else
        # 优先使用 ~/bin
        INSTALL_DIR="$HOME/bin"
        if [[ ! -d "$INSTALL_DIR" ]]; then
            mkdir -p "$INSTALL_DIR"
            ok "创建目录: $INSTALL_DIR"
        fi
    fi
    ok "安装目标: $INSTALL_DIR"
}

check_python() {
    info "检查 Python 3 环境..."
    if command -v python3 &>/dev/null; then
        local pyver
        pyver=$(python3 --version 2>&1)
        ok "找到 $pyver"
    else
        err "未找到 python3，请先安装 Python 3.8+"
        exit 1
    fi

    # 检查 Python 版本 >= 3.8
    local major minor
    major=$(python3 -c 'import sys; print(sys.version_info.major)')
    minor=$(python3 -c 'import sys; print(sys.version_info.minor)')
    if [[ "$major" -lt 3 ]] || ([[ "$major" -eq 3 ]] && [[ "$minor" -lt 8 ]]); then
        err "需要 Python 3.8+，当前版本: $major.$minor"
        exit 1
    fi
    ok "Python 版本满足要求 (>= 3.8)"
}

create_data_dir() {
    info "创建数据目录: $KG_DATA_DIR"
    mkdir -p "$KG_DATA_DIR"

    # 如果数据目录为空，创建示例数据文件
    if [[ ! -f "$KG_DATA_DIR/nodes.json" ]]; then
        info "创建示例数据文件..."
        cp "$SCRIPT_DIR/nodes.json.example" "$KG_DATA_DIR/nodes.json" 2>/dev/null || true
        cp "$SCRIPT_DIR/edges.json.example" "$KG_DATA_DIR/edges.json" 2>/dev/null || true
        cp "$SCRIPT_DIR/states.json.example" "$KG_DATA_DIR/states.json" 2>/dev/null || true
    fi
    ok "数据目录就绪: $KG_DATA_DIR"
}

install_files() {
    info "安装文件..."

    # 复制 Python 引擎
    local engine_src="$SCRIPT_DIR/longhun_kg.py"
    local engine_dest="$INSTALL_DIR/longhun_kg.py"

    if [[ ! -f "$engine_src" ]]; then
        err "未找到引擎文件: $engine_src"
        exit 1
    fi

    cp "$engine_src" "$engine_dest"
    chmod +x "$engine_dest"
    ok "安装引擎: $engine_dest"

    # 复制 kg 脚本
    local kg_src="$SCRIPT_DIR/kg"
    local kg_dest="$INSTALL_DIR/kg"

    if [[ ! -f "$kg_src" ]]; then
        err "未找到 kg 脚本: $kg_src"
        exit 1
    fi

    cp "$kg_src" "$kg_dest"
    chmod +x "$kg_dest"
    ok "安装命令: $kg_dest"
}

setup_env() {
    info "配置环境变量..."

    local shell_rc=""
    case "$(basename "$SHELL")" in
        bash) shell_rc="$HOME/.bashrc" ;;
        zsh)  shell_rc="$HOME/.zshrc" ;;
        fish) shell_rc="$HOME/.config/fish/config.fish" ;;
        *)    shell_rc="$HOME/.profile" ;;
    esac

    # 检查是否已设置 LHKG_DIR
    if [[ -f "$shell_rc" ]] && grep -q "LHKG_DIR" "$shell_rc" 2>/dev/null; then
        warn "LHKG_DIR 已存在于 $shell_rc，跳过"
    else
        echo "" >> "$shell_rc"
        echo "# 龙魂知识图谱数据目录" >> "$shell_rc"
        echo "export LHKG_DIR=\"$KG_DATA_DIR\"" >> "$shell_rc"
        ok "已添加 LHKG_DIR 到 $shell_rc"
        info "请运行: source $shell_rc"
    fi

    # 确保 ~/bin 在 PATH 中（非系统安装时）
    if [[ "$INSTALL_SYSTEM" != true ]]; then
        if [[ -f "$shell_rc" ]] && grep -q 'export PATH="$HOME/bin:$PATH"' "$shell_rc" 2>/dev/null; then
            ok "~/bin 已在 PATH 中"
        else
            echo 'export PATH="$HOME/bin:$PATH"' >> "$shell_rc"
            ok "已添加 ~/bin 到 PATH"
        fi
    fi
}

verify() {
    info "验证安装..."

    # 测试 Python 引擎
    if python3 "$INSTALL_DIR/longhun_kg.py" list --data-dir "$KG_DATA_DIR" &>/dev/null; then
        ok "Python 引擎测试通过"
    else
        warn "Python 引擎测试失败，尝试使用内建测试数据..."
        if python3 "$INSTALL_DIR/longhun_kg.py" list &>/dev/null; then
            ok "Python 引擎测试通过（使用内建数据）"
        else
            err "Python 引擎测试失败"
            exit 1
        fi
    fi

    # 测试 kg 命令
    local kg_cmd="$INSTALL_DIR/kg"
    if command -v "$kg_cmd" &>/dev/null || [[ -x "$kg_cmd" ]]; then
        if "$kg_cmd" help &>/dev/null; then
            ok "kg 命令测试通过"
        else
            warn "kg 命令测试失败"
        fi
    else
        warn "kg 命令暂不可用，请重新加载 shell 配置"
    fi
}

print_summary() {
    echo ""
    echo -e "${C_GREEN}╔══════════════════════════════════════════════════════════════╗${C_RESET}"
    echo -e "${C_GREEN}║              安装完成!                                       ║${C_RESET}"
    echo -e "${C_GREEN}╚══════════════════════════════════════════════════════════════╝${C_RESET}"
    echo ""
    echo -e "  ${C_BOLD}数据目录:${C_RESET}  $KG_DATA_DIR"
    echo -e "  ${C_BOLD}安装位置:${C_RESET}  $INSTALL_DIR"
    echo -e "  ${C_BOLD}命令:${C_RESET}       kg <command>"
    echo ""
    echo -e "  ${C_BOLD}快速开始:${C_RESET}"
    echo -e "    kg list                    # 列出所有节点"
    echo -e "    kg show CORE-01            # 显示节点详情"
    echo -e "    kg path SENS-01 ACT-01     # 查找路径"
    echo -e "    kg state CORE-01           # 查看状态历史"
    echo -e "    kg export --output kg.mmd  # 导出 Mermaid 图"
    echo ""
    echo -e "  ${C_BOLD}提示:${C_RESET} 运行 'source ~/.bashrc' (或 ~/.zshrc) 使环境变量生效"
    echo ""
}

# ---- 参数解析 ------------------------------------------------
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --system) INSTALL_SYSTEM=true; shift ;;
            --help|-h)
                banner
                echo "用法: ./install.sh [选项]"
                echo ""
                echo "选项:"
                echo "  --system    安装到 /usr/local/bin (需要 sudo)"
                echo "  --help      显示此帮助"
                exit 0
                ;;
            *) warn "未知参数: $1"; shift ;;
        esac
    done
}

# ---- 主流程 --------------------------------------------------
main() {
    parse_args "$@"
    banner
    check_python
    detect_install_dir
    create_data_dir
    install_files
    setup_env
    verify
    print_summary
}

main "$@"
