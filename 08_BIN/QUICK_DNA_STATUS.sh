#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷈小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-TOOL-QUICK_DNA_STATUS-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/bin/bash
# 龍魂 DNA 對齐狀態快速查看工具

cd ~/longhun-system

echo "════════════════════════════════════════════════════════════════"
echo "🐉 龍魂 DNA 對齐狀態查詢"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📋 兩份最新報告:"
echo "  1. 詳細審計報告:"
echo "     📄 DNA_ALIGNMENT_AUDIT_2026-06-07.md"
echo "        └─ 完整分析·253行·包含所有問題列表"
echo ""
echo "  2. 修復行動計劃:"
echo "     📄 DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo "        └─ 執行步驟·優先級·隨時可修復"
echo ""

echo "🎯 快速查看命令:"
echo "  # 查看核心問題摘要"
echo "  head -100 DNA_ALIGNMENT_AUDIT_2026-06-07.md"
echo ""
echo "  # 查看修復計劃（P0優先）"
echo "  grep -A 20 '優先級 P0' DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo ""
echo "  # 查看完整修復步驟"
echo "  grep -A 30 '執行步驟' DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo ""

echo "📊 當前狀態:"
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
    print(f"  ✅ 核心Python檔案: {has_dna}/{total} 有DNA ({pct:.1f}%)")
PYSTATUS

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "下一步: cat DNA_ALIGNMENT_REPAIR_ACTION_PLAN.md"
echo "════════════════════════════════════════════════════════════════"

