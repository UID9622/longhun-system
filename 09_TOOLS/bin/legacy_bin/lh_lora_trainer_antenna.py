#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# 龍魂 · ANTENNA-8GATE 路由知识注入训练器
# DNA：#龍芯⚡️丙午·乙未·丙申·戌时·䷝离-ANTENNA-TRAINER-v1.0-a1b2c3d4
# 创建者：诸葛鑫（UID9622）· 协议：CC BY-NC-SA 4.0
#
# 目标: 将 ANTENNA-8GATE 八卦路由知识注入 longhun-v4.1.1-bind
# 底模: Yi-1.5-9B-Chat (MLX)
# 基础: v4.1.1-bind adapter (Val 0.9659·DNA捆绑)
# 数据: 52 train + 17 valid (69条八卦路由样本)
#
# 用法:
#   python3 bin/lh_lora_trainer_antenna.py         # 训练
#   python3 bin/lh_lora_trainer_antenna.py test    # 冒烟
# ============================================================

import argparse, json, os, sys, time, shutil
from datetime import datetime
from pathlib import Path
from functools import partial

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
import numpy as np
from mlx.utils import tree_flatten, tree_map

from mlx_lm.tuner.datasets import load_dataset
from mlx_lm.tuner.trainer import (
    CacheDataset, default_loss, evaluate, iterate_batches,
)
from mlx_lm.tuner.utils import linear_to_lora_layers, print_trainable_parameters
from mlx_lm.utils import load

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

PROJECT = Path(__file__).resolve().parent.parent

class Config:
    DNA = "丙午·乙未·丙申·戌时·☲离-ANTENNA-TRAINER-v1.0-a1b2c3d4"
    model_name = "longhun-v4.1.1-bind-antenna"
    
    # 底模
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    
    # LoRA - 轻量注入
    lora_rank = 8
    lora_alpha = 16
    lora_dropout = 0.1
    lora_layers = 8
    
    # 训练 - 极小学习率，不破坏已有知识
    batch_size = 2
    lr_peak = 1e-7       # 极低：只注入路由规则，不改原有知识
    lr_min = 0.0
    warmup_steps = 3
    weight_decay = 0.01
    epochs = 3           # 数据少，多跑几轮
    max_seq_length = 2048
    grad_checkpoint = True
    
    # 控制
    val_steps = 10
    save_every = 20
    report_every = 5
    val_batches = 8
    early_stop_patience = 5
    
    # 路径
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_antenna"
    adapter_dir = output_dir / "adapter_antenna"
    merged_dir = output_dir / "merged_antenna"
    
    # 训练数据
    data_dir = project_root / "01_protocols" / "ANTENNA-8GATE" / "training_data"
    
    # 恢复点：v4.1.1-bind
    resume_adapter = (
        project_root / "models" / "longhun-v1.0" / "lora_output_v411_bind"
        / "adapter_v411_bind" / "adapters.safetensors"
    )


def _build_lr_schedule(peak, warmup, total, end=0.0):
    if total <= warmup:
        return optim.linear_schedule(0.0, peak, max(1, total))
    w = optim.linear_schedule(0.0, peak, max(1, warmup))
    c = optim.cosine_decay(peak, max(1, total - warmup), end=end)
    return optim.join_schedules([w, c], [warmup])


class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, d):
        for f in self.files: f.write(d); f.flush()
    def flush(self):
        for f in self.files: f.flush()


def train():
    cfg = Config()
    smoke_iters = int(os.environ.get("ANTENNA_SMOKE", 0))
    smoke = smoke_iters > 0
    
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    cfg.adapter_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = open(cfg.output_dir / "training.log", "w", encoding="utf-8")
    old_stdout = sys.stdout
    sys.stdout = Tee(sys.stdout, log_file)
    
    try:
        _train(cfg, smoke, smoke_iters)
    finally:
        sys.stdout = old_stdout
        log_file.close()


def _train(cfg, smoke, smoke_iters):
    print("=" * 60)
    print(f"🐉 ANTENNA-8GATE 路由知识注入训练")
    print(f"   DNA: {cfg.DNA}")
    print(f"   底模: Yi-1.5-9B-Chat (MLX)")
    print(f"   基础: v4.1.1-bind (Val 0.9659·DNA捆绑)")
    print(f"   数据: {cfg.data_dir}")
    print(f"   参数: rank={cfg.lora_rank} α={cfg.lora_alpha} lr={cfg.lr_peak}")
    print(f"   批次: {cfg.batch_size} | epochs={cfg.epochs}")
    print("=" * 60)
    
    # 检查数据
    train_file = Path(cfg.data_dir) / "train.jsonl"
    valid_file = Path(cfg.data_dir) / "valid.jsonl"
    if not train_file.exists():
        print(f"❌ train.jsonl 不存在: {train_file}")
        sys.exit(1)
    if not valid_file.exists():
        print(f"⚠️ valid.jsonl 不存在，使用 train 的20%")
        valid_file = train_file
    
    n_train = sum(1 for _ in open(train_file))
    n_valid = sum(1 for _ in open(valid_file))
    print(f"   训练集: {n_train} 条 | 验证集: {n_valid} 条")
    print(f"   总迭代: {n_train * cfg.epochs // cfg.batch_size} ({cfg.epochs}×{n_train//cfg.batch_size})")
    
    # 加载底模
    print("\n📦 加载底模 Yi-1.5-9B-Chat...")
    t0 = time.time()
    model, tokenizer = load(cfg.LOCAL_MLX_MODEL, tokenizer_config={"trust_remote_code": True})
    print(f"   加载耗时: {time.time() - t0:.1f}s")
    
    # 冻结 + LoRA
    model.freeze()
    linear_to_lora_layers(model, cfg.lora_layers, {
        "rank": cfg.lora_rank, "dropout": cfg.lora_dropout, "scale": cfg.lora_alpha,
    })
    
    # 恢复 v4.1.1-bind 权重
    resume = str(cfg.resume_adapter)
    if Path(resume).exists():
        print(f"🔄 恢复 v4.1.1-bind: {resume}")
        t0 = time.time()
        model.load_weights(resume, strict=False)
        print(f"   恢复耗时: {time.time() - t0:.1f}s")
    else:
        print("⚠️ 无恢复点，使用底模原始权重")
    
    print_trainable_parameters(model)
    
    # 加载数据
    print("\n📊 加载训练数据...")
    args = argparse.Namespace(
        data=str(cfg.data_dir), train=True, test=False,
        batch_size=cfg.batch_size, max_seq_length=cfg.max_seq_length,
    )
    train_set, valid_set, _ = load_dataset(args, tokenizer)
    
    # 计算步数
    iters_per_epoch = max(1, n_train // cfg.batch_size)
    total_iters = iters_per_epoch * cfg.epochs if not smoke else smoke_iters
    print(f"   总步数: {total_iters}")
    
    # 优化器
    lr_schedule = _build_lr_schedule(cfg.lr_peak, cfg.warmup_steps, total_iters)
    optimizer = optim.AdamW(learning_rate=lr_schedule, weight_decay=cfg.weight_decay)
    loss_fn = nn.value_and_grad(model, default_loss)
    
    # 训练
    print(f"\n🚀 开始训练 ({total_iters} 步)...\n")
    best_val = float("inf")
    patience = 0
    start = time.time()
    state = [model.state, optimizer.state]
    loss_log = []
    
    for it, batch in zip(
        range(1, total_iters + 1),
        iterate_batches(
            CacheDataset(train_set), cfg.batch_size,
            cfg.max_seq_length, loop=True,
        ),
    ):
        (loss_val, n_tok), grad = loss_fn(model, *batch)
        optimizer.update(model, grad)
        mx.eval(state)
        loss_log.append(loss_val.item())
        
        # 报告
        if it % cfg.report_every == 0 or it == 1:
            elapsed = time.time() - start
            lr_now = lr_schedule(it).item()
            avg_loss = sum(loss_log[-10:]) / min(10, len(loss_log))
            print(f"  iter {it:4d}/{total_iters} | loss {loss_val.item():.5f} "
                  f"| avg {avg_loss:.5f} | lr {lr_now:.1e} | {it/elapsed:.1f} it/s")
        
        # 验证
        if it % cfg.val_steps == 0 or it == total_iters:
            val_loss = evaluate(
                model, CacheDataset(valid_set), cfg.batch_size,
                num_batches=cfg.val_batches,
                max_seq_length=cfg.max_seq_length,
                loss=default_loss,
            )
            model.train()
            improved = val_loss < best_val
            status = "🟢 NEW BEST" if improved else "🟡"
            print(f"  --- VAL {it:4d} | loss {val_loss:.4f} {status} (best {best_val:.4f}) ---")
            
            if improved:
                best_val = val_loss
                patience = 0
                bw = dict(tree_flatten(model.trainable_parameters()))
                mx.save_safetensors(str(cfg.adapter_dir / "best_adapters.safetensors"), bw)
            else:
                patience += 1
                if patience >= cfg.early_stop_patience:
                    print(f"\n⏹ 早停: {cfg.early_stop_patience}轮未改善")
                    break
        
        # 保存
        if it % cfg.save_every == 0:
            cw = dict(tree_flatten(model.trainable_parameters()))
            mx.save_safetensors(str(cfg.adapter_dir / f"iter{it:04d}_adapters.safetensors"), cw)
    
    # 最终保存
    fw = dict(tree_flatten(model.trainable_parameters()))
    mx.save_safetensors(str(cfg.adapter_dir / "adapters.safetensors"), fw)
    
    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"✅ 训练完成 | 耗时: {elapsed:.0f}s | best_val: {best_val:.4f}")
    print(f"   adapter: {cfg.adapter_dir / 'best_adapters.safetensors'}")
    print(f"   起止loss: {loss_log[0]:.4f} → {loss_log[-1]:.4f}")
    print(f"{'='*60}")


def test_quick():
    os.environ["ANTENNA_SMOKE"] = "5"
    train()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["train", "test"], default="train", nargs="?")
    a = p.parse_args()
    {"train": train, "test": test_quick}[a.action]()
