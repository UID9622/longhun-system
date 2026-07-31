#!/bin/bash
# -*- coding: utf-8 -*-
# 龍魂系统 · 自动化日评估
# LongHun Automated Daily Assessment Wrapper

ASSESSMENT_ENGINE="$HOME/longhun-system/scripts/自動化評估.py"
ASSESSMENT_LOG_DIR="$HOME/.龍魂/assessments/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$ASSESSMENT_LOG_DIR/daily_assessment_${TIMESTAMP}.log"

# 建立日志目录
mkdir -p "$ASSESSMENT_LOG_DIR"

# 加载 webhook 配置（飞书自建应用机器人凭证、chat_id）
if [ -f "$HOME/.longhun/webhooks.env" ]; then
    set -a
    source "$HOME/.longhun/webhooks.env"
    set +a
fi

echo "════════════════════════════════════════════════════════════" >> "$LOG_FILE"
echo "🐉 龍魂系统 · 自动化日评估" >> "$LOG_FILE"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════" >> "$LOG_FILE"

# 执行评估并推送飞书
python3 "$ASSESSMENT_ENGINE" --cron --feishu >> "$LOG_FILE" 2>&1
RESULT=$?

echo "" >> "$LOG_FILE"
echo "执行状态: $([ $RESULT -eq 0 ] && echo '✅ 成功' || echo '❌ 失败')" >> "$LOG_FILE"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "════════════════════════════════════════════════════════════" >> "$LOG_FILE"

# 在生成的报告旁边记录
LATEST_REPORT=$(ls -t "$HOME/.龍魂/assessments"/local_assessment_*.json 2>/dev/null | head -1)
if [ -n "$LATEST_REPORT" ]; then
    echo "最新报告: $LATEST_REPORT" >> "$LOG_FILE"

    # 提取评分
    SCORE=$(python3 -c "import json; data=json.load(open('$LATEST_REPORT')); print(data.get('total_score', 'N/A'))" 2>/dev/null)
    STATUS=$(python3 -c "import json; data=json.load(open('$LATEST_REPORT')); print(data.get('status', 'N/A'))" 2>/dev/null)

    echo "评分: $SCORE/10 | 状态: $STATUS" >> "$LOG_FILE"
fi

exit $RESULT
