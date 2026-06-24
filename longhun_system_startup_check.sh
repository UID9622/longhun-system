#!/bin/bash
# 🐉 龍魂系统开机启动检查脚本
# ═══════════════════════════════════════════════════════════════
# DNA:#龍芯⚡️2026-06-07-LONGHUN-STARTUP-CHECK-v1.0
# 功能: 检查所有龍魂系统组件的启动状态
# 用法: bash longhun_system_startup_check.sh
# ═══════════════════════════════════════════════════════════════

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 统计变量
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# ═══════════════════════════════════════════════════════════════
# 日志函数
# ═══════════════════════════════════════════════════════════════

log_pass() {
    echo -e "${GREEN}✅${NC} $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_fail() {
    echo -e "${RED}❌${NC} $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_warn() {
    echo -e "${YELLOW}⚠️ ${NC} $1"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_info() {
    echo -e "${BLUE}ℹ️ ${NC} $1"
}

log_title() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "🐉 $1"
    echo "═══════════════════════════════════════════════════════════"
}

# ═══════════════════════════════════════════════════════════════
# 部分 1: 环境检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 1: 环境检查"

# 检查龍魂系统目录
if [ -d ~/longhun-system ]; then
    log_pass "龍魂系统目录存在: ~/longhun-system"
else
    log_fail "龍魂系统目录不存在: ~/longhun-system"
fi

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    log_pass "Python 已安装: $PYTHON_VERSION"
else
    log_fail "Python 3 未安装"
fi

# 检查 Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_pass "Node.js 已安装: $NODE_VERSION"
else
    log_warn "Node.js 未安装 (可选)"
fi

# 检查 Git
if command -v git &> /dev/null; then
    log_pass "Git 已安装"
else
    log_fail "Git 未安装"
fi

# 检查 curl
if command -v curl &> /dev/null; then
    log_pass "curl 已安装"
else
    log_fail "curl 未安装"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 2: 龍魂系统文件检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 2: 龍魂系统文件检查"

LONGHUN_DIR=~/longhun-system

# 检查关键文件
CRITICAL_FILES=(
    "brain/memories.db"
    "brain_notion_sync.py"
    "longhun_brain.py"
)

for file in "${CRITICAL_FILES[@]}"; do
    FILE_PATH="$LONGHUN_DIR/$file"
    if [ -f "$FILE_PATH" ]; then
        SIZE=$(du -h "$FILE_PATH" | cut -f1)
        log_pass "$file (大小: $SIZE)"
    else
        log_warn "$file 不存在 (可选)"
    fi
done

# 检查目录结构
CRITICAL_DIRS=(
    "brain"
    "mobile-monitoring"
    "wuxing-visual"
)

for dir in "${CRITICAL_DIRS[@]}"; do
    DIR_PATH="$LONGHUN_DIR/$dir"
    if [ -d "$DIR_PATH" ]; then
        log_pass "目录存在: $dir"
    else
        log_warn "目录不存在: $dir (可选)"
    fi
done

# ═══════════════════════════════════════════════════════════════
# 部分 3: brain_notion_sync.py 检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 3: brain_notion_sync.py 服务检查"

SYNC_FILE="$LONGHUN_DIR/brain_notion_sync.py"

if [ -f "$SYNC_FILE" ]; then
    log_pass "brain_notion_sync.py 存在"
    
    # 检查版本
    if grep -q "v1.1" "$SYNC_FILE" 2>/dev/null; then
        log_pass "brain_notion_sync 版本: v1.1 (Phase 1 升级版)"
    elif grep -q "v1.0" "$SYNC_FILE" 2>/dev/null; then
        log_warn "brain_notion_sync 版本: v1.0 (建议升级到 v1.1)"
    else
        log_warn "无法确定 brain_notion_sync 版本"
    fi
    
    # 检查 Python 语法
    if python3 -m py_compile "$SYNC_FILE" 2>/dev/null; then
        log_pass "brain_notion_sync.py 语法正确"
    else
        log_fail "brain_notion_sync.py 语法错误"
    fi
    
    # 检查关键函数
    if grep -q "retry_with_backoff" "$SYNC_FILE"; then
        log_pass "重试机制已实现"
    else
        log_warn "重试机制未实现"
    fi
    
    if grep -q "RateLimiter" "$SYNC_FILE"; then
        log_pass "限流控制器已实现"
    else
        log_warn "限流控制器未实现"
    fi
else
    log_fail "brain_notion_sync.py 不存在"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 4: 监控服务器检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 4: 监控服务器检查"

MONITORING_SERVER="$LONGHUN_DIR/mobile-monitoring/backend/python/monitoring_server.py"

if [ -f "$MONITORING_SERVER" ]; then
    log_pass "监控服务器文件存在"
    
    # 检查是否运行
    if curl -s http://localhost:9000/api/v1/monitor/health > /dev/null 2>&1; then
        log_pass "监控服务器正在运行 (localhost:9000)"
        
        # 获取服务状态
        HEALTH=$(curl -s http://localhost:9000/api/v1/monitor/health 2>/dev/null || echo "")
        if echo "$HEALTH" | grep -q "healthy"; then
            log_pass "监控服务器健康状态: 正常"
        fi
    else
        log_warn "监控服务器未运行 (localhost:9000)"
        log_info "启动方式: python3 $MONITORING_SERVER"
    fi
else
    log_warn "监控服务器文件不存在 (可选)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 5: 数据库检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 5: 数据库检查"

DB_FILE="$LONGHUN_DIR/brain/memories.db"

if [ -f "$DB_FILE" ]; then
    SIZE=$(du -h "$DB_FILE" | cut -f1)
    log_pass "memories.db 存在 (大小: $SIZE)"
    
    # 检查数据库完整性
    if sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM sqlite_master;" > /dev/null 2>&1; then
        RECORD_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM memories;" 2>/dev/null || echo "0")
        log_pass "memories.db 完整性: 正常 (记忆数: $RECORD_COUNT)"
    else
        log_fail "memories.db 可能损坏"
    fi
    
    # 检查 notion_map 表
    if sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM notion_map;" > /dev/null 2>&1; then
        MAP_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM notion_map;" 2>/dev/null || echo "0")
        log_pass "notion_map 表存在 (记录数: $MAP_COUNT)"
    else
        log_info "notion_map 表不存在 (首次运行时创建)"
    fi
else
    log_warn "memories.db 不存在 (首次运行时创建)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 6: 环境变量检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 6: 环境变量检查"

if [ -n "$NOTION_TOKEN" ]; then
    TOKEN_PREVIEW="${NOTION_TOKEN:0:10}...${NOTION_TOKEN: -5}"
    log_pass "NOTION_TOKEN 已配置: $TOKEN_PREVIEW"
else
    log_warn "NOTION_TOKEN 未配置 (可选，但需要才能同步到 Notion)"
fi

# 优先检查主权变量 DB_LU，兼容旧名 NOTION_BRAIN_DB
DB_LU_VALUE="${DB_LU:-$NOTION_BRAIN_DB}"
if [ -n "$DB_LU_VALUE" ]; then
    log_pass "DB_LU 已配置: ${DB_LU_VALUE:0:8}...${DB_LU_VALUE: -8}"
else
    log_warn "DB_LU 未配置 (可选，但需要才能同步到 Notion)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 7: 进程检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 7: 进程检查"

# 检查 brain_notion_sync 是否运行
if pgrep -f "brain_notion_sync.py --watch" > /dev/null; then
    PID=$(pgrep -f "brain_notion_sync.py --watch")
    log_pass "brain_notion_sync 正在运行 (PID: $PID)"
else
    log_warn "brain_notion_sync 未运行 (持续监听模式)"
    log_info "启动方式: python3 $SYNC_FILE --watch"
fi

# 检查 monitoring_server 是否运行
if pgrep -f "monitoring_server.py" > /dev/null; then
    PID=$(pgrep -f "monitoring_server.py")
    log_pass "monitoring_server 正在运行 (PID: $PID)"
else
    log_warn "monitoring_server 未运行"
    log_info "启动方式: python3 $MONITORING_SERVER"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 8: 磁盘空间检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 8: 磁盘空间检查"

DISK_USAGE=$(df -h ~ | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAILABLE=$(df -h ~ | awk 'NR==2 {print $4}')

if [ "$DISK_USAGE" -lt 80 ]; then
    log_pass "磁盘空间充足 (使用率: $DISK_USAGE%, 可用: $DISK_AVAILABLE)"
elif [ "$DISK_USAGE" -lt 90 ]; then
    log_warn "磁盘空间即将不足 (使用率: $DISK_USAGE%, 可用: $DISK_AVAILABLE)"
else
    log_fail "磁盘空间不足 (使用率: $DISK_USAGE%, 可用: $DISK_AVAILABLE)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 9: 网络连接检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 9: 网络连接检查"

# 检查互联网
if timeout 2 curl -s https://www.google.com > /dev/null 2>&1; then
    log_pass "互联网连接: 正常"
else
    log_warn "互联网连接: 不稳定或无法连接"
fi

# 检查 Notion API
if timeout 2 curl -s https://api.notion.com -H "Authorization: Bearer test" > /dev/null 2>&1; then
    log_pass "Notion API 可达: 正常"
else
    log_warn "Notion API 不可达或响应超时"
fi

# 检查本地 localhost
if timeout 1 curl -s http://localhost:9000 > /dev/null 2>&1; then
    log_pass "localhost:9000 可达: 正常"
else
    log_warn "localhost:9000 不可达"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 10: 日志检查
# ═══════════════════════════════════════════════════════════════

log_title "Part 10: 日志文件检查"

# 检查升级日志
if [ -f "$LONGHUN_DIR/BRAIN_NOTION_SYNC_UPGRADE_LOG.txt" ]; then
    log_pass "升级日志存在"
    LAST_UPGRADE=$(tail -1 "$LONGHUN_DIR/BRAIN_NOTION_SYNC_UPGRADE_LOG.txt" | head -1)
    log_info "最后升级: $LAST_UPGRADE"
else
    log_info "升级日志不存在 (首次安装)"
fi

# 检查 brain_notion_sync 日志
if [ -f "$LONGHUN_DIR/brain_notion_sync.log" ]; then
    SIZE=$(du -h "$LONGHUN_DIR/brain_notion_sync.log" | cut -f1)
    log_pass "brain_notion_sync 日志存在 (大小: $SIZE)"
else
    log_info "brain_notion_sync 日志不存在 (首次运行时创建)"
fi

# ═══════════════════════════════════════════════════════════════
# 最后统计和建议
# ═══════════════════════════════════════════════════════════════

log_title "最终检查报告"

echo ""
echo "📊 检查统计:"
echo "   总检查项目: $TOTAL_CHECKS"
echo -e "   ${GREEN}通过: $PASSED_CHECKS${NC}"
echo -e "   ${YELLOW}警告: $WARNING_CHECKS${NC}"
echo -e "   ${RED}失败: $FAILED_CHECKS${NC}"
echo ""

PASS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "🎯 通过率: ${PASS_RATE}%"
echo ""

# 生成建议
if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✨ 系统状态: 完美 (所有关键检查通过)${NC}"
elif [ $FAILED_CHECKS -le 2 ]; then
    echo -e "${YELLOW}⚠️  系统状态: 需要注意 (有 $FAILED_CHECKS 个失败项)${NC}"
else
    echo -e "${RED}❌ 系统状态: 需要修复 (有 $FAILED_CHECKS 个失败项)${NC}"
fi

echo ""

# 启动建议
log_title "🚀 启动建议"

if ! pgrep -f "brain_notion_sync.py --watch" > /dev/null; then
    echo ""
    echo "📌 启动 brain_notion_sync (持续监听模式):"
    echo "   cd ~/longhun-system"
    echo "   nohup python3 brain_notion_sync.py --watch > brain_notion_sync.log 2>&1 &"
    echo ""
fi

if ! curl -s http://localhost:9000/api/v1/monitor/health > /dev/null 2>&1; then
    echo "📌 启动监控服务器:"
    echo "   cd ~/longhun-system/mobile-monitoring/backend/python"
    echo "   python3 monitoring_server.py"
    echo ""
fi

# ═══════════════════════════════════════════════════════════════
# 生成检查日志
# ═══════════════════════════════════════════════════════════════

LOGFILE="$LONGHUN_DIR/LONGHUN_STARTUP_CHECK_$(date +%Y%m%d_%H%M%S).log"

cat > "$LOGFILE" << EOF
🐉 龍魂系统启动检查报告
生成时间: $(date '+%Y-%m-%d %H:%M:%S')
DNS:#龍芯⚡️2026-06-07-LONGHUN-STARTUP-CHECK-v1.0

检查统计:
  总项目: $TOTAL_CHECKS
  通过: $PASSED_CHECKS
  警告: $WARNING_CHECKS
  失败: $FAILED_CHECKS
  通过率: ${PASS_RATE}%

检查日期: $(date '+%A, %B %d, %Y')
检查者: 自动检查脚本
EOF

echo ""
log_pass "检查日志已保存: $LOGFILE"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🐉 龍魂系统启动检查完成"
echo "════════════════════════════════════════════════════════════"
echo "DNA:#龍芯⚡️2026-06-07-LONGHUN-STARTUP-CHECK-v1.0"
echo "天下无欺。"
echo ""
