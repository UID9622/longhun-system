#!/bin/bash
# 快速转换脚本 - 转换指定的大文件
# DNA: #ZHUGEXIN⚡️2026-01-27-QUICK-CONVERT-v1.0

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUNDLE_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE_ROOT="$(dirname "$BUNDLE_ROOT")"

echo "=========================================="
echo "快速转换大文件为文本"
echo "=========================================="
echo ""

# 转换 CNSH_Language_Documentation.docx (2.53 MB)
if [ -f "$WORKSPACE_ROOT/CNSH_Language_Documentation.docx" ]; then
    echo "📄 转换: CNSH_Language_Documentation.docx"
    bash "$SCRIPT_DIR/convert_binary_to_text.sh" -f "$WORKSPACE_ROOT/CNSH_Language_Documentation.docx"
    echo ""
fi

# 转换提取文字_体系.pdf (57.47 MB)
if [ -f "$WORKSPACE_ROOT/UID9622/未命名文件夹/提取文字_体系.pdf" ]; then
    echo "📄 转换: 提取文字_体系.pdf"
    bash "$SCRIPT_DIR/convert_binary_to_text.sh" -f "$WORKSPACE_ROOT/UID9622/未命名文件夹/提取文字_体系.pdf"
    echo ""
fi

# 批量转换 UID9622 目录下的所有 PDF
if [ -d "$WORKSPACE_ROOT/UID9622/未命名文件夹" ]; then
    echo "📁 批量转换: UID9622/未命名文件夹/"
    bash "$SCRIPT_DIR/convert_binary_to_text.sh" -d "$WORKSPACE_ROOT/UID9622/未命名文件夹"
    echo ""
fi

echo "=========================================="
echo "✅ 转换完成！"
echo "输出目录: $BUNDLE_ROOT/text_content/"
echo "=========================================="
