#!/bin/bash
# 🐉 龍魂 · 透明看板一键启动
# DNA: #龍芯⚡️丙午·丙申·丁酉·辰时-TRANSPARENT-DASHBOARD-STARTER-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

cd "$(dirname "$0")/.."
HOST="${1:-127.0.0.1}"
PORT="${2:-8080}"

echo "🐉 启动龍魂透明看板..."
echo "   地址: http://${HOST}:${PORT}"
echo "   DNA: #龍芯⚡️丙午·丙申·丁酉·辰时-TRANSPARENT-DASHBOARD-UID9622"
echo "   君子协议: 永远没有黑箱操作"

if [ "$HOST" = "0.0.0.0" ]; then
    echo "🟡 警告: 当前监听 0.0.0.0，数据对网络内所有设备可见"
fi

python3 08_BIN/lh_transparent_dashboard.py --host "$HOST" --port "$PORT"

# ⛓️ DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|透明看板落地-君子协议可视化契约|bhash:510e0b8a|chash:454b3bb9|←GENESIS
