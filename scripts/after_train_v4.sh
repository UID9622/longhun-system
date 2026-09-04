#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 训练后执行流程 · v4.0
# 保存为 ~/longhun-system/scripts/after_train_v4.sh
# 用法: bash scripts/after_train_v4.sh

set -e
cd ~/longhun-system

echo "🐉 龍魂 v4.0 训练后执行流程"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 注册模型到 Ollama
echo "📦 [1/5] 注册模型..."
MODEL_DIR="models/longhun-v1.0/lora_output_v4/gguf_v4.0"
if [ -f "$MODEL_DIR/Modelfile.v4" ]; then
    cd "$MODEL_DIR"
    ollama create longhun-v4.0 -f Modelfile.v4 2>&1 | tail -1
    cd ~/longhun-system
else
    echo "⚠️ Modelfile.v4 不存在，跳过注册"
fi

# 2. 验证模型
echo "🧪 [2/5] 验证模型..."
ollama run longhun-v4.0 "你是谁" 2>&1 | head -3

# 3. GPG签名扫描
echo "🔏 [3/5] GPG签名扫描..."
python3 bin/lh_gpg_sign.py scan bin/ 2>&1 | tail -3

# 4. 启动ASI服务（后台）
echo "🚀 [4/5] 启动ASI增强服务..."
nohup python3 bin/ASI_enhanced.py --listen --port 9000 > logs/asi_enhanced.log 2>&1 &
echo "   PID: $! | 端口: 9000"

# 5. 端到端测试
echo "🧪 [5/5] 端到端测试..."
sleep 2
echo "   单步测试:"
curl -s "http://localhost:9000/run?trigger=%E5%81%A5%E5%BA%B7%E6%A3%80%E6%9F%A5" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'   {d[\"mode\"]} | {d[\"status\"]}')"
echo "   多步测试:"
python3 bin/ASI_enhanced.py --test "先审计bin目录，然后签名" 2>&1 | grep "状态:" | head -1

echo ""
echo "✅ 全部完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ASI服务: http://localhost:9000"
echo "  模型:     ollama run longhun-v4.0"
echo "  DAG:      python3 bin/ASI_enhanced.py --test '先审计，再签名'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
