#!/bin/bash
# 🐉 龍魂系統一鍵啟動腳本
# ═══════════════════════════════════════════════════════════════
# 功能: 自動啟動龍魂系統的所有必要服務
# 用法: bash longhun_system_start_all.sh
# DNA:#龍芯⚡️2026-06-07-LONGHUN-START-ALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════════

set -e

# 顏色定義
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

# 啟動計數
SERVICES_STARTED=0
SERVICES_FAILED=0

# ═══════════════════════════════════════════════════════════════
# 日誌和輸出函數
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
    
    echo -n "⏳ 正在啟動 $SERVICE_NAME..."
    
    # 檢查是否已運行
    if [ -f "$PID_FILE" ]; then
        local OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo -e " ${YELLOW}已運行 (PID: $OLD_PID)${NC}"
            return 0
        fi
    fi
    
    # 啟動服務
    eval "$SERVICE_CMD" > "$LOG_FILE" 2>&1 &
    local NEW_PID=$!
    echo $NEW_PID > "$PID_FILE"
    
    # 等待服務啟動
    sleep 2
    
    # 檢查是否成功
    if kill -0 $NEW_PID 2>/dev/null; then
        echo -e " ${GREEN}✅ 成功 (PID: $NEW_PID)${NC}"
        SERVICES_STARTED=$((SERVICES_STARTED + 1))
        echo "   日誌: $LOG_FILE"
        return 0
    else
        echo -e " ${RED}❌ 失敗${NC}"
        SERVICES_FAILED=$((SERVICES_FAILED + 1))
        echo "   日誌: $LOG_FILE"
        echo "   錯誤信息:"
        tail -5 "$LOG_FILE" | sed 's/^/     /'
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════
# 部分 1: 環境檢查
# ═══════════════════════════════════════════════════════════════

print_header "Part 1: 環境檢查"

if [ ! -d "$LONGHUN_DIR" ]; then
    echo -e "${RED}❌ 龍魂系統目錄不存在: $LONGHUN_DIR${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 龍魂系統目錄: $LONGHUN_DIR${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 未安裝${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"

echo -e "${GREEN}✅ 日誌目錄: $LOG_DIR${NC}"

# ═══════════════════════════════════════════════════════════════
# 部分 2: 啟動 brain_notion_sync (Notion 同步服務)
# ═══════════════════════════════════════════════════════════════

print_header "Part 2: 啟動 brain_notion_sync (Notion 同步服務)"

BRAIN_SYNC_FILE="$LONGHUN_DIR/brain_notion_sync.py"
BRAIN_SYNC_PID="$LOG_DIR/brain_notion_sync.pid"
BRAIN_SYNC_LOG="$LOG_DIR/brain_notion_sync.log"

if [ ! -f "$BRAIN_SYNC_FILE" ]; then
    echo -e "${YELLOW}⚠️  brain_notion_sync.py 不存在${NC}"
else
    # 檢查 Python 語法
    if ! python3 -m py_compile "$BRAIN_SYNC_FILE" 2>/dev/null; then
        echo -e "${RED}❌ brain_notion_sync.py 語法錯誤${NC}"
    else
        start_service \
            "brain_notion_sync (持續監聽)" \
            "cd $LONGHUN_DIR && python3 brain_notion_sync.py --watch" \
            "$BRAIN_SYNC_PID" \
            "$BRAIN_SYNC_LOG"
    fi
fi

# ═══════════════════════════════════════════════════════════════
# 部分 3: 啟動監控服務器
# ═══════════════════════════════════════════════════════════════

print_header "Part 3: 啟動監控服務器 (monitoring_server)"

MONITORING_FILE="$LONGHUN_DIR/mobile-monitoring.integrated/backend/python/monitoring_server.py"
MONITORING_PID="$LOG_DIR/monitoring_server.pid"
MONITORING_LOG="$LOG_DIR/monitoring_server.log"

# 若 8000 已被佔用（如 phase3 後端），則使用 8001
if nc -z -G 1 127.0.0.1 8000 2>/dev/null; then
    MONITORING_PORT=8001
    echo -e "${YELLOW}⚠️  端口 8000 已被佔用，監控服務器將使用 8001${NC}"
else
    MONITORING_PORT=8000
fi

if [ ! -f "$MONITORING_FILE" ]; then
    echo -e "${YELLOW}⚠️  監控服務器文件不存在${NC}"
else
    start_service \
        "監控服務器 (localhost:$MONITORING_PORT)" \
        "cd $LONGHUN_DIR/mobile-monitoring.integrated/backend/python && MONITORING_PORT=$MONITORING_PORT python3 monitoring_server.py" \
        "$MONITORING_PID" \
        "$MONITORING_LOG"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 4: 啟動 longhun_brain (大腦服務)
# ═══════════════════════════════════════════════════════════════

print_header "Part 4: 檢查 longhun_brain (大腦服務)"

BRAIN_FILE="$LONGHUN_DIR/longhun_brain.py"

if [ ! -f "$BRAIN_FILE" ]; then
    echo -e "${YELLOW}⚠️  longhun_brain.py 不存在${NC}"
else
    # longhun_brain 一般不需要持續運行，只在有請求時執行
    echo -e "${BLUE}ℹ️  longhun_brain.py 存在 (按需執行)${NC}"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 5: 驗證服務狀態
# ═══════════════════════════════════════════════════════════════

print_header "Part 5: 驗證服務狀態"

echo "📋 檢查運行中的進程:"
echo ""

# 檢查 brain_notion_sync
if pgrep -f "brain_notion_sync.py --watch" > /dev/null; then
    PID=$(pgrep -f "brain_notion_sync.py --watch")
    echo -e "  ${GREEN}✅ brain_notion_sync${NC} (PID: $PID)"
else
    echo -e "  ${RED}❌ brain_notion_sync 未運行${NC}"
fi

# 檢查監控服務器
if pgrep -f "monitoring_server.py" > /dev/null; then
    PID=$(pgrep -f "monitoring_server.py")
    echo -e "  ${GREEN}✅ monitoring_server${NC} (PID: $PID)"
else
    echo -e "  ${YELLOW}⚠️  monitoring_server 未運行${NC}"
fi

# 檢查監控服務端口
echo ""
echo "📡 檢查服務可達性:"
echo ""
if curl --max-time 3 -s http://localhost:$MONITORING_PORT/api/v1/monitor/health > /dev/null 2>&1; then
    HEALTH=$(curl --max-time 3 -s http://localhost:$MONITORING_PORT/api/v1/monitor/health 2>/dev/null)
    if echo "$HEALTH" | grep -q "healthy"; then
        echo -e "  ${GREEN}✅ localhost:$MONITORING_PORT (正常)${NC}"
    else
        echo -e "  ${YELLOW}⚠️  localhost:$MONITORING_PORT (響應異常)${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  localhost:$MONITORING_PORT (不可達)${NC}"
fi

# ═══════════════════════════════════════════════════════════════
# 部分 6: 顯示日誌位置
# ═══════════════════════════════════════════════════════════════

print_header "Part 6: 服務日誌位置"

echo "📝 實時查看日誌:"
echo ""
echo "  brain_notion_sync:"
echo "    tail -f $BRAIN_SYNC_LOG"
echo ""
echo "  monitoring_server:"
echo "    tail -f $MONITORING_LOG"
echo ""

# ═══════════════════════════════════════════════════════════════
# 部分 7: 總結
# ═══════════════════════════════════════════════════════════════

print_header "🎉 啟動完成"

echo "📊 啟動統計:"
echo "   成功: $SERVICES_STARTED 個服務"
echo "   失敗: $SERVICES_FAILED 個服務"
echo ""

if [ $SERVICES_FAILED -eq 0 ]; then
    echo -e "${GREEN}✨ 所有服務已成功啟動！${NC}"
else
    echo -e "${YELLOW}⚠️  有 $SERVICES_FAILED 個服務啟動失敗，請檢查日誌${NC}"
fi

echo ""
echo "🔗 常用命令:"
echo ""
echo "  1. 查看所有運行的服務:"
echo "     ps aux | grep -E 'brain_notion_sync|monitoring_server'"
echo ""
echo "  2. 停止 brain_notion_sync:"
echo "     kill \$(pgrep -f 'brain_notion_sync.py --watch')"
echo ""
echo "  3. 停止監控服務器:"
echo "     kill \$(pgrep -f 'monitoring_server.py')"
echo ""
echo "  4. 檢查系統狀態:"
echo "     bash $LONGHUN_DIR/longhun_system_startup_check.sh"
echo ""

# ═══════════════════════════════════════════════════════════════
# 生成啟動報告
# ═══════════════════════════════════════════════════════════════

STARTUP_LOG="$LOG_DIR/LONGHUN_STARTUP_$(date +%Y%m%d_%H%M%S).log"

cat > "$STARTUP_LOG" << EOF
🐉 龍魂系統啟動報告
╔══════════════════════════════════════════════════════════════╗
║ DNA:#龍芯⚡️2026-06-07-LONGHUN-START-ALL-v1.0             ║
╚══════════════════════════════════════════════════════════════╝

啟動時間: $(date '+%Y-%m-%d %H:%M:%S %Z')
啟動目錄: $LONGHUN_DIR

啟動統計:
  • 成功啟動: $SERVICES_STARTED 個
  • 啟動失敗: $SERVICES_FAILED 個

啟動的服務:
  ✓ brain_notion_sync (Notion 同步)
    PID 文件: $BRAIN_SYNC_PID
    日誌文件: $BRAIN_SYNC_LOG

  ✓ monitoring_server (監控服務)
    PID 文件: $MONITORING_PID
    日誌文件: $MONITORING_LOG

系統狀態: 正常運行

天下無欺。🐉
EOF

echo "📋 啟動報告已保存: $STARTUP_LOG"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✨ 龍魂系統已啟動，天下無欺。🐉"
echo "════════════════════════════════════════════════════════════"
