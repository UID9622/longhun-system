#!/bin/bash
# ============================================================================
# LU-Taiji Bundle - 华为设备启动脚本
# ============================================================================
# 功能：在华为设备上快速启动 LU-Taiji Bundle
# DNA: #ZHUGEXIN⚡️2025-01-27-HUAWEI-START-v2.1
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
NC='\033[0m'         # 重置颜色

# ============================================================================
# 显示横幅
# ============================================================================
banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║   LU-Taiji Bundle - 华为设备启动           ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "DNA: #ZHUGEXIN⚡️2025-01-27-HUAWEI-START-v2.1"
    echo ""
}

# ============================================================================
# 环境检查
# ============================================================================
check_environment() {
    echo -e "${YELLOW}正在检查环境...${NC}"

    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}✗ Node.js 未安装${NC}"
        echo -e "${YELLOW}  请从 https://nodejs.org 下载安装${NC}"
        return 1
    fi
    echo -e "${GREEN}✓${NC} Node.js: $(node --version)"

    # 检查 npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}✗ npm 未安装${NC}"
        return 1
    fi
    echo -e "${GREEN}✓${NC} npm: $(npm --version)"

    # 检查 Bash
    if ! command -v bash &> /dev/null; then
        echo -e "${RED}✗ Bash 未安装${NC}"
        return 1
    fi
    echo -e "${GREEN}✓${NC} Bash: $(bash --version | head -n1)"

    # 检查文件系统
    local filesystem=$(df -T . | awk 'NR==2 {print $2}')
    echo -e "${GREEN}✓${NC} 文件系统: $filesystem"

    # 检查存储空间
    local avail_space=$(df -m . | awk 'NR==2 {print $4}')
    if [ $avail_space -lt 100 ]; then
        echo -e "${YELLOW}⚠️  可用空间不足: ${avail_space}MB（需要至少 100MB）${NC}"
        return 1
    fi
    echo -e "${GREEN}✓${NC} 可用空间: ${avail_space}MB"

    echo ""
    return 0
}

# ============================================================================
# 华为设备特殊优化
# ============================================================================
optimize_for_huawei() {
    echo -e "${YELLOW}正在应用华为设备优化...${NC}"

    # 设置文件权限（华为设备通常需要 755）
    chmod -R 755 "$BUNDLE_ROOT/scripts"
    chmod -R 644 "$BUNDLE_ROOT/content"/*.json
    chmod -R 644 "$BUNDLE_ROOT"/*.json
    chmod -R 644 "$BUNDLE_ROOT"/*.md

    # 创建华为特定的环境配置
    cat > "$BUNDLE_ROOT/.huawei_env" << 'EOF'
# 华为设备特定环境配置
export LU_TAIJI_DEVICE=huawei
export LU_TAIJI_FS_COMPAT=true
export LU_TAIJI_OPTIMIZED=true
EOF

    echo -e "${GREEN}✓ 华为优化已应用${NC}"
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

    # 应用华为设备优化
    optimize_for_huawei

    # 加载华为环境配置
    if [ -f "$BUNDLE_ROOT/.huawei_env" ]; then
        source "$BUNDLE_ROOT/.huawei_env"
        echo -e "${GREEN}✓ 华为环境配置已加载${NC}"
    fi

    echo -e "${BLUE}正在启动 LU-Taiji Bundle 快速安装...${NC}"
    echo ""

    # 启动快速安装
    bash "$BUNDLE_ROOT/scripts/quickstart.sh"

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✓ 华为设备启动完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "\n${CYAN}下一步操作:${NC}"
    echo -e "  1. 编辑 ${GREEN}.env${NC} 配置文件"
    echo -e "  2. 运行 ${GREEN}node scripts/validate_schema.mjs${NC}"
    echo -e "  3. 运行 ${GREEN}node scripts/import_notion.mjs${NC}"
    echo ""
}

# ============================================================================
# 执行主函数
# ============================================================================
main "$@"
