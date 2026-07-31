#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 龍魂·内网互联节点 — 启动入口脚本
# DNA: #龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-ENTRYPOINT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════════
set -e

# ── 颜色输出 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🐉 龍魂·内网互联节点 v1.0                                    ║${NC}"
    echo -e "${BLUE}║  DNA: #龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-v1.0   ║${NC}"
    echo -e "${BLUE}║  核心: 一台鲲鹏当中心，所有设备内网直连，不经过云               ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ── 获取本机IP ──
get_ip() {
    local ip=""
    # 方法1: 通过默认路由
    ip=$(ip route get 1 2>/dev/null | grep -oP 'src \K\S+' | head -1) && echo "$ip" && return 0
    # 方法2: hostname -I
    ip=$(hostname -I 2>/dev/null | awk '{print $1}') && echo "$ip" && return 0
    # 方法3: ifconfig
    ip=$(ifconfig 2>/dev/null | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -1) && echo "$ip" && return 0
    echo "127.0.0.1"
}

# ── 自动发现网关 ──
discover_gateway() {
    local my_ip=$(get_ip)
    local subnet=$(echo "$my_ip" | cut -d. -f1-3)
    local port=${LONGHUN_GATEWAY_PORT:-9622}
    
    echo -e "${YELLOW}🔍 扫描局域网网关: ${subnet}.0/24 ...${NC}"
    echo "   (可能需要30-60秒)"
    
    # 先检查常见网关位置
    for i in 1 100 254; do
        local target="${subnet}.${i}"
        if curl -s -m 1 "http://${target}:${port}/health" 2>/dev/null | grep -q "龍"; then
            echo -e "${GREEN}✅ 发现龍魂网关: ${target}${NC}"
            echo "$target"
            return 0
        fi
    done
    
    # 全子网扫描
    for i in $(seq 1 254); do
        local target="${subnet}.${i}"
        # 跳过已检查的
        [[ "$i" == "1" || "$i" == "100" || "$i" == "254" ]] && continue
        
        if curl -s -m 0.3 "http://${target}:${port}/health" 2>/dev/null | grep -q "龍"; then
            echo -e "${GREEN}✅ 发现龍魂网关: ${target}${NC}"
            echo "$target"
            return 0
        fi
    done
    
    echo ""
    return 1
}

# ── 检测设备类型 ──
detect_type() {
    if [ -f /proc/cpuinfo ]; then
        if grep -qi "kunpeng\|taishan" /proc/cpuinfo 2>/dev/null; then
            echo "kunpeng"
            return
        fi
        if grep -qi "loongson\|loongarch" /proc/cpuinfo 2>/dev/null; then
            echo "loongson"
            return
        fi
        if grep -qi "phytium\|ft-2000" /proc/cpuinfo 2>/dev/null; then
            echo "phytium"
            return
        fi
    fi
    
    if [ -f /proc/device-tree/model ] && grep -qi "raspberry" /proc/device-tree/model 2>/dev/null; then
        echo "raspberry"
        return
    fi
    
    if [ "$(uname -s)" = "Darwin" ]; then
        echo "mac"
        return
    fi
    
    local arch=$(uname -m)
    case "$arch" in
        aarch64|arm64)  echo "arm_generic" ;;
        armv7l|armv6l)  echo "arm32" ;;
        x86_64|amd64)    echo "x86" ;;
        *)               echo "linux" ;;
    esac
}

# ── 网关模式 ──
start_gateway() {
    print_banner
    
    local my_ip=$(get_ip)
    
    echo -e "${GREEN}🐉 启动龍魂网关模式 (中心节点)${NC}"
    echo "   IP:   $my_ip"
    echo "   端口:  ${LONGHUN_GATEWAY_PORT:-9622}"
    echo "   安全: L0·DNA | L1·三色审计 | L2·熔断 | L3·输入过滤 | L4·防投毒 | L5·芯片门禁"
    echo ""
    
    exec python3 /opt/longhun/scripts/longhun-api-gateway.py \
        --host 0.0.0.0 \
        --port "${LONGHUN_GATEWAY_PORT:-9622}"
}

# ── 节点模式 ──
start_peer() {
    print_banner
    
    local my_ip=$(get_ip)
    local device_type="${LONGHUN_DEVICE_TYPE:-auto}"
    if [ "$device_type" = "auto" ]; then
        device_type=$(detect_type)
    fi
    local device_name="${LONGHUN_DEVICE_NAME:-$(hostname)}"
    
    echo -e "${GREEN}🐉 启动龍魂节点模式${NC}"
    echo "   设备: $device_name ($device_type)"
    echo "   IP:   $my_ip"
    echo ""
    
    # 自动发现网关
    local gateway=""
    if [ "${LONGHUN_GATEWAY:-auto}" = "auto" ]; then
        gateway=$(discover_gateway)
        if [ -z "$gateway" ]; then
            echo -e "${YELLOW}⚠️ 未发现龍魂网关${NC}"
            echo -e "${YELLOW}   尝试启动本地网关...${NC}"
            start_gateway
            return
        fi
    else
        gateway="$LONGHUN_GATEWAY"
    fi
    
    echo -e "${GREEN}   连接网关: $gateway${NC}"
    echo ""
    
    exec python3 /opt/longhun/scripts/longhun-peer-client.py \
        "$device_name" \
        "$device_type" \
        "$gateway" \
        --port "${LONGHUN_GATEWAY_PORT:-9622}"
}

# ── 守护模式 ──
start_daemon() {
    print_banner
    
    local device_type="${LONGHUN_DEVICE_TYPE:-auto}"
    if [ "$device_type" = "auto" ]; then
        device_type=$(detect_type)
    fi
    local device_name="${LONGHUN_DEVICE_NAME:-$(hostname)}"
    local gateway="${LONGHUN_GATEWAY:-auto}"
    
    echo -e "${GREEN}🐉 启动龍魂守护模式 (后台运行)${NC}"
    echo "   设备: $device_name ($device_type)"
    echo ""
    
    exec python3 /opt/longhun/scripts/longhun-peer-client.py \
        "$device_name" \
        "$device_type" \
        "$gateway" \
        --port "${LONGHUN_GATEWAY_PORT:-9622}" \
        --daemon
}

# ── 主入口 ──
ROLE="${LONGHUN_ROLE:-${1:-peer}}"

case "$ROLE" in
    gateway|server|master)
        start_gateway
        ;;
    peer|client|node)
        start_peer
        ;;
    daemon|background)
        start_daemon
        ;;
    discover)
        discover_gateway
        ;;
    info)
        echo "设备名称: ${LONGHUN_DEVICE_NAME:-$(hostname)}"
        echo "设备类型: $(detect_type)"
        echo "IP地址:   $(get_ip)"
        echo "架构:     $(uname -m)"
        echo "内核:     $(uname -r)"
        ;;
    help|--help|-h)
        echo "用法: docker run [选项] longhun/internal-net [角色]"
        echo ""
        echo "角色:"
        echo "  gateway   - 中心网关（鲲鹏服务器）"
        echo "  peer      - 普通节点（自动发现网关）"
        echo "  daemon    - 守护模式（后台静默运行）"
        echo "  discover  - 仅扫描发现网关"
        echo "  info      - 显示本机信息"
        echo ""
        echo "环境变量:"
        echo "  LONGHUN_ROLE         - 角色 (gateway|peer|daemon)"
        echo "  LONGHUN_GATEWAY      - 网关IP (默认auto自动发现)"
        echo "  LONGHUN_DEVICE_NAME  - 设备名称"
        echo "  LONGHUN_DEVICE_TYPE  - 设备类型 (默认auto)"
        echo "  LONGHUN_GATEWAY_PORT - 网关端口 (默认9622)"
        ;;
    *)
        echo "用法: docker run longhun/internal-net [gateway|peer|daemon|discover|info|help]"
        exit 1
        ;;
esac
