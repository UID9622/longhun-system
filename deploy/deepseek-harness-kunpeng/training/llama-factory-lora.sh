#!/usr/bin/env bash
# 🐉 龍魂 · 鲲鹏/昇腾 LoRA 微调指引
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-LLAMA-FACTORY-LoRA-UID9622

set -euo pipefail

echo "🐉 龍魂 · LoRA 微调指引"
echo ""
echo "阶段一（现在就能做）：系统提示词人格注入"
echo "  → 修改 configs/longhun-system-prompt.md，零算力"
echo ""
echo "阶段二（数据积累后）：LoRA 微调"
echo "  环境要求："
echo "    - 鲲鹏 4C8G 可跑 7B 模型 LoRA（CPU）"
echo "    - 昇腾 NPU 可加速全量/LoRA 训练"
echo ""
echo "  推荐工具："
echo "    - LLaMA-Factory (https://github.com/hiyouga/LLaMA-Factory)"
echo "    - 昇腾适配：参考昇腾官方 NPU Docker 镜像"
echo ""
echo "  示例命令 A（昇腾 NPU）："
cat << 'EOF'
# 昇腾 NPU 场景: --fp16 可用 (Ascend 混合精度)
llamafactory-cli train \
  --stage sft \
  --do_train True \
  --model_name_or_path deepseek-ai/deepseek-llm-7b-base \
  --dataset longhun_identity,longhun_audit \
  --template default \
  --finetuning_type lora \
  --lora_target q_proj,v_proj \
  --output_dir ./longhun-lora \
  --overwrite_cache \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 4 \
  --lr_scheduler_type cosine \
  --logging_steps 10 \
  --save_steps 100 \
  --learning_rate 5e-5 \
  --num_train_epochs 3.0 \
  --plot_loss \
  --fp16
EOF

echo ""
echo "  示例命令 B（鲲鹏纯 CPU）："
echo "  # CPU 场景: --fp16 是 CUDA/昇腾专属参数, CPU 不可用, 必须去掉"
echo "  # 并加 --use_cpu True --overwrite_output_dir; 7B LoRA CPU 预计极慢, 建议先用 1.5B/3B 小模型验证流程"
cat << 'EOF'
llamafactory-cli train \
  --stage sft \
  --do_train True \
  --use_cpu True \
  --model_name_or_path deepseek-ai/deepseek-llm-7b-base \
  --dataset longhun_identity,longhun_audit \
  --template default \
  --finetuning_type lora \
  --lora_target q_proj,v_proj \
  --output_dir ./longhun-lora \
  --overwrite_cache \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --lr_scheduler_type cosine \
  --logging_steps 10 \
  --save_steps 100 \
  --learning_rate 5e-5 \
  --num_train_epochs 3.0 \
  --plot_loss
EOF

echo ""
echo "阶段三（未来）：昇腾 NPU 全量训练"
echo "  → 需华为云昇腾实例，当前为理论假设"
echo ""
echo "🐉 数据准备建议："
echo "  - longhun_identity.jsonl: 身份激活对话数据"
echo "  - longhun_audit.jsonl: 审计与决策数据"
echo "  - longhun_code.jsonl: 龍魂代码/协议样本"
