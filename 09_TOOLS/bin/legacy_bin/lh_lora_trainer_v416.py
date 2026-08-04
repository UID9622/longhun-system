#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.1.6 LoRA 精修器（低LR外科手术·从v4.1.4最佳恢复·修复v4.1.5退化）
DNA: #龍芯⚡️丙午·乙未·丙申·亥时·☰乾-MODEL-LORA-TRAINER-v4.1.6-REFINEMENT
底模: 01-ai/Yi-1.5-9B-Chat (MLX)
恢复: v4.1.4 best adapter (Val 0.9699·当前最佳)
数据: 45,555条 (42,535 train + 3,020 valid·v4.1.4全量+道德经2,243条)
策略: 低LR 1e-7·dropout 0.08·batch 4·3 epochs·早停 patience=5

v4.1.5退化根因:
  1. LR 5e-7 过高 → 从 Val 0.9699 继续训练需要更低LR
  2. Dropout 0.15 破坏性 → fine-tune阶段应 ≤0.08
  3. Batch 2 梯度噪 → batch 4 更稳定
v4.1.6修复:
  LR 1e-7(降5倍) · Dropout 0.08(降47%) · Batch 4(翻倍) · Epochs 3(+1轮)
  Early Stop patience=5(放宽) · 外科手术式精修

用法:
  python3 bin/lh_lora_trainer_v416.py train    # 训练
  python3 bin/lh_lora_trainer_v416.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v416.py export   # GGUF → Ollama
  python3 bin/lh_lora_trainer_v416.py all      # 一键: train→fuse→export
  python3 bin/lh_lora_trainer_v416.py test     # 冒烟测试(5 iter)

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
    DNA = "丙午·乙未·丙申·亥时·☰乾-MODEL-LORA-TRAINER-v4.1.6-REFINEMENT"

    # 底模
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.1.6-lora"

    # LoRA — 继承v4.1.4/4.1.5 rank/alpha，降低dropout
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.08      # 🔧 v4.1.5=0.15 → 0.08（保护已有知识）
    lora_layers = 12

    # 训练 — 精细微调参数
    batch_size = 4            # 🔧 v4.1.5=2 → 4（梯度更稳定）
    grad_accumulation_steps = 1
    lr_peak = 1e-7            # 🔧 v4.1.5=5e-7 → 1e-7（外科手术式微调）
    lr_min = 1e-9             # 🔧 v4.1.5=1e-8 → 1e-9（更低终点）
    warmup_steps = 80         # 🔧 v4.1.5=50 → 80（更平滑预热）
    weight_decay = 0.01
    epochs = 3                # 🔧 v4.1.5=2 → 3（低LR需要更多轮）
    max_seq_length = 2048

    # 控制
    early_stop_patience = 5   # 🔧 v4.1.5=3 → 5（给低LR更多耐心）
    val_steps = 200
    save_every = 500
    report_every = 10
    val_batches = 25
    grad_checkpoint = True

    # 路径 — v4.1.6
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v416"
    data_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v414" / "data_v415_daodejing"
    adapter_dir = output_dir / "adapter_v416"
    merged_dir = output_dir / "merged_v416"
    gguf_dir = output_dir / "gguf_v416"

    # 恢复点: v4.1.4 best (Val 0.9699·追平v4.1.1-bind)
    v414_best = (
        project_root / "models" / "longhun-v1.0" / "lora_output_v414"
        / "adapter_v414" / "best_adapters.safetensors"
    )
    v414_final = (
        project_root / "models" / "longhun-v1.0" / "lora_output_v414"
        / "adapter_v414" / "adapters.safetensors"
    )
    # v4.1.1-bind 作为后备
    v411_bind_best = (
        project_root / "models" / "longhun-v1.0" / "lora_output_v411_bind"
        / "adapter_v411_bind" / "best_adapters.safetensors"
    )

    if v414_best.exists():
        resume_adapter_file = str(v414_best)
        resume_source = "v4.1.4 best (Val 0.9699)"
    elif v414_final.exists():
        resume_adapter_file = str(v414_final)
        resume_source = "v4.1.4 final"
    elif v411_bind_best.exists():
        resume_adapter_file = str(v411_bind_best)
        resume_source = "v4.1.1-bind best (Val 0.9659)"
    else:
        resume_adapter_file = None
        resume_source = "无（从头训练）"

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
    smoke_iters = int(os.environ.get("LH_V416_SMOKE_ITERS", 0))
    smoke = smoke_iters > 0

    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    mode = "w" if not Path(cfg.adapter_dir / "adapters.safetensors").exists() else "a"
    log = open(cfg.output_dir / "training.log", mode, encoding="utf-8")
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

    train_file = Path(cfg.data_dir) / "train.jsonl"
    valid_file = Path(cfg.data_dir) / "valid.jsonl"
    if not train_file.exists():
        print(f"❌ 训练数据不存在: {train_file}")
        sys.exit(1)

    n_train = sum(1 for _ in open(train_file))
    n_valid = sum(1 for _ in open(valid_file))

    print(f"🐉 龍魂 v4.1.6 LoRA 精修训练（低LR外科手术·修复v4.1.5退化）")
    print(f"   DNA: {cfg.DNA}")
    print(f"   底模: Yi-1.5-9B-Chat (MLX)")
    print(f"   恢复: {cfg.resume_source} → {cfg.resume_adapter_file}")
    print(f"   数据: {cfg.data_dir}")
    print(f"   LR: {cfg.lr_peak:.0e} (vs v4.1.5=5e-7·降5倍), Epochs: {cfg.epochs}, Batch: {cfg.batch_size}")
    print(f"   训练集: {n_train} 条 (+2,243道德经) | 验证集: {n_valid} 条 (+337道德经)")
    print(f"   LoRA: rank={cfg.lora_rank}, alpha={cfg.lora_alpha}, dropout={cfg.lora_dropout}")
    print(f"   早停: patience={cfg.early_stop_patience} (vs v4.1.5=3·放宽)")

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

    resume = cfg.resume_adapter_file
    if resume and Path(resume).exists():
        print(f"🔄 从 {cfg.resume_source} 恢复: {resume}")
        model.load_weights(resume, strict=False)
    else:
        print("⚠️ 无恢复点，从头训练（不推荐）")

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
        "resume_adapter_file": resume,
        "resume_source": cfg.resume_source,
        "early_stop_patience": cfg.early_stop_patience,
        "val_steps": cfg.val_steps, "save_every": cfg.save_every,
        "DNA": cfg.DNA, "train_samples": n_train, "valid_samples": n_valid,
        "daodejing_samples": 2243,
        "v415_degradation_fix": {
            "lr_peak": "5e-7→1e-7",
            "dropout": "0.15→0.08",
            "batch_size": "2→4",
            "epochs": "2→3",
            "early_stop_patience": "3→5",
            "warmup_steps": "50→80",
            "lr_min": "1e-8→1e-9",
        },
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

    print(f"\n🚀 开始精修训练...\n")

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
                best_val = val_loss
                best_iter = it
                patience = 0
                bw = dict(tree_flatten(model.trainable_parameters()))
                mx.save_safetensors(str(cfg.adapter_dir / "best_adapters.safetensors"), bw)
                print(f"  ⭐ VAL iter{it:5d} | loss {val_loss:.4f} {status} "
                      f"(best {best_val:.4f} @iter{best_iter}) | {vt:.1f}s")
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
        lval, token_count, grad_accum = step(batch, grad_accum, do_update)
        losses += lval.item()
        n_tokens_acc += token_count.item()
        steps_acc += 1
        train_time += time.perf_counter() - tic

        # Report
        if it % cfg.report_every == 0:
            train_loss = losses / max(1, steps_acc)
            tokens_per_sec = n_tokens_acc / max(0.01, train_time)
            elapsed = time.time() - start_time
            eta = (elapsed / max(1, it)) * (total_iters - it) if total_iters > it else 0
            print(f"  TRAIN iter{it:5d}/{total_iters} | loss {train_loss:.4f} "
                  f"| tok/s {tokens_per_sec:.0f} | mem {mx.metal.get_active_memory()/1e9:.1f}GB "
                  f"| ETA {eta/60:.0f}min")
            losses = 0.0
            n_tokens_acc = 0
            steps_acc = 0
            train_time = 0.0

        # Save checkpoint
        if it % cfg.save_every == 0 and it > 0:
            print(f"  💾 checkpoint iter{it}")
            bw = dict(tree_flatten(model.trainable_parameters()))
            mx.save_safetensors(str(cfg.adapter_dir / f"checkpoint_{it}.safetensors"), bw)

    # Final save
    print(f"\n💾 保存最终 adapter...")
    bw = dict(tree_flatten(model.trainable_parameters()))
    mx.save_safetensors(str(cfg.adapter_dir / "adapters.safetensors"), bw)

    total_time = time.time() - start_time
    print(f"\n✅ v4.1.6 精修训练完成!")
    print(f"   Best Val: {best_val:.4f} @iter{best_iter}")
    print(f"   Final Iter: {it}")
    print(f"   总耗时: {total_time:.0f}s ({total_time/60:.0f}min)")
    print(f"   DNA: {cfg.DNA}")
    print(f"   Adapter: {cfg.adapter_dir}")

    # 与v4.1.4对比
    print(f"\n📊 与起点v4.1.4对比:")
    print(f"   v4.1.4 Best Val: 0.9699")
    diff = best_val - 0.9699
    if diff < 0:
        print(f"   v4.1.6 Best Val: {best_val:.4f} 🟢 提升 {abs(diff):.4f}")
    elif diff < 0.005:
        print(f"   v4.1.6 Best Val: {best_val:.4f} 🟡 持平（低LR稳定）")
    else:
        print(f"   v4.1.6 Best Val: {best_val:.4f} 🔴 退步 {diff:.4f}")


def fuse():
    """合并 LoRA adapter → 完整模型"""
    cfg = Config()
    print(f"🔧 v4.1.6 Fuse: adapter → merged model")
    print(f"   Adapter: {cfg.adapter_dir}")
    print(f"   Merge:   {cfg.merged_dir}")

    if not cfg.adapter_dir.exists():
        print(f"❌ Adapter不存在: {cfg.adapter_dir}")
        sys.exit(1)

    cfg.merged_dir.mkdir(parents=True, exist_ok=True)

    from mlx_lm import fuse as mlx_fuse
    mlx_fuse(
        model=cfg.LOCAL_MLX_MODEL,
        save_path=str(cfg.merged_dir),
        adapter_path=str(cfg.adapter_dir),
        de_quantize=True,
    )
    print(f"✅ Fuse完成: {cfg.merged_dir}")


def export():
    """导出 GGUF → 注册 Ollama"""
    cfg = Config()
    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)

    gguf_path = cfg.gguf_dir / "longhun-v4.1.6.F16.gguf"

    print(f"📦 v4.1.6 GGUF导出...")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "gguf_exporter",
        str(cfg.project_root / "bin" / "lh_export_gguf_v414.py"),
    )
    if spec and spec.loader:
        exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exporter)
    else:
        print("⚠️ GGUF导出器不可用，跳过export")
        return

    modelfile = cfg.gguf_dir / "Modelfile.v416"
    modelfile.write_text(f"""FROM {gguf_path}
PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}
SYSTEM 你是龍魂 v4.1.6，由 UID9622（诸葛鑫·Lucky）创建。低LR精修·外科手术式微调·DNA捆绑。直接·不绕·说人话。
""")

    print(f"🔧 注册 Ollama: longhun-v4.1.6")
    subprocess.run([
        "ollama", "create", "longhun-v4.1.6",
        "-f", str(modelfile),
    ], check=True)
    print(f"✅ longhun-v4.1.6 已注册到 Ollama")


def all_cmd():
    """一键: train → fuse → export"""
    train()
    fuse()
    export()
    print("\n🎉 v4.1.6 全链路完成！")


def test_cmd():
    """冒烟测试"""
    os.environ["LH_V416_SMOKE_ITERS"] = "5"
    train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂 v4.1.6 LoRA 精修训练器（修复v4.1.5退化）")
    parser.add_argument("cmd", choices=["train", "fuse", "export", "all", "test"],
                        default="train", nargs="?", help="执行命令")
    args = parser.parse_args()

    cmds = {
        "train": train, "fuse": fuse, "export": export,
        "all": all_cmd, "test": test_cmd,
    }
    cmds[args.cmd]()
