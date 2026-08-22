#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·Instruct 小模型训练器 v1.1
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·䷀乾-MODEL-LORA-TRAINER-INSTRUCT-V1.1-P1

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
import subprocess
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

    # transformers 4.49 与 Qwen2 新 tokenizer 兼容 bug：
    # _set_model_specific_special_tokens 期望 dict，Qwen2 传 list
    try:
        import transformers.tokenization_utils_base as tub
        _orig_set = tub.PreTrainedTokenizerBase._set_model_specific_special_tokens
        def _safe_set(self, special_tokens):
            if isinstance(special_tokens, list):
                special_tokens = {t: t for t in special_tokens}
            return _orig_set(self, special_tokens)
        tub.PreTrainedTokenizerBase._set_model_specific_special_tokens = _safe_set
    except Exception: pass
_patch_tokenizer()

PROJECT = Path(__file__).resolve().parent.parent


class Config:
    DNA = "丙午·丙申·辛酉·辰时·☰乾-MODEL-LORA-TRAINER-SMALL-V1.0-P1"

    # 底模：Qwen2.5-1.5B-Instruct 4-bit 量化版（LoRA 真正生效）
    base_model_id = "models/qwen-1.5b-instruct-4bit"
    # 如果要 3B，改成："Qwen/Qwen2.5-3B-Instruct"

    model_name = "longhun-small-instruct-v1.3-lora"

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
    output_dir = project_root / "models" / "longhun-small-instruct-v1.3"
    data_dir = output_dir / "data"
    adapter_dir = output_dir / "adapter"
    merged_dir = output_dir / "merged"
    gguf_dir = output_dir / "gguf"

    # 数据源：由 08_BIN/lh_clean_training_data_light.py 轻量清洗后的数据
    source_data_dir = project_root / "docs" / "notion_full_export" / "data_light"


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
    base_path = prepare_base_model(cfg)
    config = load_config(Path(base_path))
    save_config(config, str(save_path / "config.json"))
    tokenizer.save_pretrained(str(save_path))
    # mlx_lm.fuse 需要 adapter_config.json
    adapter_cfg = {
        "num_layers": cfg.lora_layers,
        "fine_tune_type": "lora",
        "lora_parameters": {
            "rank": cfg.lora_rank,
            "scale": cfg.lora_alpha / cfg.lora_rank,
            "dropout": cfg.lora_dropout,
        },
    }
    with open(save_path / "adapter_config.json", "w", encoding="utf-8") as f:
        json.dump(adapter_cfg, f, indent=2)


def prepare_base_model(cfg: Config) -> str:
    """准备底模：优先使用本地路径，否则从 ModelScope 下载。"""
    # 如果配置的是本地相对路径，先检查项目根目录
    candidate = cfg.project_root / cfg.base_model_id
    if candidate.is_dir() and (candidate / "config.json").exists():
        print(f"[{_now()}] 📦 使用本地底模: {candidate}")
        return str(candidate)

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
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)
    base_path = prepare_base_model(cfg)
    cmd = [
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", str(base_path),
        "--adapter-path", str(cfg.adapter_dir / "best"),
        "--save-path", str(cfg.merged_dir),
        "--dequantize",
    ]
    subprocess.run(cmd, check=True)
    print(f"[{_now()}] ✅ 合并完成: {cfg.merged_dir}")


def export_gguf(cfg: Config) -> None:
    """导出量化后的 MLX 模型（兼容 Ollama 导入）。"""
    print(f"[{_now()}] 📦 导出量化 MLX 模型...")
    from mlx_lm import convert
    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)
    convert(
        hf_path=str(cfg.merged_dir),
        mlx_path=str(cfg.gguf_dir),
        quantize=True,
        q_bits=4,
    )
    print(f"[{_now()}] ✅ 导出完成: {cfg.gguf_dir}")


def main():
    parser = argparse.ArgumentParser(description="龍魂·小模型快速训练器")
    parser.add_argument("action", choices=["test", "train", "fuse", "export", "all"], help="操作")
    parser.add_argument("--lr", type=float, default=None, help="覆盖学习率")
    parser.add_argument("--epochs", type=int, default=None, help="覆盖训练轮数")
    parser.add_argument("--patience", type=int, default=None, help="覆盖早停耐心")
    args = parser.parse_args()

    cfg = Config()
    if args.lr is not None:
        cfg.learning_rate = args.lr
        print(f"[{_now()}] ⚙️ 使用命令行学习率: {cfg.learning_rate}")
    if args.epochs is not None:
        cfg.epochs = args.epochs
        print(f"[{_now()}] ⚙️ 使用命令行 epochs: {cfg.epochs}")
    if args.patience is not None:
        cfg.early_stop_patience = args.patience
        print(f"[{_now()}] ⚙️ 使用命令行早停耐心: {cfg.early_stop_patience}")

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
