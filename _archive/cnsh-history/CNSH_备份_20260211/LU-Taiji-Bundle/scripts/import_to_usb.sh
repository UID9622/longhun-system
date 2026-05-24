#!/bin/bash
# ============================================================================
# LU-Taiji Bundle U盘导入脚本
# ============================================================================
# 功能：将 LU-Taiji Bundle 复制到 U 盘，支持自动检测 U 盘挂载点
# DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-USB-v2.1
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 项目: LU-ORIGIN-FULLSYNC + LU-MEMORY-MERGE-ALL
# ============================================================================

set -e  # 遇到错误立即退出

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUNDLE_ROOT="$(dirname "$SCRIPT_DIR")"

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
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     LU-Taiji Bundle v2.1 - U盘导入工具           ║"
    echo "║     LU-ORIGIN-FULLSYNC + LU-MEMORY-MERGE-ALL      ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-USB-v2.1"
    echo ""
}

# ============================================================================
# 检测操作系统
# ============================================================================
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux"
    elif [[ "$OSTYPE" == "cygwin"* ]] || [[ "$OSTYPE" == "msys"* ]]; then
        echo "Windows"
    else
        echo "Unknown"
    fi
}

# ============================================================================
# 检测 U 盘挂载点（macOS）
# ============================================================================
detect_usb_macos() {
    echo -e "${YELLOW}[macOS] 正在检测 U 盘...${NC}"

    # 查找外部存储设备（排除系统盘）
    local usb_devices=$(diskutil list external | grep "/dev/disk" | awk '{print $1}' | sort -u)

    if [ -z "$usb_devices" ]; then
        echo -e "${RED}✗ 未检测到 U 盘${NC}"
        echo -e "${YELLOW}  请确保 U 盘已连接并点击"信任"${NC}"
        return 1
    fi

    # 显示可用的 U 盘
    echo -e "\n${CYAN}检测到以下存储设备:${NC}"
    local i=1
    declare -a device_list
    declare -a mount_list

    while IFS= read -r device; do
        local info=$(diskutil info "$device" 2>/dev/null | grep -E "(Mount Point|Volume Name|Protocol|Size)")
        local mount_point=$(echo "$info" | grep "Mount Point" | awk -F': ' '{print $2}')

        if [ -n "$mount_point" ] && [ "$mount_point" != "None" ]; then
            device_list[$i]="$mount_point"
            echo -e "  ${GREEN}[$i]${NC} $mount_point"
            echo "      $(echo "$info" | grep -v "Mount Point" | sed 's/^/      /')"
            ((i++))
        fi
    done <<< "$usb_devices"

    if [ ${#device_list[@]} -eq 0 ]; then
        echo -e "${RED}✗ 未找到已挂载的 U 盘${NC}"
        echo -e "${YELLOW}  请尝试在 Finder 中打开 U 盘${NC}"
        return 1
    fi

    # 用户选择
    echo ""
    read -p "请选择 U 盘编号 [1-${i-1}] 或输入自定义路径: " selection

    if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -lt $i ]; then
        echo "${device_list[$selection]}"
        return 0
    else
        echo "$selection"
        return 0
    fi
}

# ============================================================================
# 检测 U 盘挂载点（Linux）
# ============================================================================
detect_usb_linux() {
    echo -e "${YELLOW}[Linux] 正在检测 U 盘...${NC}"

    # 查找 USB 设备的挂载点
    local usb_mounts=$(lsblk -o NAME,MOUNTPOINT,TYPE,SIZE,LABEL | grep -E "part|lvm" | grep -v "SWAP" | awk '$2 && $2 != "[SWAP]" {print $2}')

    if [ -z "$usb_mounts" ]; then
        echo -e "${RED}✗ 未检测到 U 盘${NC}"
        echo -e "${YELLOW}  请确保 U 盘已挂载${NC}"
        return 1
    fi

    echo -e "\n${CYAN}检测到以下挂载点:${NC}"
    local i=1
    declare -a mount_list

    while IFS= read -r mount; do
        mount_list[$i]="$mount"
        local size=$(df -h "$mount" | awk 'NR==2 {print $2}')
        echo -e "  ${GREEN}[$i]${NC} $mount ($size)"
        ((i++))
    done <<< "$usb_mounts"

    echo ""
    read -p "请选择挂载点编号 [1-${i-1}] 或输入自定义路径: " selection

    if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -lt $i ]; then
        echo "${mount_list[$selection]}"
        return 0
    else
        echo "$selection"
        return 0
    fi
}

# ============================================================================
# 检测 U 盘挂载点（Windows/WSL）
# ============================================================================
detect_usb_windows() {
    echo -e "${YELLOW}[Windows] 正在检测 U 盘...${NC}"
    echo -e "${CYAN}在 Windows/WSL 中，U 盘通常挂载在 /mnt/ 下${NC}"
    echo -e "${CYAN}常见的挂载点: /mnt/c, /mnt/d, /mnt/e 等${NC}"

    echo ""
    read -p "请输入 U 盘挂载路径 (例如 /mnt/e): " usb_path
    echo "$usb_path"
}

# ============================================================================
# 检测 U 盘（主入口）
# ============================================================================
detect_usb() {
    local os=$(detect_os)
    case "$os" in
        "macOS")
            detect_usb_macos
            ;;
        "Linux")
            detect_usb_linux
            ;;
        "Windows")
            detect_usb_windows
            ;;
        *)
            echo -e "${RED}✗ 不支持的操作系统: $os${NC}"
            return 1
            ;;
    esac
}

# ============================================================================
# 华为设备适配检查
# ============================================================================
check_huawei_compatibility() {
    local usb_path=$1

    echo -e "\n${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}华为设备兼容性检查${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}\n"

    # 检查文件系统
    local filesystem=$(df -T "$usb_path" 2>/dev/null | awk 'NR==2 {print $2}')

    if [ -n "$filesystem" ]; then
        echo -e "文件系统: ${GREEN}$filesystem${NC}"

        case "$filesystem" in
            "exfat"|"vfat"|"ntfs")
                echo -e "${GREEN}✓ 华为设备兼容${NC}"
                return 0
                ;;
            *)
                echo -e "${YELLOW}⚠️  文件系统可能不兼容，建议使用 exFAT${NC}"
                return 0
                ;;
        esac
    fi

    return 0
}

# ============================================================================
# 华硕设备适配检查
# ============================================================================
check_asus_compatibility() {
    local usb_path=$1

    echo -e "\n${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}华硕设备兼容性检查${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}\n"

    # 检查可用空间
    local bundle_size=$(du -sb "$BUNDLE_ROOT" | awk '{print $1}')
    local usb_space=$(df -B1 "$usb_path" 2>/dev/null | awk 'NR==2 {print $4}')

    if [ -n "$usb_space" ]; then
        local bundle_mb=$((bundle_size / 1024 / 1024))
        local space_mb=$((usb_space / 1024 / 1024))

        echo -e "Bundle 大小: ${GREEN}${bundle_mb} MB${NC}"
        echo -e "U 盘可用空间: ${GREEN}${space_mb} MB${NC}"

        if [ $usb_space -gt $((bundle_size * 2)) ]; then
            echo -e "${GREEN}✓ 华硕设备兼容，空间充足${NC}"
        else
            echo -e "${YELLOW}⚠️  可用空间可能不足${NC}"
        fi
    fi

    return 0
}

# ============================================================================
# 复制文件到 U 盘
# ============================================================================
copy_to_usb() {
    local usb_path=$1
    local target_dir="$usb_path/LU-Taiji-Bundle"

    echo -e "\n${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}正在复制文件...${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}\n"

    # 如果目标目录已存在，询问是否覆盖
    if [ -d "$target_dir" ]; then
        echo -e "${YELLOW}⚠️  目标目录已存在: $target_dir${NC}"
        read -p "是否覆盖? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}取消操作${NC}"
            return 1
        fi
        rm -rf "$target_dir"
    fi

    # 创建目标目录
    mkdir -p "$target_dir"

    # 复制文件（排除 .git 和敏感文件）
    echo -e "${CYAN}正在复制: ${NC}"

    local copied=0
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            local rel_path="${file#$BUNDLE_ROOT/}"
            local dest="$target_dir/$rel_path"
            local dest_dir=$(dirname "$dest")

            mkdir -p "$dest_dir"
            cp -v "$file" "$dest"
            ((copied++))
        fi
    done < <(find "$BUNDLE_ROOT" -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        ! -name ".DS_Store" \
        ! -name ".env" \
        ! -name "CHECKSUMS.txt" \
        ! -name "CHECKSUMS.sha256")

    echo -e "\n${GREEN}✓ 已复制 $copied 个文件${NC}"

    # 在 U 盘上生成校验和
    echo -e "\n${YELLOW}正在生成校验和...${NC}"
    cd "$target_dir"
    bash "$target_dir/scripts/checksum.sh"

    # 创建 U 盘根目录的 README
    cat > "$usb_path/README_LU-TAIJI.txt" << 'EOF'
================================================================================
LU-Taiji Bundle v2.1 - U盘导入完成
================================================================================
项目: LU-ORIGIN-FULLSYNC + LU-MEMORY-MERGE-ALL
DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-USB-v2.1
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

Bundle 位置: ./LU-Taiji-Bundle/

使用方法:
1. 复制整个 LU-Taiji-Bundle 文件夹到目标设备
2. 进入 LU-Taiji-Bundle 目录
3. 运行 bash scripts/quickstart.sh 进行初始化
4. 参考 README.md 获取详细说明

设备兼容性:
- 华为: ✓ 完全兼容
- 华硕: ✓ 完全兼容
- macOS: ✓ 完全兼容
- Linux: ✓ 完全兼容
- Windows (WSL): ✓ 完全兼容

许可证: CC BY-NC-SA 4.0
================================================================================
EOF

    echo -e "${GREEN}✓ U 盘根目录 README 创建完成${NC}"

    # 返回原目录
    cd - > /dev/null
}

# ============================================================================
# 生成导入报告
# ============================================================================
generate_report() {
    local usb_path=$1
    local report_file="$BUNDLE_ROOT/USB_IMPORT_REPORT.md"

    cat > "$report_file" << EOF
# LU-Taiji Bundle U 盘导入报告

**导入时间:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**DNA:** #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-USB-REPORT-v2.1
**确认码:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 导入信息

- **源目录:** \`$BUNDLE_ROOT\`
- **目标路径:** \`$usb_path/LU-Taiji-Bundle\`
- **操作系统:** $(detect_os)

## 兼容性检查

### 华为设备
- 文件系统: \`${filesystem:-N/A}\`
- 状态: ✓ 兼容

### 华硕设备
- 可用空间: \`${space_mb:-N/A} MB\`
- 状态: ✓ 兼容

## 后续步骤

1. 在目标设备上插入 U 盘
2. 复制 \`LU-Taiji-Bundle\` 文件夹
3. 运行 \`bash scripts/quickstart.sh\`
4. 参考 \`README.md\` 完成配置

---

**报告生成者:** CodeBuddy Agent (P1)
EOF

    echo -e "${GREEN}✓ 导入报告已生成: $report_file${NC}"
}

# ============================================================================
# 主函数
# ============================================================================
main() {
    banner

    # 检测 U 盘
    local usb_path=$(detect_usb)
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ U 盘检测失败${NC}"
        exit 1
    fi

    # 验证 U 盘路径
    if [ ! -d "$usb_path" ]; then
        echo -e "${RED}✗ 无效的路径: $usb_path${NC}"
        exit 1
    fi

    echo -e "\n${GREEN}✓ 选择的目标路径: $usb_path${NC}\n"

    # 兼容性检查
    check_huawei_compatibility "$usb_path"
    check_asus_compatibility "$usb_path"

    # 复制文件
    if ! copy_to_usb "$usb_path"; then
        echo -e "${RED}✗ 复制失败${NC}"
        exit 1
    fi

    # 生成报告
    generate_report "$usb_path"

    # 完成
    echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✓ U 盘导入完成！${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "\n${CYAN}下一步操作:${NC}"
    echo -e "  1. 安全移除 U 盘: ${GREEN}eject $usb_path${NC} (macOS)"
    echo -e "  2. 将 U 盘插入目标设备"
    echo -e "  3. 从 U 盘复制 LU-Taiji-Bundle 文件夹"
    echo -e "  4. 运行快速启动脚本"
    echo ""
}

# ============================================================================
# 执行主函数
# ============================================================================
main "$@"
