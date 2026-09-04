#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂每日民间防御运营 v1.0
# DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷑蛊-每日防御-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 功能: 每日一键执行网站健康检查+无为归档统计+样本统计

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$LONGHUN_ROOT/logs"
mkdir -p "$LOG_DIR"

TODAY=$(date +%Y-%m-%d)
REPORT_DIR="$LONGHUN_ROOT/output/daily_ops"
mkdir -p "$REPORT_DIR"

echo "╔══════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂每日民间防御运营 · $TODAY          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ━━━ P1: 网站健康检查 ━━━
echo "━━━ P1: 网站健康检查 ━━━"
python3 "$SCRIPT_DIR/lh_web_health_check.py" --once 2>&1 | tee -a "$LOG_DIR/health_$TODAY.log"
HEALTH_EXIT=${PIPESTATUS[0]}
echo ""

# ━━━ P2: 无为评论归档统计 ━━━
echo "━━━ P2: 无为评论归档统计 ━━━"
python3 "$SCRIPT_DIR/lh_archive_vague_comments.py" --stats 2>&1 | tee -a "$LOG_DIR/daily_ops_$TODAY.log"
echo ""

# ━━━ P3: 民间防御样本统计 ━━━
echo "━━━ P3: 民间防御样本统计 ━━━"
python3 "$SCRIPT_DIR/lh_civil_defense_samples.py" --stats 2>&1 | tee -a "$LOG_DIR/daily_ops_$TODAY.log"
echo ""

# ━━━ 汇总报告 ━━━
REPORT_FILE="$REPORT_DIR/report_$TODAY.md"
cat > "$REPORT_FILE" << EOF
# 龍魂每日防御运营报告 · $TODAY

## P1: 网站健康检查
- 退出码: $HEALTH_EXIT ($([ "$HEALTH_EXIT" -eq 0 ] && echo "✅ 正常" || echo "⚠️ 有异常"))
- 详细日志: \`logs/health_$TODAY.log\`

## P2: 无为评论归档
- 归档目录: \`audit/comment_samples/vague_pressure/\`

## P3: 民间防御样本
- 样本目录: \`data/civil_defense_samples/\`

---
> DNA: #龍芯⚡️$(date +%Y%m%d)-每日防御报告-auto
> GPG: 待签名
EOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 每日防御运营完成"
echo "📄 报告: $REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"