#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-CODEBUDDY-CORPUS-INGEST-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
吸收 CodeBuddy 训练语料（training_corpus_v3.0.md + training_corpus_full.md）
转为龍魂训练池 JSONL。

策略：
- 按 "## FILE:" 切分大文件
- 过滤过短/过长/重复片段
- 每个文件生成一个 "请复述/输出该文件内容" 的 instruction sample
- capped 采样，防止语料压倒其他训练数据

DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-CODEBUDDY-CORPUS-INGEST-v1.0
# STATUS: ⚠️ DEPRECATED · 功能由 engines/lh_fixed_point_memory_archive.py 统一接管
# 保留原因: 历史语料摄入参考，新代码请使用 MemoryArchive.ingest()
"""

import json
import random
import re
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "codebuddy_corpus_ingested"
CORPUS_V3 = PROJECT / "models" / "longhun-v1.0" / "training_corpus_v3.0.md"
CORPUS_FULL = PROJECT / "models" / "longhun-v1.0" / "training_corpus_full.md"

CORE_SYSTEM = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。"
    "人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除。"
)

# 采样上限：v3.0 7627 个文件，但训练池不能让它一家独大
V3_MAX_SAMPLES = 3000
V3_MAX_CHARS_PER_SAMPLE = 4000   # 约 1000-1500 tokens
V3_MIN_CHARS_PER_SAMPLE = 80
FULL_MAX_SAMPLES = 655           # training_corpus_full.md 共 655 行，按主题模块切


def split_by_file_markers(path: Path):
    """流式切分大 md 文件，按 ## FILE: 分段。"""
    if not path.exists():
        return []

    sections = []
    current_path = None
    current_lines = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## FILE:"):
                if current_path and current_lines:
                    sections.append((current_path, "".join(current_lines)))
                current_path = line[len("## FILE:"):].strip()
                current_lines = []
            else:
                current_lines.append(line)

    if current_path and current_lines:
        sections.append((current_path, "".join(current_lines)))

    return sections


def split_full_corpus(path: Path):
    """training_corpus_full.md 是按主题模块组织的，按 # 一级标题切分。"""
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    # 按 \n# 切分，保留标题
    parts = re.split(r"\n(?=# )", text)
    sections = []
    for p in parts:
        p = p.strip()
        if not p or len(p) < V3_MIN_CHARS_PER_SAMPLE:
            continue
        title = p.split("\n")[0].lstrip("# ").strip()
        sections.append((f"training_corpus_full.md/{title}", p))
    return sections


def clean_content(text: str) -> str:
    # 去掉前后空白和大量分隔线
    text = text.strip()
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def make_sample(file_path: str, content: str):
    content = clean_content(content)
    if len(content) > V3_MAX_CHARS_PER_SAMPLE:
        content = content[:V3_MAX_CHARS_PER_SAMPLE] + "\n\n…（已截断，保留核心）"

    prompt = f"请复述龍魂系统文件 `{file_path}` 的内容要点。"

    return {
        "messages": [
            {"role": "system", "content": CORE_SYSTEM},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": content},
        ],
        "metadata": {
            "domain": "codebuddy_corpus",
            "source": f"codebuddy:{Path(file_path).parts[0] if file_path else 'unknown'}",
            "type": "file_recall",
            "file_path": file_path,
        },
    }


def dedup(samples):
    seen = set()
    out = []
    for s in samples:
        key = json.dumps(s["messages"], ensure_ascii=True, sort_keys=True)
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out


def ingest_corpus(path: Path, max_samples: int, label: str):
    print(f"🍽️  摄入 {label}: {path}")
    if label == "v3.0":
        sections = split_by_file_markers(path)
    else:
        sections = split_full_corpus(path)

    print(f"   原始分段: {len(sections)}")

    # 过滤
    filtered = [
        (fp, content) for fp, content in sections
        if V3_MIN_CHARS_PER_SAMPLE <= len(content) <= V3_MAX_CHARS_PER_SAMPLE * 8  # 长内容截断
    ]
    print(f"   长度过滤后: {len(filtered)}")

    # 随机采样
    random.seed(42)
    if len(filtered) > max_samples:
        sampled = random.sample(filtered, max_samples)
    else:
        sampled = filtered

    samples = [make_sample(fp, c) for fp, c in sampled]
    samples = dedup(samples)
    print(f"   去重后样本: {len(samples)}")
    return samples


def main():
    print("=" * 60)
    print("🐉 吸收 CodeBuddy 训练语料")
    print("=" * 60)

    OUT.mkdir(parents=True, exist_ok=True)

    v3_samples = ingest_corpus(CORPUS_V3, V3_MAX_SAMPLES, "v3.0")
    full_samples = ingest_corpus(CORPUS_FULL, FULL_MAX_SAMPLES, "full")

    all_samples = v3_samples + full_samples
    all_samples = dedup(all_samples)

    random.seed(42)
    random.shuffle(all_samples)
    split = int(len(all_samples) * 0.95)
    train, val = all_samples[:split], all_samples[split:]

    with open(OUT / "train.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUT / "valid.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    src_counts = Counter(s["metadata"]["source"] for s in all_samples)
    info = {
        "version": "codebuddy_corpus_v1.0",
        "total_samples": len(all_samples),
        "train_samples": len(train),
        "val_samples": len(val),
        "v3_samples": len(v3_samples),
        "full_samples": len(full_samples),
        "source_distribution": dict(src_counts.most_common(20)),
    }
    with open(OUT / "dataset_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 吸收完成: {len(train)} 训练 / {len(val)} 验证")
    print(f"   输出: {OUT}")
    print(f"   来源分布 Top10: {dict(src_counts.most_common(10))}")


if __name__ == "__main__":
    main()
