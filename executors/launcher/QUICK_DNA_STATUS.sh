##龍芯⚡️2026-06-21-TOOL-QUICK_DNA_STATUS-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/bin/bash
# 龍魂 DNA 对齐状态快速查看工具

cd ~/longhun-system

echo "════════════════════════════════════════════════════════════════"
echo "🐉 龍魂 DNA 对齐状态查询"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📋 两份最新报告:"
echo "  1. 详细审计报告:"
echo "     📄 DNA_ALIGNMENT_AUDIT_2026-06-07.md"
echo "        └─ 完整分析·253行·包含所有问题列表"
echo ""
echo "  2. 修复行动计划:"
echo "     📄 DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo "        └─ 执行步骤·优先级·随时可修复"
echo ""

echo "🎯 快速查看命令:"
echo "  # 查看核心问题摘要"
echo "  head -100 DNA_ALIGNMENT_AUDIT_2026-06-07.md"
echo ""
echo "  # 查看修复计划（P0优先）"
echo "  grep -A 20 '优先级 P0' DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo ""
echo "  # 查看完整修复步骤"
echo "  grep -A 30 '执行步骤' DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo ""

echo "📊 当前状态:"
python3 << 'PYSTATUS'
import re
from pathlib import Path

SCAN_DIR = Path.home() / "longhun-system"
DNA_PATTERN = r'#龍芯⚡️'

has_dna = 0
total = 0

for f in SCAN_DIR.rglob('*.py'):
    if '.git' in f.parts or '__pycache__' in f.parts or 'venv' in f.parts:
        continue
    total += 1
    try:
        if DNA_PATTERN in f.read_text(encoding='utf-8', errors='ignore'):
            has_dna += 1
    except:
        pass

if total > 0:
    pct = (has_dna / total) * 100
    print(f"  ✅ 核心Python档案: {has_dna}/{total} 有DNA ({pct:.1f}%)")
PYSTATUS

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "下一步: cat DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo "════════════════════════════════════════════════════════════════"

