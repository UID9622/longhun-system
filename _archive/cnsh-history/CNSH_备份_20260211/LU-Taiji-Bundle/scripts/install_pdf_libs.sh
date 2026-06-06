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
# 文件: install_pdf_libs.sh | 标记时间: 2026-06-03T07:46:00+0800
# 安装 PDF 解析库脚本
# DNA: #ZHUGEXIN⚡️2026-01-27-INSTALL-PDF-LIB-v1.0

echo "=========================================="
echo "安装 PDF 解析库"
echo "=========================================="
echo ""

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装："
    echo "   brew install python3"
    exit 1
fi

echo "✓ 找到 python3: $(python3 --version)"
echo ""

# 安装 PyPDF2
echo "📦 安装 PyPDF2..."
python3 -m pip install --user PyPDF2
if [ $? -eq 0 ]; then
    echo "✓ PyPDF2 安装成功"
else
    echo "✗ PyPDF2 安装失败"
fi
echo ""

# 安装 pdfplumber
echo "📦 安装 pdfplumber..."
python3 -m pip install --user pdfplumber
if [ $? -eq 0 ]; then
    echo "✓ pdfplumber 安装成功"
else
    echo "✗ pdfplumber 安装失败"
fi
echo ""

echo "=========================================="
echo "✅ 安装完成！"
echo ""
echo "现在可以运行："
echo "  bash scripts/quick_convert.sh"
echo "=========================================="
