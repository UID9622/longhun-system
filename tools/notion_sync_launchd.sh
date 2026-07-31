#!/bin/bash
# 龍魂 Notion 同步 LaunchAgent 包装脚本
# DNA: #龍芯⚡️2026-07-05-NOTION-SYNC-LAUNCHD-WRAPPER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 注意：NOTION_TOKEN 由 notion_sync.py 自动从 ~/.longhun/secrets.env 读取，
# 不需要在此 source 整个 .bashrc，避免 banner/npmrc 噪音。

export HOME="${HOME:-/Users/zuimeidedeyihan}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export LANG="zh_CN.UTF-8"
export LC_ALL="zh_CN.UTF-8"

ROOT="$HOME/longhun-system"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

exec /opt/homebrew/bin/python3.12 "$ROOT/tools/notion_sync.py" sync \
    --config "$ROOT/config/notion_sync.json" \
    --direction pull \
    --max-blocks 500 \
    >> "$LOG_DIR/notion-sync-daily.out.log" 2>> "$LOG_DIR/notion-sync-daily.err.log"
