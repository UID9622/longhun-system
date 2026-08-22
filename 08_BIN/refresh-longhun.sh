#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统一键刷新：重新盘点模块 + 重新生成桌面主开关
# DNA:#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-LONGHUN-REFRESH-FILE1-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "🐉 龍魂系统一键刷新"
echo "═══════════════════════════════════════════════════"

echo ""
echo "[1/3] 更新模块盘点..."
python3 bin/module_inventory.py

echo ""
echo "[2/3] 重新生成模块说明文档..."
python3 bin/generate_module_readmes.py 2>/dev/null || echo "（未启用自动 README 生成）"

echo ""
echo "[3/3] 重新生成桌面主开关..."
bash bin/build-desktop-switch.sh

echo ""
echo "✅ 一键刷新完成"
echo "   请关闭旧的龍魂主开关窗口，重新打开 ~/Desktop/龍魂主开关.app"
