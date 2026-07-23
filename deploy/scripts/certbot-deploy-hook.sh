#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龙魂系统 · certbot deploy钩子 · nginx重载               ║
# ║  版本: v1.0                                                  ║
# ║  DNA: #龍芯⚡️丙午·乙未·丙申·亥时·☵坎-CERT-DEPLOY-HOOK-v1.0 ║
# ║  路径: /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh ║
# ║  触发: certbot每次成功续期后自动调用                          ║
# ╚═══════════════════════════════════════════════════════════════╝
#
# 部署到鲲鹏: scp 此文件到 /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh
# 权限: chmod 755

set -euo pipefail

LOG_FILE="/var/log/letsencrypt/deploy-hook.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# certbot通过环境变量传递续期证书信息
DOMAIN="${RENEWED_DOMAINS:-unknown}"
CERT_PATH="${RENEWED_LINEAGE:-/etc/letsencrypt/live/unknown}"

log() {
    echo "[${TIMESTAMP}] $1" | tee -a "${LOG_FILE}"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Deploy hook triggered for: ${DOMAIN}"
log "Certificate path: ${CERT_PATH}"

# ── 1. 复制证书到nginx信赖目录（可选，兼容不支持live路径的nginx版本）──
# nginx 1.24 直接读 live/ 路径没问题，这里保留备用逻辑
log "Checking certificate files..."
if [ -f "${CERT_PATH}/fullchain.pem" ] && [ -f "${CERT_PATH}/privkey.pem" ]; then
    log "✅ Certificate files present"
    # 检查证书有效期
    END_DATE=$(openssl x509 -enddate -noout -in "${CERT_PATH}/cert.pem" 2>/dev/null | cut -d= -f2 || echo "unknown")
    log "New cert valid until: ${END_DATE}"
else
    log "❌ Certificate files missing at ${CERT_PATH}"
    exit 1
fi

# ── 2. 测试nginx配置 ──
log "Testing nginx configuration..."
if nginx -t 2>&1 | tee -a "${LOG_FILE}"; then
    log "✅ nginx config test passed"
else
    log "❌ nginx config test FAILED — NOT reloading"
    exit 1
fi

# ── 3. 重载nginx ──
log "Reloading nginx..."
if systemctl reload nginx 2>&1 | tee -a "${LOG_FILE}"; then
    log "✅ nginx reloaded successfully"
else
    log "❌ nginx reload FAILED"
    exit 1
fi

# ── 4. 验证新证书已生效 ──
sleep 2
for domain in ${DOMAIN//,/ }; do
    REMOTE_CERT=$(echo | openssl s_client -connect "${domain}:443" -servername "${domain}" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2 || echo "verify_failed")
    log "Verified ${domain} serving until: ${REMOTE_CERT}"
done

# ── 5. 发送 Bark 通知 ──
if [ -f /opt/longhun-system/.env.kunpeng ]; then
    set -a
    source /opt/longhun-system/.env.kunpeng 2>/dev/null || true
    set +a
fi

BARK_KEY="${BARK_KEY:-}"
if [ -n "${BARK_KEY}" ] && [ "${BARK_KEY}" != "xxxxxxxxxxxxxxxx" ]; then
    BARK_TITLE="🔐 SSL证书已续期"
    BARK_BODY="域名: ${DOMAIN}\n路径: ${CERT_PATH}\n到期: ${END_DATE:-unknown}"
    curl -s -o /dev/null -X POST "https://api.day.app/${BARK_KEY}" \
        -d "title=${BARK_TITLE}" \
        -d "body=${BARK_BODY}" \
        -d "group=longhun-system" \
        -d "sound=bell" || true
    log "📲 Bark notification sent"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Deploy hook complete ✅"
echo ""
