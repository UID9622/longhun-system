#!/usr/bin/env bash
# DNA: #龍芯⚡️丙午·丁酉·癸未·未时·䷚颐-S3-AUTODL-RUN-V0.1-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: bash run_sft_7b.sh [4090|3060|auto] [epochs]
#   - 4090/auto(≥20G): emb 增量正式模板    - 3060(<20G): 冻结 emb 冒烟模板
# 数据/脚本须已随本目录上传 /root/autodl-tmp/s3_upload/
set -euo pipefail

GPU_HINT=${1:-auto}
EPOCHS=${2:-1}
BASE=/root/autodl-tmp/s3_upload
cd "$BASE"

echo "== S3 qlora SFT · GPU_HINT=$GPU_HINT · epochs=$EPOCHS =="
if [ "$GPU_HINT" != "auto" ]; then
  export LH_S3_GPU_HINT="$GPU_HINT"
fi

# 数据检查: 缺 valid 可只训(train 必在)
[ -f "$BASE/data/train.jsonl" ] || { echo "❌ 缺 train.jsonl → 先上传 data/"; exit 1; }

# v0.2: 显存防碎片(v0.1 60步OOM) + max_len 1536(full_emb 降激活)
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
CUDA_VISIBLE_DEVICES=0 python3 "$BASE/sft_7b.py" \
  --data_dir "$BASE/data" \
  --model_dir /root/autodl-tmp/qwen/Qwen2.5-7B-Instruct \
  --output "$BASE/out_s3" \
  --epochs "$EPOCHS" \
  --max_len 1536

echo "== 完成 · 结果回传: scp -P <port> -r root@<ip>:$BASE/out_s3* . =="
