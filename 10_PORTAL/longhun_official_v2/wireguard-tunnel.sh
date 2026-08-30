# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ============================================
# 龍魂系统 · WireGuard 隧道一键配置
# 香港节点（服务端） + 鲲鹏（客户端）
# ============================================

set -e

# ===== 配置参数（修改为你的实际 IP）=====
HK_SERVER_IP="你的香港服务器公网IP"
KUNPENG_IP="你的鲲鹏内网IP或公网IP"
WG_PORT="51820"
WG_NETWORK="10.8.0.0/24"
HK_WG_IP="10.8.0.1"
KP_WG_IP="10.8.0.2"

# 生成密钥对（如不存在）
gen_keys() {
    local priv_file=$1
    local pub_file=$2
    if [ ! -f "$priv_file" ]; then
        wg genkey | tee "$priv_file" | wg pubkey > "$pub_file"
        chmod 600 "$priv_file"
    fi
}

# ===== 香港节点服务端配置 =====
setup_hk_server() {
    echo "[龍魂] 配置香港节点 WireGuard 服务端..."

    # 安装 WireGuard
    if ! command -v wg &> /dev/null; then
        if command -v apt &> /dev/null; then
            apt update && apt install -y wireguard wireguard-tools
        elif command -v dnf &> /dev/null; then
            dnf install -y wireguard-tools
        elif command -v yum &> /dev/null; then
            yum install -y wireguard-tools
        fi
    fi

    mkdir -p /etc/wireguard
    gen_keys "/etc/wireguard/hk_private.key" "/etc/wireguard/hk_public.key"
    HK_PRIV=$(cat /etc/wireguard/hk_private.key)
    HK_PUB=$(cat /etc/wireguard/hk_public.key)

    # 生成客户端密钥（在服务端预生成，后面传给鲲鹏）
    gen_keys "/etc/wireguard/kp_private.key" "/etc/wireguard/kp_public.key"
    KP_PUB=$(cat /etc/wireguard/kp_public.key)
    KP_PRIV=$(cat /etc/wireguard/kp_private.key)

    # 服务端配置
    cat > /etc/wireguard/wg0.conf << EOF
[Interface]
Address = ${HK_WG_IP}/24
ListenPort = ${WG_PORT}
PrivateKey = ${HK_PRIV}
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# 鲲鹏客户端
PublicKey = ${KP_PUB}
AllowedIPs = ${KP_WG_IP}/32
EOF

    # 启用 IP 转发
    sysctl -w net.ipv4.ip_forward=1
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

    # 防火墙放行
    if command -v ufw &> /dev/null; then
        ufw allow ${WG_PORT}/udp
    elif command -v firewall-cmd &> /dev/null; then
        firewall-cmd --permanent --add-port=${WG_PORT}/udp
        firewall-cmd --reload
    fi

    # 启动
    wg-quick down wg0 2>/dev/null || true
    wg-quick up wg0
    systemctl enable wg-quick@wg0

    echo ""
    echo "===== 鲲鹏客户端配置（复制到鲲鹏执行）====="
    echo ""
    cat << EOF
# 在鲲鹏上执行以下命令：
mkdir -p /etc/wireguard
cat > /etc/wireguard/wg0.conf << 'KUNPENG_EOF'
[Interface]
Address = ${KP_WG_IP}/24
PrivateKey = ${KP_PRIV}
DNS = 8.8.8.8

[Peer]
PublicKey = ${HK_PUB}
Endpoint = ${HK_SERVER_IP}:${WG_PORT}
AllowedIPs = ${HK_WG_IP}/32
PersistentKeepalive = 25
KUNPENG_EOF

wg-quick down wg0 2>/dev/null || true
wg-quick up wg0
systemctl enable wg-quick@wg0
EOF
    echo ""
    echo "===== 鲲鹏配置结束 ====="
}

# ===== 鲲鹏客户端配置（单独执行）=====
setup_kunpeng_client() {
    echo "[龍魂] 配置鲲鹏 WireGuard 客户端..."
    echo "[提示] 请先在香港节点执行服务端配置，获取客户端配置后在此执行"
}

# 根据主机角色执行
if [ "$1" == "hk" ]; then
    setup_hk_server
elif [ "$1" == "kp" ]; then
    setup_kunpeng_client
else
    echo "用法: $0 hk    # 在香港节点执行服务端配置"
    echo "      $0 kp    # 在鲲鹏执行客户端配置（需先获取配置）"
    exit 1
fi

echo ""
echo "[龍魂] WireGuard 配置完成"
echo "测试连通性: ping ${KP_WG_IP} (从香港) 或 ping ${HK_WG_IP} (从鲲鹏)"
