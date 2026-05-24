#!/bin/bash
# ============================================================================
# LU-Taiji Bundle 校验和生成器
# ============================================================================
# 功能：计算所有文件的 SHA256 校验和，更新 manifest.json
# DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-CHECKSUM-v2.1
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
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
NC='\033[0m'         # 重置颜色

echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  LU-Taiji Bundle 校验和生成器${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}\n"

# ============================================================================
# 定义校验和文件路径
# ============================================================================
CHECKSUM_FILE="$BUNDLE_ROOT/CHECKSUMS.txt"
CHECKSUM_SHA256_FILE="$BUNDLE_ROOT/CHECKSUMS.sha256"

# ============================================================================
# 清空校验和文件
# ============================================================================
: > "$CHECKSUM_FILE"
: > "$CHECKSUM_SHA256_FILE"

# ============================================================================
# 步骤 1: 计算所有 JSON/JS/Shell 文件的校验和
# ============================================================================
echo -e "${YELLOW}[1/2] 正在计算校验和...${NC}"
cd "$BUNDLE_ROOT"

# 遍历所有相关文件并计算 SHA256
find . -type f \( -name "*.json" -o -name "*.mjs" -o -name "*.sh" \) | sort | while read -r file; do
    # 跳过校验和文件本身
    if [[ "$file" == "./CHECKSUMS.txt" ]] || [[ "$file" == "./CHECKSUMS.sha256" ]]; then
        continue
    fi

    # 计算 SHA256
    sha256sum=$(shasum -a 256 "$file" | awk '{print $1}')
    echo "$sha256sum  $file" >> "$CHECKSUM_SHA256_FILE"
    echo -e "  ${GREEN}✓${NC} $file"
done

# ============================================================================
# 步骤 2: 生成清单摘要
# ============================================================================
echo -e "\n${YELLOW}[2/2] 正在生成清单摘要...${NC}"

# 写入摘要信息
{
    echo "LU-Taiji Bundle v2.1 - 校验和摘要"
    echo "生成时间: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-CHECKSUM-v2.1"
    echo ""
    echo "文件数量: $(find . -type f \( -name "*.json" -o -name "*.mjs" -o -name "*.sh" \) | wc -l | tr -d ' ')"
    echo "总大小: $(du -sh . | cut -f1)"
    echo ""
    echo "--- SHA256 校验和 ---"
    cat "$CHECKSUM_SHA256_FILE"
} >> "$CHECKSUM_FILE"

# ============================================================================
# 步骤 3: 更新 manifest.json 中的 checksum 字段
# ============================================================================
echo -e "\n${YELLOW}正在更新 manifest.json...${NC}"
MANIFEST_SHA256=$(shasum -a 256 "$BUNDLE_ROOT/manifest.json" | awk '{print $1}')

# 使用临时文件更新 manifest（避免 jq 依赖）
if command -v jq &> /dev/null; then
    jq --arg sum "$MANIFEST_SHA256" '.checksum.manifest = $sum' "$BUNDLE_ROOT/manifest.json" > "$BUNDLE_ROOT/manifest.json.tmp"
    mv "$BUNDLE_ROOT/manifest.json.tmp" "$BUNDLE_ROOT/manifest.json"
    echo -e "  ${GREEN}✓ manifest.json 已更新${NC}"
else
    echo -e "  ${YELLOW}⚠ 未找到 jq，跳过 manifest 更新${NC}"
    echo -e "  ${YELLOW}  manifest 校验和: $MANIFEST_SHA256${NC}"
fi

# ============================================================================
# 完成
# ============================================================================
echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ 校验和生成完成！${NC}"
echo -e "${GREEN}    校验和已保存到:${NC}"
echo -e "    - $CHECKSUM_SHA256_FILE"
echo -e "    - $CHECKSUM_FILE"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
