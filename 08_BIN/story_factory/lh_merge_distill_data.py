# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-8d3cfcc9
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-MERGE-DISTILL-v1.0
"""
把 K3 蒸馏生成的编剧训练样本合并进 longhun-small-instruct-v1.3 训练池，
按 DNA 去重，并切分验证集。
"""

import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime

FACTORY_ROOT = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = "~/longhun-system/models/longhun-small-instruct-v1.3/data"


def dna_key(sample: dict) -> str:
    """用 system+user+assistant 内容做去重键。"""
    msgs = sample.get("messages", [])
    text = "\n".join(m.get("content", "") for m in msgs)
    return hashlib.md5(text.encode()).hexdigest()


def merge(
    distill_file: str,
    train_dir: str = DEFAULT_TRAIN_DIR,
    val_ratio: float = 0.1,
    dry_run: bool = False,
):
    train_dir = Path(train_dir).expanduser().resolve()
    train_file = train_dir / "train.jsonl"
    valid_file = train_dir / "valid.jsonl"

    # 加载现有训练数据
    existing = []
    if train_file.exists():
        with open(train_file, "r", encoding="utf-8") as f:
            existing = [json.loads(l) for l in f if l.strip()]
    existing_keys = {dna_key(s) for s in existing}
    print(f"📦 现有训练样本: {len(existing)} 条")

    # 加载蒸馏样本
    distill_path = Path(distill_file).expanduser().resolve()
    new_samples = []
    with open(distill_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            s = json.loads(line)
            key = dna_key(s)
            if key in existing_keys:
                print(f"⏭️  跳过重复样本: {s.get('dna','')}")
                continue
            new_samples.append(s)
            existing_keys.add(key)

    print(f"🆕 新增编剧样本: {len(new_samples)} 条")
    if not new_samples:
        print("✅ 无新增样本，无需合并")
        return

    # 拆训练/验证
    split_at = max(1, int(len(new_samples) * (1 - val_ratio)))
    train_new = new_samples[:split_at]
    valid_new = new_samples[split_at:]

    print(f"   → 训练集新增: {len(train_new)} 条")
    print(f"   → 验证集新增: {len(valid_new)} 条")

    if dry_run:
        print("🧪 dry-run 模式，不写入文件")
        return

    # 追加写入
    with open(train_file, "a", encoding="utf-8") as f:
        for s in train_new:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    with open(valid_file, "a", encoding="utf-8") as f:
        for s in valid_new:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"✅ 合并完成: {train_file} +{len(train_new)}, {valid_file} +{len(valid_new)}")


def main():
    parser = argparse.ArgumentParser(description="合并 K3 蒸馏样本到训练池")
    parser.add_argument("--distill-file", required=True, help="蒸馏训练样本 jsonl 路径")
    parser.add_argument("--train-dir", default=DEFAULT_TRAIN_DIR, help="训练数据目录")
    parser.add_argument("--val-ratio", type=float, default=0.1, help="验证集比例")
    parser.add_argument("--dry-run", action="store_true", help="试运行不写入")
    args = parser.parse_args()
    merge(args.distill_file, args.train_dir, args.val_ratio, args.dry_run)


if __name__ == "__main__":
    main()
