#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# 龍魂 · 支付宝沙箱环境一键配置脚本
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-SETUP-ALIPAY-SANDBOX-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 功能: 上传密钥、配置沙箱凭证、重启服务
# ============================================================

set -euo pipefail

SERVER="root@119.13.90.27"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
REMOTE_ROOT="/opt/longhun-activation"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log(){ echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $1"; }
error(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

[ -f "$SSH_KEY" ] || error "SSH 密钥不存在: $SSH_KEY"

# 读取用户输入
read -p "请输入支付宝沙箱 AppID: " APP_ID
[ -z "$APP_ID" ] && error "AppID 不能为空"

read -p "请输入支付宝沙箱公钥（从开放平台复制，含 BEGIN/END 那一整段，粘贴后按 Ctrl+D 结束）: " -d '' ALIPAY_PUB_KEY
[ -z "$ALIPAY_PUB_KEY" ] && error "支付宝公钥不能为空"

LOCAL_CERT_DIR="${HOME}/.longhun/certs"
mkdir -p "$LOCAL_CERT_DIR"

# 如果本地没有密钥，自动生成
if [ ! -f "$LOCAL_CERT_DIR/alipay_sandbox_app_private_key.pem" ]; then
    log "本地未找到沙箱私钥，自动生成 RSA2 密钥对..."
    openssl genrsa -out "$LOCAL_CERT_DIR/alipay_sandbox_app_private_key.pem" 2048 >/dev/null 2>&1
    openssl rsa -in "$LOCAL_CERT_DIR/alipay_sandbox_app_private_key.pem" -pubout -out "$LOCAL_CERT_DIR/alipay_sandbox_app_public_key.pem" >/dev/null 2>&1
    log "密钥对已生成: $LOCAL_CERT_DIR/alipay_sandbox_app_public_key.pem"
    log "请把这整段公钥上传到支付宝开放平台沙箱环境的「接口加签方式」中："
    cat "$LOCAL_CERT_DIR/alipay_sandbox_app_public_key.pem"
    echo ""
    warn "上传完成后，复制支付宝给你的公钥，重新运行本脚本填入。"
    exit 0
fi

# 生成服务器配置文件
TMP_CONFIG=$(mktemp)
cat > "$TMP_CONFIG" <<EOF
alipay:
  enabled: true
  sandbox: true
  app_id: "${APP_ID}"
  app_private_key_path: "${REMOTE_ROOT}/certs/alipay_sandbox_app_private_key.pem"
  alipay_public_key_path: "${REMOTE_ROOT}/certs/alipay_sandbox_alipay_public_key.pem"
  notify_url: "https://uid9622.cn/api/activation/payment/notify/alipay"
  return_url: "https://uid9622.cn/activation-lab/?paid=1"

wechat_pay:
  enabled: false
EOF

# 生成支付宝公钥文件
TMP_PUB=$(mktemp)
echo "$ALIPAY_PUB_KEY" > "$TMP_PUB"

log "上传证书与配置到服务器..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new "$SERVER" "mkdir -p ${REMOTE_ROOT}/certs && chmod 700 ${REMOTE_ROOT}/certs && mkdir -p ${REMOTE_ROOT}/config"

scp -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new \
  "$LOCAL_CERT_DIR/alipay_sandbox_app_private_key.pem" \
  "$TMP_PUB" \
  "${SERVER}:${REMOTE_ROOT}/certs/"

ssh -i "$SSH_KEY" "$SERVER" "mv ${REMOTE_ROOT}/certs/$(basename $TMP_PUB) ${REMOTE_ROOT}/certs/alipay_sandbox_alipay_public_key.pem && chmod 600 ${REMOTE_ROOT}/certs/*.pem"

scp -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new \
  "$TMP_CONFIG" \
  "${SERVER}:${REMOTE_ROOT}/config/payment_credentials.yaml"

log "重启激活服务..."
ssh -i "$SSH_KEY" "$SERVER" "systemctl restart longhun-activation && sleep 2 && systemctl is-active longhun-activation"

rm -f "$TMP_CONFIG" "$TMP_PUB"

log "✅ 支付宝沙箱配置完成！"
echo ""
echo "测试地址: http://119.13.90.27/activation-lab/"
echo "步骤: 生成订单 → 点击「支付宝」→ 用支付宝沙箱钱包 App 扫码支付 → 查询状态"
