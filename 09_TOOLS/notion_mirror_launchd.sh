#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 Notion 瀏覽器鏡像 LaunchAgent 包裝腳本
# DNA: #龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-NOTION-MIRROR-LAUNCHD-WRAPPER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 每 6 小時抓取一次 Notion 公開頁面鏡像，API 未共享時的兜底方案。

export HOME="${HOME:-/Users/zuimeidedeyihan}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export LANG="zh_CN.UTF-8"
export LC_ALL="zh_CN.UTF-8"

ROOT="$HOME/longhun-system"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

VENV_PYTHON="$ROOT/tools/.venv/bin/python3"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') 🔴 虛擬環境未找到: $VENV_PYTHON" >> "$LOG_DIR/notion-mirror-daily.err.log"
    exit 1
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') 🌐 Notion 瀏覽器鏡像開始" >> "$LOG_DIR/notion-mirror-daily.out.log"

exec "$VENV_PYTHON" "$ROOT/tools/notion_mirror_scraper.py" \
    --config "$ROOT/config/notion_sync.json" \
    --delay 2 \
    >> "$LOG_DIR/notion-mirror-daily.out.log" 2>> "$LOG_DIR/notion-mirror-daily.err.log"
