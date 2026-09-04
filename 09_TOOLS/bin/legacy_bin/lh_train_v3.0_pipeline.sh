#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 v3.0 训练全链路
# DNA: #龍芯⚡️丙午·乙申·己酉·亥时·TRAIN-PIPELINE-v3.0
set -e

cd /Users/zuimeidedeyihan/longhun-system
LOG="/tmp/lh_train_v3.0_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "================================================"
echo "  龍魂 v3.0 训练全链路启动"
echo "  时间: $(date)"
echo "  日志: $LOG"
echo "================================================"

# Step 1: 底模转换 (Python API 离线模式)
echo ""
echo ">>> [1/3] 底模转换: Qwen2.5-1.5B-Instruct → MLX"
python3 bin/lh_convert_model.py
echo ">>> [1/3] ✅ 转换完成"

# Step 2: LoRA训练
echo ""
echo ">>> [2/3] LoRA训练: longhun-v3.0-lora (4 epochs)"
python3 bin/lh_lora_trainer.py train
echo ">>> [2/3] ✅ 训练完成"

# Step 3: 合并+导出
echo ""
echo ">>> [3/3] 合并权重+导出GGUF"
python3 bin/lh_lora_trainer.py fuse
python3 bin/lh_lora_trainer.py export
echo ">>> [3/3] ✅ 导出完成"

echo ""
echo "================================================"
echo "  🐉 v3.0 训练全链路完成"
echo "  时间: $(date)"
echo "  日志: $LOG"
echo "================================================"
