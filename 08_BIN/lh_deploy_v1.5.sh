#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 v1.5 自动部署脚本
# DNA: #龍芯⚡️丙午·辛未·丙戌·酉·大壮-DEPLOY-v1.5
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

echo "🐉 龍魂 v1.5 自动部署"
echo "=========================================="

# Wait for training to finish
TRAIN_PID=$1
if [ -n "$TRAIN_PID" ]; then
    echo "等待训练完成 (PID=$TRAIN_PID)..."
    while ps -p $TRAIN_PID > /dev/null 2>&1; do
        sleep 5
    done
    echo "训练完成!"
fi

echo ""
echo "Step 1/3: Fuse LoRA..."
cd /Users/zuimeidedeyihan/longhun-system
python3 bin/lh_lora_trainer.py fuse 2>&1 | tail -5

echo ""
echo "Step 2/3: Export GGUF..."
python3 bin/lh_lora_trainer.py export 2>&1 | tail -5

echo ""
echo "Step 3/3: Deploy to Ollama..."
ollama create longhun-v1.5:latest -f /Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/gguf/Modelfile 2>&1

echo ""
echo "✅ longhun-v1.5:latest 部署完成"
ollama list | grep longhun
