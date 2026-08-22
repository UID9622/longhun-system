#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# DNA: #龍芯⚡️丙午·乙未·辛亥·未时·䷀乾-V40-DISTILL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ============================================================
# 龍魂v4.0 · 蒸馏数据生成
# 老师: longhun-v3.8-expanded → 学生: Llama-3.1-8B
# 用法: bash bin/lh_v40_distill.sh
# ============================================================

set -e
cd "$HOME/longhun-system"

echo "========================================"
echo "  龍魂v4.0 蒸馏数据生成"
echo "  老师: longhun-v3.8-expanded (Ollama)"
echo "  学生: Llama-3.1-8B"
echo "  数据: 616条 · 4线程 · temp=0.1"
echo "  预计: ~10分钟"
echo "========================================"

python3 -u bin/lh_distill_v40_data.py --temp 0.1 --workers 4 --max-tokens 512

echo ""
echo "========================================"
echo "  蒸馏完成！查看结果："
echo "  wc -l models/longhun-v1.0/lora_output/data_v40_distill/*.jsonl"
echo "========================================"
echo "  下一步: python3 bin/lh_train_v40.py prepare  # 验证数据"
echo "          python3 bin/lh_train_v40.py train    # LoRA训练(60-90分钟)"
echo "          python3 bin/lh_train_v40.py fuse     # 合并adapter"
echo "          python3 bin/lh_train_v40.py export   # GGUF+Q4_K_M+Ollama"
echo "========================================"
