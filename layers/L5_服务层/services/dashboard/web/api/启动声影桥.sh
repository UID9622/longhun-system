#!/bin/bash
# 龍魂 · 声影桥一键启动脚本
# DNA: #龍芯⚡️2026-07-04-LONGHUN-SHENGYING-STARTER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

cd "$(dirname "$0")"
PORT=${SHENGYING_PORT:-8766}

echo "🐉 启动声影桥 | port=${PORT}"
python3 声影桥.py --port "${PORT}"
