#!/bin/bash
# ============================================================================
# deploy-frps.sh — 公网VPS一键部署 frps 服务端
# DNA: #龍芯⚡️丙午·辛未·FRPS-DEPLOY-v1.0
#
# 用法:
#   chmod +x deploy-frps.sh && sudo bash deploy-frps.sh
#
# 部署内容:
#   - frps 二进制 (v0.58.1)
#   - 龍魂主题配置 (含Web面板)
#   - systemd 自启服务
#   - 防火墙规则
# ============================================================================

set -e

FRP_VERSION="${FRP_VERSION:-0.58.1}"
FRP_DIR="${FRP_DIR:-/opt/frp}"
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "YOUR_SERVER_IP")

# 彩色输出
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo ""
echo -e "${BOLD}🐉 龍魂系统 · frps 服务端部署${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── 收集配置 ───
read -p "frp Token [LONGHUN2026_UID9622_KUNPENG]: " FRP_TOKEN
FRP_TOKEN=${FRP_TOKEN:-LONGHUN2026_UID9622_KUNPENG}

read -p "Web面板密码 [UID9622_ADMIN]: " WEB_PASSWORD
WEB_PASSWORD=${WEB_PASSWORD:-UID9622_ADMIN}

read -p "面板端口 [7500]: " WEB_PORT
WEB_PORT=${WEB_PORT:-7500}

echo ""
echo -e "公网IP: ${GREEN}${PUBLIC_IP}${NC}"
echo -e "Token:  ${YELLOW}***${FRP_TOKEN: -4}${NC}"
echo -e "面板:   ${CYAN}http://${PUBLIC_IP}:${WEB_PORT}${NC}"
echo ""

read -p "确认部署? [Y/n]: " CONFIRM
CONFIRM=${CONFIRM:-Y}
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# ─── 1. 安装依赖 ───
echo -e "\n${CYAN}[1/6] 安装依赖...${NC}"
mkdir -p "$FRP_DIR"
cd /tmp

if ! command -v wget &>/dev/null; then
    apt-get update -qq && apt-get install -y -qq wget curl
fi

# ─── 2. 下载 frps ───
echo -e "${CYAN}[2/6] 下载 frps v${FRP_VERSION}...${NC}"
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)  FRP_ARCH="amd64" ;;
    aarch64|arm64) FRP_ARCH="arm64" ;;
    *) echo -e "${RED}不支持的架构: $ARCH${NC}"; exit 1 ;;
esac

URL="https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_${FRP_ARCH}.tar.gz"
wget -q --show-progress "$URL" -O "/tmp/frp.tar.gz" || {
    echo -e "${RED}下载失败，手动下载:${NC}"
    echo "  $URL"
    echo "  放到 /tmp/frp.tar.gz 后重新运行"
    exit 1
}

tar -xzf /tmp/frp.tar.gz
cp "frp_${FRP_VERSION}_linux_${FRP_ARCH}/frps" "$FRP_DIR/frps"
chmod +x "$FRP_DIR/frps"
rm -rf "frp_${FRP_VERSION}_linux_${FRP_ARCH}" /tmp/frp.tar.gz

# ─── 3. 写配置 ───
echo -e "${CYAN}[3/6] 写入龍魂配置...${NC}"

cat > "$FRP_DIR/frps.toml" << TOMLEOF
# ═══════════════════════════════════════════════
# 龍魂系统 · frps 服务端配置
# DNA: #龍芯⚡️丙午·辛未·FRPS-v1.0
# UID: UID9622
# 生成: $(date '+%Y-%m-%d %H:%M:%S')
# ═══════════════════════════════════════════════

bindPort = 7000
auth.method = "token"
auth.token = "${FRP_TOKEN}"

# ── Web 管理面板 ──
webServer.addr = "0.0.0.0"
webServer.port = ${WEB_PORT}
webServer.user = "longhun"
webServer.password = "${WEB_PASSWORD}"

# ── Mac → 鲲鹏 API 通道 ──
[[proxies]]
name = "longhun-kunpeng-api"
type = "tcp"
localPort = 9633
remotePort = 19622

# ── Mac → 鲲鹏 SSH 跳板 ──
[[proxies]]
name = "longhun-kunpeng-ssh"
type = "tcp"
localPort = 22
remotePort = 29622

# ── 鲲鹏 → Mac API (备用反向通道) ──
[[proxies]]
name = "longhun-mac-api"
type = "tcp"
localPort = 9634
remotePort = 39622

allowPorts = [
  { start = 19622, end = 19622 },
  { start = 29622, end = 29622 },
  { start = 39622, end = 39622 }
]

transport.maxPoolCount = 50
transport.tcpMuxKeepaliveInterval = 30
transport.heartbeatTimeout = 90

log.to = "${FRP_DIR}/frps.log"
log.level = "info"
log.maxDays = 30
TOML EOF

# ─── 4. 防火墙 ───
echo -e "${CYAN}[4/6] 配置防火墙...${NC}"

if command -v ufw &>/dev/null; then
    ufw allow 7000/tcp 2>/dev/null || true
    ufw allow ${WEB_PORT}/tcp 2>/dev/null || true
    ufw allow 19622/tcp 2>/dev/null || true
    ufw allow 29622/tcp 2>/dev/null || true
    ufw allow 39622/tcp 2>/dev/null || true
elif command -v firewall-cmd &>/dev/null; then
    for port in 7000 ${WEB_PORT} 19622 29622 39622; do
        firewall-cmd --permanent --add-port=${port}/tcp 2>/dev/null || true
    done
    firewall-cmd --reload 2>/dev/null || true
else
    for port in 7000 ${WEB_PORT} 19622 29622 39622; do
        iptables -I INPUT -p tcp --dport ${port} -j ACCEPT 2>/dev/null || true
    done
fi

# ─── 5. systemd ───
echo -e "${CYAN}[5/6] 注册 systemd 服务...${NC}"

cat > /etc/systemd/system/frps.service << SYSTEMDEOF
[Unit]
Description=FRP Server - 龍魂隧道服务端
Documentation=https://longhun888.com
After=network.target

[Service]
Type=simple
ExecStart=${FRP_DIR}/frps -c ${FRP_DIR}/frps.toml
Restart=always
RestartSec=5
User=root
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

systemctl daemon-reload
systemctl enable frps

# ─── 6. 启动 ───
echo -e "${CYAN}[6/6] 启动 frps...${NC}"
systemctl restart frps
sleep 2

# ─── 验证 ───
echo ""
echo "════════════════════════════════════════════════"
echo -e "${BOLD}🐉 龍魂 frps 部署完成${NC}"
echo "════════════════════════════════════════════════"
echo ""

if systemctl is-active --quiet frps; then
    echo -e "  服务: ${GREEN}🟢 运行中${NC}"
else
    echo -e "  服务: ${RED}🔴 异常，检查: systemctl status frps${NC}"
fi

echo ""
echo -e "  🌐 Web面板:    ${CYAN}http://${PUBLIC_IP}:${WEB_PORT}${NC}"
echo -e "  账号/密码:     longhun / ${WEB_PASSWORD}"
echo -e "  Token:         ***${FRP_TOKEN: -4}"
echo ""
echo "  端口映射:"
echo -e "    ${YELLOW}19622${NC} → 鲲鹏 API (9633)"
echo -e "    ${YELLOW}29622${NC} → 鲲鹏 SSH (22)"
echo -e "    ${YELLOW}39622${NC} → Mac API (9634)(备用)"
echo ""
echo "  下一步:"
echo "    1. 部署鲲鹏端 frpc: bash deploy/deploy-frpc-kunpeng.sh"
echo "    2. 部署 Mac 端 frpc:  python3 L6_同步层/dual_node_cli.py tunnel install"
echo "    3. ⚠️ 如果使用云服务器安全组，手动放行: 7000, ${WEB_PORT}, 19622, 29622, 39622"
echo ""
echo -e "  DNA: #龍芯⚡️丙午·辛未·FRPS-DEPLOY-v1.0"
echo ""
