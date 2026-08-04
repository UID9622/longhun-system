#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系統開機啟動檢查腳本
# ═══════════════════════════════════════════════════════════════
# DNA:#龍芯⚡️2026-06-07-LONGHUN-STARTUP-CHECK-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 功能: 檢查所有龍魂系統組件的啟動狀態
# 用法: bash longhun_system_startup_check.sh
# ═══════════════════════════════════════════════════════════════

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 統計變量
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# ═══════════════════════════════════════════════════════════════
# 日誌函數
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
# 部分 1: 環境檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 1: 環境檢查"

# 檢查龍魂系統目錄
if [ -d ~/longhun-system ]; then
    log_pass "龍魂系統目錄存在: ~/longhun-system"
else
    log_fail "龍魂系統目錄不存在: ~/longhun-system"
fi

# 檢查 Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    log_pass "Python 已安裝: $PYTHON_VERSION"
else
    log_fail "Python 3 未安裝"
fi

# 檢查 Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_pass "Node.js 已安裝: $NODE_VERSION"
else
    log_warn "Node.js 未安裝 (可選)"
fi

# 檢查 Git
if command -v git &> /dev/null; then
    log_pass "Git 已安裝"
else
    log_fail "Git 未安裝"
fi

# 檢查 curl
if command -v curl &> /dev/null; then
    log_pass "curl 已安裝"
else
    log_fail "curl 未安裝"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 2: 龍魂系統文件檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 2: 龍魂系統文件檢查"

LONGHUN_DIR=~/longhun-system

# 檢查關鍵文件
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
        log_warn "$file 不存在 (可選)"
    fi
done

# 檢查目錄結構
CRITICAL_DIRS=(
    "brain"
    "mobile-monitoring"
    "wuxing-visual"
)

for dir in "${CRITICAL_DIRS[@]}"; do
    DIR_PATH="$LONGHUN_DIR/$dir"
    if [ -d "$DIR_PATH" ]; then
        log_pass "目錄存在: $dir"
    else
        log_warn "目錄不存在: $dir (可選)"
    fi
done

# ═══════════════════════════════════════════════════════════════
# 部分 3: brain_notion_sync.py 檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 3: brain_notion_sync.py 服務檢查"

SYNC_FILE="$LONGHUN_DIR/brain_notion_sync.py"

if [ -f "$SYNC_FILE" ]; then
    log_pass "brain_notion_sync.py 存在"
    
    # 檢查版本
    if grep -q "v1.1" "$SYNC_FILE" 2>/dev/null; then
        log_pass "brain_notion_sync 版本: v1.1 (Phase 1 升級版)"
    elif grep -q "v1.0" "$SYNC_FILE" 2>/dev/null; then
        log_warn "brain_notion_sync 版本: v1.0 (建議升級到 v1.1)"
    else
        log_warn "無法確定 brain_notion_sync 版本"
    fi
    
    # 檢查 Python 語法
    if python3 -m py_compile "$SYNC_FILE" 2>/dev/null; then
        log_pass "brain_notion_sync.py 語法正確"
    else
        log_fail "brain_notion_sync.py 語法錯誤"
    fi
    
    # 檢查關鍵函數
    if grep -q "retry_with_backoff" "$SYNC_FILE"; then
        log_pass "重試機制已實現"
    else
        log_warn "重試機制未實現"
    fi
    
    if grep -q "RateLimiter" "$SYNC_FILE"; then
        log_pass "限流控制器已實現"
    else
        log_warn "限流控制器未實現"
    fi
else
    log_fail "brain_notion_sync.py 不存在"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 4: 監控服務器檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 4: 監控服務器檢查"

MONITORING_SERVER="$LONGHUN_DIR/mobile-monitoring/backend/python/monitoring_server.py"

if [ -f "$MONITORING_SERVER" ]; then
    log_pass "監控服務器文件存在"
    
    # 檢查是否運行
    if curl -s http://localhost:9000/api/v1/monitor/health > /dev/null 2>&1; then
        log_pass "監控服務器正在運行 (localhost:9000)"
        
        # 獲取服務狀態
        HEALTH=$(curl -s http://localhost:9000/api/v1/monitor/health 2>/dev/null || echo "")
        if echo "$HEALTH" | grep -q "healthy"; then
            log_pass "監控服務器健康狀態: 正常"
        fi
    else
        log_warn "監控服務器未運行 (localhost:9000)"
        log_info "啟動方式: python3 $MONITORING_SERVER"
    fi
else
    log_warn "監控服務器文件不存在 (可選)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 5: 數據庫檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 5: 數據庫檢查"

DB_FILE="$LONGHUN_DIR/brain/memories.db"

if [ -f "$DB_FILE" ]; then
    SIZE=$(du -h "$DB_FILE" | cut -f1)
    log_pass "memories.db 存在 (大小: $SIZE)"
    
    # 檢查數據庫完整性
    if sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM sqlite_master;" > /dev/null 2>&1; then
        RECORD_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM memories;" 2>/dev/null || echo "0")
        log_pass "memories.db 完整性: 正常 (記憶數: $RECORD_COUNT)"
    else
        log_fail "memories.db 可能損壞"
    fi
    
    # 檢查 notion_map 表
    if sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM notion_map;" > /dev/null 2>&1; then
        MAP_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM notion_map;" 2>/dev/null || echo "0")
        log_pass "notion_map 表存在 (記錄數: $MAP_COUNT)"
    else
        log_info "notion_map 表不存在 (首次運行時創建)"
    fi
else
    log_warn "memories.db 不存在 (首次運行時創建)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 6: 環境變量檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 6: 環境變量檢查"

if [ -n "$NOTION_TOKEN" ]; then
    TOKEN_PREVIEW="${NOTION_TOKEN:0:10}...${NOTION_TOKEN: -5}"
    log_pass "NOTION_TOKEN 已配置: $TOKEN_PREVIEW"
else
    log_warn "NOTION_TOKEN 未配置 (可選，但需要才能同步到 Notion)"
fi

# 优先检查主权变量 DB_LU，兼容旧名 NOTION_BRAIN_DB
DB_LU_VALUE="${DB_LU:-$NOTION_BRAIN_DB}"
if [ -n "$DB_LU_VALUE" ]; then
    log_pass "DB_LU 已配置: ${DB_LU_VALUE:0:8}...${DB_LU_VALUE: -8}"
else
    log_warn "DB_LU 未配置 (可選，但需要才能同步到 Notion)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 7: 進程檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 7: 進程檢查"

# 檢查 brain_notion_sync 是否運行
if pgrep -f "brain_notion_sync.py --watch" > /dev/null; then
    PID=$(pgrep -f "brain_notion_sync.py --watch")
    log_pass "brain_notion_sync 正在運行 (PID: $PID)"
else
    log_warn "brain_notion_sync 未運行 (持續監聽模式)"
    log_info "啟動方式: python3 $SYNC_FILE --watch"
fi

# 檢查 monitoring_server 是否運行
if pgrep -f "monitoring_server.py" > /dev/null; then
    PID=$(pgrep -f "monitoring_server.py")
    log_pass "monitoring_server 正在運行 (PID: $PID)"
else
    log_warn "monitoring_server 未運行"
    log_info "啟動方式: python3 $MONITORING_SERVER"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 8: 磁盤空間檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 8: 磁盤空間檢查"

DISK_USAGE=$(df -h ~ | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAILABLE=$(df -h ~ | awk 'NR==2 {print $4}')

if [ "$DISK_USAGE" -lt 80 ]; then
    log_pass "磁盤空間充足 (使用率: $DISK_USAGE%, 可用: $DISK_AVAILABLE)"
elif [ "$DISK_USAGE" -lt 90 ]; then
    log_warn "磁盤空間即將不足 (使用率: $DISK_USAGE%, 可用: $DISK_AVAILABLE)"
else
    log_fail "磁盤空間不足 (使用率: $DISK_USAGE%, 可用: $DISK_AVAILABLE)"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 9: 網絡連接檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 9: 網絡連接檢查"

# 檢查互聯網
if timeout 2 curl -s https://www.google.com > /dev/null 2>&1; then
    log_pass "互聯網連接: 正常"
else
    log_warn "互聯網連接: 不穩定或無法連接"
fi

# 檢查 Notion API
if timeout 2 curl -s https://api.notion.com -H "Authorization: Bearer test" > /dev/null 2>&1; then
    log_pass "Notion API 可達: 正常"
else
    log_warn "Notion API 不可達或響應超時"
fi

# 檢查本地 localhost
if timeout 1 curl -s http://localhost:9000 > /dev/null 2>&1; then
    log_pass "localhost:9000 可達: 正常"
else
    log_warn "localhost:9000 不可達"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 10: 日誌檢查
# ═══════════════════════════════════════════════════════════════

log_title "Part 10: 日誌文件檢查"

# 檢查升級日誌
if [ -f "$LONGHUN_DIR/BRAIN_NOTION_SYNC_UPGRADE_LOG.txt" ]; then
    log_pass "升級日誌存在"
    LAST_UPGRADE=$(tail -1 "$LONGHUN_DIR/BRAIN_NOTION_SYNC_UPGRADE_LOG.txt" | head -1)
    log_info "最後升級: $LAST_UPGRADE"
else
    log_info "升級日誌不存在 (首次安裝)"
fi

# 檢查 brain_notion_sync 日誌
if [ -f "$LONGHUN_DIR/brain_notion_sync.log" ]; then
    SIZE=$(du -h "$LONGHUN_DIR/brain_notion_sync.log" | cut -f1)
    log_pass "brain_notion_sync 日誌存在 (大小: $SIZE)"
else
    log_info "brain_notion_sync 日誌不存在 (首次運行時創建)"
fi

# ═══════════════════════════════════════════════════════════════
# 最後統計和建議
# ═══════════════════════════════════════════════════════════════

log_title "最終檢查報告"

echo ""
echo "📊 檢查統計:"
echo "   總檢查項目: $TOTAL_CHECKS"
echo -e "   ${GREEN}通過: $PASSED_CHECKS${NC}"
echo -e "   ${YELLOW}警告: $WARNING_CHECKS${NC}"
echo -e "   ${RED}失敗: $FAILED_CHECKS${NC}"
echo ""

PASS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "🎯 通過率: ${PASS_RATE}%"
echo ""

# 生成建議
if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✨ 系統狀態: 完美 (所有關鍵檢查通過)${NC}"
elif [ $FAILED_CHECKS -le 2 ]; then
    echo -e "${YELLOW}⚠️  系統狀態: 需要注意 (有 $FAILED_CHECKS 個失敗項)${NC}"
else
    echo -e "${RED}❌ 系統狀態: 需要修復 (有 $FAILED_CHECKS 個失敗項)${NC}"
fi

echo ""

# 啟動建議
log_title "🚀 啟動建議"

if ! pgrep -f "brain_notion_sync.py --watch" > /dev/null; then
    echo ""
    echo "📌 啟動 brain_notion_sync (持續監聽模式):"
    echo "   cd ~/longhun-system"
    echo "   nohup python3 brain_notion_sync.py --watch > brain_notion_sync.log 2>&1 &"
    echo ""
fi

if ! curl -s http://localhost:9000/api/v1/monitor/health > /dev/null 2>&1; then
    echo "📌 啟動監控服務器:"
    echo "   cd ~/longhun-system/mobile-monitoring/backend/python"
    echo "   python3 monitoring_server.py"
    echo ""
fi

# ═══════════════════════════════════════════════════════════════
# 生成檢查日誌
# ═══════════════════════════════════════════════════════════════

LOGFILE="$LONGHUN_DIR/LONGHUN_STARTUP_CHECK_$(date +%Y%m%d_%H%M%S).log"

cat > "$LOGFILE" << EOF
🐉 龍魂系統啟動檢查報告
生成時間: $(date '+%Y-%m-%d %H:%M:%S')
DNS:#龍芯⚡️2026-06-07-LONGHUN-STARTUP-CHECK-v1.0

檢查統計:
  總項目: $TOTAL_CHECKS
  通過: $PASSED_CHECKS
  警告: $WARNING_CHECKS
  失敗: $FAILED_CHECKS
  通過率: ${PASS_RATE}%

檢查日期: $(date '+%A, %B %d, %Y')
檢查者: 自動檢查腳本
EOF

echo ""
log_pass "檢查日誌已保存: $LOGFILE"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🐉 龍魂系統啟動檢查完成"
echo "════════════════════════════════════════════════════════════"
echo "DNA:#龍芯⚡️2026-06-07-LONGHUN-STARTUP-CHECK-v1.0"
echo "天下無欺。"
echo ""
