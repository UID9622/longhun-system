#!/bin/bash
# 龍魂主权 IP 伪装脚本·升级版 v1.0
# ~/longhun-system/tools/disguise.sh
#
# DNA: #龍芯⚡️2026-06-01-00:50-IP-SOVEREIGN-DISGUISE-v1.0
# M号: M267
# 场景分层·定点突破·业务隔离·全栈一致
#
# 用法: disguise.sh {light|medium|heavy|off|status}
#   light   - 🅛1 轻度·启动商业VPN (Mullvad/ProtonVPN)
#   medium  - 🅛2 中度·启动伪装浏览器Profile (Brave US)
#   heavy   - 🅛3 重度·启动Tor+Proxychains (仅应急)
#   off     - 🅛0 关闭所有伪装·回归主权裸奔
#   status  - 显示当前伪装状态

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 工具目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LONGHUN_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$HOME/.disguise.env"
LOG_FILE="$LONGHUN_ROOT/logs/disguise.log"

# 创建日志目录
mkdir -p "$LONGHUN_ROOT/logs"

log_action() {
    local msg="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $msg" >> "$LOG_FILE"
    echo -e "${BLUE}[龍魂]${NC} $msg"
}

get_current_ip() {
    curl -s ifconfig.me 2>/dev/null || echo "未知"
}

check_dns_leak() {
    echo -e "${YELLOW}DNS检测 (来自 dnsleaktest.com)${NC}"
    curl -s https://dnsleaktest.com/api/v1/status 2>/dev/null | head -20 || echo "DNS检测不可用 (可能需要代理)"
}

# ==================== 🅛0 裸奔（默认） ====================
mode_off() {
    log_action "🅛0 关闭所有伪装·回归主权裸奔"

    # 停止Tor
    if brew services list 2>/dev/null | grep -q "tor"; then
        brew services stop tor 2>/dev/null || true
        log_action "Tor服务已停止"
    fi

    # 清空环境变量
    unset ALL_PROXY HTTP_PROXY HTTPS_PROXY SOCKS_PROXY

    # 更新.disguise.env
    cat > "$ENV_FILE" << 'EOF'
# 龍魂伪装环境配置 - 当前模式: 裸奔
MODE=off
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
CURRENT_IP=$(curl -s ifconfig.me)
EOF
    chmod 600 "$ENV_FILE"

    echo -e "${GREEN}✅ 伪装已关闭${NC}"
    echo -e "当前 IP: $(get_current_ip)"
}

# ==================== 🅛1 轻度（商业VPN） ====================
mode_light() {
    log_action "🅛1 轻度模式·启动商业VPN (Mullvad或ProtonVPN)"

    # 检查是否装过
    if ! command -v open &> /dev/null; then
        echo -e "${RED}❌ 此脚本仅支持 macOS${NC}"
        return 1
    fi

    # 尝试启动Mullvad
    if open -a "Mullvad VPN" 2>/dev/null; then
        log_action "Mullvad客户端已启动 (请手动选择美国节点)"
        echo -e "${GREEN}✅ Mullvad启动成功${NC}"
        echo -e "${YELLOW}⚠️  请手动在客户端中选择美国节点${NC}"
        sleep 2
    # 否则尝试ProtonVPN
    elif open -a "ProtonVPN" 2>/dev/null; then
        log_action "ProtonVPN客户端已启动 (请手动选择美国节点)"
        echo -e "${GREEN}✅ ProtonVPN启动成功${NC}"
        echo -e "${YELLOW}⚠️  请手动在客户端中选择美国节点${NC}"
        sleep 2
    else
        echo -e "${RED}❌ 未找到Mullvad或ProtonVPN${NC}"
        echo -e "请先安装: ${BLUE}brew install --cask mullvad-vpn${NC} 或 ${BLUE}brew install --cask protonvpn${NC}"
        return 1
    fi

    # 更新.disguise.env
    cat > "$ENV_FILE" << EOF
# 龍魂伪装环境配置 - 当前模式: 轻度VPN
MODE=light
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
CURRENT_IP=$(get_current_ip)
VPN_CLIENT=Mullvad或ProtonVPN
EOF
    chmod 600 "$ENV_FILE"

    echo -e "${BLUE}验证VPN连接:${NC}"
    sleep 3
    echo "当前 IP: $(get_current_ip)"
}

# ==================== 🅛2 中度（伪装浏览器Profile） ====================
mode_medium() {
    log_action "🅛2 中度模式·启动伪装浏览器Profile"

    # 检查Brave是否装过
    if ! open -a "Brave Browser" &>/dev/null; then
        echo -e "${RED}❌ 未找到Brave浏览器${NC}"
        echo -e "请先安装: ${BLUE}brew install --cask brave-browser${NC}"
        return 1
    fi

    local profile_dir="$HOME/Library/Application Support/BraveSoftware/Disguise-US"
    mkdir -p "$profile_dir"

    log_action "创建Brave伪装Profile: $profile_dir"

    # 创建伪装Profile的Preferences文件（可选，主要通过--lang和--user-data-dir实现）
    cat > "$profile_dir/Preferences" << 'EOF'
{
  "intl": {
    "accept_languages": "en-US,en",
    "selected_languages": "en-US"
  },
  "browser": {
    "enable_translate": false
  },
  "spellcheck": {
    "dictionary": "en-US"
  }
}
EOF
    chmod 600 "$profile_dir/Preferences"

    # 启动Brave (后台)
    open -na "Brave Browser" --args \
        --user-data-dir="$profile_dir" \
        --lang=en-US \
        --incognito &

    log_action "Brave伪装Profile已启动 (无痕模式)"

    # 更新.disguise.env
    cat > "$ENV_FILE" << EOF
# 龍魂伪装环境配置 - 当前模式: 中度浏览器伪装
MODE=medium
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PROFILE_PATH=$profile_dir
BRAVE_SETTINGS="lang=en-US, timezone=America/Los_Angeles, fingerprinting=strict"
NOTES="在浏览器设置中手动调整:"
NOTES_TZ="⚙️ 时区: America/Los_Angeles"
NOTES_FP="⚙️ 指纹: brave://settings/shields → Fingerprinting: Strict"
NOTES_WR="⚙️ WebRTC: brave://settings/privacy → WebRTC IP Handling: Disable Non-Proxied UDP"
EOF
    chmod 600 "$ENV_FILE"

    echo -e "${GREEN}✅ Brave伪装Profile已启动${NC}"
    echo -e "${YELLOW}⚠️  手动配置项:${NC}"
    echo -e "   1. brave://settings/languages → 保留 English (United States)·删除其他"
    echo -e "   2. brave://settings/shields → Fingerprinting: Strict"
    echo -e "   3. brave://settings/privacy → WebRTC IP Handling: Disable Non-Proxied UDP"
}

# ==================== 🅛3 重度（Tor应急） ====================
mode_heavy() {
    log_action "🅛3 重度模式·启动Tor应急通道"

    # 检查/装Tor
    if ! command -v tor &> /dev/null; then
        echo -e "${YELLOW}未找到Tor·正在安装...${NC}"
        brew install tor || {
            echo -e "${RED}❌ Tor安装失败${NC}"
            return 1
        }
    fi

    # 配置torrc
    local torrc="/opt/homebrew/etc/tor/torrc"
    if [ ! -f "$torrc" ]; then
        echo -e "${YELLOW}创建Tor配置文件...${NC}"
        cat > "$torrc" << 'EOF'
SocksPort 127.0.0.1:9050
ExitNodes {us},{de},{nl}
StrictNodes 1
DNSPort 5353
AutomapHostsOnResolve 1
EOF
        chmod 600 "$torrc"
    fi

    # 启动Tor
    brew services start tor 2>/dev/null || {
        echo -e "${RED}❌ Tor启动失败${NC}"
        return 1
    }

    log_action "Tor服务已启动 (SOCKS5: 127.0.0.1:9050)"

    sleep 3

    # 更新.disguise.env
    cat > "$ENV_FILE" << 'EOF'
# 龍魂伪装环境配置 - 当前模式: 重度Tor应急
MODE=heavy
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
TOR_SOCKS=127.0.0.1:9050
TOR_DNS=127.0.0.1:5353
WARNING="⚠️  重度模式仅用于极端应急·日常业务禁止使用"
USAGE_INSTRUCTION="在新终端执行: export ALL_PROXY=socks5h://127.0.0.1:9050"
EOF
    chmod 600 "$ENV_FILE"

    echo -e "${GREEN}✅ Tor应急通道已启动${NC}"
    echo -e "${RED}⚠️  警告:${NC}"
    echo -e "   龍魂日常业务(操作台/DeepSeek桥/Notion)${RED}禁止${NC}走Tor"
    echo -e "   Tor 仅在极端匿名需求时启用"
    echo -e ""
    echo -e "${BLUE}在新终端运行代理命令:${NC}"
    echo -e "   ${YELLOW}export ALL_PROXY=socks5h://127.0.0.1:9050${NC}"
    echo -e "   ${YELLOW}curl ifconfig.me${NC}"
}

# ==================== 状态查询 ====================
mode_status() {
    echo -e "${BLUE}═══ 龍魂伪装系统状态 ═══${NC}"
    echo ""

    # 读取环境配置
    if [ -f "$ENV_FILE" ]; then
        echo -e "${GREEN}[配置文件]${NC} $ENV_FILE"
        cat "$ENV_FILE" | grep -v '^#' | sed 's/^/  /'
        echo ""
    fi

    # 当前IP
    echo -e "${BLUE}[网络状态]${NC}"
    echo -e "  当前 IP: $(get_current_ip)"
    echo -e "  ISP 信息: $(curl -s https://ifconfig.co/json 2>/dev/null | grep -o '"[^"]*"' | head -5 | tr '\n' ' ')"
    echo ""

    # Tor状态
    echo -e "${BLUE}[服务状态]${NC}"
    if brew services list 2>/dev/null | grep -q "tor.*started"; then
        echo -e "  Tor: ${GREEN}✅ 运行中${NC}"
    else
        echo -e "  Tor: ${YELLOW}⏸ 已停止${NC}"
    fi
    echo ""

    # 日志
    echo -e "${BLUE}[最近操作日志]${NC}"
    if [ -f "$LOG_FILE" ]; then
        tail -5 "$LOG_FILE" | sed 's/^/  /'
    fi
}

# ==================== 主逻辑 ====================
MODE="${1:-status}"

case "$MODE" in
    light)
        mode_light
        ;;
    medium)
        mode_medium
        ;;
    heavy)
        mode_heavy
        ;;
    off)
        mode_off
        ;;
    status|*)
        mode_status
        ;;
esac

log_action "命令完成: disguise.sh $MODE"
echo ""
