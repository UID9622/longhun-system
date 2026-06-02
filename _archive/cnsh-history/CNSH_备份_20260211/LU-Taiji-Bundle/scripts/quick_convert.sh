#!/bin/bash
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: quick_convert.sh | 标记时间: 2026-06-03T07:46:00+0800
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
