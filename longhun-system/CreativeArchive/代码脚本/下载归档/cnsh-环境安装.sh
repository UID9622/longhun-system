#!/bin/bash
# CNSH环境一键安装脚本
# DNA追溯码：#ZHUGEXIN-2026-01-27-环境安装
# 创建者：诸葛鑫（UID9622）

echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🇨🇳 CNSH环境一键安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否已安装Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 正在安装Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "✅ Homebrew安装完成"
else
    echo "✅ Homebrew已安装"
fi

echo ""

# 检查是否已安装Node.js
if ! command -v node &> /dev/null; then
    echo "📦 正在安装Node.js..."
    brew install node
    echo "✅ Node.js安装完成"
else
    echo "✅ Node.js已安装"
    echo "   版本：$(node --version)"
fi

echo ""

# 检查GCC（Mac自带）
if command -v gcc &> /dev/null; then
    echo "✅ GCC已就绪（Mac自带）"
    echo "   版本：$(gcc --version | head -n 1)"
else
    echo "⚠️  GCC未找到，需要安装Xcode Command Line Tools"
    echo "📦 正在安装..."
    xcode-select --install
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 环境安装完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 现在可以运行CNSH程序了："
echo "   1. node cnsh-compiler.js 你的程序.cnsh"
echo "   2. gcc 生成的.c -o 输出文件"
echo "   3. ./输出文件"
echo ""
echo "🧬 DNA追溯已生效"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
