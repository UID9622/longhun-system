#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════
# 龍魂·审计即服务 · 鲲鹏部署脚本 v1.0
# DNA: #龍芯⚡️丙午·癸未·甲子·庚午·䷾既济-AUDIT-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════
set -euo pipefail

KUNPENG="root@119.13.90.27"
SSH="ssh -o StrictHostKeyChecking=no -i ~/.ssh/longhun_kunpeng_ed25519"
REMOTE_DIR="/root/longhun-system"

echo "🚀 龍魂·审计即服务 — 部署到鲲鹏"
echo ""

# ── 1. 同步新文件 ──
echo "📦 同步文件..."
rsync -avz -e "ssh -i ~/.ssh/longhun_kunpeng_ed25519" \
    bin/lh_api_guard.py \
    bin/lh_audit_as_a_service.py \
    bin/lh_audit_as_a_service_api.py \
    bin/lh_vendor_hunter.py \
    bin/lh_hunter_internal_audit.py \
    brand/ \
    portal/hunter/ \
    governance/audit/reports/ \
    $KUNPENG:$REMOTE_DIR/bin/ \
    $KUNPENG:$REMOTE_DIR/brand/ \
    $KUNPENG:$REMOTE_DIR/portal/hunter/ \
    $KUNPENG:$REMOTE_DIR/governance/audit/reports/

# ── 2. 安装 systemd ──
echo ""
echo "⚙️  安装 systemd service..."
$SSH $KUNPENG "cat > /tmp/longhun-audit.service" < deploy/longhun-audit.service
$SSH $KUNPENG "cp /tmp/longhun-audit.service /etc/systemd/system/ && systemctl daemon-reload"

# ── 3. 安装 nginx config ──
echo ""
echo "🔒 安装 nginx 配置..."
$SSH $KUNPENG "cat > /tmp/longhun-audit-nginx.conf" < deploy/nginx-audit.conf
$SSH $KUNPENG "cp /tmp/longhun-audit-nginx.conf /etc/nginx/sites-available/longhun-audit && \
    ln -sf /etc/nginx/sites-available/longhun-audit /etc/nginx/sites-enabled/longhun-audit && \
    nginx -t"

# ── 4. 重启服务 ──
echo ""
echo "🔄 启动服务..."
$SSH $KUNPENG "systemctl enable longhun-audit && systemctl restart longhun-audit && systemctl reload nginx"

# ── 5. 验证 ──
echo ""
echo "✅ 等待3秒后验证..."
sleep 3

# 本地服务
echo ""
echo "── 本地服务状态 ──"
$SSH $KUNPENG "systemctl is-active longhun-audit && systemctl status longhun-audit --no-pager | head -8"

# API 验证
echo ""
echo "── API 健康检查 ──"
$SSH $KUNPENG "curl -sk https://localhost/audit/health 2>/dev/null || echo 'nginx未就绪'"
$SSH $KUNPENG "curl -s http://127.0.0.1:8771/audit/health 2>/dev/null || echo 'direct未就绪'"

# nginx
echo ""
echo "── Nginx ──"
$SSH $KUNPENG "systemctl is-active nginx"

echo ""
echo "🏆 部署完成"
echo "   https://uid9622.cn/audit/health"
echo "   https://uid9622.cn/audit/leaderboard"
echo "   https://uid9622.cn/hunter"
echo ""
echo "DNA: #龍芯⚡️丙午·癸未·甲子·庚午·䷾既济-AUDIT-DEPLOY-v1.0"
