#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂每日復盤·帶密鑰激活運行器
# 負責在 LaunchAgent / Cron 環境中加載 ~/.longhun/secrets.env 與 ~/.uid9622/git-tokens.sh
# 再調用 tools/logging/daily_review_enhanced.py 發送郵件/Notion/日曆
# DNA: #龍芯⚡️2026-06-29-DAILY-REVIEW-RUNNER-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

# 加載龍魂密鑰
if [ -f "$HOME/longhun-system/_private/密钥资料/启动脚本/activate_longhun_keys.sh" ]; then
    set -a
    source "$HOME/longhun-system/_private/密钥资料/启动脚本/activate_longhun_keys.sh"
    set +a
fi

# 加載可選 webhook 通道（企業微信/釘釘/飛書）
if [ -f "$HOME/.longhun/webhooks.env" ]; then
    set -a
    source "$HOME/.longhun/webhooks.env"
    set +a
fi

# 運行復盤引擎
/opt/homebrew/bin/python3 "$ROOT/tools/logging/daily_review_enhanced.py" \
    >> "$LOG_DIR/daily_review_enhanced.out.log" 2>> "$LOG_DIR/daily_review_enhanced.err.log"
