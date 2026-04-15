#!/bin/bash
# 验证打包内容完整性

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 验证 longhun-os-v1.0-universal.tar.gz"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查文件是否存在
if [ ! -f "longhun-os-v1.0-universal.tar.gz" ]; then
    echo "❌ 打包文件不存在！"
    exit 1
fi

echo "✅ 打包文件存在"
echo ""

# 显示文件大小
echo "📊 文件信息:"
ls -lh longhun-os-v1.0-universal.tar.gz
echo ""

# 显示包含的文件
echo "📋 包含文件列表:"
tar -tzf longhun-os-v1.0-universal.tar.gz | wc -l
echo "个文件"
echo ""

# 验证关键文件
echo "🔍 验证关键文件:"
FILES=(
    "longhun-os-v1.0-universal/README.md"
    "longhun-os-v1.0-universal/start.sh"
    "longhun-os-v1.0-universal/start.bat"
    "longhun-os-v1.0-universal/longhun_police_system.py"
    "longhun-os-v1.0-universal/longhun_dual_auth.py"
    "longhun-os-v1.0-universal/longhun_os.py"
    "longhun-os-v1.0-universal/cnsh_compiler.py"
    "longhun-os-v1.0-universal/cnsh-editor-v2.html"
    "longhun-os-v1.0-universal/dual-auth-demo.html"
    "longhun-os-v1.0-universal/longhun-os-console.html"
)

for file in "${FILES[@]}"; do
    if tar -tzf longhun-os-v1.0-universal.tar.gz | grep -q "^${file}$"; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 验证完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
