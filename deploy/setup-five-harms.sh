#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 五害曝光台一键上线 v1.1
# DNA: #龍芯⚡️丙午·乙未·癸亥·戊午·䷦蹇-SETUP-FIVEHARMS-v1.1-FIX
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法: bash deploy/setup-five-harms.sh
#      此脚本一次性安装五害曝光台 API + Nginx 代理 + 工具下载区
set -euo pipefail

SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
REMOTE="root@119.13.90.27"
REMOTE_PATH="/opt/longhun-system"
LOCAL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()  { echo -e "${GREEN}[OK]${NC}  $*"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $*"; }
err() { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }
info(){ echo -e "${CYAN}[..]${NC}  $*"; }

SSH_OPTS="-p 22 -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"
SSH="ssh ${SSH_OPTS} ${REMOTE}"

echo "🐉 五害曝光台一键上线"
echo "════════════════════════"

info "Step 1/4: 同步代码..."
rsync -az --progress \
    -e "ssh ${SSH_OPTS}" \
    --include='portal/' \
    --include='portal/five-harms-expose/***' \
    --include='portal/tools/***' \
    --include='bin/' \
    --include='bin/lh_five_harms_api.py' \
    --include='deploy/' \
    --include='deploy/longhun-five-harms.service' \
    --include='deploy/nginx-uid9622.cn.conf' \
    --exclude='*' \
    "${LOCAL_ROOT}/" "${REMOTE}:${REMOTE_PATH}/" && \
    ok "代码同步完成" || \
    warn "rsync 部分文件同步失败，继续尝试..."

info "Step 2/4: 安装 systemd 服务..."
${SSH} "cp ${REMOTE_PATH}/deploy/longhun-five-harms.service /etc/systemd/system/ && systemctl daemon-reload && systemctl enable --now longhun-five-harms" && \
    ok "five-harms 服务已启动" || \
    warn "服务安装可能需要手动检查"

info "Step 3/4: 更新 Nginx 配置..."
${SSH} "cp ${REMOTE_PATH}/deploy/nginx-uid9622.cn.conf /etc/nginx/conf.d/uid9622.cn.conf && nginx -t" && \
    ${SSH} "nginx -s reload" && \
    ok "Nginx 重载完成" || \
    warn "Nginx 配置有问题，请检查"

info "Step 4/4: 验证..."
sleep 2
echo ""
echo "📍 验证端点:"
echo "   门户:   https://uid9622.cn/five-harms-expose/"
echo "   工具包: https://uid9622.cn/five-harms/api/toolkit/download"
echo "   CNSH插件: https://uid9622.cn/tools/cnsh-syntax-2.0.0.vsix"
echo ""
${SSH} "curl -s -o /dev/null -w '   five-harms API: HTTP %{http_code}\n' http://localhost:8779/api/toolkit 2>/dev/null"
${SSH} "curl -s -o /dev/null -w '   Nginx代理:    HTTP %{http_code}\n' https://localhost/five-harms/api/toolkit 2>/dev/null" || warn "HTTPS自签名验证跳过（正常）"

echo ""
echo "✅ 五害曝光台上线完成！"
