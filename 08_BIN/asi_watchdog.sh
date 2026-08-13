#!/bin/bash
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-ASI-WATCHDOG-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# 🐉 龍魂 ASI · 合规巡检 watchdog
# 每6小时自动执行全量 ASI 测试，输出报告到 12_DOCS/agent_reports
#
# crontab 示例:
# 0 */6 * * * /opt/cnsh-ide/08_BIN/asi_watchdog.sh >> /var/log/asi_watchdog.log 2>&1

set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="/var/log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo ""
echo "🐉 龍魂 ASI 合规巡检启动 - ${TIMESTAMP}"
echo "========================================"

cd "${BASE_DIR}"

# 确保日志目录可写
if [ ! -w "${LOG_DIR}" ]; then
    LOG_DIR="${BASE_DIR}/logs"
    mkdir -p "${LOG_DIR}"
fi

# 执行全量测试（静默模式）
python3 08_BIN/asi_test_runner.py \
    --kunpeng \
    --auto \
    --output-dir 12_DOCS/agent_reports \
    >> "${LOG_DIR}/asi_watchdog.log" 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "🔴 巡检执行失败 (exit ${EXIT_CODE})"
    echo "   日志: ${LOG_DIR}/asi_watchdog.log"
    exit $EXIT_CODE
fi

echo "✅ 巡检完成"
echo "   报告目录: ${BASE_DIR}/12_DOCS/agent_reports"
echo "   最新报告: $(ls -t ${BASE_DIR}/12_DOCS/agent_reports/asi_test_report_*.md | head -1)"
echo "========================================"
