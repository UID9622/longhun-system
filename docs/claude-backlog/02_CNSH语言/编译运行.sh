#!/bin/bash
# CNSH快速编译运行脚本

echo "🇨🇳 CNSH编译运行工具"
echo "━━━━━━━━━━━━━━━━━━"

# 获取输入文件名
INPUT_FILE="${1:-hello.cnsh}"

# 检查文件是否存在
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ 找不到文件：$INPUT_FILE"
    echo ""
    echo "📝 使用方法："
    echo "   bash 编译运行.sh [文件名.cnsh]"
    echo ""
    echo "示例："
    echo "   bash 编译运行.sh hello.cnsh"
    echo "   bash 编译运行.sh 个体户收支分析.cnsh"
    exit 1
fi

echo "📄 编译文件：$INPUT_FILE"
echo ""

# 编译CNSH代码
echo "🔧 开始编译..."
node cnsh-compiler.js "$INPUT_FILE"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 编译失败！"
    exit 1
fi

# 提取基础文件名（去掉扩展名）
BASENAME=$(basename "$INPUT_FILE" .cnsh)
C_FILE="${BASENAME}.c"
EXE_FILE="${BASENAME}"

echo ""
echo "✅ CNSH代码编译完成！"
echo "📄 生成文件：$C_FILE"
echo ""

# 检查C文件是否存在
if [ ! -f "$C_FILE" ]; then
    echo "❌ 找不到生成的C文件：$C_FILE"
    exit 1
fi

# 编译C代码
echo "🔧 编译C代码..."
gcc "$C_FILE" -o "$EXE_FILE"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ C代码编译失败！"
    exit 1
fi

echo ""
echo "✅ C代码编译完成！"
echo "🎯 生成可执行文件：$EXE_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━"
echo "🚀 运行程序："
echo "━━━━━━━━━━━━━━━━━━"
echo ""

# 运行程序
"./$EXE_FILE"

echo ""
echo "━━━━━━━━━━━━━━━━━━"
echo "✅ 程序执行完成！"
