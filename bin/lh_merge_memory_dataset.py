#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-19-MERGE-MEMORY-DATASET-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
合并 v3.7 稳定数据 + 全记忆 ingestion 数据 → v4.0.6 训练集
DNA: #龍芯⚡️2026-07-19-MERGE-MEMORY-DATASET-v1.0
"""

import json
import random
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "memory_ingested_data_v1.0"

v37_train = PROJECT / "models" / "longhun-v1.0" / "lora_output_v405" / "data_v405" / "train.jsonl"
v37_val = PROJECT / "models" / "longhun-v1.0" / "lora_output_v405" / "data_v405" / "valid.jsonl"
mem_train = OUT / "train.jsonl"
mem_val = OUT / "valid.jsonl"

def load(path: Path):
    samples = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except Exception:
                pass
    return samples

v37 = load(v37_train) + load(v37_val)
mem = load(mem_train) + load(mem_val)

print(f"v3.7 数据: {len(v37)}")
print(f"记忆数据: {len(mem)}")

# 给记忆样本补默认 metadata
for s in mem:
    if "metadata" not in s:
        s["metadata"] = {"domain": "memory_ingested"}

# 合并、去重（assistant 内容 hash）
seen = set()
uniq = []
for s in v37 + mem:
    key = json.dumps(s["messages"], ensure_ascii=True, sort_keys=True)
    if key not in seen:
        seen.add(key)
        uniq.append(s)

print(f"合并去重后: {len(uniq)}")

random.seed(42)
random.shuffle(uniq)
split = int(len(uniq) * 0.9)
train, val = uniq[:split], uniq[split:]

with open(OUT / "train_v406_merged.jsonl", "w", encoding="utf-8") as f:
    for s in train:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

with open(OUT / "valid_v406_merged.jsonl", "w", encoding="utf-8") as f:
    for s in val:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

domains = Counter(s.get("metadata", {}).get("domain", "unknown").split("_")[0] for s in uniq)
info = {
    "version": "v4.0.6_merged_memory",
    "total_samples": len(uniq),
    "train_samples": len(train),
    "val_samples": len(val),
    "sources": {"v37": len(v37), "memory_ingested": len(mem)},
    "domains": dict(domains),
}
with open(OUT / "dataset_info_v406_merged.json", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

print(f"✅ 合并完成: {len(train)} 训练 / {len(val)} 验证")
print(f"域分布: {dict(domains.most_common(10))}")
