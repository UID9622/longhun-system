#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂·小模型快速训练器 v1.0
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·☰乾-MODEL-LORA-TRAINER-SMALL-V1.0-P1

基于 Qwen2.5-1.5B/3B-Instruct，使用 mlx_lm 快速 LoRA 微调，
专门用于把龍魂规则、铁律、DNA 注入小模型，1~2 小时出结果。

用法:
  python3 08_BIN/lh_lora_trainer_small.py test      # 冒烟测试
  python3 08_BIN/lh_lora_trainer_small.py train     # 完整训练
  python3 08_BIN/lh_lora_trainer_small.py fuse      # 合并 adapter
  python3 08_BIN/lh_lora_trainer_small.py export    # GGUF → Ollama
  python3 08_BIN/lh_lora_trainer_small.py all       # 一键 train→fuse→export
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from functools import partial
from pathlib import Path

import numpy as np
from mlx_lm.utils import load_config, save_config

# 国内网络优先走 hf-mirror，避免 huggingface.co 超时
if not os.environ.get("HF_ENDPOINT"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    print(f"[auto] 未设置 HF_ENDPOINT，自动使用镜像: {os.environ['HF_ENDPOINT']}")

# 兼容 patch
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
    DNA = "丙午·丙申·辛酉·辰时·☰乾-MODEL-LORA-TRAINER-SMALL-V1.0-P1"

    # 底模：Qwen2.5-1.5B-Instruct（从 ModelScope 下载，避免 huggingface.co 被墙）
    base_model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    # 如果要 3B，改成："Qwen/Qwen2.5-3B-Instruct"

    model_name = "longhun-small-v1.0-lora"

    # LoRA 参数（小模型用稍大 rank，学得更快）
    lora_rank = 32
    lora_alpha = 64
    lora_dropout = 0.05
    lora_layers = 16

    # 训练参数（快速收敛）
    batch_size = 4
    grad_accumulation_steps = 1
    learning_rate = 5e-5
    epochs = 1                 # 小模型 1 epoch 就够
    max_seq_length = 1024      # 小模型缩短序列，省内存

    # 控制
    early_stop_patience = 3
    val_steps = 50
    save_every = 200
    report_every = 10
    val_batches = 10
    grad_checkpoint = True

    # 路径
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-small-v1.0"
    data_dir = output_dir / "data"
    adapter_dir = output_dir / "adapter"
    merged_dir = output_dir / "merged"
    gguf_dir = output_dir / "gguf"

    # 数据源：复用 v4.1.4 道德经数据（可以改）
    source_data_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v414" / "data_v415_daodejing"


CSP = None  # placeholder


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def prepare_data(cfg: Config, smoke: bool = False) -> None:
    """准备训练数据：复用现有 jsonl，并采样加速。"""
    print(f"[{_now()}] 📊 准备训练数据...")
    cfg.data_dir.mkdir(parents=True, exist_ok=True)

    train_src = cfg.source_data_dir / "train.jsonl"
    valid_src = cfg.source_data_dir / "valid.jsonl"

    if not train_src.exists() or not valid_src.exists():
        raise FileNotFoundError(f"找不到数据：{train_src} 或 {valid_src}")

    # 读取并采样
    with open(train_src, "r", encoding="utf-8") as f:
        train_lines = [l for l in f if l.strip()]
    with open(valid_src, "r", encoding="utf-8") as f:
        valid_lines = [l for l in f if l.strip()]

    if smoke:
        train_lines = train_lines[:256]
        valid_lines = valid_lines[:32]
    else:
        # 小模型快速训练：最多用 10000 条训练 + 500 条验证
        train_lines = train_lines[:10000]
        valid_lines = valid_lines[:500]

    with open(cfg.data_dir / "train.jsonl", "w", encoding="utf-8") as f:
        f.writelines(train_lines)
    with open(cfg.data_dir / "valid.jsonl", "w", encoding="utf-8") as f:
        f.writelines(valid_lines)

    print(f"[{_now()}]    训练集 {len(train_lines)} 条 | 验证集 {len(valid_lines)} 条")


def train(cfg: Config, smoke: bool = False) -> None:
    """使用 mlx_lm 训练 LoRA。"""
    print("🐉 龍魂·小模型快速训练")
    print(f"   DNA: {cfg.DNA}")
    print(f"   底模: {cfg.base_model_id}")
    print(f"   模型名: {cfg.model_name}")
    print(f"   数据: {cfg.data_dir}")
    print(f"   LoRA: rank={cfg.lora_rank}, alpha={cfg.lora_alpha}, dropout={cfg.lora_dropout}")
    print(f"   LR: {cfg.learning_rate}, Epochs: {cfg.epochs}, Batch: {cfg.batch_size}")

    # 延迟导入，避免 patch 前先加载
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    from mlx_lm.tuner.datasets import load_dataset
    from mlx_lm.tuner.trainer import (
        CacheDataset, default_loss, evaluate, grad_checkpoint, iterate_batches,
    )
    from mlx_lm.tuner.utils import linear_to_lora_layers, print_trainable_parameters
    from mlx_lm.utils import load

    base_path = prepare_base_model(cfg)
    print(f"[{_now()}] 📦 加载底模 {base_path} ...")
    model, tokenizer = load(base_path, tokenizer_config={"trust_remote_code": True})

    print(f"[{_now()}] 🔄 添加 LoRA 层...")
    # mlx_lm 新版签名：linear_to_lora_layers(model, num_layers, config)
    lora_config = {
        "rank": cfg.lora_rank,
        "scale": cfg.lora_alpha / cfg.lora_rank,
        "dropout": cfg.lora_dropout,
    }
    linear_to_lora_layers(model, cfg.lora_layers, lora_config)
    print_trainable_parameters(model)

    print(f"[{_now()}] 📊 加载训练数据...")
    # mlx_lm 新版 load_dataset 需要 args 对象
    class _DatasetArgs:
        data = str(cfg.data_dir)
        train = True
        test = False
        val = True
    dataset_args = _DatasetArgs()
    train_set, valid_set, test_set = load_dataset(dataset_args, tokenizer)

    # 新版数据集需要 CacheDataset 包裹以预处理为 token 元组
    train_set = CacheDataset(train_set)
    valid_set = CacheDataset(valid_set)

    total_steps = (len(train_set) // cfg.batch_size) * cfg.epochs
    print(f"[{_now()}]    总步数: {total_steps} ({cfg.epochs} epochs)")

    # 优化器
    opt = optim.Adam(learning_rate=cfg.learning_rate)

    # 训练状态
    model.train()
    loss_and_grad = nn.value_and_grad(model, default_loss)
    if cfg.grad_checkpoint and model.layers:
        # grad_checkpoint 作用于单层模块类型，model.layers[0] 即可作用到全部同类型层
        grad_checkpoint(model.layers[0])

    best_val_loss = float("inf")
    patience_counter = 0
    step = 0
    start_time = time.time()

    for epoch in range(cfg.epochs):
        print(f"\n[{_now()}] 🚀 Epoch {epoch + 1}/{cfg.epochs}")
        for batch, lengths in iterate_batches(
            train_set, cfg.batch_size, cfg.max_seq_length
        ):
            step += 1
            (loss, ntoks), grads = loss_and_grad(model, batch, lengths)
            opt.update(model.trainable_parameters(), grads)
            mx.eval(model.trainable_parameters(), opt.state, loss, ntoks)

            if step % cfg.report_every == 0:
                elapsed = time.time() - start_time
                eta = (elapsed / step) * (total_steps - step) if step > 0 else 0
                print(f"  TRAIN iter {step}/{total_steps} | loss {loss.item():.4f} | ntoks {ntoks.item():.0f} | ETA {int(eta//60)}min")

            if step % cfg.val_steps == 0 or step == total_steps:
                model.eval()
                val_loss = evaluate(model, valid_set, cfg.batch_size, cfg.val_batches, cfg.max_seq_length)
                model.train()
                marker = "🟢" if val_loss < best_val_loss else "🔴"
                print(f"  {marker} VAL iter {step} | loss {val_loss:.4f} | best {best_val_loss:.4f}")

                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    patience_counter = 0
                    save_adapter(cfg, model, tokenizer, "best")
                else:
                    patience_counter += 1

                if patience_counter >= cfg.early_stop_patience:
                    print(f"[{_now()}] 🛑 早停触发，连续 {cfg.early_stop_patience} 次未改善")
                    break

            if step % cfg.save_every == 0:
                save_adapter(cfg, model, tokenizer, f"step_{step}")

        if patience_counter >= cfg.early_stop_patience:
            break

    # 保存最终 adapter
    save_adapter(cfg, model, tokenizer, "final")

    elapsed_total = time.time() - start_time
    print(f"\n[{_now()}] ✅ 训练完成")
    print(f"   Best Val Loss: {best_val_loss:.4f}")
    print(f"   总耗时: {int(elapsed_total//60)} 分钟")
    print(f"   Adapter: {cfg.adapter_dir}")


def save_adapter(cfg: Config, model, tokenizer, name: str) -> None:
    """保存 adapter。"""
    save_path = cfg.adapter_dir / name
    save_path.mkdir(parents=True, exist_ok=True)
    model.save_weights(str(save_path / "adapters.safetensors"))
    config = load_config(cfg.output_dir / "base_model")
    save_config(config, str(save_path / "config.json"))
    tokenizer.save_pretrained(str(save_path))


def prepare_base_model(cfg: Config) -> str:
    """从 ModelScope 拉取底模到本地，返回本地路径。"""
    local_path = cfg.output_dir / "base_model"
    config_file = local_path / "config.json"
    if config_file.exists():
        print(f"[{_now()}] 📦 底模已存在: {local_path}")
        return str(local_path)

    print(f"[{_now()}] 📦 从 ModelScope 下载底模 {cfg.base_model_id} ...")
    print(f"[{_now()}]    约 3GB，请耐心等待...")
    from modelscope.hub.snapshot_download import snapshot_download
    snapshot_download(
        cfg.base_model_id,
        local_dir=str(local_path),
        revision="master",
    )
    print(f"[{_now()}] ✅ 底模下载完成: {local_path}")
    return str(local_path)


def fuse(cfg: Config) -> None:
    """合并 adapter 到底模。"""
    print(f"[{_now()}] 🔥 合并 adapter...")
    from mlx_lm import fuse
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)
    base_path = prepare_base_model(cfg)
    fuse(
        model=base_path,
        adapter_path=str(cfg.adapter_dir / "best"),
        save_path=str(cfg.merged_dir),
        de_quantize=True,
    )
    print(f"[{_now()}] ✅ 合并完成: {cfg.merged_dir}")


def export_gguf(cfg: Config) -> None:
    """导出 GGUF。"""
    print(f"[{_now()}] 📦 导出 GGUF...")
    from mlx_lm import convert
    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)
    convert(
        hf_path_or_model=str(cfg.merged_dir),
        mlx_path=str(cfg.gguf_dir),
        quantize=True,
        q_bits=4,
    )
    print(f"[{_now()}] ✅ 导出完成: {cfg.gguf_dir}")


def main():
    parser = argparse.ArgumentParser(description="龍魂·小模型快速训练器")
    parser.add_argument("action", choices=["test", "train", "fuse", "export", "all"], help="操作")
    args = parser.parse_args()

    cfg = Config()

    if args.action == "test":
        prepare_data(cfg, smoke=True)
        train(cfg, smoke=True)
    elif args.action == "train":
        prepare_data(cfg, smoke=False)
        train(cfg, smoke=False)
    elif args.action == "fuse":
        fuse(cfg)
    elif args.action == "export":
        export_gguf(cfg)
    elif args.action == "all":
        prepare_data(cfg, smoke=False)
        train(cfg, smoke=False)
        fuse(cfg)
        export_gguf(cfg)


if __name__ == "__main__":
    main()
