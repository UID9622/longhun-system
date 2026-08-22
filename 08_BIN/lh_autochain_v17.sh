#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 v1.7 全自动训练→部署链
# DNA: #龍芯⚡️丙午·辛未·乙酉·辰时·䷅讼-AUTOCHAIN-v1.7
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
LOG=/tmp/lh_autochain_v17.log
echo "=== AUTOCHAIN START $(date) ===" > $LOG

echo "[0/4] 等待训练完成..." | tee -a $LOG
while pgrep -f "lh_lora_trainer.py train" > /dev/null 2>&1; do
    sleep 15
done
echo "[0/4] 训练已结束 $(date)" | tee -a $LOG

echo "[1/4] Fuse LoRA → base model..." | tee -a $LOG
cd /Users/zuimeidedeyihan/longhun-system
python3 bin/lh_lora_trainer.py fuse >> $LOG 2>&1
echo "[1/4] Fuse done" | tee -a $LOG

echo "[2/4] Export GGUF..." | tee -a $LOG
python3 bin/lh_lora_trainer.py export >> $LOG 2>&1
echo "[2/4] Export done" | tee -a $LOG

echo "[3/4] Copy GGUF → v1.7 + Ollama import..." | tee -a $LOG
bash bin/lh_deploy_v17.sh >> $LOG 2>&1
echo "[3/4] Deploy done" | tee -a $LOG

echo "[4/4] ✅ AUTOCHAIN COMPLETE $(date)" | tee -a $LOG
echo "" | tee -a $LOG
echo "待人工: 主权边界5项测试" | tee -a $LOG
