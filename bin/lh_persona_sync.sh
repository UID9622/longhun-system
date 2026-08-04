#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🔄 人格报表定时刷新 + 飞书推送
# DNA: #龍芯⚡️2026-07-07-PERSONA-REPORT-SYNC-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 作用: 生成最新报表 → 写入 portal data → 可选推送到飞书群
# 用法: bash bin/lh_persona_sync.sh [--push-feishu]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

echo "🧬 生成人格评估报表..."
python3 "$ROOT/bin/lh_persona_report.py"

if [ "$1" = "--push-feishu" ]; then
    FEISHU_WEBHOOK="${FEISHU_PERSONA_WEBHOOK:-}"
    if [ -z "$FEISHU_WEBHOOK" ]; then
        echo "⚠️ 未设置 FEISHU_PERSONA_WEBHOOK 环境变量，跳过飞书推送"
        exit 0
    fi
    
    echo "📤 推送到飞书群..."
    CARD=$(python3 "$ROOT/bin/lh_persona_report.py" --feishu-card)
    
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "$CARD" > /dev/null
    
    echo "✅ 已推送到飞书群"
fi

echo "✅ 同步完成 · $(date '+%Y-%m-%d %H:%M:%S')"
