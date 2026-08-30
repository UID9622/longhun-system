#!/bin/bash
# 🐉 CNSH 测试工具链 · 一键安装
# DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-TEST-SETUP-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层

set -e
echo "🐉 CNSH 测试工具链 v1.0 · 安装开始"
echo "DNA: #龍芯⚡️$(date +%Y-%m-%d)-TEST-SETUP-UID9622"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT"

# Step 1: 目录结构
echo "[1/7] 创建目录结构..."
mkdir -p include bin tests/cnsh_samples tests/transpile test_reports _work

# Step 2: Python 依赖
echo "[2/7] 安装 Python 依赖..."
pip3 install -q pyyaml 2>/dev/null || true

# Step 3: 文件权限
echo "[3/7] 设置脚本权限..."
chmod +x bin/cnsh_test_runner.py bin/cnsh_dna_check.py \
          bin/cnsh_coverage.py bin/lh_audit_gate.py 2>/dev/null || true

# Step 4: 创建示例测试文件（真实 CNSH 语法: 功能/打印/如果/循环）
echo "[4/7] 创建示例测试文件..."
if [ ! -f tests/cnsh_samples/test_hello.cnsh ]; then
cat > tests/cnsh_samples/test_hello.cnsh << 'EOF'
# DNA: #龍芯⚡️$(date +%Y-%m-%d)-CNSH-HELLO-v1.0-UID9622
功能 主() {
    打印("龍魂系统·CNSH测试通过")
}
EOF
fi

# Step 5: 验证编译器
echo "[5/7] 验证 CNSH 编译器..."
python3 bin/cnsh_compiler.py --version 2>&1 | tail -1

# Step 6: 运行 DNA 校验（快速验证工具链）
echo "[6/7] 快速验证 DNA 校验工具..."
python3 bin/cnsh_dna_check.py --loose 2>&1 | tail -2 || true

# Step 7: 运行测试运行器（冒烟）
echo "[7/7] 测试运行器冒烟..."
python3 bin/cnsh_test_runner.py 2>&1 | tail -6 || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ CNSH 测试工具链安装完成"
echo "🚀 立即可用: python3 bin/cnsh_test_runner.py"
echo "🚀 正规审计闸: python3 bin/lh_audit_gate.py"
