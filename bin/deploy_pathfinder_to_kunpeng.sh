#!/usr/bin/env bash
# ============================================================
# 龍魂 · 路径规划引擎 · 生产级鲲鹏部署
# DNA: #龍芯⚡️丙午·癸未·丁未·离为火-DEPLOY-PATHFINDER-PROD-v4.1.5
# 目标: 119.13.90.27 (华为云 / 鲲鹏节点)
# 功能: 部署路径规划 REST API，含 systemd + logrotate + 监控 + 灰度
# ============================================================

set -euo pipefail

DNA="#龍芯⚡️丙午·癸未·丁未·离为火-DEPLOY-PATHFINDER-PROD-v4.1.5"
SERVER="root@119.13.90.27"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
REMOTE_ROOT="/opt/longhun-pathfinder"
NGINX_CONF="/etc/nginx/sites-enabled/00-default-ip.conf"
API_PORT=9650

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log(){ echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $1"; }
error(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

[ -f "$SSH_KEY" ] || error "SSH 密钥不存在: $SSH_KEY"
command -v rsync >/dev/null 2>&1 || error "本机需要安装 rsync"

log "开始部署路径规划引擎: $SERVER"

# ── 1. 同步代码到服务器（严格白名单） ──────────────────────
log "同步项目文件到 ${REMOTE_ROOT} ..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new "$SERVER" "mkdir -p ${REMOTE_ROOT}"

rsync -avz --delete \
  -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new" \
  --include='/engines/' \
  --include='/engines/***' \
  --include='/bin/' \
  --include='/bin/lh_pathfinder_api.py' \
  --include='/bin/lh_pathfinder_deploy_monitor.sh' \
  --include='/requirements.txt' \
  --include='/portal/' \
  --include='/portal/pathfinder-lab/' \
  --include='/portal/pathfinder-lab/***' \
  --include='/portal/nginx/' \
  --include='/portal/nginx/00-default-ip-video-studio.conf' \
  --exclude='*' \
  "$(pwd)/" "${SERVER}:${REMOTE_ROOT}/"

# ── 2. 服务器端安装依赖、配置、启动服务 ────────────────────
log "在服务器上安装依赖并配置服务..."
ssh -i "$SSH_KEY" "$SERVER" bash -s <<'REMOTE'
set -euo pipefail
REMOTE_ROOT="/opt/longhun-pathfinder"
VENV="${REMOTE_ROOT}/venv"

# 创建虚拟环境并安装依赖
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --upgrade pip >/dev/null 2>&1
"$VENV/bin/pip" install -q flask

# 创建日志目录
mkdir -p /var/log/longhun/pathfinder
mkdir -p /etc/longhun/pathfinder

# ── systemd 服务（生产级：自动重启、日志、环境变量）
cat > /etc/systemd/system/longhun-pathfinder.service <<'SVC'
[Unit]
Description=龍魂路径规划引擎 API v4.1.5
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/longhun-pathfinder
ExecStart=/opt/longhun-pathfinder/venv/bin/python3 bin/lh_pathfinder_api.py --host 127.0.0.1 --port 9650
Restart=always
RestartSec=5
Environment=PATH=/opt/longhun-pathfinder/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONUNBUFFERED=1
StandardOutput=append:/var/log/longhun/pathfinder/app.log
StandardError=append:/var/log/longhun/pathfinder/app.log

[Install]
WantedBy=multi-user.target
SVC

# ── 灰度实例（端口 9651，用于无缝升级）
cat > /etc/systemd/system/longhun-pathfinder-canary.service <<'SVC'
[Unit]
Description=龍魂路径规划引擎 API · 灰度实例
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/longhun-pathfinder
ExecStart=/opt/longhun-pathfinder/venv/bin/python3 bin/lh_pathfinder_api.py --host 127.0.0.1 --port 9651
Restart=always
RestartSec=5
Environment=PATH=/opt/longhun-pathfinder/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONUNBUFFERED=1
StandardOutput=append:/var/log/longhun/pathfinder/app-canary.log
StandardError=append:/var/log/longhun/pathfinder/app-canary.log
SVC

# ── logrotate 日志轮转
cat > /etc/logrotate.d/longhun-pathfinder <<'LR'
/var/log/longhun/pathfinder/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
    sharedscripts
    postrotate
        systemctl reload longhun-pathfinder longhun-pathfinder-canary 2>/dev/null || true
    endscript
}
LR

# ── 健康监控脚本
cat > /etc/longhun/pathfinder/health_check.sh <<'CHK'
#!/bin/bash
# 龍魂路径规划引擎 · 健康监控
LOG=/var/log/longhun/pathfinder/health.log
TS=$(date '+%Y-%m-%d %H:%M:%S')
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:9650/health || echo "000")
if [ "$code" != "200" ]; then
    echo "[$TS] ALERT: pathfinder health=$code, restarting..." >> "$LOG"
    systemctl restart longhun-pathfinder
else
    echo "[$TS] OK: pathfinder health=$code" >> "$LOG"
fi
CHK
chmod +x /etc/longhun/pathfinder/health_check.sh

# ── 定时监控（每2分钟）
echo '*/2 * * * * root /etc/longhun/pathfinder/health_check.sh' > /etc/cron.d/longhun-pathfinder
chmod 644 /etc/cron.d/longhun-pathfinder

systemctl daemon-reload
systemctl enable longhun-pathfinder longhun-pathfinder-canary
systemctl restart longhun-pathfinder longhun-pathfinder-canary

sleep 2
REMOTE

# ── 3. 同步 Web 静态页面到门户目录 ─────────────────────────
log "同步路径规划推演舱页面..."
ssh -i "$SSH_KEY" "$SERVER" "mkdir -p /opt/longhun/portal/pathfinder-lab"
rsync -avz --delete \
  -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new" \
  "$(pwd)/portal/pathfinder-lab/" "${SERVER}:/opt/longhun/portal/pathfinder-lab/"

# ── 3. 配置 nginx ──────────────────────────────────────────
log "配置 nginx 反向代理..."
ssh -i "$SSH_KEY" "$SERVER" python3 - <<'PY'
import os
path = "/etc/nginx/sites-enabled/00-default-ip.conf"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "longhun-pathfinder" in content:
    print("nginx 路径规划路由已存在，跳过")
    exit(0)

snippet = '''
    # 🧭 龍魂路径规划推演舱
    location /pathfinder-lab/ {
        alias /opt/longhun/portal/pathfinder-lab/;
        index index.html;
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-cache" always;
    }

    # ── 龍魂路径规划引擎 API ──
    location /api/pathfinder/ {
        rewrite ^/api/pathfinder/(.*) /$1 break;
        proxy_pass http://127.0.0.1:9650;
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

    location /pathfinder/ {
        proxy_pass http://127.0.0.1:9650/;
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

    location /pathfinder-canary/ {
        proxy_pass http://127.0.0.1:9651/;
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
idx = content.find('    # 🐉 统一后端 API')
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

# ── 4. 健康检查 ────────────────────────────────────────────
log "执行公网健康检查..."
sleep 2
for url in \
  "http://119.13.90.27/pathfinder-lab/" \
  "http://119.13.90.27/api/pathfinder/health" \
  "http://119.13.90.27/pathfinder/health" \
  "http://119.13.90.27/pathfinder-canary/health"; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" || true)
    if [ "$code" = "200" ]; then
        log "  ✅ ${url} -> ${code}"
    else
        warn "  🟡 ${url} -> ${code:-失败}"
    fi
done

log "部署完成！"
echo ""
echo "🧭 路径规划推演舱: http://119.13.90.27/pathfinder-lab/"
echo "🧭 路径规划 API:   http://119.13.90.27/api/pathfinder/"
echo "🧭 灰度实例:      http://119.13.90.27/pathfinder-canary/"
echo ""
echo "后续管理："
echo "  systemctl status longhun-pathfinder"
echo "  journalctl -u longhun-pathfinder -f"
echo "  tail -f /var/log/longhun/pathfinder/health.log"
