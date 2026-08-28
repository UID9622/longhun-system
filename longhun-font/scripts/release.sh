#!/bin/bash
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-RELEASE-v1.0
#
# LonghunFont 发布脚本 v1.0
# 一键完成字元库校验、字体构建、样张渲染、双仓发布。
# 用法：./scripts/release.sh [版本号，例如 v0013]

set -euo pipefail

DNA="#龍芯⚡️2026-06-22-LONGHUN-FONT-RELEASE-v1.0"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RELEASE_REPO="${HOME}/longhun-system/_work/repos/LonghunFont"

# 稳定版字元库路径
GLYPH_LIBRARY="${PROJECT_DIR}/glyphs/龍魂字元库_v0013_稳定版.json"

# 输出目录
SOURCE_OUTPUT_DIR="${PROJECT_DIR}/output"
RELEASE_OUTPUT_DIR="${RELEASE_REPO}/output"

echo "============================================================"
echo "🐉 LonghunFont 发布流程"
echo "DNA: ${DNA}"
echo "项目目录: ${PROJECT_DIR}"
echo "发布仓库: ${RELEASE_REPO}"
echo "============================================================"
echo

# 若未传入版本号，从字元库元数据读取
if [ -z "${1:-}" ]; then
    if [ ! -f "${GLYPH_LIBRARY}" ]; then
        echo "❌ 稳定版字元库不存在: ${GLYPH_LIBRARY}"
        exit 1
    fi
    # 从 JSON 元数据中提取版本，并去掉 "-稳定版" 等后缀
    VERSION=$(python3 - <<PY
import json
with open("${GLYPH_LIBRARY}", "r", encoding="utf-8") as f:
    data = json.load(f)
ver = data.get("元数据", {}).get("版本", "")
ver = ver.split("-")[0] if ver else ""
print(ver)
PY
    )
    if [ -z "${VERSION}" ]; then
        echo "❌ 无法从字元库元数据解析版本号"
        exit 1
    fi
    echo "📌 未指定版本号，从字元库元数据读取: ${VERSION}"
else
    VERSION="$1"
    echo "📌 使用指定版本号: ${VERSION}"
fi

SAMPLE_HTML="sample_v${VERSION}.html"
SVG_DIR="all_glyphs_v${VERSION}"
OTF_FILE="LonghunFont-Regular.otf"
TAG_NAME="${VERSION}"

echo

# 1. 校验字元库
echo "🔍 步骤 1/7: 校验字元库"
python3 "${SCRIPT_DIR}/check_font.py" "${GLYPH_LIBRARY}"
echo

# 2. 构建 OTF 字体
echo "🔨 步骤 2/7: 构建 OTF 字体"
python3 "${SCRIPT_DIR}/build_font.py" "${GLYPH_LIBRARY}" "${SOURCE_OUTPUT_DIR}/${OTF_FILE}"
if [ ! -f "${SOURCE_OUTPUT_DIR}/${OTF_FILE}" ]; then
    echo "❌ OTF 构建失败: ${SOURCE_OUTPUT_DIR}/${OTF_FILE} 未生成"
    exit 1
fi
echo

# 3. 批量渲染 SVG 样张
echo "🎨 步骤 3/7: 批量渲染 SVG 样张"
python3 "${SCRIPT_DIR}/batch_render.py" \
    "${GLYPH_LIBRARY}" \
    "${SOURCE_OUTPUT_DIR}/${SVG_DIR}" \
    "${SOURCE_OUTPUT_DIR}/${SAMPLE_HTML}"
if [ ! -f "${SOURCE_OUTPUT_DIR}/${SAMPLE_HTML}" ]; then
    echo "❌ HTML 样张未生成: ${SOURCE_OUTPUT_DIR}/${SAMPLE_HTML}"
    exit 1
fi
echo

# 4. 复制产物到发布仓库
echo "📦 步骤 4/7: 复制产物到发布仓库"
if [ ! -d "${RELEASE_REPO}" ]; then
    echo "❌ 发布仓库不存在: ${RELEASE_REPO}"
    exit 1
fi
mkdir -p "${RELEASE_OUTPUT_DIR}"
cp -v "${SOURCE_OUTPUT_DIR}/${OTF_FILE}" "${RELEASE_OUTPUT_DIR}/${OTF_FILE}"
cp -v "${SOURCE_OUTPUT_DIR}/${SAMPLE_HTML}" "${RELEASE_OUTPUT_DIR}/${SAMPLE_HTML}"
cp -v "${GLYPH_LIBRARY}" "${RELEASE_REPO}/"
cp -v "${PROJECT_DIR}/README.md" "${RELEASE_REPO}/"
cp -v "${PROJECT_DIR}/操作清单.md" "${RELEASE_REPO}/"
mkdir -p "${RELEASE_REPO}/docs"
cp -v "${PROJECT_DIR}/docs/PUA编码表.md" "${RELEASE_REPO}/docs/"
echo

# 5. 在发布仓库提交
echo "📝 步骤 5/7: 在发布仓库提交变更"
cd "${RELEASE_REPO}"
git add -A
git commit -m "Release ${VERSION} · ${DNA}" || {
    echo "⚠️ 没有新的变更需要提交，或提交失败"
    exit 1
}
echo

# 6. 打标签
echo "🏷️  步骤 6/7: 创建 annotated 标签 ${TAG_NAME}"
git tag -a "${TAG_NAME}" -m "LonghunFont ${VERSION} · ${DNA}"
echo

# 7. 推送双仓
echo "🚀 步骤 7/7: 推送到 Gitee 与 GitHub"
./push_both.sh
echo "🏷️  推送标签 ${TAG_NAME} 到双仓"
git push origin "${TAG_NAME}"
git push github "${TAG_NAME}"
echo

# 发布摘要
echo "============================================================"
echo "✅ LonghunFont ${VERSION} 发布完成"
echo "DNA: ${DNA}"
echo "   字元库: ${GLYPH_LIBRARY}"
echo "   OTF:    ${RELEASE_OUTPUT_DIR}/${OTF_FILE}"
echo "   样张:   ${RELEASE_OUTPUT_DIR}/${SAMPLE_HTML}"
echo "   SVG:    ${SOURCE_OUTPUT_DIR}/${SVG_DIR}/"
echo "   标签:   ${TAG_NAME}"
echo "============================================================"
