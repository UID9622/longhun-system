#!/bin/bash
# ═══════════════════════════════════════════════
# 龍魂 · WireGuard 客户端一键部署 (Mac)
# DNA: #龍芯⚡️丙午·乙申·己酉·亥时·WG-CLIENT-SETUP-v1.0
# 目标: macOS (Apple Silicon / Intel)
# ═══════════════════════════════════════════════
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
err()  { echo -e "${RED}[✗]${NC} $*"; exit 1; }
info() { echo -e "${BLUE}[i]${NC} $*"; }

WG_IF="wg0"
WG_PORT="${1:-51820}"
WG_SERVER_ENDPOINT="${2:-119.13.90.27}"
WG_SERVER_IP="10.200.200.1"
WG_CLIENT_IP="10.200.200.2"
WG_NET="10.200.200.0/24"

echo ""
echo "══════════════════════════════════════"
echo "  龍魂 WireGuard Mac 客户端部署"
echo "  服务器: ${WG_SERVER_ENDPOINT}:${WG_PORT}"
echo "══════════════════════════════════════"
echo ""

# ── 系统检查 ──
[[ "$(uname)" == "Darwin" ]] || err "此脚本仅适用于 macOS"

# ── Step 1: 安装 WireGuard ──
if ! command -v wg &>/dev/null; then
    log "安装 wireguard-tools..."
    if command -v brew &>/dev/null; then
        brew install wireguard-tools
    else
        err "需要 Homebrew。请先安装: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    fi
fi
log "wireguard-tools 就绪: $(wg --version 2>&1 | head -1)"

# ── Step 2: 生成密钥 ──
log "生成密钥对..."
mkdir -p ~/.wg
chmod 700 ~/.wg
cd ~/.wg

# 备份旧密钥
[ -f privatekey ] && mv privatekey "privatekey.bak.$(date +%s)"
[ -f publickey ]  && mv publickey  "publickey.bak.$(date +%s)"

wg genkey | tee privatekey | wg pubkey > publickey
CLIENT_PRIVATE=$(cat privatekey)
CLIENT_PUBLIC=$(cat publickey)
chmod 600 privatekey publickey
log "密钥对已生成"

# ── Step 3: 请求服务器公钥 ──
echo ""
info "请输入服务器公钥（服务器端脚本输出的那串字符）："
read -r SERVER_PUBKEY
if [ -z "$SERVER_PUBKEY" ]; then
    warn "未输入服务器公钥。稍后手动编辑 /usr/local/etc/wireguard/wg0.conf"
    SERVER_PUBKEY="<SERVER_PUBLIC_KEY>"
fi

# 验证公钥格式（Base64, 43-44 字符）
PK_LEN=$(echo -n "$SERVER_PUBKEY" | wc -c | tr -d ' ')
if [ "$SERVER_PUBKEY" != "<SERVER_PUBLIC_KEY>" ] && [ "$PK_LEN" -ne 44 ] && [ "$PK_LEN" -ne 43 ]; then
    warn "公钥长度 ${PK_LEN} 字符（预期 44），可能是复制时多了空格/换行"
    info "将直接使用你输入的值，如果连不上请检查公钥"
fi

# ── Step 4: 写配置 ──
log "生成 /usr/local/etc/wireguard/wg0.conf..."
sudo mkdir -p /usr/local/etc/wireguard

# 备份旧配置
[ -f /usr/local/etc/wireguard/wg0.conf ] && \
    sudo cp /usr/local/etc/wireguard/wg0.conf "/usr/local/etc/wireguard/wg0.conf.bak.$(date +%s)"

sudo tee /usr/local/etc/wireguard/wg0.conf > /dev/null << WGCONF
[Interface]
PrivateKey = ${CLIENT_PRIVATE}
Address    = ${WG_CLIENT_IP}/24
DNS        = 114.114.114.114, 223.5.5.5

# MTU 优化（如遇分片问题可调整）
# MTU = 1420

[Peer]
PublicKey           = ${SERVER_PUBKEY}
Endpoint            = ${WG_SERVER_ENDPOINT}:${WG_PORT}
AllowedIPs          = ${WG_NET}, 192.168.0.0/16
PersistentKeepalive = 25
WGCONF

sudo chmod 600 /usr/local/etc/wireguard/wg0.conf
log "配置文件已生成"

# ── Step 5: 启动 WireGuard ──
log "启动 WireGuard..."
sudo wg-quick down ${WG_IF} 2>/dev/null || true
sudo wg-quick up ${WG_IF}
log "WireGuard 已启动"

# ── Step 6: 创建日志目录 ──
sudo mkdir -p /usr/local/var/log
sudo touch /usr/local/var/log/longhun-wireguard.log
sudo chmod 644 /usr/local/var/log/longhun-wireguard.log

# ── Step 7: 配置 launchd 守护 ──
log "配置 launchd 自动重连守护..."
sudo tee /Library/LaunchDaemons/com.longhun.wireguard.plist > /dev/null << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.wireguard</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>-c</string>
        <string>
            while true; do
                if ! ping -c 1 -W 3 10.200.200.1 > /dev/null 2>&1; then
                    echo "[$(date +%Y-%m-%dT%H:%M:%S)] WireGuard 断连，重连中..."
                    /usr/bin/wg-quick down wg0 2>/dev/null
                    sleep 2
                    /usr/bin/wg-quick up wg0 2>/dev/null
                    if ping -c 1 -W 3 10.200.200.1 > /dev/null 2>&1; then
                        echo "[$(date +%Y-%m-%dT%H:%M:%S)] 重连成功"
                    else
                        echo "[$(date +%Y-%m-%dT%H:%M:%S)] 重连失败，30秒后再试"
                    fi
                fi
                sleep 30
            done
        </string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/longhun-wireguard.log</string>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/longhun-wireguard.err</string>
</dict>
</plist>
PLIST_EOF

sudo chown root:wheel /Library/LaunchDaemons/com.longhun.wireguard.plist
sudo launchctl unload /Library/LaunchDaemons/com.longhun.wireguard.plist 2>/dev/null || true
sudo launchctl load /Library/LaunchDaemons/com.longhun.wireguard.plist
log "launchd 守护已加载"

# ── Step 8: 验证 ──
sleep 1
echo ""
echo "══════════════════════════════════════"
echo "  部署完成！"
echo "══════════════════════════════════════"
echo ""
echo "  📋 Mac 公钥（发给服务器）："
echo "  ${CLIENT_PUBLIC}"
echo ""
echo "  🌐 本机 WireGuard IP: ${WG_CLIENT_IP}"
echo "  🎯 服务器 IP: ${WG_SERVER_IP}"
echo ""

# 连通性测试
echo "  ═══ 连通性测试 ═══"
if ping -c 2 -W 3 ${WG_SERVER_IP} > /dev/null 2>&1; then
    echo -e "  ${GREEN}🟢 隧道连通！ping ${WG_SERVER_IP} OK${NC}"
    echo ""
    echo "  试试："
    echo "    ssh root@${WG_SERVER_IP}          # 隧道内 SSH"
    echo "    curl http://${WG_SERVER_IP}:9627  # Dashboard"
else
    echo -e "  ${RED}🔴 ping 不通${NC}"
    echo ""
    echo "  可能原因："
    echo "    1. 服务器公钥没填对 → 检查 /usr/local/etc/wireguard/wg0.conf"
    echo "    2. 服务器还没把 Mac 公钥加进去 → 把上面的公钥发给服务器端"
    echo "    3. 华为云安全组未放行 UDP ${WG_PORT}"
    echo "    4. 服务器 WireGuard 没启动 → ssh 过去执行 wg show"
fi

echo ""
echo "  守护状态:"
sudo launchctl list | grep longhun.wireguard && echo "  🟢 launchd 守护运行中" || echo "  🔴 launchd 守护未加载"

echo ""
echo "  ═══ 下一步（服务器端） ═══"
echo "  vim /etc/wireguard/wg0.conf"
echo "  取消 [Peer] 段注释，填入 Mac 公钥:"
echo "  ${CLIENT_PUBLIC}"
echo "  然后: wg-quick down wg0 && wg-quick up wg0"
echo ""
