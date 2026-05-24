#!/bin/bash
# 依赖安装脚本
echo "=========================================="
echo "安装 PDF 解析库"
echo "=========================================="

# 安装 PyPDF2
echo "安装 PyPDF2..."
python3 -m pip install --user PyPDF2

# 安装 pdfplumber
echo "安装 pdfplumber..."
python3 -m pip install --user pdfplumber

echo "=========================================="
echo "安装完成！"
echo "=========================================="
