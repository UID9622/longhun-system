#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂流控压测 · 清理脚本
# DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-CLEANUP-UID9622
# License: MulanPSL v2 (工程层)

set -e

echo "🐉 龍魂流控压测 · 清理"
echo "========================="

# 删除测试报告
rm -f load_test_report.html
rm -f step_load_report.html

# 删除审计报告
rm -f tests/reports/tricolor_audit.json

# 删除临时文件
rm -f tests/test_data/*.tmp

echo "✅ 清理完成"
