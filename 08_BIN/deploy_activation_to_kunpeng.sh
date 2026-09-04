#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# 龍魂 · 激活经济舱 + MFA 三件套 · 鲲鹏部署
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-DEPLOY-ACTIVATION-PROD-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 目标: 119.13.90.27 (华为云 / 鲲鹏节点)
# 功能: 部署激活经济 API、激活舱页面、MFA 脚本
# ============================================================

set -euo pipefail

DNA="#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-DEPLOY-ACTIVATION-PROD-v1.0"
SERVER="root@119.13.90.27"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
REMOTE_ROOT="/opt/longhun-activation"
NGINX_CONF="/etc/nginx/sites-enabled/00-default-ip.conf"
API_PORT=9656

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log(){ echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $1"; }
error(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

[ -f "$SSH_KEY" ] || error "SSH 密钥不存在: $SSH_KEY"
command -v rsync >/dev/null 2>&1 || error "本机需要安装 rsync"

log "开始部署激活经济舱 + MFA: $SERVER"

# ── 1. 同步代码到服务器 ────────────────────────────────────
log "同步项目文件到 ${REMOTE_ROOT} ..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new "$SERVER" "mkdir -p ${REMOTE_ROOT}"

rsync -avz --delete \
  -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new" \
  --include='/bin/' \
  --include='/bin/lh_payment_activate.py' \
  --include='/bin/lh_payment_activate.py.asc' \
  --include='/bin/lh_activation_api.py' \
  --include='/bin/lh_activation_api.py.asc' \
  --include='/bin/lh_mfa_activate.py' \
  --include='/bin/lh_mfa_activate.py.asc' \
  --include='/bin/lh_mfa_bind.py' \
  --include='/bin/lh_mfa_bind.py.asc' \
  --include='/bin/payment_providers/' \
  --include='/bin/payment_providers/***' \
  --include='/01_protocols/' \
  --include='/01_protocols/LH-ACTIVATION-ECONOMY-v1.0.md' \
  --include='/01_protocols/LH-ACTIVATION-ECONOMY-v1.0.md.asc' \
  --include='/01_protocols/LH-MFA-ACTIVATE-v2.0.md' \
  --include='/01_protocols/LH-MFA-ACTIVATE-v2.0.md.asc' \
  --include='/01_protocols/LH-ACTIVATION-PAYMENT-v1.0.md' \
  --include='/01_protocols/LH-ACTIVATION-PAYMENT-v1.0.md.asc' \
  --include='/portal/' \
  --include='/portal/activation-lab/' \
  --include='/portal/activation-lab/***' \
  --exclude='*' \
  "$(pwd)/" "${SERVER}:${REMOTE_ROOT}/"

# ── 2. 服务器端安装依赖并配置服务 ──────────────────────────
log "在服务器上安装依赖并配置服务..."
ssh -i "$SSH_KEY" "$SERVER" bash -s <<'REMOTE'
set -euo pipefail
REMOTE_ROOT="/opt/longhun-activation"
VENV="${REMOTE_ROOT}/venv"

if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --upgrade pip >/dev/null 2>&1
"$VENV/bin/pip" install -q flask qrcode Pillow wechatpayv3 python-alipay-sdk pyyaml

mkdir -p /var/log/longhun/activation
mkdir -p /etc/longhun/activation
mkdir -p ${REMOTE_ROOT}/config
mkdir -p ${REMOTE_ROOT}/certs
chmod 700 ${REMOTE_ROOT}/certs

cat > /etc/systemd/system/longhun-activation.service <<'SVC'
[Unit]
Description=龍魂激活经济舱 API v1.0
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/longhun-activation
ExecStart=/opt/longhun-activation/venv/bin/python3 bin/lh_activation_api.py --host 127.0.0.1 --port 9656
Restart=always
RestartSec=5
Environment=PATH=/opt/longhun-activation/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONUNBUFFERED=1
StandardOutput=append:/var/log/longhun/activation/app.log
StandardError=append:/var/log/longhun/activation/app.log

[Install]
WantedBy=multi-user.target
SVC

cat > /etc/logrotate.d/longhun-activation <<'LR'
/var/log/longhun/activation/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
    sharedscripts
    postrotate
        systemctl reload longhun-activation 2>/dev/null || true
    endscript
}
LR

cat > /etc/longhun/activation/health_check.sh <<'CHK'
#!/bin/bash
LOG=/var/log/longhun/activation/health.log
TS=$(date '+%Y-%m-%d %H:%M:%S')
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:9656/health || echo "000")
if [ "$code" != "200" ]; then
    echo "[$TS] ALERT: activation health=$code, restarting..." >> "$LOG"
    systemctl restart longhun-activation
else
    echo "[$TS] OK: activation health=$code" >> "$LOG"
fi
CHK
chmod +x /etc/longhun/activation/health_check.sh

echo '*/2 * * * * root /etc/longhun/activation/health_check.sh' > /etc/cron.d/longhun-activation
chmod 644 /etc/cron.d/longhun-activation

systemctl daemon-reload
systemctl enable longhun-activation
systemctl restart longhun-activation

sleep 2
REMOTE

# ── 3. 同步 Web 静态页面到门户目录 ─────────────────────────
log "同步激活舱页面..."
ssh -i "$SSH_KEY" "$SERVER" "mkdir -p /opt/longhun/portal/activation-lab"
rsync -avz --delete \
  -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new" \
  "$(pwd)/portal/activation-lab/" "${SERVER}:/opt/longhun/portal/activation-lab/"

# ── 4. 配置 nginx ──────────────────────────────────────────
log "配置 nginx 反向代理..."
ssh -i "$SSH_KEY" "$SERVER" python3 - <<'PY'
path = "/etc/nginx/sites-enabled/00-default-ip.conf"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "longhun-activation" in content:
    print("nginx 激活舱路由已存在，跳过")
    exit(0)

snippet = '''
    # 🎫 龍魂激活经济舱
    location /activation-lab/ {
        alias /opt/longhun/portal/activation-lab/;
        index index.html;
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-cache" always;
    }

    location /api/activation/ {
        rewrite ^/api/activation/(.*) /$1 break;
        proxy_pass http://127.0.0.1:9656;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
        proxy_buffering off;
    }

'''
idx = content.find('    # 🧭 龍魂路径规划推演舱')
if idx == -1:
    idx = content.find('    # ── 龍魂路径规划引擎 API ──')
if idx == -1:
    idx = content.find('    location /pathfinder-lab/ {')
if idx == -1:
    idx = content.find('    location /api/ {')
if idx == -1:
    print("找不到插入位置")
    exit(1)
content = content[:idx] + snippet + content[idx:]
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("nginx 配置已更新")
PY

ssh -i "$SSH_KEY" "$SERVER" "nginx -t && systemctl reload nginx"

# ── 5. 健康检查 ────────────────────────────────────────────
log "执行公网健康检查..."
sleep 2
for url in \
  "http://119.13.90.27/activation-lab/" \
  "http://119.13.90.27/api/activation/health"; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" || true)
    if [ "$code" = "200" ]; then
        log "  ✅ ${url} -> ${code}"
    else
        warn "  🟡 ${url} -> ${code:-失败}"
    fi
done

log "部署完成！"
echo ""
echo "🎫 激活经济舱: http://119.13.90.27/activation-lab/"
echo "🎫 激活 API:   http://119.13.90.27/api/activation/"
echo ""
echo "后续管理："
echo "  systemctl status longhun-activation"
echo "  journalctl -u longhun-activation -f"
echo "  tail -f /var/log/longhun/activation/health.log"
