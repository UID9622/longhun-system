#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-EXAMPLE-DEMO-SH-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: AGPL-3.0-or-later
# 🐉 longhun-cli 标准调用示例 — flow / health / bazi（命令行形态）
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== 1. 流场计算 lh flow ==="
lh flow "龙魂对外首发" --json

echo
echo "=== 2. 健康自检 lh health ==="
lh health --json

echo
echo "=== 3. 八字排盘 lh bazi ==="
lh bazi --date 1990-01-01 --time 08:00 --json

echo
echo "=== 4. 可解析性断言（机器可消费） ==="
lh flow "龙魂对外首发" --json | python3 -c "
import sys, json
d = json.load(sys.stdin)
assert d['element'] in '水火木金土', '五行非法'
assert d['node_id'].startswith('FLOW-9622-'), 'node_id 非法'
print('✅ flow JSON 解析通过 ·', d['node_id'], '·', d['digital_root'], '·', d['element'])
"

lh bazi --date 1990-01-01 --time 08:00 --json | python3 -c "
import sys, json
d = json.load(sys.stdin)
assert d['status'] == 'ok', 'bazi 失败'
print('✅ bazi JSON 解析通过 ·', d['bazi'], '· 主导', d['dominant'])
"

echo
echo "✅ 演示完成 · 全部输出为可解析 Node JSON"
