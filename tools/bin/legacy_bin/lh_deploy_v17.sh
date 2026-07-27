#!/bin/bash
# 龍魂 v1.7 一键部署脚本
# DNA: #龍芯⚡️丙午·辛未·乙酉·辰时·讼-DEPLOY-v1.7
set -e

PROJECT="/Users/zuimeidedeyihan/longhun-system"
GGUF_SRC="$PROJECT/models/longhun-v1.0/lora_output/gguf/longhun-v1.0.F16.gguf"
GGUF_DST="$PROJECT/models/longhun-v1.0/lora_output/gguf/longhun-v1.7.F16.gguf"
MODELFILE="$PROJECT/models/longhun-v1.7.Modelfile"
LOG="/tmp/lh_deploy_v17.log"

echo "=== v1.7 Deploy Start ===" | tee -a $LOG
date >> $LOG

# Step 1: Copy GGUF
echo "[1/2] Copy GGUF → v1.7..." | tee -a $LOG
if [ -f "$GGUF_SRC" ]; then
    cp "$GGUF_SRC" "$GGUF_DST"
    echo "   ✅ $GGUF_DST ($(du -sh "$GGUF_DST" | cut -f1))" | tee -a $LOG
else
    echo "   ❌ GGUF not found: $GGUF_SRC" | tee -a $LOG
    exit 1
fi

# Step 2: Ollama create
echo "[2/2] Ollama create longhun-v1.7..." | tee -a $LOG
ollama create longhun-v1.7 -f "$MODELFILE" 2>&1 | tee -a $LOG

echo "" | tee -a $LOG
echo "=== v1.7 Deploy Complete ===" | tee -a $LOG
ollama list | grep longhun | tee -a $LOG
