#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂流控压测 · 环境准备
# DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-PREPARE-ENV-UID9622
# License: MulanPSL v2 (工程层)

set -e

echo "🐉 龍魂流控压测 · 环境准备"
echo "============================"

# 检查依赖
echo "📋 检查 Python 依赖..."
pip show locust > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "  ❌ locust 未安装，正在安装..."
    pip install locust
fi
echo "  ✅ locust 已安装"

# 检查配置文件
echo "📋 检查配置文件..."
if [ ! -f "config/flow_control.yaml" ]; then
    echo "  ⚠️ 配置文件不存在，使用默认配置"
else
    echo "  ✅ 配置文件存在"
fi

# 创建测试数据目录
echo "📋 创建测试数据目录..."
mkdir -p tests/test_data
mkdir -p tests/reports

# 生成测试prompt库
echo "📋 生成测试prompt库..."
cat > tests/test_data/prompts.txt << 'EOF'
请用 200 字介绍一下龍魂 AI 网关的架构设计
解释一下 TokenBucket 算法的原理
如何实现流式输出的限速控制？
降级策略 passthrough/degrade/block 的区别是什么？
写一个 Python 的 TokenBucket 实现
三色审计的R值计算公式是什么？
DNA追溯码如何保证不可篡改？
龍魂系统的史官机制是如何工作的？
EOF

echo "✅ 环境准备完成"
