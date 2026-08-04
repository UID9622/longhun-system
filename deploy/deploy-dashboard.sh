#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · Dashboard 一键部署到鲲鹏
# DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-DASHBOARD-DEPLOY-v1.0
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVER="root@119.13.90.27"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
REMOTE_DIR="/opt/longhun-system"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
err()  { log "${RED}🔴${NC} $*"; }

log "🐉 龍魂 Dashboard 部署到鲲鹏"

# 1. 同步文件
ok "1/5 同步文件..."
ssh -i "$SSH_KEY" -o ConnectTimeout=10 "$SERVER" "mkdir -p ${REMOTE_DIR}/{bin,portal/dashboard,deploy/systemd,data}"

# 同步 Dashboard 页面
scp -i "$SSH_KEY" -o ConnectTimeout=10 \
  "${LONGHUN_ROOT}/portal/dashboard/index.html" \
  "${SERVER}:${REMOTE_DIR}/portal/dashboard/"

# 同步 Dashboard 服务端
scp -i "$SSH_KEY" -o ConnectTimeout=10 \
  "${LONGHUN_ROOT}/bin/lh_dashboard_server.py" \
  "${SERVER}:${REMOTE_DIR}/bin/"

# 同步激活API (如果存在)
if [ -f "${LONGHUN_ROOT}/bin/lh_activation_api.py" ]; then
  scp -i "$SSH_KEY" -o ConnectTimeout=10 \
    "${LONGHUN_ROOT}/bin/lh_activation_api.py" \
    "${SERVER}:${REMOTE_DIR}/bin/"
fi

# 同步证书
if [ -f "${HOME}/.longhun/certs/alipay_sandbox_app_private_key.pem" ]; then
  ssh -i "$SSH_KEY" "$SERVER" "mkdir -p /opt/longhun-activation/certs"
  scp -i "$SSH_KEY" -o ConnectTimeout=10 \
    "${HOME}/.longhun/certs/alipay_sandbox_app_private_key.pem" \
    "${SERVER}:/opt/longhun-activation/certs/"
fi

# 2. 安装 systemd 服务
ok "2/5 安装 systemd 服务..."
scp -i "$SSH_KEY" -o ConnectTimeout=10 \
  "${LONGHUN_ROOT}/deploy/systemd/longhun-dashboard.service" \
  "${LONGHUN_ROOT}/deploy/systemd/longhun-activation-api.service" \
  "${SERVER}:/etc/systemd/system/"

ssh -i "$SSH_KEY" "$SERVER" "systemctl daemon-reload"

# 3. 启动服务
ok "3/5 启动 Dashboard 服务..."
ssh -i "$SSH_KEY" "$SERVER" "systemctl enable longhun-dashboard && systemctl restart longhun-dashboard"

ok "4/5 启动激活API服务..."
ssh -i "$SSH_KEY" "$SERVER" "systemctl enable longhun-activation-api && systemctl restart longhun-activation-api"

# 4. 重载 Nginx
ok "5/5 重载 Nginx..."
ssh -i "$SSH_KEY" "$SERVER" "nginx -t && nginx -s reload"

# 5. 验证
sleep 2
ok "验证中..."
HTTP_CODE=$(ssh -i "$SSH_KEY" "$SERVER" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9627/")
DASHBOARD_ACTIVE=$(ssh -i "$SSH_KEY" "$SERVER" "systemctl is-active longhun-dashboard")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  部署结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Dashboard (9627):  HTTP ${HTTP_CODE} · systemd: ${DASHBOARD_ACTIVE}"
echo "  官网:              https://uid9622.cn/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "部署完成！"
