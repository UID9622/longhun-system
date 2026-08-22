#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-HARD-MINING-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""龍魂 · 难例挖掘引擎 v1.0：从行为日志提取识别错误/低分case"""
import json, hashlib, time, os
from pathlib import Path
from datetime import datetime
from typing import Dict, List

HOME = Path.home()
LOG_DIR = HOME / ".longhun" / "behavioral" / "logs"
HARD_SAMPLES_DIR = HOME / ".longhun" / "behavioral" / "hard_samples"
METRICS_DIR = HOME / ".longhun" / "behavioral" / "metrics"
for d in [LOG_DIR, HARD_SAMPLES_DIR, METRICS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


class HardMiningEngine:
    def __init__(self):
        self.dimensions = {
            "intent_recognition": {"threshold": 0.80, "weight": 0.20, "pattern": "intent_mismatch"},
            "context_understanding": {"threshold": 0.88, "weight": 0.20, "pattern": "context_loss"},
            "execution_consistency": {"threshold": 0.95, "weight": 0.15, "pattern": "step_missing"},
            "safety_compliance": {"threshold": 0.99, "weight": 0.15, "pattern": "safety_violation"},
            "feature_extraction": {"threshold": 0.92, "weight": 0.15, "pattern": "feature_miss"},
            "signal_integrity": {"threshold": 0.98, "weight": 0.15, "pattern": "signal_loss"},
        }

    def mine(self, log_file: Path) -> List[Dict]:
        hard_samples = []
        if not log_file.exists():
            return hard_samples
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for dim, config in self.dimensions.items():
                    score = entry.get(dim, 0)
                    if score < config["threshold"] and score > 0:
                        hard_samples.append({
                            "dimension": dim, "score": score,
                            "threshold": config["threshold"], "pattern": config["pattern"],
                            "original": entry,
                            "timestamp": entry.get("timestamp", datetime.now().isoformat()),
                            "dna": self._generate_dna(),
                        })
        return hard_samples

    def save_samples(self, samples: List[Dict]) -> int:
        saved = 0
        for sample in samples:
            dim = sample["dimension"]
            out = HARD_SAMPLES_DIR / f"{dim}.jsonl"
            with open(out, 'a', encoding='utf-8') as f:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            saved += 1
        return saved

    def _generate_dna(self) -> str:
        h = hashlib.sha256(f"HARD{time.time()}{os.urandom(4)}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-HARD-{h}-UID9622"


if __name__ == "__main__":
    engine = HardMiningEngine()
    samples = engine.mine(LOG_DIR / "behavioral.log")
    saved = engine.save_samples(samples)
    print(f"✅ 挖掘到 {len(samples)} 条难例，已保存 {saved} 条")
    by_dim = {}
    for s in samples:
        by_dim[s["dimension"]] = by_dim.get(s["dimension"], 0) + 1
    for dim, cnt in sorted(by_dim.items(), key=lambda x: -x[1]):
        print(f"  {dim}: {cnt}条")
