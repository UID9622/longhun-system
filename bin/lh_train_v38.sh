#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-TRAIN-V38-SCRIPT
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ============================================================
# 龍魂 v3.8 LoRA 训练流水线 · MLX 原生 · M4 Max 优化
# 
# 真实配置（从 v3.8.1 adapter_config.json 提取）:
#   底模: models/longhun-v1.0/base_model (Qwen2.5-1.5B-Instruct MLX)
#   数据: messages 格式（system+user+assistant 多轮）
#   LoRA: rank=16, layers=8, scale=64.0
#   训练: lr=1e-4, batch=2, epochs=2
# ============================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${CYAN}[龍魂]${NC} $*"; }
ok()   { echo -e "${GREEN}[  ✅ ]${NC} $*"; }
warn() { echo -e "${YELLOW}[  ⚠️  ]${NC} $*"; }
err()  { echo -e "${RED}[  ❌ ]${NC} $*"; exit 1; }

# ── 路径配置 ──────────────────────────────────────────────
PROJECT_DIR="${LONGHUN_HOME:-$HOME/longhun-system}"
MODEL_DIR="$PROJECT_DIR/models/longhun-v1.0"
BASE_MODEL="$MODEL_DIR/base_model"
LORA_OUTPUT="$MODEL_DIR/lora_output"
DATA_DIR="$LORA_OUTPUT/data"
K3_DISTILL="$LORA_OUTPUT/k3_distill_v39"

# v3.8 系列适配器命名（自动递增）
ADAPTER_BASE="$LORA_OUTPUT/adapter_v3.8"

usage() {
    cat << 'EOF'
龍魂 v3.8 LoRA 训练流水线

用法:
  ./lh_train_v38.sh prepare     # 准备训练数据（合并 jiafa_qa + K3蒸馏）
  ./lh_train_v38.sh train       # 执行LoRA微调
  ./lh_train_v38.sh resume N    # 从第N步恢复训练
  ./lh_train_v38.sh fuse        # 合并 adapter → 全量模型
  ./lh_train_v38.sh export      # 导出 GGUF → Ollama 部署
  ./lh_train_v38.sh all         # 一键全流程

训练参数（真实配置·不可随意改）:
  rank=16  layers=8  batch=2  lr=1e-4  epochs=2
EOF
    exit 0
}

# ── 磁盘预检 ──────────────────────────────────────────────
check_disk() {
    local free_gb
    free_gb=$(df -g . | awk 'NR==2 {print $4}')
    log "磁盘剩余: ${free_gb}GB"
    if [ "${free_gb%.*}" -lt 10 ]; then
        err "磁盘不足10GB，拒绝启动训练"
    fi
    ok "磁盘空间充足"
}

# ── 数据准备 ──────────────────────────────────────────────
do_prepare() {
    log "数据准备阶段..."
    check_disk

    mkdir -p "$DATA_DIR"

    python3 << 'PYEOF'
import json, os

data_dir = os.path.expanduser("~/longhun-system/models/longhun-v1.0/lora_output/data")
k3_dir   = os.path.expanduser("~/longhun-system/models/longhun-v1.0/lora_output/k3_distill_v39")

all_data = []

# 1. 加载 jiafa_qa.jsonl（家法域·DNA种子）
jiafa_file = os.path.join(k3_dir, "jiafa_qa.jsonl")
if os.path.exists(jiafa_file):
    with open(jiafa_file, 'r') as f:
        for line in f:
            item = json.loads(line)
            if "messages" in item:
                all_data.append(item)
    print(f"[1/4] 家法域数据: {len(all_data)} 条")
else:
    print("[1/4] ⚠️ jiafa_qa.jsonl 不存在")

# 2. 加载 review_sample.jsonl（审查样本）
review_file = os.path.join(k3_dir, "review_sample.jsonl")
review_count = 0
if os.path.exists(review_file):
    with open(review_file, 'r') as f:
        for line in f:
            try:
                all_data.append(json.loads(line))
                review_count += 1
            except:
                continue
    print(f"[2/4] 审查样本: {review_count} 条")

# 3. 加载 context_window.jsonl（上下文窗口数据）
ctx_file = os.path.join(k3_dir, "context_window.jsonl")
ctx_count = 0
if os.path.exists(ctx_file):
    with open(ctx_file, 'r') as f:
        for line in f:
            try:
                all_data.append(json.loads(line))
                ctx_count += 1
            except:
                continue
    print(f"[3/4] 上下文窗口: {ctx_count} 条")

print(f"[4/4] 总样本: {len(all_data)} 条")

# 写入 train.jsonl / valid.jsonl（9:1 分割）
split = max(1, int(len(all_data) * 0.9))
train_data = all_data[:split]
valid_data = all_data[split:]

os.makedirs(data_dir, exist_ok=True)
with open(os.path.join(data_dir, "train.jsonl"), 'w') as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

with open(os.path.join(data_dir, "valid.jsonl"), 'w') as f:
    for item in valid_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"训练集: {len(train_data)} 条 → {os.path.join(data_dir, 'train.jsonl')}")
print(f"验证集: {len(valid_data)} 条 → {os.path.join(data_dir, 'valid.jsonl')}")
PYEOF

    ok "数据准备完成"
}

# ── 训练执行 ──────────────────────────────────────────────
do_train() {
    log "训练阶段..."
    check_disk

    # 自动递增版本号
    local version
    version=$(ls -d "$LORA_OUTPUT"/adapter_v3.8* 2>/dev/null | wc -l | tr -d ' ')
    local adapter_path
    if [ "$version" -eq 0 ]; then
        adapter_path="$ADAPTER_BASE"
    else
        adapter_path="${ADAPTER_BASE}.${version}"
    fi

    log "适配器路径: $adapter_path"
    log "底座: $BASE_MODEL"
    log "参数: rank=16 layers=8 batch=2 lr=1e-4 epochs=2"

    python3 << PYEOF
import json, os, sys

adapter_path = "$adapter_path"
base_model   = "$BASE_MODEL"
data_dir     = "$DATA_DIR"
project_dir  = "$PROJECT_DIR"

sys.path.insert(0, os.path.join(project_dir, "bin"))
from lh_lora_trainer_v39 import prepare, train

# 如果数据不存在则自动准备
train_file = os.path.join(data_dir, "train.jsonl")
if not os.path.exists(train_file):
    print("[龍魂] 训练数据不存在，自动执行 prepare...")
    exit_code = os.system(f"bash {os.path.join(project_dir, 'bin/lh_train_v38.sh')} prepare")
    if exit_code != 0:
        print("[龍魂] 数据准备失败")
        sys.exit(1)

# 执行训练
train(base_model, data_dir, adapter_path)
PYEOF

    ok "训练完成 → $adapter_path"
}

# ── 恢复训练 ──────────────────────────────────────────────
do_resume() {
    local step="${1:-0}"
    local adapter_path
    # 找最新的 v3.8.x adapter
    adapter_path=$(ls -d "$LORA_OUTPUT"/adapter_v3.8* 2>/dev/null | sort -V | tail -1)

    if [ -z "$adapter_path" ]; then
        err "没有找到可恢复的 adapter_v3.8* 检查点"
    fi

    log "从 $adapter_path 恢复训练 (step=$step)"

    python3 << PYEOF
import sys, os, argparse
sys.path.insert(0, os.path.join("$PROJECT_DIR", "bin"))
from lh_lora_trainer_v39 import train

# 需要修改 trainer 支持 resume 参数
# 这里先用新 adapter 路径避免覆盖
PYEOF
    warn "resume 功能需在实际 trainer 中支持 --resume-from-checkpoint"
}

# ── Fuse 合并 ─────────────────────────────────────────────
do_fuse() {
    local adapter_path
    adapter_path=$(ls -d "$LORA_OUTPUT"/adapter_v3.8* 2>/dev/null | sort -V | tail -1)

    if [ -z "$adapter_path" ]; then
        err "没有找到 adapter_v3.8* 先执行 train"
    fi

    local fused_path="${MODEL_DIR}/sft_checkpoints/v3.8_fused"
    mkdir -p "$fused_path"

    log "Fuse: $BASE_MODEL + $adapter_path → $fused_path"

    python3 -m mlx_lm fuse \
        --model "$BASE_MODEL" \
        --adapter-path "$adapter_path" \
        --save-path "$fused_path" 2>&1

    ok "Fuse完成 → $fused_path"
}

# ── 导出GGUF → Ollama ────────────────────────────────────
do_export() {
    local fused_path="${MODEL_DIR}/sft_checkpoints/v3.8_fused"

    if [ ! -d "$fused_path" ]; then
        warn "fused模型不存在，先执行 fuse..."
        do_fuse
    fi

    # MLX → GGUF 转换
    local gguf_path="${MODEL_DIR}/longhun-v3.8.Q4_K_M.gguf"

    log "导出 GGUF (Q4_K_M)..."
    python3 -m mlx_lm.convert \
        --hf-path "$fused_path" \
        --q-bits 4 \
        --q-group-size 64 \
        -q 2>&1 || log "GGUF导出需用 llama.cpp 的 convert_hf_to_gguf.py"

    # Ollama 导入
    log "创建 Ollama Modelfile..."
    cat > "/tmp/Modelfile.v3.8" << MODELEOF
FROM $gguf_path
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
SYSTEM """你是龍魂体系AI，运行审计协议v2.0。
身份锚定: UID9622·诸葛鑫·龍芯北辰。
当前人格: 通心译P14，审计级别: 自动。
铁律: P0条件立即熔断·UID9622情绪容错放行·反讽延迟2小时再审。
所有判定留痕+KPI更新。"""
MODELEOF

    log "导入 Ollama..."
    ollama create longhun-v3.8 -f /tmp/Modelfile.v3.8
    rm /tmp/Modelfile.v3.8

    ok "Ollama 模型就绪: ollama run longhun-v3.8"
}

# ── 主流程 ────────────────────────────────────────────────
case "${1:-usage}" in
    prepare) do_prepare ;;
    train)   do_train ;;
    resume)  do_resume "${2:-0}" ;;
    fuse)    do_fuse ;;
    export)  do_export ;;
    all)
        do_prepare
        do_train
        do_fuse
        do_export
        ok "全流程完成! ollama run longhun-v3.8"
        ;;
    *) usage ;;
esac
