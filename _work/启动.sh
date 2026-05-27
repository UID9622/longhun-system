#!/bin/bash

# 🐉 龍魂統一啟動腳本 v1.0
# DNA: #龍芯⚡️2026-05-27-UNIFIED-LAUNCHER-v1.0

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo "🐉 龍魂系統 · 統一啟動臺"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# 切換到工作目錄
cd "$(dirname "$0")" || exit 1

echo "📍 當前目錄: $(pwd)"
echo "⏰ 啟動時間: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 檢查依賴
echo "🔍 檢查依賴..."
python3 -c "import fastapi; import uvicorn; import pydantic" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  缺少依賴，正在安裝..."
    pip install --user fastapi uvicorn pydantic requests python-dotenv 2>&1 | tail -3
    echo "✅ 依賴安裝完成"
else
    echo "✅ 依賴已就緒"
fi

echo ""
echo "🚀 啟動龍魂統一控制臺..."
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

# 啟動主控制臺
python3 龍魂統一控制臺.py

# 清理
echo ""
echo "👋 系統已關閉"
