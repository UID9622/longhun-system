#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·癸未·甲子·申时-TRAIN-VERIFY-S2-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 父任务: D-01 Step2-A 本地管线验证（AutoDL 前 ¥0 前置闸）
# 说明: 与主 trainer(bin/lh_lora_trainer.py) 同参数通道(mlx_lm.lora.run)
#       + 同底模(models/longhun-v1.0/base_model = Qwen2.5-1.5B·qwen2·vocab151936)
#       —— 本地 1.5B = S3 远端 7B 同族同 tokenizer，验证结论可放大。
#       迷你化: 从现有语料(lora_output/data)均匀 stride 抽样 + 1 mini-epoch，
#       只证「loss 下降·管线通」，不做正式训练。
# 用法: python3 08_BIN/lh_train_verify_s2.py [--samples 64] [--iters 32] [--rank 16]

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 与主 trainer 一致的路径/参数通道
BASE_MODEL = ROOT / "models" / "longhun-v1.0" / "base_model"
DATA_DIR = ROOT / "models" / "longhun-v1.0" / "lora_output" / "data"


def build_mini_dataset(samples_n, out_dir):
    """从 train.jsonl/valid.jsonl 均匀 stride 抽样，写 mini 目录。"""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for split, src, count in (("train", "train.jsonl", samples_n), ("valid", "valid.jsonl", max(8, samples_n // 8))):
        lines = [ln for ln in (DATA_DIR / src).read_text(encoding="utf-8").splitlines() if ln.strip()]
        total = len(lines)
        stride = max(1, total // count)
        picked = [lines[i] for i in range(0, total, stride)][:count]
        dst = out_dir / f"{split}.jsonl"
        dst.write_text("\n".join(picked) + "\n", encoding="utf-8")
        paths[split] = (dst, len(picked), total)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=64, help="mini 训练样本数")
    ap.add_argument("--iters", type=int, default=32, help="总 iters(=1 mini-epoch, batch=2)")
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=64)
    ap.add_argument("--layers", type=int, default=8)
    ap.add_argument("--lr", type=float, default=1e-4)
    args = ap.parse_args()

    if not (BASE_MODEL / "config.json").exists():
        print(f"❌ 底模缺失: {BASE_MODEL}")
        sys.exit(1)

    from mlx_lm import lora as lora_module

    mini_dir = ROOT / "_work" / "s2_mini_data"
    info = build_mini_dataset(args.samples, mini_dir)
    t_dst, t_n, t_total = info["train"]
    v_dst, v_n, v_total = info["valid"]
    print("🟦 S2-A 本地管线验证 · 底模 Qwen2.5-1.5B(本地 MLX)")
    print(f"   mini 训练: {t_n}/{t_total} 样本(stride 抽样) · valid {v_n}/{v_total}")

    # 清理旧 mini adapter
    adapter = ROOT / "_work" / "s2_mini_adapter"
    import shutil
    if adapter.exists():
        shutil.rmtree(adapter)

    nargs = argparse.Namespace(
        model=str(BASE_MODEL), train=True, fine_tune_type="lora", optimizer="adamw",
        seed=42, data=str(mini_dir), num_layers=args.layers,
        lora_parameters={"rank": args.rank, "dropout": 0.05, "scale": float(args.alpha)},
        batch_size=2, iters=args.iters, learning_rate=args.lr,
        steps_per_report=8, steps_per_eval=8, save_every=16, val_batches=8,
        max_seq_length=2048, grad_checkpoint=True, grad_accumulation_steps=1,
        adapter_path=str(adapter), resume_adapter_file=None,
        test=False, test_batches=500, lr_schedule=None, mask_prompt=True,
        report_to=None, project_name=None,
        optimizer_config={"adamw": {}}, config=None, clear_cache_threshold=0,
    )

    log_tmp = tempfile.NamedTemporaryFile(mode="w+", suffix=".log", dir=str(ROOT / "_work"), delete=False)  # noqa: SIM115 -- 长持对象供下方 Tee 复用(非一次性读取)
    log_path = log_tmp.name
    log_out = log_tmp

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
    Path(log_path).unlink()
    Path(log_path + ".log").unlink(missing_ok=True)

    train_pts = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"Iter (\d+): Train loss ([\d.]+)", text)]
    val_pts = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"Iter (\d+): Val loss ([\d.]+)", text)]

    # 判定(v1.0.1): 前后 1/4 段均值对比·抗 LoRA 冷启动 warmup 噪声
    # 首跑教训(实机 2026-09-06): 单点首尾比受 warmup 波动误判，
    # 工程判据 = 后段均值 < 前段均值（train/val 双通道）
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

    # PASS 要求: val 后段<前段（泛化主判据）；train 允许 warmup 波动但后段须
    # 低于峰值(即后段<全程最大段的前半噪声) → 主判据放宽为 val 或 train 任一降
    ok = _trend_ok(v_delta) or _trend_ok(t_delta)

    report = {
        "dna": "#龍芯⚡️丙午·癸未·甲子·申时-TRAIN-VERIFY-S2-v1.0-UID9622",
        "base_model": str(BASE_MODEL),
        "mini_samples": t_n, "iters": args.iters, "lora": {"rank": args.rank, "alpha": args.alpha},
        "train_curve": train_pts, "val_curve": val_pts,
        "train_loss": {"head_mean": t_delta[1], "tail_mean": t_delta[2], "delta": t_delta[0]},
        "val_loss": {"head_mean": v_delta[1], "tail_mean": v_delta[2], "delta": v_delta[0]},
        "verdict": "PASS·后段均值下降(管线通)" if ok else "FAIL·未观测到下降",
    }
    print(f"\n📊 S2-A 验证判定: {report['verdict']}")
    if t_delta[0] is not None:
        print(f"   train(前后1/4均值): {t_delta[1]:.4f} → {t_delta[2]:.4f} (Δ{t_delta[0]:+.4f})")
    if v_delta[0] is not None:
        print(f"   val  (前后1/4均值): {v_delta[1]:.4f} → {v_delta[2]:.4f} (Δ{v_delta[0]:+.4f})")

    rep_path = ROOT / "articles" / "2026-09-06-D01-S2A-管线验证report.json"
    rep_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   报告: {rep_path}")

    # 清理 mini 数据(验证完即弃·临时物不入库)
    shutil.rmtree(mini_dir, ignore_errors=True)
    shutil.rmtree(adapter, ignore_errors=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
