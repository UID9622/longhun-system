#!/bin/bash
set -e
cd "$(dirname "$0")"
source ~/.longhun/secrets.env
source ./.env.shield
export LONGHUN_BAN_DRY_RUN=0
mkdir -p data/sm2 logs
nohup .venv_longhun_math/bin/python longhun_shield_panel.py > logs/shield_panel.log 2>&1 &
echo $! > .shield_panel.pid
echo "龍魂护盾 Web 面板已启动，PID: $(cat .shield_panel.pid)，端口: ${LONGHUN_PANEL_PORT:-8788}"
