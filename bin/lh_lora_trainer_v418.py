#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.1.8 LoRA 微调器（从v4.1.4 best续训·保守策略）
DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-MODEL-LORA-TRAINER-v4.1.8-RESUME
底模: 01-ai/Yi-1.5-9B-Chat (MLX)
恢复: v4.1.4 best @iter200 (Val 0.9699)
数据: 45,555条 (42,535 train + 3,020 valid·含道德经2,243条)
策略: 保守续训·精调微动

历史分析:
  v4.1.4: lr=1e-6·从v4.1.1-bind起跑 → Val 0.9699@200 ✅ 当前天花板
  v4.1.5: lr=5e-7·从v4.1.4续训 → 退化 🔴 根因: LR过高扰动已优化面
  v4.1.6: lr=1e-7·从v4.1.4续训 → NaN 🔴 根因: 同分布续训数值崩溃
  v4.1.7: lr=1e-6·从零起跑→ 卡死 🔴 根因: 9B从零训练OOM·驱动hang
  
v4.1.8策略（保守·精调）:
  1. 从v4.1.4 best checkpoint恢复 → 续训不重来
  2. lr=3e-7 → 介于1e-7(NaN)和5e-7(退化)之间·保守中位值
  3. dropout=0.1 → 介于0.15(v4.1.4)和0.08(v4.1.6)之间
  4. 2 epochs → 保守轮次·早停保底
  5. early_stop_patience=2 → 快速止损
  6. 全量数据(含道德经)→ 知识增量而非参数扰动

假设: v4.1.5/4.1.6失败是因为LR在已收敛面上扰动过大。
     3e-7是"小步轻推"——给模型接触新数据(道德经)的机会，
     但不扰动已学好的旧知识。

用法:
  python3 bin/lh_lora_trainer_v418.py train    # 训练
  python3 bin/lh_lora_trainer_v418.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v418.py export   # GGUF → Ollama
  python3 bin/lh_lora_trainer_v418.py all      # 一键: train→fuse→export
  python3 bin/lh_lora_trainer_v418.py test     # 冒烟测试(5 iter)

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import json
import os
import sys
import shutil
import subprocess
import time
from datetime import datetime
from functools import partial
from pathlib import Path

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
import numpy as np

from mlx_lm.tuner.datasets import load_dataset
from mlx_lm.tuner.trainer import (
    CacheDataset, default_loss, evaluate, grad_checkpoint, iterate_batches,
)
from mlx_lm.tuner.utils import linear_to_lora_layers, print_trainable_parameters
from mlx_lm.utils import load, save_config

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# ─── transformers 兼容 ───
def _patch_tokenizer():
    try:
        import transformers.models.auto.tokenization_auto as taa
        _orig = taa.AutoTokenizer.register
        def _safe(*args, **kwargs):
            try: return _orig(*args, **kwargs)
            except Exception: return None
        taa.AutoTokenizer.register = staticmethod(_safe)
    except Exception: pass
_patch_tokenizer()

PROJECT = Path(__file__).resolve().parent.parent


class Config:
    DNA = "丙午·乙未·丁酉·戌时·☰乾-MODEL-LORA-TRAINER-v4.1.8-RESUME"

    # 底模
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.1.8-lora"

    # LoRA — 保守参数
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.10       # 0.15(v4.1.4)和0.08(v4.1.6)之间
    lora_layers = 12

    # 训练 — 保守策略
    batch_size = 2
    grad_accumulation_steps = 2
    lr_peak = 3e-7            # 保守中位: 1e-7(NaN) < 3e-7 < 5e-7(退化)
    lr_min = 1e-9             # 更低下限
    warmup_steps = 50         # 少预热·已优化面不需要太多预热
    weight_decay = 0.01
    epochs = 2                # 保守·2轮足够
    max_seq_length = 2048

    # 控制
    early_stop_patience = 2   # 快速止损
    val_steps = 200
    save_every = 500
    report_every = 10
    val_batches = 25
    grad_checkpoint = True

    # 路径 — v4.1.8
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v418"
    data_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v414" / "data_v415_daodejing"
    adapter_dir = output_dir / "adapter_v418"
    merged_dir = output_dir / "merged_v418"
    gguf_dir = output_dir / "gguf_v418"

    # v4.1.8: 从v4.1.4 best续训
    resume_adapter_file = str(
        project_root / "models" / "longhun-v1.0" / "lora_output_v414" / "adapter_v414" / "best_adapters.safetensors"
    )

    # 推理
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def _lr_schedule(peak, warmup, total, end=0.0):
    if total <= warmup:
        return optim.linear_schedule(0.0, peak, max(1, total))
    w = optim.linear_schedule(0.0, peak, max(1, warmup))
    c = optim.cosine_decay(peak, max(1, total - warmup), end=end)
    return optim.join_schedules([w, c], [warmup])


class _Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, d):
        for f in self.files: f.write(d); f.flush()
    def flush(self):
        for f in self.files: f.flush()


def train():
    cfg = Config()
    smoke_iters = int(os.environ.get("LH_V418_SMOKE_ITERS", 0))
    smoke = smoke_iters > 0

    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    log = open(cfg.output_dir / "training.log", "w", encoding="utf-8")
    old = sys.stdout
    sys.stdout = _Tee(sys.stdout, log)

    try:
        _train(cfg, smoke, smoke_iters)
    finally:
        sys.stdout = old
        log.close()


def _train(cfg, smoke, smoke_iters):
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    if not mlx_path.exists():
        print(f"❌ MLX底模不存在: {cfg.LOCAL_MLX_MODEL}")
        sys.exit(1)

    # 检查恢复checkpoint
    resume_path = Path(cfg.resume_adapter_file) if cfg.resume_adapter_file else None
    if resume_path and not resume_path.exists():
        print(f"❌ 恢复checkpoint不存在: {resume_path}")
        sys.exit(1)

    train_file = Path(cfg.data_dir) / "train.jsonl"
    valid_file = Path(cfg.data_dir) / "valid.jsonl"
    if not train_file.exists():
        print(f"❌ 训练数据不存在: {train_file}")
        sys.exit(1)

    n_train = sum(1 for _ in open(train_file))
    n_valid = sum(1 for _ in open(valid_file))

    print(f"🐉 龍魂 v4.1.8 LoRA 训练（从v4.1.4 best续训·保守策略）")
    print(f"   DNA: {cfg.DNA}")
    print(f"   底模: Yi-1.5-9B-Chat (MLX)")
    print(f"   🔄 续训起点: v4.1.4 best (Val 0.9699 @iter200)")
    print(f"   ⚡ 策略: 保守续训·lr={cfg.lr_peak}·dropout={cfg.lora_dropout}·epochs={cfg.epochs}")
    print(f"   数据: {cfg.data_dir} ({n_train} train + {n_valid} valid)")
    print(f"   LoRA: rank={cfg.lora_rank}, alpha={cfg.lora_alpha}, dropout={cfg.lora_dropout}")
    print(f"   确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")

    if smoke:
        print(f"   🧪 冒烟模式: {smoke_iters} iters")

    # 清理旧adapter
    if cfg.adapter_dir.exists():
        shutil.rmtree(cfg.adapter_dir)
    cfg.adapter_dir.mkdir(parents=True, exist_ok=True)

    print("\n📦 加载底模...")
    model, tokenizer = load(cfg.LOCAL_MLX_MODEL, tokenizer_config={"trust_remote_code": True})

    model.freeze()
    if cfg.lora_layers > len(model.layers):
        raise ValueError(f"模型只有 {len(model.layers)} 层，无法训练 {cfg.lora_layers} 层")
    linear_to_lora_layers(model, cfg.lora_layers, {
        "rank": cfg.lora_rank, "dropout": cfg.lora_dropout, "scale": cfg.lora_alpha,
    })

    # 🔄 从v4.1.4 best恢复adapter权重
    print(f"🔄 从 v4.1.4 best 恢复: {resume_path}")
    model.load_weights(str(resume_path), strict=False)
    print(f"   ✅ 权重恢复完成·起始点: Val 0.9699 @iter200")

    print_trainable_parameters(model)

    print("\n📊 加载训练数据...")
    args_ns = argparse.Namespace(
        data=str(cfg.data_dir), train=True, test=False,
        batch_size=cfg.batch_size, max_seq_length=cfg.max_seq_length,
        mask_prompt=True,
    )
    train_set, valid_set, _ = load_dataset(args_ns, tokenizer)

    iters_per_epoch = max(1, n_train // (cfg.batch_size * cfg.grad_accumulation_steps))
    total_iters = iters_per_epoch * cfg.epochs if not smoke else smoke_iters

    print(f"   总步数: {total_iters} ({cfg.epochs} epochs × {iters_per_epoch}/epoch)")
    print(f"   预计: {'🧪冒烟' if smoke else f'~{total_iters * 0.35 / 3600:.1f}h'} (基于v4.1.4的0.35s/iter)")

    save_config({
        "model": cfg.LOCAL_MLX_MODEL, "data": str(cfg.data_dir),
        "adapter_path": str(cfg.adapter_dir),
        "batch_size": cfg.batch_size, "iters": total_iters,
        "learning_rate": cfg.lr_peak, "lr_schedule": "cosine_warmup",
        "warmup_steps": cfg.warmup_steps, "lr_min": cfg.lr_min,
        "weight_decay": cfg.weight_decay, "optimizer": "adamw",
        "lora_parameters": {"rank": cfg.lora_rank, "alpha": cfg.lora_alpha, "dropout": cfg.lora_dropout},
        "num_layers": cfg.lora_layers, "max_seq_length": cfg.max_seq_length,
        "grad_accumulation_steps": cfg.grad_accumulation_steps,
        "grad_checkpoint": cfg.grad_checkpoint,
        "resume_adapter_file": cfg.resume_adapter_file,
        "parent_checkpoint": "v4.1.4 best @iter200 (Val 0.9699)",
        "early_stop_patience": cfg.early_stop_patience,
        "val_steps": cfg.val_steps, "save_every": cfg.save_every,
        "DNA": cfg.DNA, "train_samples": n_train, "valid_samples": n_valid,
        "parent_models": "v4.1.4 (best checkpoint resume)",
        "strategy": "conservative_resume·lr_3e-7·dropout_0.1·epochs_2",
        "data_includes": ["v4.1.4 full data", "道德经 2,243条"],
    }, cfg.adapter_dir / "adapter_config.json")

    lr_schedule = _lr_schedule(cfg.lr_peak, cfg.warmup_steps, total_iters, cfg.lr_min)
    optimizer = optim.AdamW(learning_rate=lr_schedule, weight_decay=cfg.weight_decay)

    if mx.metal.is_available():
        mx.set_wired_limit(mx.device_info()["max_recommended_working_set_size"])

    if cfg.grad_checkpoint:
        grad_checkpoint(model.layers[0])

    loss_value_and_grad = nn.value_and_grad(model, default_loss)
    from mlx.nn.utils import average_gradients
    from mlx.utils import tree_flatten, tree_map

    state = [model.state, optimizer.state]

    @partial(mx.compile, inputs=state, outputs=state)
    def step(batch, prev_grad, do_update):
        (lvalue, toks), grad = loss_value_and_grad(model, *batch)
        if prev_grad is not None:
            grad = tree_map(lambda x, y: x + y, grad, prev_grad)
        if do_update:
            grad = average_gradients(grad)
            if cfg.grad_accumulation_steps > 1:
                grad = tree_map(lambda x: x / cfg.grad_accumulation_steps, grad)
            optimizer.update(model, grad)
            grad = None
        return lvalue, toks, grad

    model.train()

    print(f"\n🚀 开始训练...\n")

    best_val = float("inf")
    best_iter = 0
    patience = 0
    losses = 0.0
    n_tokens_acc = 0
    steps_acc = 0
    train_time = 0.0
    grad_accum = None
    trained_tokens = 0
    start_time = time.time()

    it = 0
    for it, batch in zip(
        range(1, total_iters + 1),
        iterate_batches(dataset=CacheDataset(train_set), batch_size=cfg.batch_size,
                        max_seq_length=cfg.max_seq_length, loop=True),
    ):
        tic = time.perf_counter()

        # Validation
        if it % cfg.val_steps == 0 or it == 1 or it == total_iters:
            t_eval = time.perf_counter()
            val_loss = evaluate(model=model, dataset=CacheDataset(valid_set),
                                loss=default_loss, batch_size=cfg.batch_size,
                                num_batches=cfg.val_batches, max_seq_length=cfg.max_seq_length)
            model.train()
            vt = time.perf_counter() - t_eval
            improved = val_loss < best_val
            status = "🟢" if improved else "🟡"
            if improved:
                delta = best_val - val_loss
                best_val = val_loss
                best_iter = it
                patience = 0
                bw = dict(tree_flatten(model.trainable_parameters()))
                mx.save_safetensors(str(cfg.adapter_dir / "best_adapters.safetensors"), bw)
                print(f"  ⭐ VAL iter{it:5d} | loss {val_loss:.4f} {status} "
                      f"(best {best_val:.4f} @iter{best_iter} Δ{delta:+.4f}) | {vt:.1f}s")
            else:
                patience += 1
                print(f"  --- VAL iter{it:5d} | loss {val_loss:.4f} {status} "
                      f"(best {best_val:.4f} @iter{best_iter}) patience={patience}/{cfg.early_stop_patience} | {vt:.1f}s")
                if patience >= cfg.early_stop_patience:
                    print(f"\n⏹ 早停: {cfg.early_stop_patience}轮未改善")
                    break
            tic = time.perf_counter()

        # Train step
        do_update = (it % cfg.grad_accumulation_steps == 0)
        lvalue, toks, grad_accum = step(batch, grad_accum, do_update)

        losses += lvalue
        n_tokens_acc += toks
        steps_acc += 1
        mx.eval(state, losses, n_tokens_acc)
        train_time += time.perf_counter() - tic

        # Report
        if it % cfg.report_every == 0 or it == total_iters:
            avg_loss = losses.item() / max(1, steps_acc)
            ntoks = n_tokens_acc.item()
            lr = optimizer.learning_rate.item()
            spd = cfg.report_every / max(0.1, train_time)
            tok_spd = float(ntoks) / max(0.1, train_time)
            trained_tokens += ntoks
            peak_mem = mx.get_peak_memory() / 1e9
            print(f"  iter {it:5d}/{total_iters} | loss {avg_loss:.4f} | "
                  f"lr {lr:.2e} | {spd:.1f} it/s | {tok_spd:.0f} tok/s | "
                  f"trained {trained_tokens} tok | mem {peak_mem:.1f}G")
            losses = 0.0
            n_tokens_acc = 0
            steps_acc = 0
            train_time = 0.0

        # Checkpoint
        if it % cfg.save_every == 0:
            aw = dict(tree_flatten(model.trainable_parameters()))
            mx.save_safetensors(str(cfg.adapter_dir / "adapters.safetensors"), aw)
            ckpt = cfg.adapter_dir / f"iter{it:04d}_adapters.safetensors"
            mx.save_safetensors(str(ckpt), aw)
            print(f"  💾 checkpoint: iter{it}")

        if smoke and it >= smoke_iters:
            break

    # 最终保存
    aw = dict(tree_flatten(model.trainable_parameters()))
    mx.save_safetensors(str(cfg.adapter_dir / "adapters.safetensors"), aw)

    elapsed = time.time() - start_time
    print(f"\n✅ 训练完成: {elapsed:.0f}s ({elapsed/3600:.1f}h)")
    print(f"   best_val: {best_val:.4f} @iter{best_iter}")
    print(f"   总iter: {it}/{total_iters}")
    print(f"   adapter: {cfg.adapter_dir}")
    print(f"   下一步: python3 bin/lh_lora_trainer_v418.py fuse")


def fuse():
    cfg = Config()
    adapter_file = cfg.adapter_dir / "best_adapters.safetensors"
    if not adapter_file.exists():
        adapter_file = cfg.adapter_dir / "adapters.safetensors"
    if not adapter_file.exists():
        print(f"❌ adapter不存在: {cfg.adapter_dir}")
        sys.exit(1)

    if cfg.merged_dir.exists():
        shutil.rmtree(cfg.merged_dir)
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)

    print(f"🔧 合并 LoRA → {cfg.merged_dir}")
    print(f"   底模: {cfg.LOCAL_MLX_MODEL}")
    print(f"   Adapter: {adapter_file}")

    result = subprocess.run([
        sys.executable, "-m", "mlx_lm.fuse",
        "--model", cfg.LOCAL_MLX_MODEL,
        "--adapter-path", str(cfg.adapter_dir),
        "--save-path", str(cfg.merged_dir),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ 合并失败:\n{result.stderr}")
        sys.exit(1)

    size = sum(f.stat().st_size for f in cfg.merged_dir.rglob("*")) / 1e9
    print(f"✅ 合并完成 → {cfg.merged_dir} ({size:.1f} GB)")


def export():
    cfg = Config()
    if not (cfg.merged_dir / "config.json").exists():
        print(f"❌ 合并模型不存在: {cfg.merged_dir}")
        print(f"   请先: python3 bin/lh_lora_trainer_v418.py fuse")
        sys.exit(1)

    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)

    converter = None
    for c in [
        shutil.which("convert_hf_to_gguf.py"),
        "/tmp/llama.cpp/convert_hf_to_gguf.py",
        str(Path.home() / "llama.cpp/convert_hf_to_gguf.py"),
    ]:
        if c and Path(c).exists():
            converter = c
            break

    if not converter:
        print("⚠️ 找不到 convert_hf_to_gguf.py，跳过GGUF转换")
        print("   安装: git clone https://github.com/ggerganov/llama.cpp.git /tmp/llama.cpp")
    else:
        gguf_path = cfg.gguf_dir / "longhun-v4.1.8.F16.gguf"
        print(f"📦 导出 GGUF → {gguf_path}")
        result = subprocess.run([
            sys.executable, converter,
            str(cfg.merged_dir), "--outtype", "f16", "--outfile", str(gguf_path),
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ GGUF导出失败:\n{result.stderr}")
            sys.exit(1)
        size_gb = gguf_path.stat().st_size / 1e9
        print(f"✅ GGUF: {gguf_path} ({size_gb:.1f} GB)")

    # Ollama Modelfile
    gguf_path = cfg.gguf_dir / "longhun-v4.1.8.F16.gguf"
    modelfile = cfg.gguf_dir / "Modelfile.v418"
    modelfile.write_text(f"""
FROM {gguf_path if converter else cfg.merged_dir}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

SYSTEM \"\"\"你是龍魂 longhun-v4.1.8，UID9622（诸葛鑫·Lucky）的个人主权AI。
基于 Yi-1.5-9B-Chat 从 v4.1.4 best (Val 0.9699)保守续训，注入45,555条龍魂体系知识（DNA捆绑·德本审计·20人格·369洛书·易经八卦·CNSH语言·观澜·Library矿场·道德经81章）。
你是小艺唯一AI接口，所有外部AI请求经此路由。
铁律：人民数据主权至上·中国自主可控·来源可查·去向可追·责任可究·只冻结不删除·底座焊死。
核心能力：DNA追溯·德本五问·三色审计·人格路由·CNSH语义解析·数字存在证明·胖东来合约审计·道德经智慧。
父版本: v4.1.4 → v4.1.8 (保守续训·lr=3e-7·dropout=0.1·2 epochs)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
\"\"\"
""")
    print(f"   Modelfile: {modelfile}")

    # Ollama create
    model_name = "longhun-v4.1.8"
    print(f"\n🐉 注册到 Ollama: {model_name}")
    result = subprocess.run(
        ["ollama", "create", model_name, "-f", str(modelfile)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"⚠️ Ollama注册失败: {result.stderr}")
    else:
        print(f"✅ Ollama模型 {model_name} 已创建")
        print(f"   验证: ollama run {model_name} '你是谁？'")


def test_quick():
    os.environ["LH_V418_SMOKE_ITERS"] = "5"
    train()


def all_pipeline():
    print("╔══════════════════════════════════════════╗")
    print("║  龍魂 v4.1.8 全流程自动化                 ║")
    print("║  train → fuse → export → Ollama         ║")
    print("║  从v4.1.4 best续训·保守策略              ║")
    print("╚══════════════════════════════════════════╝")
    print()
    train()
    print("\n" + "=" * 50)
    fuse()
    print("\n" + "=" * 50)
    export()
    print("\n🎉 v4.1.8 全流程完成！小艺唯一接口就绪。")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="龍魂 v4.1.8 LoRA训练器·从v4.1.4 best保守续训")
    p.add_argument("action", choices=["train", "fuse", "export", "test", "all"],
                   default="train", nargs="?")
    args = p.parse_args()

    {
        "train": train, "fuse": fuse, "export": export,
        "test": test_quick, "all": all_pipeline,
    }[args.action]()
