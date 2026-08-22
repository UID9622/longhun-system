#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂湍流治理框架 · arXiv 一键打包脚本
# DNA: #龍芯⚡️丙午·乙未·辛酉·甲午·䷯井-TURBULENCE-PACKAGE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC_DIR="$PROJECT_ROOT/arxiv/turbulence-longhun-v3.1"
DIST_DIR="$PROJECT_ROOT/dist"
ZIP_NAME="turbulence-longhun-v3.1-arxiv.zip"

echo "=== 龍魂湍流治理框架 · arXiv 打包 ==="
echo "DNA: #龍芯⚡️丙午·乙未·辛酉·甲午·䷯井-TURBULENCE-PACKAGE-v1.0"

# 检查源文件
if [ ! -f "$SRC_DIR/turbulence-longhun-v3.1.tex" ]; then
    echo "错误：LaTeX 源文件不存在"
    exit 1
fi
if [ ! -f "$SRC_DIR/turbulence-longhun-v3.1.bbl" ]; then
    echo "错误：bbl 文件不存在"
    exit 1
fi

# 编译验证
echo "[1/3] 编译验证..."
cd "$SRC_DIR"
pdflatex -interaction=nonstopmode turbulence-longhun-v3.1.tex > /tmp/turbulence_arxiv_build.log 2>&1
if [ ! -f turbulence-longhun-v3.1.pdf ]; then
    echo "错误：编译失败，查看 /tmp/turbulence_arxiv_build.log"
    exit 1
fi
echo "      ✅ 编译成功"

# 清理辅助文件
echo "[2/3] 清理辅助文件..."
rm -f "$SRC_DIR"/*.aux "$SRC_DIR"/*.log "$SRC_DIR"/*.out "$SRC_DIR"/*.toc "$SRC_DIR"/*.pdf

# 打包
echo "[3/3] 生成 zip..."
mkdir -p "$DIST_DIR"
cd "$PROJECT_ROOT/arxiv"
zip -r "$DIST_DIR/$ZIP_NAME" turbulence-longhun-v3.1/

echo ""
echo "=== 打包完成 ==="
echo "输出: $DIST_DIR/$ZIP_NAME"
echo "内容:"
unzip -l "$DIST_DIR/$ZIP_NAME"
