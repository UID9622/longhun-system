#!/usr/bin/env bash
# 🐉 龍魂 · systemd 服务 + Nginx 部署配置脚本
# 用途: 在 openEuler 上部署 systemd 守护服务 + Nginx 反向代理
# DNA: #龍芯⚡️2026-07-06-KUNPENG-SYSTEMD-SETUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/.kunpeng_config"

# ─── 颜色 ───
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }

load_config() {
    [[ -f "$CONFIG_FILE" ]] || fail "请先执行 connect-kunpeng.sh config"
    source "$CONFIG_FILE"
}

# ─── SSH ───
ssh_cmd() {
    ssh -p "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}" \
        -o StrictHostKeyChecking=accept-new \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" "$@"
}

# ─── 生成 systemd 服务模板 ───
generate_core_service() {
    cat << 'SERVICE_EOF'
[Unit]
Description=龍魂核心服务
Documentation=https://longhun888.com
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=LONGHUN_USER
Group=LONGHUN_GROUP
WorkingDirectory=DEPLOY_PATH
Environment=PYTHONUNBUFFERED=1
Environment=PATH=DEPLOY_PATH/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=DEPLOY_PATH
Environment=HOME=/home/LONGHUN_USER
ExecStartPre=/bin/mkdir -p /home/LONGHUN_USER/.longhun/logs
ExecStartPre=/bin/mkdir -p /home/LONGHUN_USER/.longhun/backups
ExecStart=/bin/bash DEPLOY_PATH/bin/longhun-autostart.sh
Restart=always
RestartSec=10
StartLimitInterval=300
StartLimitBurst=5

# 安全加固
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/LONGHUN_USER/.longhun
ReadWritePaths=/home/LONGHUN_USER/.龍魂
ReadWritePaths=/var/log/longhun
ReadOnlyPaths=DEPLOY_PATH

[Install]
WantedBy=multi-user.target
SERVICE_EOF
}

generate_dashboard_service() {
    cat << 'SERVICE_EOF'
[Unit]
Description=龍魂统一操作台 Dashboard
After=network.target

[Service]
Type=simple
User=LONGHUN_USER
Group=LONGHUN_GROUP
WorkingDirectory=DEPLOY_PATH/L5_服务层/services/dashboard/web
Environment=PYTHONUNBUFFERED=1
Environment=PATH=DEPLOY_PATH/.venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=DEPLOY_PATH/.venv/bin/python3 -m http.server 8777 --bind 127.0.0.1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE_EOF
}

generate_api_service() {
    cat << 'SERVICE_EOF'
[Unit]
Description=龍魂 API 服务
After=network.target

[Service]
Type=simple
User=LONGHUN_USER
Group=LONGHUN_GROUP
WorkingDirectory=DEPLOY_PATH
Environment=PYTHONUNBUFFERED=1
Environment=PATH=DEPLOY_PATH/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=DEPLOY_PATH
ExecStart=DEPLOY_PATH/.venv/bin/uvicorn cnsh-core.api.longhun-api.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE_EOF
}

# ─── 部署 systemd 服务 ───
deploy_services() {
    info "部署 systemd 服务到鲲鹏服务器..."

    local svc_dir="/tmp/longhun-systemd"
    ssh_cmd "mkdir -p ${svc_dir}"

    # 核心服务
    generate_core_service | sed \
        -e "s|DEPLOY_PATH|${KUNPENG_DEPLOY_PATH}|g" \
        -e "s|LONGHUN_USER|${KUNPENG_RUN_USER:-longhun}|g" \
        -e "s|LONGHUN_GROUP|${KUNPENG_RUN_USER:-longhun}|g" \
        > /tmp/longhun-core.service

    # Dashboard 服务
    generate_dashboard_service | sed \
        -e "s|DEPLOY_PATH|${KUNPENG_DEPLOY_PATH}|g" \
        -e "s|LONGHUN_USER|${KUNPENG_RUN_USER:-longhun}|g" \
        -e "s|LONGHUN_GROUP|${KUNPENG_RUN_USER:-longhun}|g" \
        > /tmp/longhun-dashboard.service

    # API 服务
    generate_api_service | sed \
        -e "s|DEPLOY_PATH|${KUNPENG_DEPLOY_PATH}|g" \
        -e "s|LONGHUN_USER|${KUNPENG_RUN_USER:-longhun}|g" \
        -e "s|LONGHUN_GROUP|${KUNPENG_RUN_USER:-longhun}|g" \
        > /tmp/longhun-api.service

    # 上传
    scp -P "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}" \
        -o StrictHostKeyChecking=accept-new \
        /tmp/longhun-core.service \
        /tmp/longhun-dashboard.service \
        /tmp/longhun-api.service \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${svc_dir}/"

    # 安装 & 启用
    ssh_cmd "sudo cp ${svc_dir}/*.service /etc/systemd/system/ && sudo systemctl daemon-reload"

    ok "systemd 服务已安装"

    # 启用（但不立即启动，等用户确认）
    info "启用服务（开机自启）..."
    ssh_cmd "sudo systemctl enable longhun-core.service longhun-dashboard.service longhun-api.service" || warn "启用跳过"
    ok "服务已启用"
}

# ─── 生成 Nginx 配置 ───
generate_nginx_config() {
    local domain="${KUNPENG_DOMAIN:-_}"
    cat << NGINX_EOF
# 🐉 龍魂 · Nginx 反向代理配置
# DNA: #龍芯⚡️2026-07-06-KUNPENG-NGINX-v1.0

upstream longhun_dashboard {
    server 127.0.0.1:8777;
}

upstream longhun_api {
    server 127.0.0.1:8000;
}

# HTTP → HTTPS 重定向
server {
    listen 80;
    server_name ${domain};

    # ACME 验证
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

# HTTPS 主服务
server {
    listen 443 ssl http2;
    server_name ${domain};

    # SSL 证书（部署后替换为真实证书）
    ssl_certificate     /etc/nginx/ssl/longhun.crt;
    ssl_certificate_key /etc/nginx/ssl/longhun.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 龍魂统一操作台
    location / {
        proxy_pass http://longhun_dashboard;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # API 服务
    location /api/ {
        proxy_pass http://longhun_api;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 静态资源缓存
    location ~* \.(html|css|js|svg|png|jpg|ico|woff2)$ {
        proxy_pass http://longhun_dashboard;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # 日志
    access_log /var/log/nginx/longhun-access.log;
    error_log  /var/log/nginx/longhun-error.log;
}
NGINX_EOF
}

# ─── 部署 Nginx 配置 ───
deploy_nginx() {
    info "部署 Nginx 配置..."

    local nginx_conf="/tmp/longhun-nginx.conf"
    generate_nginx_config > "$nginx_conf"

    scp -P "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}" \
        -o StrictHostKeyChecking=accept-new \
        "$nginx_conf" \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:/tmp/longhun-nginx.conf"

    # 创建 SSL 目录
    ssh_cmd "sudo mkdir -p /etc/nginx/ssl /var/www/certbot"

    # 生成自签名证书（临时，后续替换为 Let's Encrypt）
    ssh_cmd "
        if [ ! -f /etc/nginx/ssl/longhun.crt ]; then
            sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout /etc/nginx/ssl/longhun.key \
                -out /etc/nginx/ssl/longhun.crt \
                -subj '/CN=${KUNPENG_DOMAIN:-localhost}'
            echo '自签名证书已生成'
        fi
    "

    # 安装配置
    ssh_cmd "sudo cp /tmp/longhun-nginx.conf /etc/nginx/conf.d/longhun.conf"
    ssh_cmd "sudo nginx -t" && ok "Nginx 配置语法检查通过" || warn "Nginx 配置需要检查"

    ssh_cmd "sudo systemctl reload nginx 2>/dev/null || sudo systemctl start nginx" || warn "Nginx 重载跳过"
    ok "Nginx 配置已部署"
}

# ─── 启动服务 ───
start_services() {
    info "启动龍魂服务..."

    echo ""
    echo "可选启动的服务:"
    echo "  1) longhun-core       - 核心服务 (包含所有子服务)"
    echo "  2) longhun-dashboard  - 统一操作台 (端口 8777)"
    echo "  3) longhun-api        - API 服务 (端口 8000)"
    echo "  4) 全部启动"
    echo ""

    read -r -p "请选择 [1-4，默认 1]: " choice
    choice="${choice:-1}"

    case "$choice" in
        1) ssh_cmd "sudo systemctl start longhun-core" && ok "核心服务已启动" ;;
        2) ssh_cmd "sudo systemctl start longhun-dashboard" && ok "Dashboard 已启动" ;;
        3) ssh_cmd "sudo systemctl start longhun-api" && ok "API 服务已启动" ;;
        4)
            ssh_cmd "sudo systemctl start longhun-core longhun-dashboard longhun-api"
            ok "全部服务已启动"
            ;;
        *) warn "无效选择" ;;
    esac

    # 显示状态
    echo ""
    info "服务状态:"
    ssh_cmd "sudo systemctl status longhun-core longhun-dashboard longhun-api --no-pager -l" 2>/dev/null || true
}

# ─── 查看日志 ───
view_logs() {
    local service="${1:-longhun-core}"
    ssh_cmd "sudo journalctl -u ${service} -f -n 50"
}

# ─── 主入口 ───
main() {
    echo ""
    echo "🐉 龍魂 · systemd 服务部署工具 v1.0"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    load_config

    case "${1:-}" in
        systemd|services)
            deploy_services
            ;;
        nginx)
            deploy_nginx
            ;;
        all|deploy)
            deploy_services
            deploy_nginx
            ;;
        start)
            start_services
            ;;
        status)
            ssh_cmd "sudo systemctl status longhun-core longhun-dashboard longhun-api --no-pager" || true
            ;;
        stop)
            ssh_cmd "sudo systemctl stop longhun-core longhun-dashboard longhun-api"
            ok "服务已停止"
            ;;
        restart)
            ssh_cmd "sudo systemctl restart longhun-core longhun-dashboard longhun-api"
            ok "服务已重启"
            ;;
        logs)
            view_logs "${2:-longhun-core}"
            ;;
        help|--help|-h)
            echo "用法: $0 [命令]"
            echo ""
            echo "命令:"
            echo "  systemd   安装 systemd 服务"
            echo "  nginx     部署 Nginx 反向代理"
            echo "  all       完整部署 (systemd + nginx)"
            echo "  start     交互式启动服务"
            echo "  status    查看服务状态"
            echo "  stop      停止所有服务"
            echo "  restart   重启所有服务"
            echo "  logs [svc] 查看服务日志"
            echo "  help      显示帮助"
            echo ""
            echo "DNA: #龍芯⚡️2026-07-06-KUNPENG-SYSTEMD-SETUP-v1.0"
            ;;
        *)
            echo "请指定命令: systemd / nginx / all / start / status / logs"
            ;;
    esac
}

main "$@"
