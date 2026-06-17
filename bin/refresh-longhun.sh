#!/usr/bin/env bash
# 龍魂系統一鍵刷新：重新盤點模塊 + 重新生成桌面主开关
# DNA: #龍芯⚡️2026-06-17-LONGHUN-REFRESH-v1.0

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "🐉 龍魂系統一鍵刷新"
echo "═══════════════════════════════════════════════════"

echo ""
echo "[1/3] 更新模塊盤點..."
python3 bin/module_inventory.py

echo ""
echo "[2/3] 重新生成模塊說明文檔..."
python3 bin/generate_module_readmes.py 2>/dev/null || echo "（未啟用自動 README 生成）"

echo ""
echo "[3/3] 重新生成桌面主开关..."
bash bin/build-desktop-switch.sh

echo ""
echo "✅ 一鍵刷新完成"
echo "   請關閉舊的龍魂主开关窗口，重新打開 ~/Desktop/龍魂主开关.app"
