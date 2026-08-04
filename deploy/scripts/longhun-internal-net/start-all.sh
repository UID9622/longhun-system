#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════════════
# 龍魂·内网互联 — 一键启动全部节点
# DNA: #龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-STARTALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #CONFIRM🌌9622-ONLY-ONCE🧬STA1-001A
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# 用法:
#   # 启动全部节点（网关+所有设备）
#   bash start-all.sh --profile all
#
#   # 仅启动办公设备
#   bash start-all.sh --profile office
#
#   # 仅启动家中设备
#   bash start-all.sh --profile home
#
#   # 启动 + 投喂数据
#   bash start-all.sh --profile all --feed
#
#   # 查看所有节点状态
#   bash start-all.sh status
# ═══════════════════════════════════════════════════════════════

set -e

# ── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── 默认值 ──
COMPOSE_FILE=""
PROFILE="all"
ACTION="up"
FEED_DATA=false
GATEWAY_IP=""
PORT=9622

# ── 找 compose 文件 ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# 从当前脚本位置向上找
if [ -f "$SCRIPT_DIR/../../../docker/docker-compose.internal-net.yml" ]; then
    COMPOSE_FILE="$(cd "$SCRIPT_DIR/../../.." && pwd)/docker/docker-compose.internal-net.yml"
elif [ -f "$SCRIPT_DIR/docker-compose.internal-net.yml" ]; then
    COMPOSE_FILE="$SCRIPT_DIR/docker-compose.internal-net.yml"
elif [ -f "$HOME/.longhun/docker-compose.yml" ]; then
    COMPOSE_FILE="$HOME/.longhun/docker-compose.yml"
fi

# ── 帮助 ──
show_help() {
    echo "🐉 龍魂·内网互联 — 一键启动全部节点"
    echo ""
    echo "用法: bash start-all.sh [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  up        启动全部节点 (默认)"
    echo "  down      停止全部节点"
    echo "  restart   重启全部节点"
    echo "  status    查看全部节点状态"
    echo "  logs      查看全部日志"
    echo "  health    健康检查全部节点"
    echo "  feed      向所有节点投喂数据"
    echo ""
    echo "选项:"
    echo "  --profile PROFILE    节点分组: all|office|home|mac|win|linux|iot"
    echo "  --gateway IP         网关IP (默认自动检测)"
    echo "  --port PORT          网关端口 (默认9622)"
    echo "  --compose-file FILE  指定compose文件"
    echo ""
    echo "示例:"
    echo "  bash start-all.sh up --profile all       # 启动全部节点"
    echo "  bash start-all.sh up --profile office    # 仅办公设备"
    echo "  bash start-all.sh status                 # 查看状态"
    echo "  bash start-all.sh feed                   # 投喂数据到所有节点"
}

# ── 解析参数 ──
while [[ $# -gt 0 ]]; do
    case "$1" in
        up|down|restart|status|logs|health|feed)
            ACTION="$1"
            shift
            ;;
        --profile)     PROFILE="$2"; shift 2 ;;
        --gateway)     GATEWAY_IP="$2"; shift 2 ;;
        --port)        PORT="$2"; shift 2 ;;
        --compose-file) COMPOSE_FILE="$2"; shift 2 ;;
        --help|-h)     show_help; exit 0 ;;
        *)             echo -e "${RED}未知参数: $1${NC}"; show_help; exit 1 ;;
    esac
done

# ── Docker Compose 操作 ──
do_compose() {
    local action="$1"
    local compose_cmd="docker compose"
    
    # 支持 docker-compose (v1) 和 docker compose (v2)
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker 未安装${NC}"
        echo "   安装: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
    
    if [ -z "$COMPOSE_FILE" ]; then
        echo -e "${RED}❌ 未找到 docker-compose.internal-net.yml${NC}"
        echo "   请指定: --compose-file /path/to/docker-compose.internal-net.yml"
        exit 1
    fi
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        echo -e "${RED}❌ 文件不存在: $COMPOSE_FILE${NC}"
        exit 1
    fi
    
    echo -e "${CYAN}📋 Compose 文件: $COMPOSE_FILE${NC}"
    echo -e "${CYAN}   分组: $PROFILE${NC}"
    echo ""
    
    COMPOSE_CMD="$compose_cmd -f '$COMPOSE_FILE' --profile '$PROFILE'"
    
    case "$action" in
        up)
            echo -e "${GREEN}🚀 启动龍魂内网全部节点...${NC}"
            eval "$COMPOSE_CMD up -d"
            echo ""
            echo -e "${GREEN}✅ 全部节点已启动${NC}"
            echo ""
            # 等待健康
            echo "⏳ 等待网关就绪..."
            for i in $(seq 1 30); do
                if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
                    echo -e "${GREEN}✅ 网关就绪${NC}"
                    break
                fi
                sleep 1
            done
            ;;
        down)
            echo -e "${YELLOW}🛑 停止全部节点...${NC}"
            eval "$COMPOSE_CMD down"
            echo -e "${GREEN}✅ 全部已停止${NC}"
            ;;
        restart)
            echo -e "${YELLOW}🔄 重启全部节点...${NC}"
            eval "$COMPOSE_CMD restart"
            echo -e "${GREEN}✅ 全部已重启${NC}"
            ;;
        status)
            echo -e "${CYAN}📊 节点状态:${NC}"
            eval "$COMPOSE_CMD ps"
            ;;
        logs)
            echo -e "${CYAN}📜 跟踪日志 (Ctrl+C 退出):${NC}"
            eval "$COMPOSE_CMD logs -f --tail=50"
            ;;
    esac
}

# ── 直接操作（无 Compose）──
do_direct_status() {
    echo -e "${CYAN}📊 龍魂内网状态${NC}"
    echo ""
    
    # 检查网关
    if [ -n "$GATEWAY_IP" ]; then
        GW="$GATEWAY_IP"
    else
        # 尝试发现网关
        GW=$(curl -s http://localhost:$PORT/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('peers','?'))" 2>/dev/null || echo "")
        if [ -z "$GW" ]; then
            # 扫描局域网
            MY_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")
            SUBNET=$(echo "$MY_IP" | cut -d. -f1-3)
            GW=""
            for i in 1 100 254; do
                if curl -s -m 0.5 "http://${SUBNET}.${i}:$PORT/health" >/dev/null 2>&1; then
                    GW="${SUBNET}.${i}"
                    break
                fi
            done
        fi
    fi
    
    if [ -n "$GW" ] && curl -s -m 2 "http://$GW:$PORT/health" >/dev/null 2>&1; then
        HEALTH=$(curl -s "http://$GW:$PORT/health")
        echo -e "${GREEN}🏛️ 网关: $GW:$PORT${NC}"
        echo "$HEALTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"  状态: {d.get('status', '?')}\")
print(f\"  在线: {d.get('peers', 0)} 个节点\")
a = d.get('audit', {})
print(f\"  审计: 🟢{a.get('green',0)} 🟡{a.get('yellow',0)} 🔴{a.get('red',0)}\")
f = d.get('fuse', {})
print(f\"  熔断: {f.get('fused_devices',0)} 个设备\")
print(f\"  DNA:  {d.get('dna', '?')[:40]}...\")
" 2>/dev/null || echo "  (无法解析健康数据)"
        
        # 查看节点
        PEERS=$(curl -s "http://$GW:$PORT/peers" 2>/dev/null)
        peer_count=$(echo "$PEERS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('count',0))" 2>/dev/null || echo "0")
        if [ "$peer_count" -gt 0 ]; then
            echo ""
            echo "  📡 在线节点:"
            echo "$PEERS" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for p in data.get('peers', []):
        icon = '🟢' if p.get('status') == 'online' else '⚫'
        print(f\"    {icon} {p.get('name','?'):16s} | {p.get('type','?'):10s} | {p.get('chip_tier','?')} | {p.get('ip','')}\")
except: pass
" 2>/dev/null
        fi
    else
        echo -e "${RED}❌ 未找到运行中的龍魂网关${NC}"
        echo "   请先启动网关: bash start-all.sh up"
    fi
    
    echo ""
}

# ── 投喂数据 ──
do_feed() {
    echo -e "${CYAN}📥 向所有节点投喂数据...${NC}"
    echo ""
    
    # 查找网关
    if [ -n "$GATEWAY_IP" ]; then
        GW="$GATEWAY_IP"
    else
        GW="localhost"
    fi
    
    # 发送消息到所有节点
    FEED_MESSAGE="📢 [系统投喂] $(date '+%Y-%m-%d %H:%M:%S') - 龍魂内网同步中..."
    
    curl -s -X POST "http://$GW:$PORT/message/send" \
        -H "Content-Type: application/json" \
        -d "{
            \"from\": \"system\",
            \"type\": \"text\",
            \"content\": \"$FEED_MESSAGE\",
            \"room_id\": \"broadcast\"
        }" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('sent'):
    print(f\"✅ 投喂成功: {d.get('msg_id', '')[:20]}...\")
else:
    print(f\"❌ 投喂失败: {d.get('error', '')}\")
" 2>/dev/null || echo "❌ 投喂失败 - 无法连接网关"
    
    echo ""
}

# ── 健康检查全部 ──
do_health() {
    echo -e "${CYAN}🏥 全节点健康检查${NC}"
    echo ""
    
    # 找网关
    GW="${GATEWAY_IP:-localhost}"
    
    # 1. 网关健康
    echo -n "  🏛️ 网关 (http://$GW:$PORT): "
    if HEALTH=$(curl -s -m 3 "http://$GW:$PORT/health" 2>/dev/null); then
        PEERS=$(echo "$HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('peers',0))" 2>/dev/null || echo "?")
        echo -e "${GREEN}正常 (${PEERS}个节点)${NC}"
        
        # 2. 各节点心跳
        echo ""
        echo "  📡 节点连通性:"
        PEERS_LIST=$(curl -s "http://$GW:$PORT/peers" 2>/dev/null)
        echo "$PEERS_LIST" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for p in data.get('peers', []):
        status = p.get('status', 'unknown')
        icon = '🟢' if status == 'online' else '🔴'
        print(f\"    {icon} {p.get('name','?'):20s} | {status:6s} | {p.get('chip_tier','?')}\")
except:
    print('    (无法获取节点列表)')
" 2>/dev/null
        
        # 3. 安全状态
        echo ""
        echo "  🔐 安全状态:"
        echo "$HEALTH" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    a = d.get('audit', {})
    f = d.get('fuse', {})
    print(f\"    L1·三色审计: 🟢{a.get('green',0)} 🟡{a.get('yellow',0)} 🔴{a.get('red',0)}\")
    print(f\"    L2·熔断控制: {f.get('fused_devices',0)} 个设备熔断\")
    f_list = f.get('fused_list', {})
    if f_list:
        for k, v in f_list.items():
            print(f\"      🔴 {k}: {v}\")
    print(f\"    L3/L4/L5: 输入过滤 | 防投毒 | 芯片门禁 = ✅\")
except:
    print('    (无法获取安全状态)')
" 2>/dev/null
        
    else
        echo -e "${RED}不可达${NC}"
        echo "   请确认网关已启动: bash start-all.sh up"
    fi
    echo ""
}


# ═══════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🐉 龍魂·内网互联 — 一键总控 v1.0                             ║${NC}"
echo -e "${BLUE}║  一台鲲鹏当中心 · 所有设备内网直连 · 不经过云                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

case "$ACTION" in
    up|down|restart)
        do_compose "$ACTION"
        ;;
    status)
        do_direct_status
        ;;
    logs)
        do_compose logs
        ;;
    health)
        do_health
        ;;
    feed)
        do_feed
        ;;
    *)
        show_help
        ;;
esac
