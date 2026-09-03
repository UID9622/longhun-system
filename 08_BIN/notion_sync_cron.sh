#!/bin/bash
# 🐉 龍魂 Notion 索引每日增量同步
# DNA: #龍芯⚡️2026-08-31-NOTION-SYNC-CRON-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# cron: 0 6 * * * bash ~/longhun-system/08_BIN/notion_sync_cron.sh
# 说明: 增量扫描(只处理变化页) + bridge 存活守护(挂了才拉起) · 全量语义补全由每周 --embed 承担

LOG_DIR="$HOME/.longhun/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/notion_sync_$(date +%Y%m%d).log"

echo "[$(date -Iseconds)] 🐉 开始 Notion 增量同步" >> "$LOG_FILE"
cd "$HOME/longhun-system"

# 清代理坑（urllib/httpx 走 socks5h 会 Remote end closed / SOCKS 报错）
for k in HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy; do unset "$k"; done
export NO_PROXY="*"

python3 08_BIN/lh_notion_scanner.py --incremental >> "$LOG_FILE" 2>&1

# bridge 存活检查（挂了才拉起 · 不反复重启）
if ! pgrep -f "lh_notion_mcp_bridge.py" > /dev/null; then
    nohup python3 08_BIN/lh_notion_mcp_bridge.py --port 8898 >> "$LOG_DIR/bridge.log" 2>&1 &
    echo "[$(date -Iseconds)] 🚑 bridge 已拉起" >> "$LOG_FILE"
fi

echo "[$(date -Iseconds)] ✅ 同步完成" >> "$LOG_FILE"
exit 0
