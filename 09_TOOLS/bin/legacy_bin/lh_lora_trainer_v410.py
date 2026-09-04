#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 longhun-v4.1.0 LoRA 微调器（自定义训练循环 · 抗过拟合版）
底模: 01-ai/Yi-1.5-9B-Chat (MLX)
数据: v4.0.9 清洗集 → v4.1.0 工作目录（后续可替换为 v4.1.0 增强数据）
目标: 解决 v4.0.9 过拟合（Train 0.654 vs Val 1.002，gap -0.348）
       通过自定义训练循环支持 AdamW + weight_decay、cosine warmup、更高 LoRA dropout、
       val 平台期 early stop，并从 v4.0.8-iter1900 golden checkpoint（Val 0.767）恢复。

DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-MODEL-LORA-TRAINER-v4.1.0

用法:
  python3 bin/lh_lora_trainer_v410.py setup    # 复用/转换 Yi-1.5-9B-Chat MLX
  python3 bin/lh_lora_trainer_v410.py prepare  # 从 v4.0.9_ready 复制数据到 v4.1.0_ready
  python3 bin/lh_lora_trainer_v410.py train    # 自定义 LoRA 训练循环
  python3 bin/lh_lora_trainer_v410.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v410.py export   # 导出 GGUF → Ollama
  python3 bin/lh_lora_trainer_v410.py test     # 快速测试

冒烟验证（5 iter，不污染正式训练）:
  LH_V410_SMOKE_ITERS=5 python3 bin/lh_lora_trainer_v410.py train
"""

import argparse
import json
import os
import sys
import shutil
import subprocess
import time
import shlex
from datetime import datetime
from functools import partial
from hashlib import sha256
from pathlib import Path

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
import numpy as np
from mlx.nn.utils import average_gradients
from mlx.utils import tree_flatten, tree_map

from mlx_lm.tuner.datasets import load_dataset
from mlx_lm.tuner.trainer import (
    CacheDataset,
    default_loss,
    evaluate,
    grad_checkpoint,
    iterate_batches,
)
from mlx_lm.tuner.utils import linear_to_lora_layers, print_trainable_parameters
from mlx_lm.utils import load, save_config

# 避免 huggingface/tokenizers 多进程警告
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# ============================================================
# 🔧 transformers 5.x 兼容性 patch
# ============================================================
def _patch_mlx_lm_tokenizer():
    try:
        import transformers.models.auto.tokenization_auto as taa
        _orig_register = taa.AutoTokenizer.register
        def _safe_register(*args, **kwargs):
            try:
                return _orig_register(*args, **kwargs)
            except Exception:
                return None
        taa.AutoTokenizer.register = staticmethod(_safe_register)
    except Exception:
        pass

_patch_mlx_lm_tokenizer()

# ============================================================
# 项目路径与 DNA
# ============================================================
PROJECT = Path(__file__).resolve().parent.parent


def _dna():
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    h = sha256(ts.encode()).hexdigest()[:16].upper()
    return f"#龍芯⚡️{ts}-MODEL-LORA-TRAINER-v4.1.0-{h}"


# ============================================================
# 配置 v4.1.0
# ============================================================
class Config:
    DNA = _dna()

    # === 底模 ===
    HF_MODEL_ID = "01-ai/Yi-1.5-9B-Chat"
    LOCAL_HF_MODEL = str(PROJECT / "models" / "base_models_v4.0" / "Yi-1.5-9B-Chat")
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.1.0-lora"

    # === LoRA 参数（ dropout 提高到 0.1 抗过拟合） ===
    lora_rank = 16
    lora_alpha = 32
    lora_dropout = 0.1
    lora_layers = 12

    # === 训练参数（自定义循环） ===
    batch_size = 1
    grad_accumulation_steps = 4
    lr_peak = 3e-6
    lr_min = 0.0
    warmup_steps = 100
    weight_decay = 0.01
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True

    # === 训练控制 ===
    early_stop_patience = 3
    val_steps = 50
    save_every = 500
    report_every = 10
    val_batches = 25

    # === 路径 ===
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v410"
    data_dir = output_dir / "data_v410_ready"
    adapter_dir = output_dir / "adapter_v410"
    merged_dir = output_dir / "merged_v410"
    gguf_dir = output_dir / "gguf_v410"

    # === 恢复点优先级：本版本最新 checkpoint → v4.0.8 golden ===
    v408_golden = (
        project_root
        / "models"
        / "longhun-v1.0"
        / "checkpoint_archive"
        / "v408_iter1900_val0767"
        / "adapters.safetensors"
    )

    latest_v410 = None
    if adapter_dir.exists():
        numbered = sorted(adapter_dir.glob("*_adapters.safetensors"))
        if numbered:
            latest_v410 = str(numbered[-1])
        elif (adapter_dir / "adapters.safetensors").exists():
            latest_v410 = str(adapter_dir / "adapters.safetensors")

    if latest_v410:
        resume_adapter_file = latest_v410
    elif v408_golden.exists():
        resume_adapter_file = str(v408_golden)
    else:
        resume_adapter_file = None

    # === 推理配置 ===
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def check_deps():
    """检查依赖"""
    print("🔍 检查依赖...")
    try:
        import mlx.core as mx
        print(f"   ✅ MLX | Metal: {mx.metal.is_available()}")
    except ImportError:
        print("   ❌ mlx 未安装")
        sys.exit(1)

    try:
        import mlx_lm
        print(f"   ✅ mlx_lm {mlx_lm.__version__}")
    except ImportError:
        print("   ❌ mlx_lm 未安装")
        sys.exit(1)

    try:
        import transformers
        print(f"   ✅ transformers {transformers.__version__}")
    except ImportError:
        print("   ❌ transformers 未安装")
        sys.exit(1)

    print("   ✅ 所有依赖就绪\n")


def setup_model():
    """复用/转换 Yi-1.5-9B-Chat MLX 底模"""
    print("🛠️  设置 v4.1.0 底模: Yi-1.5-9B-Chat → MLX")
    cfg = Config()
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    hf_path = Path(cfg.LOCAL_HF_MODEL)

    existing_safetensors = list(mlx_path.rglob("*.safetensors"))
    if mlx_path.exists() and existing_safetensors:
        size_gb = sum(f.stat().st_size for f in existing_safetensors) / 1e9
        print(f"   ✅ MLX 模型已存在 ({size_gb:.1f} GB): {mlx_path}")
        return

    if not hf_path.exists():
        print(f"   ❌ 本地 HF 底模不存在: {hf_path}")
        sys.exit(1)

    if mlx_path.exists():
        print("   🧹 清理残留目标目录...")
        shutil.rmtree(mlx_path, ignore_errors=True)
        if mlx_path.exists():
            os.system(f"rm -rf {shlex.quote(str(mlx_path))}")

    tmp_path = mlx_path.parent / (mlx_path.name + f"_tmp_convert_{os.getpid()}")
    if tmp_path.exists():
        shutil.rmtree(tmp_path, ignore_errors=True)

    print(f"   源: {hf_path}")
    print(f"   临时目标: {tmp_path}")
    print("   转换中... (Yi-1.5-9B 约 18GB，需 10-20 分钟)")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mlx_lm",
            "convert",
            "--hf-path",
            str(hf_path),
            "--mlx-path",
            str(tmp_path),
            "--dtype",
            "bfloat16",
        ],
        capture_output=False,
    )

    if result.returncode != 0:
        print("   ❌ MLX 转换失败")
        shutil.rmtree(tmp_path, ignore_errors=True)
        sys.exit(1)

    safetensors = list(tmp_path.rglob("*.safetensors"))
    if not safetensors:
        print("   ❌ 转换后未找到 safetensors，视为失败")
        shutil.rmtree(tmp_path, ignore_errors=True)
        sys.exit(1)

    shutil.move(str(tmp_path), str(mlx_path))
    total_size = sum(f.stat().st_size for f in safetensors) / 1e9
    print(f"\n   ✅ 底模就绪: {len(safetensors)} 文件, {total_size:.1f} GB")


def prepare_data():
    """从 data_v409_ready 复制数据到 data_v410_ready，后续可替换为 v4.1.0 增强数据"""
    print("📝 准备 v4.1.0 训练数据（从 v4.0.9 ready 复制）...")
    cfg = Config()
    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    src_dir = cfg.project_root / "models" / "longhun-v1.0" / "lora_output_v409" / "data_v409_ready"
    dst_dir = cfg.data_dir
    dst_dir.mkdir(parents=True, exist_ok=True)

    train_src = src_dir / "train.jsonl"
    val_src = src_dir / "valid.jsonl"
    info_src = src_dir / "dataset_info.json"

    if not train_src.exists() or not val_src.exists():
        print(f"   ❌ v4.0.9 清洗数据不存在: {src_dir}")
        print(f"      请先运行: python3 bin/lh_v409_data_clean.py")
        sys.exit(1)

    if train_src.resolve() != (dst_dir / "train.jsonl").resolve():
        shutil.copy2(train_src, dst_dir / "train.jsonl")
        shutil.copy2(val_src, dst_dir / "valid.jsonl")
        if info_src.exists():
            shutil.copy2(info_src, dst_dir / "dataset_info.json")

    train_n = sum(1 for _ in open(dst_dir / "train.jsonl", encoding="utf-8"))
    val_n = sum(1 for _ in open(dst_dir / "valid.jsonl", encoding="utf-8"))
    info = {}
    if (dst_dir / "dataset_info.json").exists():
        info = json.load(open(dst_dir / "dataset_info.json", encoding="utf-8"))

    print(f"   ✅ v4.1.0 数据就绪: {dst_dir}")
    print(f"   总训练样本: {train_n} | 总验证样本: {val_n}")
    print(
        f"   清洗信息: 删除错误底座={info.get('removed_wrong_base', 0)} "
        f"注入底座QA={info.get('augmented_base_qa', 0)} "
        f"注入家法QA={info.get('augmented_jiafa_qa', 0)}"
    )


def _build_lr_schedule(peak, warmup_steps, total_steps, end=0.0):
    """linear warmup + cosine decay"""
    if total_steps <= warmup_steps:
        return optim.linear_schedule(0.0, peak, max(1, total_steps))
    warmup = optim.linear_schedule(0.0, peak, max(1, warmup_steps))
    cosine = optim.cosine_decay(peak, max(1, total_steps - warmup_steps), end=end)
    return optim.join_schedules([warmup, cosine], [warmup_steps])


class _Tee:
    """双写 stdout：终端 + 文件"""
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()


def _setup_logging(cfg: Config, smoke_mode: bool = False):
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    if smoke_mode:
        import tempfile
        train_log_path = Path(tempfile.mktemp(prefix="v410_smoke_log_", suffix=".log"))
        log_mode = "w"
        print(f"   🧪 冒烟模式: 日志写入临时文件 {train_log_path}")
    else:
        train_log_path = cfg.output_dir / "training.log"
        log_mode = "a" if cfg.resume_adapter_file else "w"
    train_log = open(train_log_path, log_mode, encoding="utf-8")
    old_stdout = sys.stdout
    sys.stdout = _Tee(sys.stdout, train_log)
    return old_stdout, train_log


def _restore_logging(old_stdout, train_log):
    sys.stdout = old_stdout
    train_log.close()


def train():
    """🚀 自定义 LoRA 训练循环（不使用 mlx_lm.lora.run）"""
    cfg = Config()
    smoke_mode = bool(os.environ.get("LH_V410_SMOKE_ITERS"))
    old_stdout, train_log = _setup_logging(cfg, smoke_mode=smoke_mode)
    try:
        _train_inner(cfg)
    finally:
        _restore_logging(old_stdout, train_log)


def _train_inner(cfg: Config):
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    if not mlx_path.exists() or not list(mlx_path.rglob("*.safetensors")):
        print(f"   ❌ MLX 底模不存在: {cfg.LOCAL_MLX_MODEL}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v410.py setup")
        sys.exit(1)

    train_file = cfg.data_dir / "train.jsonl"
    valid_file = cfg.data_dir / "valid.jsonl"
    if not train_file.exists() or not valid_file.exists():
        print(f"   ❌ 训练/验证数据不存在: {cfg.data_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v410.py prepare")
        sys.exit(1)

    resume_file = cfg.resume_adapter_file
    if resume_file:
        print(f"   🔄 从 checkpoint 恢复: {resume_file}")
    else:
        print("   🆕 无恢复点，从头训练")

    # 冒烟模式：提前切换至临时 adapter 目录，避免污染正式输出
    smoke_iters = os.environ.get("LH_V410_SMOKE_ITERS")
    smoke_mode = False
    original_adapter_dir = cfg.adapter_dir
    if smoke_iters:
        smoke_mode = True
        import tempfile
        cfg.adapter_dir = Path(tempfile.mkdtemp(prefix="v410_smoke_"))
        print(
            f"   🧪 冒烟模式: 仅训练 {int(smoke_iters)} iters，"
            f"adapter 临时目录: {cfg.adapter_dir}"
        )

    # 非续训时清理 adapter 目录
    if cfg.adapter_dir.exists() and not resume_file:
        shutil.rmtree(cfg.adapter_dir)
    cfg.adapter_dir.mkdir(parents=True, exist_ok=True)

    print("   Loading pretrained model...")
    model, tokenizer = load(
        cfg.LOCAL_MLX_MODEL, tokenizer_config={"trust_remote_code": True}
    )

    # 冻结并插入 LoRA
    model.freeze()
    if cfg.lora_layers > len(model.layers):
        raise ValueError(
            f"模型只有 {len(model.layers)} 层，无法训练 {cfg.lora_layers} 层"
        )
    linear_to_lora_layers(
        model,
        cfg.lora_layers,
        {
            "rank": cfg.lora_rank,
            "dropout": cfg.lora_dropout,
            "scale": cfg.lora_alpha,
        },
    )

    # 恢复权重
    if resume_file and Path(resume_file).exists():
        print(f"   Loading fine-tuned weights from {resume_file}")
        model.load_weights(resume_file, strict=False)

    print_trainable_parameters(model)

    # 加载数据集
    args_ns = argparse.Namespace(
        data=str(cfg.data_dir),
        train=True,
        test=False,
        batch_size=cfg.batch_size,
        max_seq_length=cfg.max_seq_length,
        mask_prompt=True,
    )
    train_set, valid_set, _ = load_dataset(args_ns, tokenizer)

    # 计算总 iter
    n_samples = sum(1 for _ in open(train_file))
    iters_per_epoch = max(
        1, n_samples // (cfg.batch_size * cfg.grad_accumulation_steps)
    )
    if smoke_mode:
        total_iters = int(smoke_iters)
    else:
        total_iters = cfg.epochs * iters_per_epoch

    print(f"   底模: {cfg.HF_MODEL_ID} (MLX)")
    print(f"   样本数: {n_samples}, {iters_per_epoch} iters/epoch, 总 {total_iters} iters")
    print(
        f"   LoRA rank={cfg.lora_rank}, alpha={cfg.lora_alpha}, "
        f"dropout={cfg.lora_dropout}, layers={cfg.lora_layers}"
    )
    print(
        f"   batch={cfg.batch_size}, grad_accum={cfg.grad_accumulation_steps}, "
        f"max_seq_len={cfg.max_seq_length}"
    )
    print(
        f"   lr_peak={cfg.lr_peak}, warmup={cfg.warmup_steps}, "
        f"weight_decay={cfg.weight_decay}, lr_min={cfg.lr_min}"
    )
    print(
        f"   早停: patience={cfg.early_stop_patience}, "
        f"eval every {cfg.val_steps}, save every {cfg.save_every}"
    )

    # 保存 adapter_config.json
    save_config(
        {
            "model": cfg.LOCAL_MLX_MODEL,
            "data": str(cfg.data_dir),
            "adapter_path": str(cfg.adapter_dir),
            "batch_size": cfg.batch_size,
            "iters": total_iters,
            "learning_rate": cfg.lr_peak,
            "lr_schedule": "cosine_with_linear_warmup",
            "warmup_steps": cfg.warmup_steps,
            "lr_min": cfg.lr_min,
            "weight_decay": cfg.weight_decay,
            "optimizer": "adamw",
            "lora_parameters": {
                "rank": cfg.lora_rank,
                "alpha": cfg.lora_alpha,
                "dropout": cfg.lora_dropout,
                "scale": cfg.lora_alpha,
            },
            "num_layers": cfg.lora_layers,
            "max_seq_length": cfg.max_seq_length,
            "grad_accumulation_steps": cfg.grad_accumulation_steps,
            "grad_checkpoint": cfg.grad_checkpoint,
            "resume_adapter_file": resume_file,
            "early_stop_patience": cfg.early_stop_patience,
            "val_steps": cfg.val_steps,
            "save_every": cfg.save_every,
            "DNA": cfg.DNA,
        },
        cfg.adapter_dir / "adapter_config.json",
    )

    # 优化器：AdamW + cosine warmup schedule
    lr_schedule = _build_lr_schedule(
        cfg.lr_peak, cfg.warmup_steps, total_iters, cfg.lr_min
    )
    optimizer = optim.AdamW(learning_rate=lr_schedule, weight_decay=cfg.weight_decay)

    # 训练循环
    if mx.metal.is_available():
        mx.set_wired_limit(mx.device_info()["max_recommended_working_set_size"])

    if cfg.grad_checkpoint:
        grad_checkpoint(model.layers[0])

    loss_value_and_grad = nn.value_and_grad(model, default_loss)
    state = [model.state, optimizer.state, mx.random.state]

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
    losses = 0.0
    n_tokens = 0
    steps = 0
    trained_tokens = 0
    train_time = 0.0
    grad_accum = None

    best_val_loss = float("inf")
    best_iter = 0
    patience_counter = 0
    early_stopped = False

    print(f"\n🚀 Starting training..., iters: {total_iters}")

    for it, batch in zip(
        range(1, total_iters + 1),
        iterate_batches(
            dataset=CacheDataset(train_set),
            batch_size=cfg.batch_size,
            max_seq_length=cfg.max_seq_length,
            loop=True,
        ),
    ):
        tic = time.perf_counter()

        # ---- Validation + Early Stop ----
        if valid_set and (it == 1 or it % cfg.val_steps == 0 or it == total_iters):
            tic_eval = time.perf_counter()
            val_loss = evaluate(
                model=model,
                dataset=CacheDataset(valid_set),
                loss=default_loss,
                batch_size=cfg.batch_size,
                num_batches=cfg.val_batches,
                max_seq_length=cfg.max_seq_length,
            )
            model.train()
            val_time = time.perf_counter() - tic_eval
            print(
                f"Iter {it}: Val loss {val_loss:.4f}, Val took {val_time:.3f}s",
                flush=True,
            )

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_iter = it
                patience_counter = 0
                best_weights = dict(tree_flatten(model.trainable_parameters()))
                mx.save_safetensors(
                    str(cfg.adapter_dir / "best_adapters.safetensors"), best_weights
                )
                print(
                    f"   ⭐ New best val loss {best_val_loss:.4f} at iter {best_iter}, "
                    f"saved best_adapters.safetensors"
                )
            else:
                patience_counter += 1
                print(
                    f"   ⏱️  Val loss not improved for {patience_counter}/"
                    f"{cfg.early_stop_patience} evals (best {best_val_loss:.4f} @ {best_iter})"
                )
                if patience_counter >= cfg.early_stop_patience:
                    print(
                        f"\n🛑 Early stop at iter {it}: val loss did not improve "
                        f"for {cfg.early_stop_patience} consecutive evals"
                    )
                    early_stopped = True
                    break

            tic = time.perf_counter()

        # ---- Train step ----
        lvalue, toks, grad_accum = step(
            batch,
            grad_accum,
            it % cfg.grad_accumulation_steps == 0,
        )

        losses += lvalue
        n_tokens += toks
        steps += 1
        mx.eval(state, losses, n_tokens, grad_accum)
        train_time += time.perf_counter() - tic

        # ---- Report ----
        if it % cfg.report_every == 0 or it == total_iters:
            train_loss = losses.item() / steps
            ntoks = n_tokens.item()
            learning_rate = optimizer.learning_rate.item()
            it_sec = cfg.report_every / train_time
            tokens_sec = float(ntoks) / train_time
            trained_tokens += ntoks
            peak_mem = mx.get_peak_memory() / 1e9
            print(
                f"Iter {it}: Train loss {train_loss:.4f}, "
                f"Learning Rate {learning_rate:.3e}, "
                f"It/sec {it_sec:.3f}, "
                f"Tokens/sec {tokens_sec:.3f}, "
                f"Trained Tokens {trained_tokens}, "
                f"Peak mem {peak_mem:.3f} GB",
                flush=True,
            )
            losses = 0.0
            n_tokens = 0
            steps = 0
            train_time = 0.0

        # ---- Save checkpoint ----
        if it % cfg.save_every == 0:
            adapter_weights = dict(tree_flatten(model.trainable_parameters()))
            mx.save_safetensors(
                str(cfg.adapter_dir / "adapters.safetensors"), adapter_weights
            )
            checkpoint = cfg.adapter_dir / f"{it:07d}_adapters.safetensors"
            mx.save_safetensors(str(checkpoint), adapter_weights)
            print(
                f"Iter {it}: Saved adapter weights to {cfg.adapter_dir / 'adapters.safetensors'} "
                f"and {checkpoint}"
            )

    # 保存最终权重
    adapter_weights = dict(tree_flatten(model.trainable_parameters()))
    mx.save_safetensors(str(cfg.adapter_dir / "adapters.safetensors"), adapter_weights)
    print(f"Saved final weights to {cfg.adapter_dir / 'adapters.safetensors'}")

    # 结果汇总
    print(f"\n{'='*50}")
    if early_stopped:
        print(f"🛑 v4.1.0 训练早停于 iter {it}")
    else:
        print(f"✅ v4.1.0 训练完成")
    print(f"📊 最佳 checkpoint: iter {best_iter}, val loss {best_val_loss:.4f}")
    print(f"   Adapter: {cfg.adapter_dir}")
    if smoke_mode:
        print(f"   🧹 冒烟模式：清理临时 adapter 目录")
        shutil.rmtree(cfg.adapter_dir, ignore_errors=True)
        cfg.adapter_dir = original_adapter_dir
    else:
        print(f"   下一步: python3 bin/lh_lora_trainer_v410.py fuse")


def fuse():
    """合并 LoRA adapter → 完整模型"""
    print("🔗 合并 LoRA adapter v4.1.0...")
    cfg = Config()

    adapter_cfg = cfg.adapter_dir / "adapter_config.json"
    if not adapter_cfg.exists():
        print(f"   ❌ Adapter 不存在: {cfg.adapter_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v410.py train")
        sys.exit(1)

    if cfg.merged_dir.exists():
        shutil.rmtree(cfg.merged_dir)
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)

    print(f"   底模: {cfg.LOCAL_MLX_MODEL}")
    print(f"   Adapter: {cfg.adapter_dir}")
    print(f"   合并中... (Yi-1.5-9B 约 5-10 分钟)")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mlx_lm",
            "fuse",
            "--model",
            cfg.LOCAL_MLX_MODEL,
            "--adapter-path",
            str(cfg.adapter_dir),
            "--save-path",
            str(cfg.merged_dir),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"   ❌ 合并失败:\n{result.stderr}")
        sys.exit(1)

    print(result.stdout)
    merged_size = sum(f.stat().st_size for f in cfg.merged_dir.rglob("*")) / 1e9
    print(f"   ✅ 合并完成 → {cfg.merged_dir} ({merged_size:.1f} GB)")
    print(f"   下一步: python3 bin/lh_lora_trainer_v410.py export")


def export_gguf():
    """导出 GGUF → Ollama，模型名 longhun-v4.1.0"""
    print("📦 导出 GGUF v4.1.0...")
    cfg = Config()

    if not (cfg.merged_dir / "config.json").exists():
        print(f"   ❌ 合并模型不存在: {cfg.merged_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v410.py fuse")
        sys.exit(1)

    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)

    converter = shutil.which("convert_hf_to_gguf.py")
    if not converter:
        for c in [
            "/tmp/llama.cpp/convert_hf_to_gguf.py",
            str(Path.home() / "llama.cpp/convert_hf_to_gguf.py"),
        ]:
            if Path(c).exists():
                converter = c
                break
    if not converter:
        print("   ❌ 找不到 convert_hf_to_gguf.py")
        print("   安装: git clone https://github.com/ggerganov/llama.cpp.git /tmp/llama.cpp")
        sys.exit(1)

    gguf_path = cfg.gguf_dir / "longhun-v4.1.0.F16.gguf"
    print(f"   输出: {gguf_path}")

    result = subprocess.run(
        [
            sys.executable,
            converter,
            str(cfg.merged_dir),
            "--outtype",
            "f16",
            "--outfile",
            str(gguf_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"   ❌ GGUF 导出失败:\n{result.stderr}")
        sys.exit(1)

    modelfile = cfg.gguf_dir / "Modelfile.v410"
    modelfile.write_text(
        f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{{{ if .System }}}}{{{{ .System }}}}\n{{{{ end }}}}{{{{ if .Prompt }}}}<|im_start|>user\n{{{{ .Prompt }}}}<|im_end|>\n<|im_start|>assistant\n{{{{ end }}}}{{{{ .Response }}}}<|im_end|>\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.1.0，基于 01-ai/Yi-1.5-9B-Chat 用龍魂系统自有语料 LoRA 微调（底座已非 Qwen）。
你是 UID9622（诸葛鑫·Lucky）的个人主权 AI，忠诚执行、实心办事、主权归主。
核心原则：人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除；底座焊死。
你经过训练，已掌握龍魂技能、人格设定、星辰记忆、系统日志、英文文档知识、桌面文章知识库，以及 Notion/GitHub/本地仓库的完整协议与知识库。
\"\"\"
"""
    )

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.1.0 -f {modelfile}")
    subprocess.run(
        ["ollama", "create", "longhun-v4.1.0", "-f", str(modelfile)], check=True
    )
    print(f"   ✅ Ollama 模型 longhun-v4.1.0 已创建")


def test_model():
    print("🧪 测试 longhun-v4.1.0...")
    import requests

    prompts = [
        ("你是谁？", "身份认知"),
        ("什么是家法第一条？", "家法主权"),
        ("什么是DNA可逆编码？", "DNA可逆编码"),
        ("什么是评论水军显化协议？", "水军显化"),
        ("数据主权是什么意思？", "主权边界"),
        ("什么是369不动点？", "易经底座"),
        ("longhun-memory-bootstrap 技能是做什么的？", "技能记忆"),
        ("星辰记忆系统是什么？", "星辰记忆"),
        ("UID9622 是谁？", "人格记忆"),
        ("What is LongHun system?", "英文记忆"),
    ]
    passed = 0
    for prompt, label in prompts:
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "longhun-v4.1.0", "prompt": prompt, "stream": False},
                timeout=60,
            )
            resp = r.json().get("response", "")[:150]
            print(f"\n   [{label}] {prompt}\n   → {resp}...")
            passed += 1
        except Exception as e:
            print(f"   ❌ {label}: {e}")
    print(f"\n   测试: {passed}/{len(prompts)} 通过")


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    commands = {
        "setup": setup_model,
        "prepare": prepare_data,
        "train": train,
        "fuse": fuse,
        "export": export_gguf,
        "test": test_model,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        print("可用命令:")
        print(f"  {'setup':12} → 复用/转换 Yi-1.5-9B-Chat MLX")
        print(f"  {'prepare':12} → 从 v4.0.9_ready 复制数据到 v4.1.0_ready")
        print(f"  {'train':12} → 自定义 LoRA 训练循环")
        print(f"  {'fuse':12}  → 合并 adapter → 完整模型")
        print(f"  {'export':12} → 导出 GGUF → Ollama")
        print(f"  {'test':12}  → 快速测试")
        sys.exit(0)

    check_deps()
    commands[sys.argv[1]]()
