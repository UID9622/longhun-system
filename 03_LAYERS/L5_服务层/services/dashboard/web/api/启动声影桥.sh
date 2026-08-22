#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · 声影桥一键启动脚本
# DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-SHENGYING-STARTER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

cd "$(dirname "$0")"
PORT=${SHENGYING_PORT:-8766}

echo "🐉 启动声影桥 | port=${PORT}"
python3 声影桥.py --port "${PORT}"
