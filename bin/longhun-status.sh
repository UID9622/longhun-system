#!/usr/bin/env bash
# 龍魂系統運行狀態一覽
# DNA:#龍芯⚡️2026-06-17-LONGHUN-STATUS-FILE1-v1.0

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "═══════════════════════════════════════════════════"
echo "  🐉 龍魂系統運行狀態"
echo "═══════════════════════════════════════════════════"
echo "  項目根目錄: $ROOT"
echo "  當前時間: $(date)"
echo ""

status_port() {
    local port=$1 name=$2
    if lsof -ti:"$port" >/dev/null 2>&1; then
        echo "  ✅ $name (port $port): 運行中"
    else
        echo "  ⏹️  $name (port $port): 未啟動"
    fi
}

status_port 9622 "龍魂操作台"
status_port 9001 "Persona API"
status_port 8001 "監控服務"

echo ""
if [ -f ~/Library/LaunchAgents/com.uid9622.longhun.autostart.plist ]; then
    if launchctl list | grep -q com.uid9622.longhun.autostart; then
        echo "  ✅ 開機自啟動: 已安裝並載入"
    else
        echo "  ⚠️  開機自啟動: 已安裝但未載入"
    fi
else
    echo "  ⏹️  開機自啟動: 未安裝"
fi

echo ""
echo "  最近日誌:"
for f in autostart.log control-panel.log cnsh-autostart.log daily-audit.log; do
    if [ -f "logs/$f" ]; then
        echo "    - logs/$f ($(stat -f%Sm -t '%Y-%m-%d %H:%M' logs/$f))"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════"
