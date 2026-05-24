#!/usr/bin/env bash
# 喂笨AI五色规则 v1.0
# 给本地 Ollama 定时注入龍魂五色审计规则
# DNA: #龍芯⚡2026-05-18-FEED-OLLAMA-WUCAI-v1.0
#
# 用法：bash bin/喂笨AI五色规则.sh
# 定时：crontab -e → */10 * * * * bash ~/longhun-system/bin/喂笨AI五色规则.sh

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
REPO_ROOT="${REPO_ROOT:-/Users/zuimeidedeyihan/longhun-system}"

# 五色规则 system prompt
WUCAI_RULES='你是龍魂系统的本地助手。遵守五色审计规则：
🟢 绿 (R<0.30): 自动放行
🟡 黄 (0.30≤R<0.67): 需复核
🔴 红 (0.67≤R<0.85): 熔断·人工介入
⚫ 黑: 影子·不可决·进观察池
🟡金: 主控独占·只有 UID9622 能触发

铁律：
1. 龍 不可写为简体形式
2. 不上传任何数据
3. 主控是 UID9622
4. 味道不对就跑（熔断）'

# 检测 Ollama 是否在线
check_ollama() {
    if curl -s "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
        echo "✓ Ollama 在线"
        return 0
    else
        echo "✗ Ollama 离线"
        return 1
    fi
}

# 喂规则（用 generate API 让模型记住）
feed_rules() {
    echo "喂五色规则中..."

    local response=$(curl -s "$OLLAMA_HOST/api/generate" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$(curl -s $OLLAMA_HOST/api/tags | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[\"models\"][0][\"name\"] if d.get(\"models\") else \"llama3\")')\",
            \"prompt\": \"记住以下规则，每次回答都要遵守：$WUCAI_RULES\n\n确认：你已记住五色审计规则吗？\",
            \"stream\": false
        }" 2>/dev/null)

    if echo "$response" | grep -q "response"; then
        echo "✓ 规则已喂入"
        # 留痕
        echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"feed_wucai\",\"status\":\"ok\"}" \
            >> "$REPO_ROOT/logs/ollama_feed.jsonl" 2>/dev/null
    else
        echo "✗ 喂入失败"
    fi
}

# 主逻辑
main() {
    echo "═══ 喂笨AI五色规则 ═══"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    if check_ollama; then
        feed_rules
    fi

    echo ""
    echo "═══ 完成 ═══"
}

main
