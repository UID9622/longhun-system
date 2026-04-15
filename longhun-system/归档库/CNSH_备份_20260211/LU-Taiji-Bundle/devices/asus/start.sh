#!/bin/bash
# ============================================================================
# LU-Taiji Bundle - 华硕设备启动脚本
# ============================================================================
# 功能：在华硕设备上快速启动 LU-Taiji Bundle
# DNA: #ZHUGEXIN⚡️2025-01-27-ASUS-START-v2.1
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 项目: LU-ORIGIN-FULLSYNC + LU-MEMORY-MERGE-ALL
# ============================================================================

set -e  # 遇到错误立即退出

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVICE_DIR="$(dirname "$SCRIPT_DIR")"
BUNDLE_ROOT="$(dirname "$DEVICE_DIR")"

# ============================================================================
# ANSI 颜色定义
# ============================================================================
GREEN='\033[0;32m'   # 绿色 - 成功
RED='\033[0;31m'     # 红色 - 错误
YELLOW='\033[0;33m' # 黄色 - 警告
BLUE='\033[0;34m'    # 蓝色 - 信息
CYAN='\033[0;36m'    # 青色 - 提示
NC='\033[0m'         # 重置颜色

# ============================================================================
# 显示横幅
# ============================================================================
banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║   LU-Taiji Bundle - 华硕设备启动           ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "DNA: #ZHUGEXIN⚡️2025-01-27-ASUS-START-v2.1"
    echo ""
}

# ============================================================================
# 环境检查
# ============================================================================
check_environment() {
    echo -e "${YELLOW}正在检查环境...${NC}"

    # 检查 Node.js（华硕推荐 20.0.0）
    if ! command -v node &> /dev/null; then
        echo -e "${RED}✗ Node.js 未安装${NC}"
        echo -e "${YELLOW}  请从 https://nodejs.org 下载安装${NC}"
        return 1
    fi

    local node_version=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js: $node_version"

    # 提示升级（如果版本过低）
    local major_version=$(echo $node_version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ $major_version -lt 18 ]; then
        echo -e "${YELLOW}⚠️  建议升级到 Node.js 18.0.0 或更高版本${NC}"
    fi

    # 检查 npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}✗ npm 未安装${NC}"
        return 1
    fi
    echo -e "${GREEN}✓${NC} npm: $(npm --version)"

    # 检查 Shell（优先使用 zsh）
    if command -v zsh &> /dev/null; then
        echo -e "${GREEN}✓${NC} Shell: $(zsh --version)"
    elif command -v bash &> /dev/null; then
        echo -e "${GREEN}✓${NC} Shell: $(bash --version | head -n1)"
    else
        echo -e "${RED}✗ 未找到支持的 Shell${NC}"
        return 1
    fi

    # 检查文件系统
    local filesystem=$(df -T . | awk 'NR==2 {print $2}')
    echo -e "${GREEN}✓${NC} 文件系统: $filesystem"

    # 检查可用空间
    local bundle_size=$(du -sb "$BUNDLE_ROOT" | awk '{print $1}')
    local avail_space=$(df -B1 . | awk 'NR==2 {print $4}')
    local required_space=$((bundle_size * 2))

    local avail_mb=$((avail_space / 1024 / 1024))
    local required_mb=$((required_space / 1024 / 1024))

    if [ $avail_space -lt $required_space ]; then
        echo -e "${YELLOW}⚠️  可用空间不足${NC}"
        echo -e "${YELLOW}  需要: ${required_mb}MB${NC}"
        echo -e "${YELLOW}  可用: ${avail_mb}MB${NC}"
        echo ""
        read -p "是否继续? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    echo -e "${GREEN}✓${NC} 可用空间: ${avail_mb}MB"

    echo ""
    return 0
}

# ============================================================================
# 华硕设备特殊优化
# ============================================================================
optimize_for_asus() {
    echo -e "${YELLOW}正在应用华硕设备优化...${NC}"

    # 设置文件权限（华硕推荐 644/755）
    chmod -R 644 "$BUNDLE_ROOT/content"/*.json
    chmod -R 644 "$BUNDLE_ROOT"/*.json
    chmod -R 644 "$BUNDLE_ROOT"/*.md
    chmod -R 755 "$BUNDLE_ROOT/scripts"
    chmod -R 755 "$BUNDLE_ROOT/devices"

    # 保留文件权限（华硕设备特性）
    chmod -R +X "$BUNDLE_ROOT"

    # 创建华硕特定的环境配置
    cat > "$BUNDLE_ROOT/.asus_env" << 'EOF'
# 华硕设备特定环境配置
export LU_TAIJI_DEVICE=asus
export LU_TAIJI_FS_COMPAT=true
export LU_TAIJI_ZSH_OPTIMIZED=true
export LU_TAIJI_PERFORMANCE_MODE=true
EOF

    echo -e "${GREEN}✓ 华硕优化已应用${NC}"
    echo ""
}

# ============================================================================
# 主启动流程
# ============================================================================
main() {
    banner

    # 环境检查
    if ! check_environment; then
        echo -e "${RED}✗ 环境检查失败${NC}"
        exit 1
    fi

    # 应用华硕设备优化
    optimize_for_asus

    # 加载华硕环境配置
    if [ -f "$BUNDLE_ROOT/.asus_env" ]; then
        source "$BUNDLE_ROOT/.asus_env"
        echo -e "${GREEN}✓ 华硕环境配置已加载${NC}"
    fi

    echo -e "${BLUE}正在启动 LU-Taiji Bundle 快速安装...${NC}"
    echo ""

    # 启动快速安装
    bash "$BUNDLE_ROOT/scripts/quickstart.sh"

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✓ 华硕设备启动完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "\n${CYAN}下一步操作:${NC}"
    echo -e "  1. 编辑 ${GREEN}.env${NC} 配置文件"
    echo -e "  2. 运行 ${GREEN}node scripts/validate_schema.mjs${NC}"
    echo -e "  3. 运行 ${GREEN}node scripts/import_notion.mjs${NC}"
    echo -e "\n${CYAN}性能提示:${NC}"
    echo -e "  华硕设备已启用 Zsh 优化模式"
    echo ""
}

# ============================================================================
# 执行主函数
# ============================================================================
main "$@"
