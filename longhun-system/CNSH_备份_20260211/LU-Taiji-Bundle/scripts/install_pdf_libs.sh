#!/bin/bash
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
