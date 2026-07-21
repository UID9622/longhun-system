#!/bin/bash
# ============================================================================
# deploy-frpc-kunpeng.sh — 华为鲲鹏一键部署 frpc 客户端
# DNA: #龍芯⚡️丙午·辛未·FRPC-KUNPENG-v1.0
#
# 在鲲鹏服务器上执行，将本地 API/SSH 暴露到公网
# ============================================================================

set -e

FRP_VERSION="${FRP_VERSION:-0.58.1}"
LONGHUN_ROOT="${LONGHUN_ROOT:-/opt/longhun-system}"
FRP_DIR="${LONGHUN_ROOT}/frpc"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo ""
echo -e "${BOLD}🐉 龍魂系统 · 鲲鹏端 frpc 部署${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── 检查配置 ───
read -p "公网frps服务器IP: " FRP_SERVER
if [ -z "$FRP_SERVER" ]; then
    echo -e "${RED}❌ 必须提供公网服务器IP${NC}"
    exit 1
fi

read -p "frp Token [LONGHUN2026_UID9622_KUNPENG]: " FRP_TOKEN
FRP_TOKEN=${FRP_TOKEN:-LONGHUN2026_UID9622_KUNPENG}

echo ""
echo -e "服务器: ${GREEN}${FRP_SERVER}${NC}"
echo -e "路径:   ${CYAN}${LONGHUN_ROOT}${NC}"
read -p "确认部署? [Y/n]: " CONFIRM
CONFIRM=${CONFIRM:-Y}
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

mkdir -p "$FRP_DIR" "${LONGHUN_ROOT}/logs"

# ─── 1. 下载 ARM64 frpc ───
echo -e "\n${CYAN}[1/5] 下载 ARM64 frpc...${NC}"
cd /tmp

ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    FRP_ARCH="amd64"
elif [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
    FRP_ARCH="arm64"
else
    echo -e "${RED}未知架构: $ARCH${NC}"
    exit 1
fi

URL="https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_${FRP_ARCH}.tar.gz"
wget -q --show-progress "$URL" -O "/tmp/frp.tar.gz" || {
    echo -e "${RED}下载失败${NC}"
    exit 1
}

tar -xzf /tmp/frp.tar.gz
cp "frp_${FRP_VERSION}_linux_${FRP_ARCH}/frpc" "$FRP_DIR/frpc"
chmod +x "$FRP_DIR/frpc"
rm -rf "frp_${FRP_VERSION}_linux_${FRP_ARCH}" /tmp/frp.tar.gz

# ─── 2. 写配置 ───
echo -e "${CYAN}[2/5] 写入配置...${NC}"

cat > "$FRP_DIR/frpc.toml" << TOMLEOF
# 龍魂系统 · 鲲鹏端 frpc 配置
# DNA: #龍芯⚡️丙午·辛未·FRPC-KUNPENG

serverAddr = "${FRP_SERVER}"
serverPort = 7000
auth.method = "token"
auth.token = "${FRP_TOKEN}"

# ── 暴露双节点 API ──
[[proxies]]
name = "longhun-kunpeng-api"
type = "tcp"
localIP = "127.0.0.1"
localPort = 9633
remotePort = 19622

# ── 暴露 SSH 跳板 ──
[[proxies]]
name = "longhun-kunpeng-ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 29622

log.to = "${LONGHUN_ROOT}/logs/frpc-kunpeng.log"
log.level = "info"
log.maxDays = 30
TOML EOF

# ─── 3. 启动双节点 API（如果未启动）───
echo -e "${CYAN}[3/5] 检查双节点 API...${NC}"

if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "   安装 fastapi..."
    pip3 install fastapi uvicorn -q
fi

# 检查 9633 端口是否在监听
if ! ss -tlnp | grep -q 9633 2>/dev/null; then
    echo "   启动双节点 API (端口 9633)..."
    if [ -f "${LONGHUN_ROOT}/L6_同步层/dual_node_api.py" ]; then
        nohup python3 "${LONGHUN_ROOT}/L6_同步层/dual_node_api.py" serve --role kunpeng --host 0.0.0.0 --port 9633 \
            > "${LONGHUN_ROOT}/logs/dual_node_api.log" 2>&1 &
        echo "   PID: $!"
    else
        echo -e "   ${RED}⚠️  L6_同步层/dual_node_api.py 不存在，跳过${NC}"
    fi
else
    echo "   🟢 端口 9633 已监听"
fi

# ─── 4. systemd ───
echo -e "${CYAN}[4/5] 注册 systemd...${NC}"

cat > /etc/systemd/system/frpc-kunpeng.service << SYSTEMDEOF
[Unit]
Description=FRP Client - 龍魂鲲鹏隧道
After=network.target

[Service]
Type=simple
ExecStart=${FRP_DIR}/frpc -c ${FRP_DIR}/frpc.toml
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

systemctl daemon-reload
systemctl enable frpc-kunpeng

# ─── 5. 启动 ───
echo -e "${CYAN}[5/5] 启动 frpc...${NC}"
systemctl restart frpc-kunpeng
sleep 2

# ─── 验证 ───
echo ""
echo "════════════════════════════════════════════════"
echo -e "${BOLD}🐉 鲲鹏 frpc 部署完成${NC}"
echo "════════════════════════════════════════════════"
echo ""

if systemctl is-active --quiet frpc-kunpeng; then
    echo -e "  frpc:  ${GREEN}🟢 运行中${NC}"
else
    echo -e "  frpc:  ${RED}🔴 异常${NC}"
    echo -e "  ${CYAN}日志: journalctl -u frpc-kunpeng -f${NC}"
fi

echo ""
echo -e "  API 公网: ${GREEN}${FRP_SERVER}:19622${NC}"
echo -e "  SSH 跳板: ${GREEN}${FRP_SERVER}:29622${NC}"
echo ""
echo "  测试:"
echo -e "    curl http://${FRP_SERVER}:19622/health"
echo ""
echo "  日志:"
echo -e "    journalctl -u frpc-kunpeng -f"
echo -e "    tail -f ${LONGHUN_ROOT}/logs/frpc-kunpeng.log"
echo ""
echo -e "  DNA: #龍芯⚡️丙午·辛未·FRPC-KUNPENG-v1.0"
echo ""
