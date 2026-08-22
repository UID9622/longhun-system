#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-TRAIN-DATA-GEN-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""龍魂 · 训练数据生成器 v1.0：难例→可直接喂本地训练的JSONL"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

HOME = Path.home()
HARD_SAMPLES_DIR = HOME / ".longhun" / "behavioral" / "hard_samples"
TRAINING_DATA_DIR = HOME / ".longhun" / "behavioral" / "training_data"
TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)


class TrainDataGenerator:
    def collect_hard_samples(self) -> List[Dict]:
        samples = []
        if not HARD_SAMPLES_DIR.exists():
            return samples
        for jsonl in sorted(HARD_SAMPLES_DIR.glob("*.jsonl")):
            with open(jsonl, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        samples.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return samples

    def generate(self, hard_samples: List[Dict]) -> Dict:
        training_data = {
            "version": "1.0",
            "target_system": "龍魂系统",
            "evaluation_date": datetime.now().isoformat(),
            "dimensions": {},
        }
        for sample in hard_samples:
            dim = sample.get("dimension", "unknown")
            if dim not in training_data["dimensions"]:
                training_data["dimensions"][dim] = {
                    "samples": [],
                    "current_score": round(sample.get("score", 0), 2),
                    "target_score": round(sample.get("threshold", 0.9), 2),
                }
            original = sample.get("original", {})
            training_data["dimensions"][dim]["samples"].append({
                "input": original.get("input", ""),
                "expected": original.get("expected", ""),
                "actual": original.get("actual", ""),
                "score": sample.get("score", 0),
                "pattern": sample.get("pattern", ""),
                "dna": sample.get("dna", ""),
            })
        return training_data

    def save(self, data: Dict, filename: str = "train_dataset.jsonl") -> Path:
        out = TRAINING_DATA_DIR / filename
        with open(out, 'w', encoding='utf-8') as f:
            for dim, info in data["dimensions"].items():
                for sample in info["samples"]:
                    record = {
                        "instruction": f"识别用户意图与上下文（维度: {dim}）",
                        "input": sample["input"],
                        "output": sample.get("expected", ""),
                        "pattern": sample.get("pattern", ""),
                        "dimension": dim,
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return out


if __name__ == "__main__":
    gen = TrainDataGenerator()
    samples = gen.collect_hard_samples()
    if samples:
        data = gen.generate(samples)
        out = gen.save(data)
        total = sum(len(d["samples"]) for d in data["dimensions"].values())
        print(f"✅ 生成训练数据: {total} 条样本 -> {out}")
        for dim, info in data["dimensions"].items():
            print(f"  {dim}: {len(info['samples'])}条 (当前{info['current_score']} → 目标{info['target_score']})")
    else:
        print("⚠️ 暂无难例，先运行: lh-behavioral mine")
        print("   或手工写入日志: ~/.longhun/behavioral/logs/behavioral.log")
