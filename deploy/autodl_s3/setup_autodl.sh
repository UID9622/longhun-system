#!/usr/bin/env bash
# DNA: #龍芯⚡️丙午·丁酉·癸未·未时·䷚颐-S3-AUTODL-SETUP-V0.1-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 作用: AutoDL 实例环境初始化（在实例内运行·root）
#   1) 依赖安装  2) modelscope 拉 Qwen2.5-7B-Instruct(国内镜像)
#   3) S1 词表迁移产物覆盖 tokenizer(vocab 151643→151832)
# 前置: 老大已按 README 把 tokenizer_longhun.json(.report.json) scp 到 /root/autodl-tmp/s3_upload/
set -euo pipefail

echo "== S3 AutoDL 环境初始化 =="
export HF_ENDPOINT=https://hf-mirror.com
export PIP_DISABLE_PIP_VERSION_CHECK=1

MODEL_DIR=/root/autodl-tmp/qwen/Qwen2.5-7B-Instruct
UP_DIR=/root/autodl-tmp/s3_upload
mkdir -p "$UP_DIR" /root/autodl-tmp/qwen

echo "== 1/3 依赖安装(peft/qlora 栈·PyTorch 用镜像自带) =="
pip install -q --upgrade \
  "transformers>=4.44" "peft>=0.12" "bitsandbytes>=0.43" \
  "accelerate>=0.33" "datasets>=2.20" "modelscope>=1.17" \
  "trl>=0.9" 2>&1 | tail -2

echo "== 2/3 权重拉取(Qwen2.5-7B-Instruct·国内镜像) =="
if [ ! -f "$MODEL_DIR/config.json" ]; then
  python3 - <<'PY'
from modelscope import snapshot_download
p = snapshot_download("Qwen/Qwen2.5-7B-Instruct",
                      local_dir="/root/autodl-tmp/qwen/Qwen2.5-7B-Instruct")
print("权重就绪:", p)
PY
else
  echo "权重已存在: $MODEL_DIR (跳过)"
fi

echo "== 3/3 tokenizer 覆盖(S1 v1.1 产物·vocab 151832·先备份) =="
if [ -f "$MODEL_DIR/tokenizer.json" ]; then
  cp "$MODEL_DIR/tokenizer.json" "$MODEL_DIR/tokenizer.json.bak_s1"
fi
cp "$UP_DIR/tokenizer_longhun.json" "$MODEL_DIR/tokenizer.json"
echo "tokenizer 已覆盖(原文件备份为 tokenizer.json.bak_s1)"

python3 - <<PY
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("$MODEL_DIR", trust_remote_code=True)
print("vocab_size =", len(tok))
assert len(tok) == 151832, f"词表应=151832,实得{len(tok)} → 迁移产物未生效,停"
# 抽查注入词可解码(报告词汇表见 tokenizer_longhun_report.json)
print("tokenizer OK · vocab=151832")
PY

echo "== 完成 · 下一步 bash run_sft_7b.sh 4090|3060 =="
