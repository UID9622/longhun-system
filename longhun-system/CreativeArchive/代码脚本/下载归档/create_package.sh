#!/bin/bash
# 龍魂操作系统打包脚本
# DNA追溯码: #龍芯⚡️2026-02-02-打包脚本-v1.0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐉 龍魂操作系统 v1.0 - 打包程序"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 创建打包目录
PACKAGE_DIR="longhun-os-v1.0-universal"
echo "📦 创建打包目录: $PACKAGE_DIR"
rm -rf $PACKAGE_DIR
mkdir -p $PACKAGE_DIR

# 创建子目录
mkdir -p $PACKAGE_DIR/core
mkdir -p $PACKAGE_DIR/web
mkdir -p $PACKAGE_DIR/docs
mkdir -p $PACKAGE_DIR/examples

echo "✅ 目录结构创建完成"
echo ""

# 复制核心系统文件
echo "📋 复制核心系统..."
cp longhun_police_system.py $PACKAGE_DIR/core/
cp longhun_dual_auth.py $PACKAGE_DIR/core/
cp longhun_os.py $PACKAGE_DIR/core/
cp cnsh_compiler.py $PACKAGE_DIR/core/ 2>/dev/null || echo "  跳过: cnsh_compiler.py"
echo "✅ 核心系统复制完成"
echo ""

# 复制Web界面
echo "🌐 复制Web界面..."
cp cnsh-editor-v2.html $PACKAGE_DIR/web/ 2>/dev/null || echo "  跳过: cnsh-editor-v2.html"
cp dual-auth-demo.html $PACKAGE_DIR/web/
cp longhun-os-console.html $PACKAGE_DIR/web/
echo "✅ Web界面复制完成"
echo ""

# 复制演示脚本
echo "🎬 复制演示脚本..."
cp demo_scam_detection.py $PACKAGE_DIR/examples/ 2>/dev/null || echo "  跳过: demo_scam_detection.py"
echo "✅ 演示脚本复制完成"
echo ""

# 复制文档
echo "📚 复制文档..."
cp POLICE_SYSTEM_DEPLOYMENT.md $PACKAGE_DIR/docs/ 2>/dev/null || echo "  跳过文档1"
cp DUAL_AUTH_DEPLOYMENT.md $PACKAGE_DIR/docs/ 2>/dev/null || echo "  跳过文档2"
cp AI_OPTIMIZATION_PLAN.md $PACKAGE_DIR/docs/ 2>/dev/null || echo "  跳过文档3"
cp QUANTUM_OPTIMIZATION.md $PACKAGE_DIR/docs/ 2>/dev/null || echo "  跳过文档4"
cp TODAY_DELIVERY_SUMMARY.md $PACKAGE_DIR/docs/ 2>/dev/null || echo "  跳过文档5"
echo "✅ 文档复制完成"
echo ""

echo "📦 正在打包..."
