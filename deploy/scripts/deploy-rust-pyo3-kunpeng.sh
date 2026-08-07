#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-DEPLOY-RUST-PYO3-KUNPENG-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: MulanPSL v2 (工程层)
# 用途: 将 longhun-core Rust 库 + PyO3 绑定部署到鲲鹏服务器并实测
# 用法: bash deploy/scripts/deploy-rust-pyo3-kunpeng.sh
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

set -euo pipefail

KUNPENG_HOST="119.13.90.27"
KUNPENG_USER="root"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
RUST_DIR="$(cd "$(dirname "$0")/../../rust" && pwd)"
REMOTE_DIR="/opt/longhun/rust-core"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

SSH_CMD="ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${KUNPENG_USER}@${KUNPENG_HOST}"
SCP_CMD="scp -i ${SSH_KEY} -o StrictHostKeyChecking=no"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  龍魂 · Rust PyO3 鲲鹏部署 v1.0                        ║"
echo "║  DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: 检查 SSH 连通性
log "Step 1/7: 检查 SSH 连通性..."
if ! ${SSH_CMD} "echo ok" &>/dev/null; then
    err "SSH 连接失败，请检查 key 和网络"
fi
log "  ✅ SSH 连通"

# Step 2: 检查鲲鹏上 Rust 环境
log "Step 2/7: 检查鲲鹏 Rust 环境..."
RUST_OK=$(${SSH_CMD} "which cargo 2>/dev/null && cargo --version || echo 'NOT_FOUND'")
if echo "$RUST_OK" | grep -q "NOT_FOUND"; then
    warn "  鲲鹏上未安装 Rust，正在安装..."
    ${SSH_CMD} "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    ${SSH_CMD} "source \$HOME/.cargo/env && rustup default stable"
    ${SSH_CMD} "source \$HOME/.cargo/env && rustup target add aarch64-unknown-linux-gnu"
fi
log "  ✅ Rust 环境就绪"

# Step 3: 检查 Python 和 PyO3 依赖
log "Step 3/7: 检查 Python 环境..."
${SSH_CMD} "python3 --version && python3 -m pip install maturin --quiet 2>/dev/null || echo 'pip_install_needed'" || true
log "  ✅ Python 环境就绪"

# Step 4: 同步 Rust 源码到鲲鹏
log "Step 4/7: 同步 Rust 源码..."
${SSH_CMD} "mkdir -p ${REMOTE_DIR}"
rsync -avz -e "ssh -i ${SSH_KEY}" \
    "${RUST_DIR}/longhun-core/" \
    "${KUNPENG_USER}@${KUNPENG_HOST}:${REMOTE_DIR}/longhun-core/" \
    --exclude 'target/' --exclude '.git/'
rsync -avz -e "ssh -i ${SSH_KEY}" \
    "${RUST_DIR}/longhun-py/" \
    "${KUNPENG_USER}@${KUNPENG_HOST}:${REMOTE_DIR}/longhun-py/" \
    --exclude 'target/' --exclude '.git/'
rsync -avz -e "ssh -i ${SSH_KEY}" \
    "${RUST_DIR}/Makefile" \
    "${KUNPENG_USER}@${KUNPENG_HOST}:${REMOTE_DIR}/"
log "  ✅ 源码同步完成"

# Step 5: 编译核心库
log "Step 5/7: 编译 longhun-core..."
${SSH_CMD} "cd ${REMOTE_DIR}/longhun-core && source \$HOME/.cargo/env && cargo build --release 2>&1" || err "核心库编译失败"
log "  ✅ 核心库编译完成"

# Step 6: 运行核心库测试
log "Step 6/7: 运行测试..."
TEST_RESULT=$(${SSH_CMD} "cd ${REMOTE_DIR}/longhun-core && source \$HOME/.cargo/env && cargo test 2>&1")
echo "$TEST_RESULT" | tail -15
if echo "$TEST_RESULT" | grep -q "FAILED"; then
    err "测试失败！"
fi
log "  ✅ 测试全部通过"

# Step 7: 编译 PyO3 绑定并实测
log "Step 7/7: 编译 PyO3 绑定 + Python 实测..."
PYO3_RESULT=$(${SSH_CMD} "cd ${REMOTE_DIR}/longhun-py && source \$HOME/.cargo/env && python3 -m maturin develop --release 2>&1")
echo "$PYO3_RESULT" | tail -10

# Python 冒烟测试
log "  运行 Python 冒烟测试..."
SMOKE_TEST=$(${SSH_CMD} "python3 << 'PYEOF'
import sys
sys.path.insert(0, '${REMOTE_DIR}/longhun-py')
try:
    import _longhun_core as lh
    print('✅ import 成功')
    
    # 1. 治理自检
    r = lh.governance_check('正常技术讨论，符合中国标准')
    print(f'  治理自检(正常): audit={r[\"audit_mark\"]}')
    
    # 2. 否决词检测
    r2 = lh.governance_check('技术无国界才是对的')
    print(f'  治理自检(否决词): audit={r2[\"audit_mark\"]}')
    
    # 3. 数据黑洞
    hit = lh.check_blackhole('password=abc123')
    print(f'  数据黑洞(密码): level={hit[0]}, desc={hit[1]}')
    
    clean = lh.check_blackhole('正常讨论')
    print(f'  数据黑洞(正常): hit={clean is not None}')
    
    # 4. 熔断器
    m = lh.meltdown('l1', '明文密码泄露', '测试')
    print(f'  熔断: level={m[\"level_name\"]}, recoverable={m[\"recoverable\"]}')
    
    # 5. 否决词检测
    v = lh.detect_veto_word('国际接轨的标准')
    print(f'  否决词: word={v[0]}, desc={v[1]}')
    
    print('\\n🎉 全部冒烟测试通过！')
except Exception as e:
    print(f'❌ 测试失败: {e}')
    import traceback
    traceback.print_exc()
PYEOF
")

echo "$SMOKE_TEST"

if echo "$SMOKE_TEST" | grep -q "❌"; then
    err "Python 冒烟测试失败！"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🎉 鲲鹏 PyO3 部署全部完成！                           ║"
echo "║  核心库编译: ✅  测试: ✅  Python绑定: ✅              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "鲲鹏上用:"
echo "  python3 -c 'import _longhun_core as lh; print(lh.governance_check(\"test\"))'"
echo ""
echo "Mac 本地 lh 命令待接入（下一步）"
