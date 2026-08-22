#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·踪迹复原引擎 — 鲲鹏部署脚本 v1.0
# DNA: #龍芯⚡️丙午·乙未·壬寅·巳时·䷀乾-TRACE-DEPLOY-V1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用法: bash deploy/scripts/trace_reconstructor_deploy.sh
set -euo pipefail

KUNPENG_HOST="119.13.90.27"
KUNPENG_USER="root"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
SSH="ssh -i $SSH_KEY $KUNPENG_USER@$KUNPENG_HOST"
SCP="scp -i $SSH_KEY"
SERVICE_NAME="longhun-trace-reconstructor"
SERVICE_PORT=8774
REMOTE_DIR="/opt/longhun"
LOCAL_BIN="bin/lh_trace_reconstructor_api.py"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "${YELLOW}🚀 龍魂·踪迹复原引擎 — 鲲鹏部署${NC}"
echo ""

# 1. 检查连接
echo -e "${BLUE}[1/6] 检查鲲鹏连接...${NC}"
if $SSH "echo ok" 2>/dev/null | grep -q ok; then
    echo -e "  ${GREEN}✅ 鲲鹏可达${NC}"
else
    echo -e "  ❌ 鲲鹏不可达"
    exit 1
fi

# 2. 上传代码
echo -e "${BLUE}[2/6] 上传复原引擎...${NC}"
$SSH "mkdir -p $REMOTE_DIR/bin $REMOTE_DIR/data/traces"
$SCP "$LOCAL_BIN" "${KUNPENG_USER}@${KUNPENG_HOST}:${REMOTE_DIR}/bin/"
$SSH "chmod +x $REMOTE_DIR/bin/lh_trace_reconstructor_api.py"
echo -e "  ${GREEN}✅ 代码已上传${NC}"

# 3. 安装依赖
echo -e "${BLUE}[3/6] 安装Python依赖...${NC}"
$SSH "pip3 install fastapi uvicorn pydantic 2>&1 | tail -3"
echo -e "  ${GREEN}✅ 依赖安装完成${NC}"

# 4. 创建 systemd 服务
echo -e "${BLUE}[4/6] 创建 systemd 服务...${NC}"
$SSH "cat > /etc/systemd/system/${SERVICE_NAME}.service" << SERVICEEOF
[Unit]
Description=龍魂·踪迹复原引擎
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${REMOTE_DIR}
ExecStart=/usr/bin/python3 ${REMOTE_DIR}/bin/lh_trace_reconstructor_api.py
Restart=always
RestartSec=10
StandardOutput=append:${REMOTE_DIR}/data/traces/reconstructor.log
StandardError=append:${REMOTE_DIR}/data/traces/reconstructor.err
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICEEOF

$SSH "systemctl daemon-reload"
$SSH "systemctl enable $SERVICE_NAME"
echo -e "  ${GREEN}✅ systemd 服务已创建${NC}"

# 5. Nginx 反代配置
echo -e "${BLUE}[5/6] 配置 Nginx 反代...${NC}"
$SSH "cat > /etc/nginx/conf.d/longhun-trace.conf" << NGINXEOF
# 龍魂·踪迹复原引擎 — Nginx 反代
# 路径: /api/trace-reconstruct → :8774
location /api/trace-reconstruct/ {
    proxy_pass http://127.0.0.1:8774/;
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_read_timeout 30s;
    proxy_connect_timeout 10s;
    
    # 只允许 POST /v1/reconstruct
    limit_except POST {
        deny all;
    }
}
NGINXEOF

$SSH "nginx -t && systemctl reload nginx" 2>&1
echo -e "  ${GREEN}✅ Nginx 配置完成${NC}"

# 6. 启动服务
echo -e "${BLUE}[6/6] 启动服务...${NC}"
$SSH "systemctl restart $SERVICE_NAME"
sleep 3

# 健康检查
if $SSH "curl -sf http://127.0.0.1:${SERVICE_PORT}/health" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 复原引擎启动成功${NC}"
else
    echo -e "  ❌ 复原引擎启动失败，检查日志"
    $SSH "journalctl -u $SERVICE_NAME --no-pager -n 20"
    exit 1
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "  本地访问:  http://127.0.0.1:8774/health"
echo "  公网访问:  https://uid9622.cn/api/trace-reconstruct/health"
echo "  API文档:   https://uid9622.cn/api/trace-reconstruct/docs"
echo ""
echo "  管理命令:"
echo "    systemctl status $SERVICE_NAME"
echo "    systemctl restart $SERVICE_NAME"
echo "    journalctl -u $SERVICE_NAME -f"
