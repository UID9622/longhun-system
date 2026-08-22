#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 快速评估状态检查

HOME=${HOME:-~}
ASSESSMENT_DIR="$HOME/.龍魂/assessments"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂系统 · 评估状态检查                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 1. 检查最新报告
echo "【📊 最新评估报告】"
LATEST_REPORT=$(ls -t "$ASSESSMENT_DIR"/local_assessment_*.json 2>/dev/null | head -1)

if [ -n "$LATEST_REPORT" ]; then
    MTIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$LATEST_REPORT" 2>/dev/null)
    SCORE=$(python3 -c "import json; data=json.load(open('$LATEST_REPORT')); print(data.get('total_score', 'N/A'))" 2>/dev/null)
    STATUS=$(python3 -c "import json; data=json.load(open('$LATEST_REPORT')); print(data.get('status', 'N/A'))" 2>/dev/null)

    echo "  档案: $(basename $LATEST_REPORT)"
    echo "  时间: $MTIME"
    echo "  评分: $SCORE/10"
    echo "  状态: $STATUS"
else
    echo "  ❌ 未找到评估报告"
fi

echo ""

# 2. 检查最新日志
echo "【📋 最新执行日志】"
LATEST_LOG=$(ls -t "$ASSESSMENT_DIR"/logs/daily_assessment_*.log 2>/dev/null | head -1)

if [ -n "$LATEST_LOG" ]; then
    LAST_EXEC=$(tail -1 "$LATEST_LOG" | grep "结束时间" | cut -d: -f2-)
    RESULT=$(tail -1 "$LATEST_LOG" | grep "执行状态" | cut -d: -f2-)

    echo "  档案: $(basename $LATEST_LOG)"
    if [ -n "$RESULT" ]; then
        echo "  结果: $RESULT"
    fi
    if [ -n "$LAST_EXEC" ]; then
        echo "  时间: $LAST_EXEC"
    fi
else
    echo "  ℹ️  还没有执行日志 (首次执行时生成)"
fi

echo ""

# 3. 检查 Cron 状态
echo "【⏱️  Cron 任务状态】"
CRON_JOB=$(crontab -l 2>/dev/null | grep "longhun_daily_assessment")

if [ -n "$CRON_JOB" ]; then
    echo "  状态: ✅ 已启用"
    echo "  设定: $CRON_JOB"

    # 计算下次执行时间
    NOW=$(date '+%s')
    TODAY_22_30=$(date -j -f "%Y-%m-%d %H:%M:%S" "$(date '+%Y-%m-%d') 22:30:00" '+%s' 2>/dev/null)

    if [ $NOW -lt $TODAY_22_30 ]; then
        NEXT_TIME=$(date -r $TODAY_22_30 '+%H:%M:%S (今天)')
    else
        TOMORROW_22_30=$(date -j -f "%Y-%m-%d %H:%M:%S" "$(date -v+1d '+%Y-%m-%d') 22:30:00" '+%s' 2>/dev/null)
        NEXT_TIME=$(date -r $TOMORROW_22_30 '+%Y-%m-%d %H:%M:%S')
    fi

    echo "  下次执行: $NEXT_TIME"
else
    echo "  状态: ❌ 未启用"
fi

echo ""

# 4. 系统概览
echo "【🎯 系统概览】"
REPORT_COUNT=$(ls "$ASSESSMENT_DIR"/local_assessment_*.json 2>/dev/null | wc -l)
LOG_COUNT=$(ls "$ASSESSMENT_DIR"/logs/daily_assessment_*.log 2>/dev/null | wc -l)

echo "  评估报告: $REPORT_COUNT 个"
echo "  执行日志: $LOG_COUNT 个"
echo "  总大小: $(du -sh "$ASSESSMENT_DIR" 2>/dev/null | cut -f1)"

echo ""
echo "────────────────────────────────────────────────────────────"
echo "💡 更多命令:"
echo "  查看完整评估: python3 ~/local_assessment_engine.py"
echo "  手动检查: python3 -c \"import json; f=sorted(__import__('glob').glob('~/.龍魂/assessments/local_assessment_*.json'))[-1]; d=json.load(open(f)); print(json.dumps(d, indent=2, ensure_ascii=False))\""
echo "────────────────────────────────────────────────────────────"
