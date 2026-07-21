#!/bin/bash
# ═══════════════════════════════════════════════
# 龍魂 · WireGuard 服务器端一键部署
# DNA: #龍芯⚡️丙午·乙申·己酉·亥时·WG-SERVER-SETUP-v1.0
# 目标: 华为云鲲鹏 (Ubuntu/Debian)
# ═══════════════════════════════════════════════
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
err()  { echo -e "${RED}[✗]${NC} $*"; exit 1; }

# ── 权限检查 ──
[[ $EUID -eq 0 ]] || err "请用 root 执行: sudo bash $0"

WG_IF="wg0"
WG_PORT="${1:-51820}"
WG_NET="10.200.200.0/24"
WG_SERVER_IP="10.200.200.1"

echo ""
echo "══════════════════════════════════════"
echo "  龍魂 WireGuard 服务器端部署"
echo "  端口: ${WG_PORT}  网络: ${WG_NET}"
echo "══════════════════════════════════════"
echo ""

# ── Step 1: 检测系统 ──
if [ -f /etc/os-release ]; then
    . /etc/os-release
    log "系统: $NAME $VERSION_ID"
else
    err "无法检测系统版本"
fi

# ── Step 2: 安装 WireGuard ──
log "安装 WireGuard..."
case "$ID" in
    ubuntu|debian)
        apt-get update -qq
        apt-get install -y -qq wireguard wireguard-tools iptables
        ;;
    centos|rhel|fedora|openEuler)
        yum install -y wireguard-tools iptables 2>/dev/null || \
        dnf install -y wireguard-tools iptables
        ;;
    *)
        warn "未知发行版 $ID，尝试 apt-get..."
        apt-get update -qq && apt-get install -y -qq wireguard wireguard-tools iptables || \
        err "自动安装失败，请手动安装 wireguard-tools"
        ;;
esac
log "WireGuard 已安装"

# ── Step 3: 检测默认网卡 ──
DEFAULT_IF=$(ip route show default 2>/dev/null | awk '/default/ {print $5}' | head -1)
if [ -z "$DEFAULT_IF" ]; then
    DEFAULT_IF=$(ip link show | grep -E '^[0-9]+: (eth|ens|enp)' | head -1 | awk -F': ' '{print $2}')
fi
[ -z "$DEFAULT_IF" ] && err "无法检测默认网卡，请手动指定"
log "默认网卡: $DEFAULT_IF"

# ── Step 4: 生成密钥 ──
log "生成密钥对..."
mkdir -p /etc/wireguard
cd /etc/wireguard
umask 077

# 备份旧密钥（如果存在）
[ -f privatekey ] && mv privatekey "privatekey.bak.$(date +%s)"
[ -f publickey ]  && mv publickey  "publickey.bak.$(date +%s)"

wg genkey | tee privatekey | wg pubkey > publickey
SERVER_PRIVATE=$(cat privatekey)
SERVER_PUBLIC=$(cat publickey)
chmod 600 privatekey publickey
log "密钥对已生成"

# ── Step 5: 写配置 ──
log "生成 /etc/wireguard/wg0.conf..."

# 备份旧配置
[ -f wg0.conf ] && cp wg0.conf "wg0.conf.bak.$(date +%s)"

cat > /etc/wireguard/wg0.conf << WGCONF
[Interface]
Address    = ${WG_SERVER_IP}/24
ListenPort = ${WG_PORT}
PrivateKey = ${SERVER_PRIVATE}

# NAT 转发规则
PostUp   = iptables -A FORWARD -i ${WG_IF} -j ACCEPT
PostUp   = iptables -t nat -A POSTROUTING -o ${DEFAULT_IF} -j MASQUERADE
PostDown = iptables -D FORWARD -i ${WG_IF} -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ${DEFAULT_IF} -j MASQUERADE

# ═══ 客户端 Peers ═══
# 把客户端公钥填入下面（运行客户端脚本后会输出公钥）

# Mac 客户端
#[Peer]
#PublicKey  = <MAC_PUBLIC_KEY>
#AllowedIPs = 10.200.200.2/32

# iPhone 客户端
#[Peer]
#PublicKey  = <IPHONE_PUBLIC_KEY>
#AllowedIPs = 10.200.200.3/32

# iPad 客户端
#[Peer]
#PublicKey  = <IPAD_PUBLIC_KEY>
#AllowedIPs = 10.200.200.4/32
WGCONF

chmod 600 wg0.conf
log "配置文件已生成"

# ── Step 6: 启用 IP 转发 ──
log "启用 IP 转发..."
sysctl -w net.ipv4.ip_forward=1 > /dev/null
if ! grep -q 'net.ipv4.ip_forward = 1' /etc/sysctl.conf; then
    echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf
fi
log "IP 转发已启用"

# ── Step 7: 防火墙规则 ──
log "配置防火墙..."
if command -v ufw &>/dev/null && ufw status | grep -q "Status: active"; then
    ufw allow ${WG_PORT}/udp comment "WireGuard VPN"
    log "ufw 已放行 UDP ${WG_PORT}"
fi
# iptables 限速（防暴力）
iptables -C INPUT -p udp --dport ${WG_PORT} -m limit --limit 10/sec -j ACCEPT 2>/dev/null || \
iptables -I INPUT -p udp --dport ${WG_PORT} -m limit --limit 10/sec -j ACCEPT
log "iptables 限速规则已添加"

# ── Step 8: 启动服务 ──
log "启动 WireGuard..."
wg-quick down ${WG_IF} 2>/dev/null || true
wg-quick up ${WG_IF}
systemctl enable wg-quick@${WG_IF} 2>/dev/null || true
log "WireGuard 已启动 + 开机自启"

# ── Step 9: 验证 ──
sleep 1
echo ""
echo "══════════════════════════════════════"
echo "  部署完成！"
echo "══════════════════════════════════════"
echo ""
echo "  📋 服务器公钥："
echo "  ${SERVER_PUBLIC}"
echo ""
echo "  🌐 WireGuard 内网 IP: ${WG_SERVER_IP}"
echo "  🔌 监听端口: UDP ${WG_PORT}"
echo "  🖧  默认网卡: ${DEFAULT_IF}"
echo ""
echo "  ═══ 下一步 ═══"
echo "  1. 在 Mac 上执行: sudo bash deploy/wireguard/client-setup.sh"
echo "  2. 把客户端脚本输出的公钥贴到此处:"
echo "     vim /etc/wireguard/wg0.conf"
echo "     取消 [Peer] 段注释，填入 PublicKey"
echo "  3. 华为云安全组放行 UDP ${WG_PORT}"
echo "  4. 重启服务: wg-quick down wg0 && wg-quick up wg0"
echo ""
echo "  当前状态:"
wg show
