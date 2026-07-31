#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂湍流治理引擎 · 性能基准 v1.0
DNA: #龍芯⚡️丙午·乙未·辛酉·井-TURBULENCE-BENCHMARK-v1.0
"""

import sys
import time
import json
import random
import numpy as np
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.turbulence import (
    AnchorDiscovery, SevenFactor, PersonaRouter,
    LayeredProtocol, DNAAuditLoop,
    WeightLearner, PersonaMatrixLearner, ThresholdController, SocialReynolds,
    TurbulenceGovernor
)
from engines.turbulence.lh_layered_protocol import ProtocolLevel


def benchmark_anchor_discovery(n_trials: int = 1000) -> dict:
    engine = AnchorDiscovery(space_dim=5, q=0.5, max_iter=30, epsilon=1e-4)
    t0 = time.perf_counter()
    for _ in range(n_trials):
        engine.discover_all(initial_guess=np.random.randn(5))
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_seven_factor(n_trials: int = 1000) -> dict:
    engine = SevenFactor()
    fps = [engine.register(f"u{i}", [random.random() for _ in range(7)]) for i in range(n_trials)]
    t0 = time.perf_counter()
    engine.detect_water_army(fps, min_cluster_size=3)
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_persona_router(n_trials: int = 1000) -> dict:
    engine = PersonaRouter()
    scenes = [np.random.rand(5) for _ in range(n_trials)]
    t0 = time.perf_counter()
    for s in scenes:
        engine.route(s)
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_layered_protocol(n_trials: int = 1000) -> dict:
    engine = LayeredProtocol()
    t0 = time.perf_counter()
    for i in range(n_trials):
        engine.add_rule(f"P2-{i:04d}", ProtocolLevel.P2,
                        f"规则{i}", f"#DNA-{i}")
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_dna_audit(n_trials: int = 1000) -> dict:
    audit = DNAAuditLoop(epsilon_0=0.15, kappa=1)
    t0 = time.perf_counter()
    for i in range(n_trials):
        proj = audit.issue_projection(
            prediction=0.8 + i * 0.001,
            persona_channel="P01",
            anchor_level=3,
            rules_applied=["R-001"],
            weights=[1 / 7] * 7
        )
        audit.verify(proj.projection_id, actual_value=0.81 + i * 0.001)
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_param_learner(n_trials: int = 1000) -> dict:
    wl = WeightLearner()
    t0 = time.perf_counter()
    for i in range(n_trials):
        wl.update([random.random() for _ in range(7)], error=random.random() * 0.5)
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_social_reynolds(n_trials: int = 1000) -> dict:
    sr = SocialReynolds(Re_c=100.0)
    t0 = time.perf_counter()
    for _ in range(n_trials):
        sr.compute(v=random.random() * 1000, L=random.random() * 100000,
                   rational_ratio=random.random(), transparency=random.random())
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def benchmark_governor(n_trials: int = 100) -> dict:
    gov = TurbulenceGovernor()
    t0 = time.perf_counter()
    for _ in range(n_trials):
        gov.assess(
            social_velocity=random.random() * 1000,
            social_scope=random.random() * 100000,
            rational_ratio=random.random(),
            transparency=random.random()
        )
    elapsed = time.perf_counter() - t0
    return {"ops": n_trials, "time_ms": elapsed * 1000, "ops_per_sec": n_trials / elapsed}


def main():
    sizes = [100, 1000, 10000]
    report = {
        "dna": "#龍芯⚡️丙午·乙未·辛酉·井-TURBULENCE-BENCHMARK-v1.0",
        "generated_at": datetime.now().isoformat(),
        "platform": "macOS M4 Max",
        "engines": {}
    }

    benchmarks = {
        "anchor_discovery": benchmark_anchor_discovery,
        "seven_factor": benchmark_seven_factor,
        "persona_router": benchmark_persona_router,
        "dna_audit": benchmark_dna_audit,
        "param_learner": benchmark_param_learner,
        "social_reynolds": benchmark_social_reynolds,
        "governor": benchmark_governor,
    }

    for name, func in benchmarks.items():
        report["engines"][name] = {}
        for size in sizes:
            if name == "governor" and size > 1000:
                continue
            result = func(size)
            report["engines"][name][str(size)] = result
            print(f"{name:20s} n={size:6d}  {result['time_ms']:10.2f} ms  {result['ops_per_sec']:10.2f} ops/s")

    out_dir = PROJECT_ROOT / "_work" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "turbulence_benchmark.json"
    with open(out_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {out_path}")


if __name__ == "__main__":
    main()
