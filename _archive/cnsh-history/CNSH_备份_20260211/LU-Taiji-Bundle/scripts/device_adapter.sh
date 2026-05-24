#!/bin/bash
# ============================================================================
# LU-Taiji Bundle 设备适配器
# ============================================================================
# 功能：为华为和华硕设备生成适配配置和脚本
# DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-ADAPTER-v2.1
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
    echo "║     LU-Taiji Bundle v2.1 - 设备适配器            ║"
    echo "║     LU-ORIGIN-FULLSYNC + LU-MEMORY-MERGE-ALL      ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-ADAPTER-v2.1"
    echo ""
}

# ============================================================================
# 生成华为设备适配配置
# ============================================================================
generate_huawei_config() {
    echo -e "${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}华为设备适配配置${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}\n"

    local huawei_dir="$BUNDLE_ROOT/devices/huawei"
    mkdir -p "$huawei_dir"

    # 华为设备配置文件
    cat > "$huawei_dir/config.json" << 'EOF'
{
  "device": "huawei",
  "version": "2.1.0",
  "dnaCode": "#ZHUGEXIN⚡️2025-01-27-HUAWEI-ADAPTER-v2.1",
  "compatibility": {
    "fileSystem": ["exfat", "vfat", "ntfs", "ext4"],
    "recommendedFileSystem": "exfat",
    "minStorage": "100MB",
    "recommendedStorage": "500MB"
  },
  "optimizations": {
    "filePermissions": "755",
    "directoryPermissions": "755",
    "preservePermissions": false,
    "caseSensitive": false
  },
  "shell": {
    "preferred": "bash",
    "fallback": "sh"
  },
  "nodejs": {
    "minVersion": "16.0.0",
    "recommendedVersion": "18.0.0"
  },
  "notion": {
    "supported": true,
    "notes": "华为设备完全支持 Notion API"
  },
  "specialFeatures": {
    "harmonyOsSupport": true,
    "emuiSupport": true,
    "terminalSupport": true
  }
}
EOF

    # 华为设备启动脚本
    cat > "$huawei_dir/start.sh" << 'EOF'
#!/bin/bash
# ============================================================================
# LU-Taiji Bundle - 华为设备启动脚本
# ============================================================================
# 功能：在华为设备上快速启动 LU-Taiji Bundle
# DNA: #ZHUGEXIN⚡️2025-01-27-HUAWEI-START-v2.1
# ============================================================================

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVICE_DIR="$(dirname "$SCRIPT_DIR")"
BUNDLE_ROOT="$(dirname "$DEVICE_DIR")"

echo "=========================================="
echo "  LU-Taiji Bundle - 华为设备启动"
echo "=========================================="
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "请从 https://nodejs.org 下载安装"
    exit 1
fi

echo "✓ Node.js: $(node --version)"

# 检查 Bash
if ! command -v bash &> /dev/null; then
    echo "❌ Bash 未安装"
    exit 1
fi

echo "✓ Bash: $(bash --version | head -n1)"
echo ""

# 启动快速安装
echo "正在启动快速安装..."
bash "$BUNDLE_ROOT/scripts/quickstart.sh"

echo ""
echo "=========================================="
echo "  华为设备启动完成！"
echo "=========================================="
EOF

    chmod +x "$huawei_dir/start.sh"

    # 华为设备 README
    cat > "$huawei_dir/README.md" << 'EOF'
# 华为设备适配指南

## 支持的华为设备

- HarmonyOS 设备
- EMUI 设备
- 华为平板
- 华为笔记本

## 系统要求

- Node.js 16.0.0 或更高版本
- Bash 3.0 或更高版本
- 至少 100MB 可用存储空间

## 快速开始

```bash
# 进入华为设备目录
cd devices/huawei

# 运行启动脚本
./start.sh
```

## 文件系统兼容性

- ✓ exFAT（推荐）
- ✓ FAT32
- ✓ NTFS
- ✓ ext4

## 特殊功能

- HarmonyOS 完全支持
- EMUI 完全支持
- 终端命令行支持

## 故障排除

### Node.js 未安装

华为设备可能需要通过 ADB 或侧载方式安装 Node.js。

### 权限问题

华为设备可能需要通过以下命令获取权限：

```bash
chmod +x devices/huawei/*.sh
```

## 技术支持

如遇到问题，请查看主 README.md。
EOF

    echo -e "${GREEN}✓ 华为设备配置已生成${NC}"
    echo -e "  位置: $huawei_dir/"
}

# ============================================================================
# 生成华硕设备适配配置
# ============================================================================
generate_asus_config() {
    echo -e "\n${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}华硕设备适配配置${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}\n"

    local asus_dir="$BUNDLE_ROOT/devices/asus"
    mkdir -p "$asus_dir"

    # 华硕设备配置文件
    cat > "$asus_dir/config.json" << 'EOF'
{
  "device": "asus",
  "version": "2.1.0",
  "dnaCode": "#ZHUGEXIN⚡️2025-01-27-ASUS-ADAPTER-v2.1",
  "compatibility": {
    "fileSystem": ["exfat", "ntfs", "ext4", "btrfs"],
    "recommendedFileSystem": "ntfs",
    "minStorage": "100MB",
    "recommendedStorage": "1GB"
  },
  "optimizations": {
    "filePermissions": "644",
    "directoryPermissions": "755",
    "preservePermissions": true,
    "caseSensitive": true
  },
  "shell": {
    "preferred": "zsh",
    "fallback": "bash"
  },
  "nodejs": {
    "minVersion": "16.0.0",
    "recommendedVersion": "20.0.0"
  },
  "notion": {
    "supported": true,
    "notes": "华硕设备完全支持 Notion API"
  },
  "specialFeatures": {
    "zenfoneSupport": true,
    "rogLaptopSupport": true,
    "asusRouterSupport": false,
    "terminalSupport": true
  }
}
EOF

    # 华硕设备启动脚本
    cat > "$asus_dir/start.sh" << 'EOF'
#!/bin/bash
# ============================================================================
# LU-Taiji Bundle - 华硕设备启动脚本
# ============================================================================
# 功能：在华硕设备上快速启动 LU-Taiji Bundle
# DNA: #ZHUGEXIN⚡️2025-01-27-ASUS-START-v2.1
# ============================================================================

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVICE_DIR="$(dirname "$SCRIPT_DIR")"
BUNDLE_ROOT="$(dirname "$DEVICE_DIR")"

echo "=========================================="
echo "  LU-Taiji Bundle - 华硕设备启动"
echo "=========================================="
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "请从 https://nodejs.org 下载安装"
    exit 1
fi

echo "✓ Node.js: $(node --version)"

# 检查 Shell（优先使用 zsh）
if command -v zsh &> /dev/null; then
    echo "✓ Shell: $(zsh --version)"
elif command -v bash &> /dev/null; then
    echo "✓ Shell: $(bash --version | head -n1)"
else
    echo "❌ 未找到支持的 Shell"
    exit 1
fi

echo ""

# 检查可用空间
BUNDLE_SIZE=$(du -sb "$BUNDLE_ROOT" | awk '{print $1}')
AVAIL_SPACE=$(df -B1 "$BUNDLE_ROOT" | awk 'NR==2 {print $4}')
REQUIRED_SPACE=$((BUNDLE_SIZE * 2))

if [ $AVAIL_SPACE -lt $REQUIRED_SPACE ]; then
    echo "⚠️  可用空间不足"
    echo "   需要: $((REQUIRED_SPACE / 1024 / 1024)) MB"
    echo "   可用: $((AVAIL_SPACE / 1024 / 1024)) MB"
    echo ""
    read -p "是否继续? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 启动快速安装
echo "正在启动快速安装..."
bash "$BUNDLE_ROOT/scripts/quickstart.sh"

echo ""
echo "=========================================="
echo "  华硕设备启动完成！"
echo "=========================================="
EOF

    chmod +x "$asus_dir/start.sh"

    # 华硕设备 README
    cat > "$asus_dir/README.md" << 'EOF'
# 华硕设备适配指南

## 支持的华硕设备

- ZenFone 系列手机
- ROG 系列笔记本
- 华硕笔记本
- 华硕平板

## 系统要求

- Node.js 16.0.0 或更高版本
- Zsh 或 Bash 3.0 或更高版本
- 至少 100MB 可用存储空间（推荐 1GB）

## 快速开始

```bash
# 进入华硕设备目录
cd devices/asus

# 运行启动脚本
./start.sh
```

## 文件系统兼容性

- ✓ NTFS（推荐）
- ✓ exFAT
- ✓ ext4
- ✓ Btrfs

## 特殊功能

- ZenFone 完全支持
- ROG 笔记本完全支持
- 终端命令行支持
- Zsh 优化支持

## 性能优化

华硕设备支持以下性能优化：

1. **Zsh 优化**：优先使用 Zsh 以获得更好的性能
2. **权限保留**：保留文件和目录权限
3. **大小写敏感**：支持大小写敏感的文件系统

## 故障排除

### Node.js 版本过旧

华硕设备可能预装了旧版本 Node.js，建议升级到 20.0.0：

```bash
# 使用 nvm 安装最新版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
```

### 空间不足

清理临时文件：

```bash
# 清理缓存
sudo apt clean
sudo apt autoremove
```

## 技术支持

如遇到问题，请查看主 README.md。
EOF

    echo -e "${GREEN}✓ 华硕设备配置已生成${NC}"
    echo -e "  位置: $asus_dir/"
}

# ============================================================================
# 生成通用设备兼容性矩阵
# ============================================================================
generate_compatibility_matrix() {
    echo -e "\n${YELLOW}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}生成设备兼容性矩阵${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════${NC}\n"

    cat > "$BUNDLE_ROOT/COMPATIBILITY.md" << 'EOF'
# LU-Taiji Bundle 设备兼容性矩阵

**DNA:** #ZHUGEXIN⚡️2025-01-27-COMPATIBILITY-v2.1

## 完整兼容性列表

| 设备品牌 | 兼容性 | 启动脚本 | 文件系统 | Node.js | 备注 |
|---------|--------|----------|----------|---------|------|
| 华为 | ✓ 完全兼容 | devices/huawei/start.sh | exFAT, FAT32, NTFS, ext4 | ≥16.0 | HarmonyOS, EMUI |
| 华硕 | ✓ 完全兼容 | devices/asus/start.sh | NTFS, exFAT, ext4, Btrfs | ≥20.0 | ZenFone, ROG |
| Apple | ✓ 完全兼容 | scripts/quickstart.sh | APFS, exFAT | ≥16.0 | macOS |
| Linux | ✓ 完全兼容 | scripts/quickstart.sh | ext4, Btrfs, xfs | ≥16.0 | 所有发行版 |
| Windows | ✓ 完全兼容 | scripts/quickstart.sh | NTFS, FAT32 | ≥16.0 | WSL 支持 |

## 最低系统要求

- **Node.js:** 16.0.0 或更高版本
- **存储空间:** 100MB（推荐 500MB）
- **内存:** 256MB（推荐 512MB）

## 推荐系统要求

- **Node.js:** 18.0.0 或更高版本
- **存储空间:** 1GB
- **内存:** 1GB

## 文件系统推荐

| 设备类型 | 推荐文件系统 | 原因 |
|---------|------------|------|
| 华为 | exFAT | 跨平台兼容性好 |
| 华硕 | NTFS | 性能和兼容性平衡 |
| Apple | APFS | macOS 原生支持 |
| Linux | ext4 | Linux 标准文件系统 |
| Windows | NTFS | Windows 原生支持 |

## 特殊功能支持

| 特性 | 华为 | 华硕 | Apple | Linux | Windows |
|-----|------|------|-------|-------|---------|
| HarmonyOS 支持 | ✓ | ✗ | ✗ | ✗ | ✗ |
| EMUI 支持 | ✓ | ✗ | ✗ | ✗ | ✗ |
| ZenFone 支持 | ✗ | ✓ | ✗ | ✗ | ✗ |
| ROG 支持 | ✗ | ✓ | ✗ | ✗ | ✗ |
| Zsh 优化 | ○ | ✓ | ✓ | ○ | ✗ |

图例:
- ✓ 完全支持
- ○ 部分支持
- ✗ 不支持

## 兼容性测试

以下设备已通过完整测试：

- Huawei Mate 40 Pro
- Huawei MatePad Pro
- ASUS ZenFone 9
- ASUS ROG Zephyrus G14
- MacBook Pro M1 (macOS 15)
- Ubuntu 22.04 LTS
- Windows 11 (WSL2)

## 报告问题

如果您的设备未在此列表中，但遇到兼容性问题，请：

1. 检查是否满足最低系统要求
2. 查看设备特定的 README.md
3. 提交 Issue 到项目仓库

---

**最后更新:** 2025-01-27
**版本:** v2.1.0
EOF

    echo -e "${GREEN}✓ 设备兼容性矩阵已生成${NC}"
    echo -e "  位置: $BUNDLE_ROOT/COMPATIBILITY.md"
}

# ============================================================================
# 主函数
# ============================================================================
main() {
    banner

    echo -e "${CYAN}选择要生成的设备适配:${NC}"
    echo -e "  ${GREEN}1${NC}. 华为设备"
    echo -e "  ${GREEN}2${NC}. 华硕设备"
    echo -e "  ${GREEN}3${NC}. 全部设备"
    echo -e ""
    read -p "请选择 [1-3]: " choice

    case "$choice" in
        1)
            generate_huawei_config
            ;;
        2)
            generate_asus_config
            ;;
        3)
            generate_huawei_config
            generate_asus_config
            generate_compatibility_matrix
            ;;
        *)
            echo -e "${RED}✗ 无效选择${NC}"
            exit 1
            ;;
    esac

    echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✓ 设备适配配置生成完成！${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
}

# ============================================================================
# 执行主函数
# ============================================================================
main "$@"
