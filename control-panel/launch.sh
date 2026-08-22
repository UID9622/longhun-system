#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂操作台 MVP v1.1 啟動腳本
# DNA:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-LONGHUN-CONTROL-PANEL-LAUNCHER-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

cd "$(dirname "$0")"
echo "🐉 啟動龍魂操作台 MVP v1.1"
echo "=================================================="

# 可選：安裝依賴
if [ "$1" == "--install" ]; then
    echo "📦 安裝依賴..."
    pip3 install -r requirements.txt
fi

echo "🌐 訪問地址："
echo "   操作台 UI : http://127.0.0.1:9622/static/index.html"
echo "   API 根節點 : http://127.0.0.1:9622/"
echo "   健康檢查  : http://127.0.0.1:9622/api/health"
echo ""
echo "🚀 啟動服務..."
python3 main.py
