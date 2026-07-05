#!/bin/bash
set -e
cd "$(dirname "$0")"
source ~/.longhun/secrets.env
source ./.env.shield
mkdir -p "$HOME/.longhun/quarantine" logs
PYTHONUNBUFFERED=1 nohup .venv_longhun_math/bin/python longhun_download_guard.py --watch > logs/download_guard.log 2>&1 &
echo $! > .download_guard.pid
echo "龍魂下载守卫已启动，PID: $(cat .download_guard.pid)，看守：${LONGHUN_WATCH_DIRS:-$HOME/Downloads}"
