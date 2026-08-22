#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 longhun-v4.1.3 LoRA 微调器（全量数据·DNA捆绑继承）
DNA: #龍芯⚡️丙午·乙未·丙申·亥时·䷀乾-MODEL-LORA-TRAINER-v4.1.3-RESTART
底模: 01-ai/Yi-1.5-9B-Chat (MLX)
恢复: v4.1.1-bind adapter (Val 0.9659·DNA捆绑) — 当前最佳9B模型
数据: v4.1.1训练集 + 观澜16条 + Library矿场1082条 = 43,312条 (40,629 train + 2,683 valid)
目标: 全量数据注入·DNA捆绑继承·维持/提升Val Loss

用法:
  python3 bin/lh_lora_trainer_v413.py train    # 训练
  python3 bin/lh_lora_trainer_v413.py test     # 冒烟测试(5 iter)
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
    DNA = "丙午·乙未·丙申·亥时·☰乾-MODEL-LORA-TRAINER-v4.1.3-RESTART"
    
    # 底模
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.1.3-lora"
    
    # LoRA 参数（与 v4.1.1 一致，便于恢复）
    lora_rank = 16
    lora_alpha = 32
    lora_dropout = 0.15
    lora_layers = 12
    
    # 训练参数（保守：小学习率微调新知识）
    batch_size = 4
    grad_accumulation_steps = 1
    lr_peak = 5e-7          # 极低学习率，避免遗忘已有知识
    lr_min = 0.0
    warmup_steps = 50
    weight_decay = 0.01
    epochs = 1              # 只1轮，注入16条新知
    max_seq_length = 2048
    grad_checkpoint = True
    
    # 训练控制
    early_stop_patience = 3
    val_steps = 100
    save_every = 500
    report_every = 10
    val_batches = 20
    
    # 路径
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v413"
    data_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v411" / "data_v413_fused"
    adapter_dir = output_dir / "adapter_v413"
    merged_dir = output_dir / "merged_v413"
    gguf_dir = output_dir / "gguf_v413"
    
    # 恢复点：v4.1.1-bind adapter（DNA捆绑·Val 0.9659·当前最佳9B）
    v411_adapter = (
        project_root / "models" / "longhun-v1.0" / "lora_output_v411_bind" / "adapter_v411_bind" / "adapters.safetensors"
    )
    v411_best = (
        project_root / "models" / "longhun-v1.0" / "lora_output_v411_bind" / "adapter_v411_bind" / "best_adapters.safetensors"
    )
    
    resume_adapter_file = str(v411_adapter) if v411_adapter.exists() else None
    
    # 推理
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def _build_lr_schedule(peak, warmup_steps, total_steps, end=0.0):
    if total_steps <= warmup_steps:
        return optim.linear_schedule(0.0, peak, max(1, total_steps))
    warmup = optim.linear_schedule(0.0, peak, max(1, warmup_steps))
    cosine = optim.cosine_decay(peak, max(1, total_steps - warmup_steps), end=end)
    return optim.join_schedules([warmup, cosine], [warmup_steps])


class _Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, data):
        for f in self.files:
            f.write(data); f.flush()
    def flush(self):
        for f in self.files:
            f.flush()


def train():
    cfg = Config()
    smoke_iters = int(os.environ.get("LH_V413_SMOKE_ITERS", 0))
    smoke_mode = smoke_iters > 0
    
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志
    log_mode = "w"
    train_log = open(cfg.output_dir / "training.log", log_mode, encoding="utf-8")
    old_stdout = sys.stdout
    sys.stdout = _Tee(sys.stdout, train_log)
    
    try:
        _train_inner(cfg, smoke_mode, smoke_iters)
    finally:
        sys.stdout = old_stdout
        train_log.close()


def _train_inner(cfg, smoke_mode, smoke_iters):
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    if not mlx_path.exists():
        print(f"❌ MLX 底模不存在: {cfg.LOCAL_MLX_MODEL}")
        sys.exit(1)
    
    train_file = Path(cfg.data_dir) / "train.jsonl"
    valid_file = Path(cfg.data_dir) / "valid.jsonl"
    if not train_file.exists():
        print(f"❌ 训练数据不存在: {train_file}")
        sys.exit(1)
    
    print(f"🐉 龍魂 v4.1.3 LoRA 训练")
    print(f"   DNA: {cfg.DNA}")
    print(f"   底模: Yi-1.5-9B-Chat (MLX)")
    print(f"   恢复: {cfg.resume_adapter_file}")
    print(f"   数据: {cfg.data_dir}")
    print(f"   学习率: {cfg.lr_peak}, Epochs: {cfg.epochs}")
    print(f"   训练集: {sum(1 for _ in open(train_file))} 条")
    print(f"   验证集: {sum(1 for _ in open(valid_file))} 条")
    
    if smoke_mode:
        print(f"   🧪 冒烟模式: {smoke_iters} iters")
    
    # 清理旧 adapter
    if cfg.adapter_dir.exists() and not cfg.resume_adapter_file:
        shutil.rmtree(cfg.adapter_dir)
    cfg.adapter_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n📦 加载底模...")
    model, tokenizer = load(cfg.LOCAL_MLX_MODEL, tokenizer_config={"trust_remote_code": True})
    
    # 冻结 + LoRA
    model.freeze()
    linear_to_lora_layers(model, cfg.lora_layers, {
        "rank": cfg.lora_rank, "dropout": cfg.lora_dropout, "scale": cfg.lora_alpha,
    })
    
    # 恢复 v4.1.1 权重
    resume = cfg.resume_adapter_file
    if resume and Path(resume).exists():
        print(f"🔄 从 v4.1.1 恢复: {resume}")
        model.load_weights(resume, strict=False)
    else:
        print("⚠️ 无恢复点，从头训练（不推荐）")
    
    print_trainable_parameters(model)
    
    # 加载数据
    print("\n📊 加载训练数据...")
    args_ns = argparse.Namespace(
        data=str(cfg.data_dir), train=True, test=False,
        batch_size=cfg.batch_size, max_seq_length=cfg.max_seq_length,
        mask_prompt=True,
    )
    train_set, valid_set, _ = load_dataset(args_ns, tokenizer)
    
    # 计算步数
    n_train = sum(1 for _ in open(train_file))
    iters_per_epoch = max(1, n_train // cfg.batch_size)
    total_iters = iters_per_epoch * cfg.epochs if not smoke_mode else smoke_iters
    
    print(f"   总步数: {total_iters} ({cfg.epochs} epochs × {iters_per_epoch}/epoch)")
    
    # 优化器
    lr_schedule = _build_lr_schedule(cfg.lr_peak, cfg.warmup_steps, total_iters, cfg.lr_min)
    optimizer = optim.AdamW(learning_rate=lr_schedule, weight_decay=cfg.weight_decay)
    
    # 损失函数（与 v4.1.1 一致）
    loss_value_and_grad = nn.value_and_grad(model, default_loss)
    
    # 训练循环
    print(f"\n🚀 开始训练...\n")
    best_val = float("inf")
    patience_counter = 0
    start_time = time.time()
    
    state = [model.state, optimizer.state]
    
    for it, batch in zip(
        range(1, total_iters + 1),
        iterate_batches(
            dataset=CacheDataset(train_set),
            batch_size=cfg.batch_size,
            max_seq_length=cfg.max_seq_length,
            loop=True,
        ),
    ):
        # Forward + backward（与 v4.1.1 一致：展开 batch → default_loss）
        (loss_value, n_tokens), grad = loss_value_and_grad(model, *batch)
        optimizer.update(model, grad)
        mx.eval(state)
        
        # 报告
        if it % cfg.report_every == 0 or it == 1:
            elapsed = time.time() - start_time
            speed = it / elapsed if elapsed > 0 else 0
            lr = lr_schedule(it).item()
            print(f"  iter {it:5d}/{total_iters} | loss {loss_value.item():.4f} | "
                  f"lr {lr:.2e} | {speed:.1f} it/s | tok {n_tokens.item()}")
        
        # 验证
        if it % cfg.val_steps == 0 or it == total_iters:
            val_loss = evaluate(
                model=model,
                dataset=CacheDataset(valid_set),
                loss=default_loss,
                batch_size=cfg.batch_size,
                num_batches=cfg.val_batches,
                max_seq_length=cfg.max_seq_length,
            )
            model.train()
            improved = val_loss < best_val
            status = "🟢" if improved else "🟡"
            print(f"  --- val {it:5d} | loss {val_loss:.4f} {status} "
                  f"(best {best_val:.4f}) ---")
            
            if improved:
                best_val = val_loss
                patience_counter = 0
                # 保存最佳（只保存LoRA训练参数，不是全模型）
                best_path = cfg.adapter_dir / "best_adapters.safetensors"
                best_weights = dict(tree_flatten(model.trainable_parameters()))
                mx.save_safetensors(str(best_path), best_weights)
                print(f"  💾 最佳权重已保存: {best_path}")
            else:
                patience_counter += 1
                if patience_counter >= cfg.early_stop_patience:
                    print(f"\n⏹ 早停: {cfg.early_stop_patience} 轮未改善")
                    break
        
        # 保存检查点
        if it % cfg.save_every == 0:
            ckpt = cfg.adapter_dir / f"iter{it:04d}_adapters.safetensors"
            ckpt_weights = dict(tree_flatten(model.trainable_parameters()))
            mx.save_safetensors(str(ckpt), ckpt_weights)
            print(f"  💾 checkpoint: {ckpt}")
    
    # 最终保存
    final_path = cfg.adapter_dir / "adapters.safetensors"
    final_weights = dict(tree_flatten(model.trainable_parameters()))
    mx.save_safetensors(str(final_path), final_weights)
    
    elapsed = time.time() - start_time
    print(f"\n✅ 训练完成: {elapsed:.0f}s | best_val {best_val:.4f}")
    print(f"   adapter: {final_path}")
    print(f"   best: {cfg.adapter_dir / 'best_adapters.safetensors'}")


def fuse():
    """合并 LoRA adapter 到完整模型"""
    cfg = Config()
    adapter = cfg.adapter_dir / "best_adapters.safetensors"
    if not adapter.exists():
        adapter = cfg.adapter_dir / "adapters.safetensors"
    if not adapter.exists():
        print(f"❌ adapter 不存在: {cfg.adapter_dir}")
        sys.exit(1)
    
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🔧 合并 adapter → {cfg.merged_dir}")
    cmd = [
        sys.executable, "-m", "mlx_lm.fuse",
        "--model", cfg.LOCAL_MLX_MODEL,
        "--adapter-path", str(adapter),
        "--save-path", str(cfg.merged_dir),
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ 合并完成: {cfg.merged_dir}")


def export():
    """导出 GGUF → Ollama"""
    cfg = Config()
    merged = cfg.merged_dir
    if not merged.exists():
        print(f"❌ merged 模型不存在，请先 fuse")
        sys.exit(1)
    
    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)
    gguf_file = cfg.gguf_dir / "longhun-v4.1.3.Q4_K_M.gguf"
    
    print(f"📦 导出 GGUF → {gguf_file}")
    cmd = [
        sys.executable, "-m", "mlx_lm.convert",
        "--hf-path", str(merged),
        "--mlx-path", str(merged),
        "-q", "--q-bits", "4",
        "--q-group-size", "64",
    ]
    # 实际上用 mlx_lm 的 export 功能
    # 简化：直接用 llama.cpp 转换
    print("   导出完成（占位，需手动执行 GGUF 转换）")
    print(f"   目标: {gguf_file}")


def test_quick():
    """快速测试：5 iter 冒烟"""
    os.environ["LH_V413_SMOKE_ITERS"] = "5"
    train()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="龍魂 v4.1.3 LoRA 训练器")
    p.add_argument("action", choices=["train", "fuse", "export", "test"],
                   default="train", nargs="?")
    args = p.parse_args()
    
    {
        "train": train,
        "fuse": fuse,
        "export": export,
        "test": test_quick,
    }[args.action]()
