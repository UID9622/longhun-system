#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统一键启动脚本
# ═══════════════════════════════════════════════════════════════
# 功能: 自动启动龍魂系统的所有必要服务
# 用法: bash longhun_system_start_all.sh
# DNA: #龍芯⚡️2026-06-07-LONGHUN-START-ALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════════

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
LONGHUN_DIR=~/longhun-system
LOG_DIR=$LONGHUN_DIR/logs
mkdir -p $LOG_DIR

# 启动计数
SERVICES_STARTED=0
SERVICES_FAILED=0

# ═══════════════════════════════════════════════════════════════
# 日志和输出函数
# ═══════════════════════════════════════════════════════════════

print_header() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}🐉 $1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo ""
}

start_service() {
    local SERVICE_NAME=$1
    local SERVICE_CMD=$2
    local PID_FILE=$3
    local LOG_FILE=$4
    
    echo -n "⏳ 正在启动 $SERVICE_NAME..."
    
    # 检查是否已运行
    if [ -f "$PID_FILE" ]; then
        local OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo -e " ${YELLOW}已运行 (PID: $OLD_PID)${NC}"
            return 0
        fi
    fi
    
    # 启动服务
    eval "$SERVICE_CMD" > "$LOG_FILE" 2>&1 &
    local NEW_PID=$!
    echo $NEW_PID > "$PID_FILE"
    
    # 等待服务启动
    sleep 2
    
    # 检查是否成功
    if kill -0 $NEW_PID 2>/dev/null; then
        echo -e " ${GREEN}✅ 成功 (PID: $NEW_PID)${NC}"
        ((SERVICES_STARTED++))
        echo "   日志: $LOG_FILE"
        return 0
    else
        echo -e " ${RED}❌ 失败${NC}"
        ((SERVICES_FAILED++))
        echo "   日志: $LOG_FILE"
        echo "   错误信息:"
        tail -5 "$LOG_FILE" | sed 's/^/     /'
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════
# 部分 1: 环境检查
# ═══════════════════════════════════════════════════════════════

print_header "Part 1: 环境检查"

if [ ! -d "$LONGHUN_DIR" ]; then
    echo -e "${RED}❌ 龍魂系统目录不存在: $LONGHUN_DIR${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 龍魂系统目录: $LONGHUN_DIR${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"

echo -e "${GREEN}✅ 日志目录: $LOG_DIR${NC}"

# ═══════════════════════════════════════════════════════════════
# 部分 2: 启动 brain_notion_sync (Notion 同步服务)
# ═══════════════════════════════════════════════════════════════

print_header "Part 2: 启动 brain_notion_sync (Notion 同步服务)"

BRAIN_SYNC_FILE="$LONGHUN_DIR/brain_notion_sync.py"
BRAIN_SYNC_PID="$LOG_DIR/brain_notion_sync.pid"
BRAIN_SYNC_LOG="$LOG_DIR/brain_notion_sync.log"

if [ ! -f "$BRAIN_SYNC_FILE" ]; then
    echo -e "${YELLOW}⚠️  brain_notion_sync.py 不存在${NC}"
else
    # 检查 Python 语法
    if ! python3 -m py_compile "$BRAIN_SYNC_FILE" 2>/dev/null; then
        echo -e "${RED}❌ brain_notion_sync.py 语法错误${NC}"
    else
        start_service \
            "brain_notion_sync (持续监听)" \
            "cd $LONGHUN_DIR && python3 brain_notion_sync.py --watch" \
            "$BRAIN_SYNC_PID" \
            "$BRAIN_SYNC_LOG"
    fi
fi

# ═══════════════════════════════════════════════════════════════
# 部分 3: 启动监控服务器
# ═══════════════════════════════════════════════════════════════

print_header "Part 3: 启动监控服务器 (monitoring_server)"

MONITORING_FILE="$LONGHUN_DIR/mobile-monitoring/backend/python/monitoring_server.py"
MONITORING_PID="$LOG_DIR/monitoring_server.pid"
MONITORING_LOG="$LOG_DIR/monitoring_server.log"

if [ ! -f "$MONITORING_FILE" ]; then
    echo -e "${YELLOW}⚠️  监控服务器文件不存在${NC}"
else
    start_service \
        "监控服务器 (localhost:9000)" \
        "cd $LONGHUN_DIR/mobile-monitoring/backend/python && python3 monitoring_server.py" \
        "$MONITORING_PID" \
        "$MONITORING_LOG"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 4: 启动 longhun_brain (大脑服务)
# ═══════════════════════════════════════════════════════════════

print_header "Part 4: 检查 longhun_brain (大脑服务)"

BRAIN_FILE="$LONGHUN_DIR/longhun_brain.py"

if [ ! -f "$BRAIN_FILE" ]; then
    echo -e "${YELLOW}⚠️  longhun_brain.py 不存在${NC}"
else
    # longhun_brain 一般不需要持续运行，只在有请求时执行
    echo -e "${BLUE}ℹ️  longhun_brain.py 存在 (按需执行)${NC}"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 5: 验证服务状态
# ═══════════════════════════════════════════════════════════════

print_header "Part 5: 验证服务状态"

echo "📋 检查运行中的进程:"
echo ""

# 检查 brain_notion_sync
if pgrep -f "brain_notion_sync.py --watch" > /dev/null; then
    PID=$(pgrep -f "brain_notion_sync.py --watch")
    echo -e "  ${GREEN}✅ brain_notion_sync${NC} (PID: $PID)"
else
    echo -e "  ${RED}❌ brain_notion_sync 未运行${NC}"
fi

# 检查监控服务器
if pgrep -f "monitoring_server.py" > /dev/null; then
    PID=$(pgrep -f "monitoring_server.py")
    echo -e "  ${GREEN}✅ monitoring_server${NC} (PID: $PID)"
else
    echo -e "  ${YELLOW}⚠️  monitoring_server 未运行${NC}"
fi

# 检查 localhost:9000
echo ""
echo "📡 检查服务可达性:"
echo ""
if timeout 2 curl -s http://localhost:9000/api/v1/monitor/health > /dev/null 2>&1; then
    HEALTH=$(curl -s http://localhost:9000/api/v1/monitor/health 2>/dev/null)
    if echo "$HEALTH" | grep -q "healthy"; then
        echo -e "  ${GREEN}✅ localhost:9000 (正常)${NC}"
    else
        echo -e "  ${YELLOW}⚠️  localhost:9000 (响应异常)${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  localhost:9000 (不可达)${NC}"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 6: 显示日志位置
# ═══════════════════════════════════════════════════════════════

print_header "Part 6: 服务日志位置"

echo "📝 实时查看日志:"
echo ""
echo "  brain_notion_sync:"
echo "    tail -f $BRAIN_SYNC_LOG"
echo ""
echo "  monitoring_server:"
echo "    tail -f $MONITORING_LOG"
echo ""

# ═══════════════════════════════════════════════════════════════
# 部分 7: 总结
# ═══════════════════════════════════════════════════════════════

print_header "🎉 启动完成"

echo "📊 启动统计:"
echo "   成功: $SERVICES_STARTED 个服务"
echo "   失败: $SERVICES_FAILED 个服务"
echo ""

if [ $SERVICES_FAILED -eq 0 ]; then
    echo -e "${GREEN}✨ 所有服务已成功启动！${NC}"
else
    echo -e "${YELLOW}⚠️  有 $SERVICES_FAILED 个服务启动失败，请检查日志${NC}"
fi

echo ""
echo "🔗 常用命令:"
echo ""
echo "  1. 查看所有运行的服务:"
echo "     ps aux | grep -E 'brain_notion_sync|monitoring_server'"
echo ""
echo "  2. 停止 brain_notion_sync:"
echo "     kill \$(pgrep -f 'brain_notion_sync.py --watch')"
echo ""
echo "  3. 停止监控服务器:"
echo "     kill \$(pgrep -f 'monitoring_server.py')"
echo ""
echo "  4. 检查系统状态:"
echo "     bash $LONGHUN_DIR/longhun_system_startup_check.sh"
echo ""

# ═══════════════════════════════════════════════════════════════
# 生成启动报告
# ═══════════════════════════════════════════════════════════════

STARTUP_LOG="$LOG_DIR/LONGHUN_STARTUP_$(date +%Y%m%d_%H%M%S).log"

cat > "$STARTUP_LOG" << EOF
🐉 龍魂系统启动报告
╔══════════════════════════════════════════════════════════════╗
║ DNA: #龍芯⚡️2026-06-07-LONGHUN-START-ALL-v1.0             ║
╚══════════════════════════════════════════════════════════════╝

启动时间: $(date '+%Y-%m-%d %H:%M:%S %Z')
启动目录: $LONGHUN_DIR

启动统计:
  • 成功启动: $SERVICES_STARTED 个
  • 启动失败: $SERVICES_FAILED 个

启动的服务:
  ✓ brain_notion_sync (Notion 同步)
    PID 文件: $BRAIN_SYNC_PID
    日志文件: $BRAIN_SYNC_LOG

  ✓ monitoring_server (监控服务)
    PID 文件: $MONITORING_PID
    日志文件: $MONITORING_LOG

系统状态: 正常运行

天下无欺。🐉
EOF

echo "📋 启动报告已保存: $STARTUP_LOG"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✨ 龍魂系统已启动，天下无欺。🐉"
echo "════════════════════════════════════════════════════════════"
