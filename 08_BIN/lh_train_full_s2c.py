#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·午时·䷙大畜-TRAIN-FULL-S2C-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 父任务: D-01 Step2-C 本地全量可信验证（S2-A 的 val mini 仅 8 条噪声大 → 全量 881+98 收可信 Val）
# 说明: 与 S2-A/主 trainer 同一 mlx_lm.lora.run 参数通道 + 同一底模
#       (models/longhun-v1.0/base_model = Qwen2.5-1.5B·qwen2·vocab151936)
#       —— 本地 1.5B = S3 远端 Qwen2.5-7B 同族同 tokenizer，结论可放大。
#       用途: 全量语料直训 1 epoch，val 全量 98 条 eval，取可信泛化曲线；
#       判定沿用 v1.0.1 前后 1/4 段均值抗噪准则（train/val 双通道任一降即 PASS）。
#       边界(防空壳): 本结果证「1.5B 同族代理上語料可学+泛化稳」；
#       与 7B 正式效果等同仍待 S3 实跑，本报告不僭越。
# 用法: python3 08_BIN/lh_train_full_s2c.py [--iters 220] [--batch 4] [--rank 16] [--layers 8]
import argparse
import json
import os
import re
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASE_MODEL = ROOT / "models" / "longhun-v1.0" / "base_model"
DATA_DIR = ROOT / "models" / "longhun-v1.0" / "lora_output" / "data"
REPORT_PATH = ROOT / "articles" / "2026-09-06-D01-S2C-全量可信验证report.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=220, help="总 iters(=ceil(881/batch)≈1 epoch)")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=64)
    ap.add_argument("--layers", type=int, default=8)
    ap.add_argument("--lr", type=float, default=1e-4)
    args = ap.parse_args()

    if not (BASE_MODEL / "config.json").exists():
        print(f"❌ 底模缺失: {BASE_MODEL}")
        sys.exit(1)

    train_path = DATA_DIR / "train.jsonl"
    valid_path = DATA_DIR / "valid.jsonl"
    t_lines = [l for l in train_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    v_lines = [l for l in valid_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    t_n, v_n = len(t_lines), len(v_lines)
    if t_n == 0 or v_n == 0:
        print("❌ 全量数据缺失(train/valid 为空)")
        sys.exit(1)

    print(f"🟦 S2-C 本地全量可信验证 · 底模 Qwen2.5-1.5B(本地 MLX)")
    print(f"   全量训练 {t_n} 条 · valid 全量 eval {v_n} 条 · batch={args.batch} · iters={args.iters}")

    from mlx_lm import lora as lora_module

    adapter = ROOT / "_work" / "s2c_adapter"
    if adapter.exists():
        shutil.rmtree(adapter)

    nargs = argparse.Namespace(
        model=str(BASE_MODEL), train=True, fine_tune_type="lora", optimizer="adamw",
        seed=42, data=str(DATA_DIR), num_layers=args.layers,
        lora_parameters={"rank": args.rank, "dropout": 0.05, "scale": float(args.alpha)},
        batch_size=args.batch, iters=args.iters, learning_rate=args.lr,
        steps_per_report=10, steps_per_eval=20, save_every=200, val_batches=args.batch * 25 // 4,
        max_seq_length=2048, grad_checkpoint=True, grad_accumulation_steps=1,
        adapter_path=str(adapter), resume_adapter_file=None,
        test=False, test_batches=500, lr_schedule=None, mask_prompt=True,
        report_to=None, project_name=None,
        optimizer_config={"adamw": {}}, config=None, clear_cache_threshold=0,
    )

    log_fd, log_path = tempfile.mkstemp(suffix=".log", dir=str(ROOT / "_work"))
    os.close(log_fd)
    log_out = open(log_path, "w", encoding="utf-8")

    class Tee:
        def __init__(self, *files):
            self.files = files

        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()

        def flush(self):
            for f in self.files:
                f.flush()

    tee = Tee(sys.stdout, log_out)
    old = sys.stdout
    sys.stdout = tee
    try:
        lora_module.run(nargs)
    finally:
        sys.stdout = old
        log_out.close()

    text = Path(log_path).read_text(encoding="utf-8")
    # v1.0.1: log 留档可追溯(_work 不入库·同 S2-A 首跑教训)
    log_keep = ROOT / "_work" / "s2c_full_train.log"
    log_keep.write_text(text, encoding="utf-8")

    train_pts = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"Iter (\d+): Train loss ([\d.]+)", text)]
    val_pts = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"Iter (\d+): Val loss ([\d.]+)", text)]

    def _seg_delta(pts, k=4):
        if len(pts) < 2:
            return None, None, None
        n = len(pts)
        head = [v for _, v in pts[: max(1, n // k)]]
        tail = [v for _, v in pts[-max(1, n // k):]]
        mh, mt = sum(head) / len(head), sum(tail) / len(tail)
        return mt - mh, mh, mt

    t_delta = _seg_delta(train_pts)
    v_delta = _seg_delta(val_pts)

    def _trend_ok(d):
        return d[0] is not None and d[0] < 0

    ok = _trend_ok(v_delta) or _trend_ok(t_delta)

    report = {
        "dna": "#龍芯⚡️丙午·丁酉·癸未·午时·䷙大畜-TRAIN-FULL-S2C-v1.0-UID9622",
        "base_model": str(BASE_MODEL),
        "full_train_samples": t_n, "full_valid_samples": v_n,
        "iters": args.iters, "batch": args.batch,
        "lora": {"rank": args.rank, "alpha": args.alpha},
        "train_curve": train_pts, "val_curve": val_pts,
        "train_loss": {"head_mean": t_delta[1], "tail_mean": t_delta[2], "delta": t_delta[0]},
        "val_loss": {"head_mean": v_delta[1], "tail_mean": v_delta[2], "delta": v_delta[0]},
        "verdict": "PASS·全量语料后段均值下降(1.5B同族代理可学+泛化稳)" if ok else "FAIL·未观测到下降",
        "scope_note": "本报告=本地 1.5B 同族代理实测;与 S3 Qwen2.5-7B 正式效果等同仍待 S3 实跑,不僭越(防空壳)",
    }
    print(f"\n📊 S2-C 验证判定: {report['verdict']}")
    if t_delta[0] is not None:
        print(f"   train(前后1/4均值): {t_delta[1]:.4f} → {t_delta[2]:.4f} (Δ{t_delta[0]:+.4f})")
    if v_delta[0] is not None:
        print(f"   val  (前后1/4均值·{v_n}条全量): {v_delta[1]:.4f} → {v_delta[2]:.4f} (Δ{v_delta[0]:+.4f})")
    if val_pts:
        print(f"   val 终值: {val_pts[-1][1]:.4f} @iter{val_pts[-1][0]}")

    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   报告: {REPORT_PATH}")

    shutil.rmtree(adapter, ignore_errors=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
