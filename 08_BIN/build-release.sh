#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 发布打包脚本
# DNA:#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-RELEASE-BUILDER-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 用法：bash bin/build-release.sh [版本号]
# 默认版本号：v5.1

set -e

VERSION="${1:-v5.1}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RELEASE_DIR="${ROOT}/releases/${VERSION}"
STAGING_DIR="${RELEASE_DIR}/staging"
ZIP_NAME="龍魂系统-${VERSION}.zip"
ZIP_PATH="${RELEASE_DIR}/${ZIP_NAME}"

echo "🐉 开始打包龍魂系统 ${VERSION}"
echo "=================================================="

# 清理旧目录
rm -rf "${STAGING_DIR}"
mkdir -p "${STAGING_DIR}"

# 要包含的核心模块
MODULES=(
    "cnsh-terminal"
    "control-panel"
    "editor"
    "xpay"
    "crypto-stack"
    "memory-universe"
    "brain"
    "agents"
    "executors/kimi-agent-v2"
    "systems/kfpp"
    "baobao-guardian"
    "protocols"
    "01_技能库"
    "02_执行记录"
    "03_知识图谱"
    "04_决策日志"
    "05_系统报告"
    "06_技术文档"
    "desktop"
    "bin"
    "skills"
    "cnsh"
    "cnsh.integrated"
)

# 复制模块
echo "📦 复制核心模块..."
for mod in "${MODULES[@]}"; do
    if [ -e "${ROOT}/${mod}" ]; then
        target_dir="${STAGING_DIR}/$(dirname "${mod}")"
        mkdir -p "${target_dir}"
        cp -R "${ROOT}/${mod}" "${target_dir}/"
        echo "  ✅ ${mod}"
    else
        echo "  ⚠️  跳过不存在：${mod}"
    fi
done

# 复制顶层文件
echo "📄 复制顶层文件..."
cp "${ROOT}/README.md" "${STAGING_DIR}/" 2>/dev/null || true
cp "${ROOT}/CNSH-PROTOCOL.md" "${STAGING_DIR}/" 2>/dev/null || true
cp "${ROOT}/CNSH-SEMANTIC.md" "${STAGING_DIR}/" 2>/dev/null || true
cp -R "${ROOT}/releases/${VERSION}/README-zh.md" "${STAGING_DIR}/README-发布说明-中文.md" 2>/dev/null || true
cp -R "${ROOT}/releases/${VERSION}/README-en.md" "${STAGING_DIR}/README-RELEASE-NOTES-EN.md" 2>/dev/null || true

# 清理不需要的文件
echo "🧹 清理临时文件..."
find "${STAGING_DIR}" -type d \( \
    -name ".git" -o \
    -name "__pycache__" -o \
    -name ".pytest_cache" -o \
    -name ".obsidian" -o \
    -name ".claude" -o \
    -name ".DS_Store" \
    \) -print0 | xargs -0 rm -rf 2>/dev/null || true

# 打包
rm -f "${ZIP_PATH}"
echo "🗜️  生成压缩包..."
cd "${RELEASE_DIR}"
zip -r -q "${ZIP_NAME}" staging

echo ""
echo "=================================================="
echo "✅ 发布包已生成：${ZIP_PATH}"
echo "📦 包含模块数：${#MODULES[@]}"
echo "🧬 DNA: #龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-RELEASE-${VERSION}"
echo "=================================================="
