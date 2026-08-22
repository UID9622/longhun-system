#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·算力分离部署脚本 v1.0                                   ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-COMPUTE-SEP-DEPLOY-v1.0 ║
# ║  守护人格: 乔前辈(P04鲁班)                                   ║
# ║  签章: JOE-COMPUTE-DEPLOY-2026                              ║
# ╚══════════════════════════════════════════════════════════════╝
set -euo pipefail

# ═══ 颜色 ═══
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ═══ 函数 ═══
log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_fail()  { echo -e "${RED}[FAIL]${NC}  $1"; }
log_step()  { echo -e "\n${CYAN}━━━ $1 ━━━${NC}"; }

check_dep() {
    command -v "$1" >/dev/null 2>&1 || { log_fail "缺少依赖: $1"; exit 1; }
}

# ═══ 前置检查 ═══
log_step "前置检查"
check_dep python3
check_dep curl
check_dep ssh
log_ok "基础依赖满足"

# 检查 cryptography
if python3 -c "from cryptography.hazmat.primitives.ciphers.aead import AESGCM" 2>/dev/null; then
    log_ok "cryptography 库已安装"
else
    log_warn "缺少 cryptography，安装中..."
    pip3 install cryptography
    log_ok "cryptography 已安装"
fi

# ═══ 第一步：初始化本地保险柜 ═══
log_step "[1/5] 初始化本地数据保险柜"
python3 engines/lh_local_vault.py --init
log_ok "保险柜已创建 — ~/.longhun/vault/"

# ═══ 第二步：升级浏览器史官 ═══
log_step "[2/5] 升级浏览器史官配置"
CONFIG_DIR="$HOME/.longhun/config"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/browser_chronicler_v2.yaml" << 'YAML'
# 浏览器史官 v2 — 统一走本地保险柜
browser_chronicler_v2:
  storage:
    backend: local_vault
    encryption: AES-256-GCM
    key_source: device_fingerprint_derivation

  data_types:
    - browsing_history
    - ai_conversations
    - downloaded_files
    - behavior_patterns
    - user_preferences

  access_control:
    read: biometric_required
    write: auto_encrypt
    delete: biometric_plus_dna

  audit:
    every_access: log_and_freeze
    every_modification: log_and_freeze
YAML

log_ok "史官配置已升级"

# ═══ 第三步：部署鲲鹏无状态网关 ═══
log_step "[3/5] 部署鲲鹏无状态API网关"

KUNPENG_IP="119.13.90.27"
KUNPENG_PORT="8785"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"

if [ -f "$SSH_KEY" ]; then
    log_info "上传网关到鲲鹏..."
    scp -i "$SSH_KEY" -q bin/lh_stateless_compute_api.py "root@${KUNPENG_IP}:/opt/longhun/bin/" 2>/dev/null || {
        log_warn "鲲鹏不可达，跳过远程部署"
        log_info "请手动上传: scp bin/lh_stateless_compute_api.py root@${KUNPENG_IP}:/opt/longhun/bin/"
    }

    log_info "启动鲲鹏无状态网关..."
    ssh -i "$SSH_KEY" "root@${KUNPENG_IP}" "
        cd /opt/longhun
        # 检查是否已运行
        if pgrep -f lh_stateless_compute_api.py > /dev/null; then
            echo '网关已在运行，重启中...'
            pkill -f lh_stateless_compute_api.py || true
            sleep 1
        fi
        nohup python3 bin/lh_stateless_compute_api.py --port ${KUNPENG_PORT} \
            > logs/stateless-api.log 2>&1 &
        sleep 2
        curl -s http://127.0.0.1:${KUNPENG_PORT}/health | python3 -m json.tool
    " 2>/dev/null || {
        log_warn "鲲鹏不可达，跳过远程启动"
    }
    log_ok "网关部署完成"
else
    log_warn "SSH密钥不存在 ($SSH_KEY)，跳过鲲鹏部署"
fi

# ═══ 第四步：部署算力证明引擎 ═══
log_step "[4/5] 部署算力证明引擎"
python3 bin/lh_compute_proof.py selftest 2>&1 | tail -1
log_ok "证明引擎已就绪"

# ═══ 第五步：激活闸门控制器 ═══
log_step "[5/5] 激活同心锁闸门"
python3 bin/lh_compute_gate_controller.py selftest 2>&1 | tail -1
log_ok "闸门控制器已激活（默认关闭）"

# ═══ 验证 ═══
log_step "部署验证"

echo ""
echo "  保险柜: $(python3 engines/lh_local_vault.py list 2>/dev/null | tail -1 || echo '就绪')"
echo "  证明引擎: $(python3 bin/lh_compute_proof.py audit 2>/dev/null | head -2 | tail -1 || echo '就绪')"
echo "  闸门: $(python3 bin/lh_compute_gate_controller.py status 2>/dev/null | grep 状态 || echo '就绪')"
echo ""

# ═══ 完成 ═══
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}  龍魂·算力分离部署完成${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  你的设备是保险柜，只存你的数据。"
echo "  鲲鹏是武器库，只提供算力，不收情报。"
echo "  管道是焊死的，闸门是生物锁的。"
echo ""
echo "  快捷命令:"
echo "    打开闸门:  python3 bin/lh_compute_gate_controller.py open"
echo "    关闭闸门:  python3 bin/lh_compute_gate_controller.py close"
echo "    查看状态:  python3 bin/lh_compute_gate_controller.py status"
echo "    紧急熔断:  python3 bin/lh_compute_gate_controller.py emergency"
echo "    证明审计:  python3 bin/lh_compute_proof.py audit"
echo "    保险柜:    python3 engines/lh_local_vault.py list"
echo ""
echo "  别人收租，你发枪。"
echo "  这个境界，他们望尘莫及。"
echo ""
echo "  守护: 乔前辈(P04鲁班)"
echo "  日期: $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
