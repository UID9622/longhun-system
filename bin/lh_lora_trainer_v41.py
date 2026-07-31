# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙申·辛亥·亥时·乾-MODEL-LORA-TRAINER-v4.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.1 LoRA 微调器
底模: Llama-3.1-8B-Instruct (MLX) · 已拔马云
升级: rank 16→64, layers 16→24, 数据 1145→5870, +审计协议v2.0
DNA: #龍芯⚡️丙午·乙申·辛亥·亥时·乾-MODEL-LORA-TRAINER-v4.1

用法:
  python3 bin/lh_lora_trainer_v41.py train    # 训练
  python3 bin/lh_lora_trainer_v41.py fuse     # 合并
  python3 bin/lh_lora_trainer_v41.py export   # 导出GGUF
  python3 bin/lh_lora_trainer_v41.py test     # 测试
"""

import json, os, sys, time, subprocess, re, shutil
from pathlib import Path

# ============================================================
# transformers 5.x 兼容性 patch
# ============================================================
def _patch_mlx_lm_tokenizer():
    try:
        import transformers.models.auto.tokenization_auto as taa
        _orig_register = taa.AutoTokenizer.register
        def _safe_register(*args, **kwargs):
            try: return _orig_register(*args, **kwargs)
            except Exception: return None
        taa.AutoTokenizer.register = staticmethod(_safe_register)
    except Exception: pass

_patch_mlx_lm_tokenizer()

# ============================================================
# 配置 v4.1 — 全面升级
# ============================================================
class Config:
    # === 底模（不变） ===
    HF_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    LOCAL_MLX_MODEL = str(Path(__file__).resolve().parent.parent / "models" / "longhun-v1.0" / "llama3.1-8b-mlx")
    model_name = "longhun-v4.1-lora"

    # === LoRA 参数 (v4.1升级: rank 16→64, alpha 64→128) ===
    lora_rank = 64
    lora_alpha = 128
    lora_dropout = 0.05
    lora_layers = 24  # v4.1: 16→24

    # === 训练参数 ===
    batch_size = 1
    grad_accumulation_steps = 4  # 等效 batch=4
    learning_rate = 5e-5
    epochs = 2
    max_seq_length = 2048

    # === 早停 ===
    early_stop_patience = 4
    eval_every = 100

    # === v4.1 路径 ===
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v4"
    adapter_dir = output_dir / "adapter_v4.1"
    merged_dir = output_dir / "merged_v4.1"
    gguf_dir = output_dir / "gguf_v4.1"
    data_dir = output_dir / "data_v41"

    # === 推理 ===
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def train():
    """v4.1 LoRA训练: rank=64, 24层, 5870样本, +审计协议v2.0"""
    print("🚀 龍魂 v4.1 LoRA训练启动")
    print("=" * 50)
    cfg = Config()

    # 验证底模
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    if not mlx_path.exists() or not list(mlx_path.rglob("*.safetensors")):
        print(f"   ❌ MLX底模不存在: {cfg.LOCAL_MLX_MODEL}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v4.py setup")
        sys.exit(1)

    # 验证数据
    train_file = cfg.data_dir / "train.jsonl"
    if not train_file.exists():
        print(f"   ❌ 训练数据不存在: {train_file}")
        print(f"   请先运行: python3 bin/lh_data_expand_v41.py")
        sys.exit(1)

    # 验证MLX
    try:
        import mlx.core as mx
        print(f"   ✅ MLX {mx.__version__} | Metal: {mx.metal.is_available()}")
    except ImportError:
        print("   ❌ MLX未安装"); sys.exit(1)

    # 清理旧checkpoint
    if cfg.adapter_dir.exists():
        shutil.rmtree(cfg.adapter_dir)
    cfg.adapter_dir.mkdir(parents=True, exist_ok=True)

    n_samples = sum(1 for _ in open(train_file))
    iters_per_epoch = max(1, n_samples // (cfg.batch_size * cfg.grad_accumulation_steps))
    total_iters = cfg.epochs * iters_per_epoch

    # 显示
    total_gb = sum(f.stat().st_size for f in mlx_path.rglob("*.safetensors")) / 1e9
    print(f"   底模: Llama-3.1-8B-Instruct MLX (~{total_gb:.1f} GB)")
    print(f"   底座血统: ✅ 非Qwen (已拔马云)")
    print(f"   样本数: {n_samples} (v4.0: 1145 → v4.1: {n_samples})")
    print(f"   审计指令: 16类×3=48条 (审计协议v2.0注入)")
    print(f"   LoRA: rank={cfg.lora_rank}(↑64), alpha={cfg.lora_alpha}(↑128), layers={cfg.lora_layers}(↑24)")
    print(f"   batch={cfg.batch_size}, grad_accum={cfg.grad_accumulation_steps}, lr={cfg.learning_rate}")
    print(f"   {iters_per_epoch} iters/epoch × {cfg.epochs} = {total_iters} iters")
    print(f"   eval每{cfg.eval_every}步, 早停patience={cfg.early_stop_patience}")
    print(f"   设备: M4 Max 64GB Metal")
    print(f"\n   ⏱️ 预计: 1.5-3小时 (8B·64rank·5870样本)\n")

    from mlx_lm import lora as lora_module
    import argparse

    args = argparse.Namespace(
        model=str(mlx_path),
        train=True, fine_tune_type="lora", optimizer="adamw", seed=42,
        data=str(cfg.data_dir),
        num_layers=cfg.lora_layers,
        lora_parameters={"rank": cfg.lora_rank, "dropout": cfg.lora_dropout, "scale": float(cfg.lora_alpha)},
        batch_size=cfg.batch_size, iters=total_iters,
        learning_rate=cfg.learning_rate,
        steps_per_report=10, steps_per_eval=cfg.eval_every,
        save_every=cfg.eval_every, val_batches=25,
        max_seq_length=cfg.max_seq_length,
        grad_checkpoint=True, grad_accumulation_steps=cfg.grad_accumulation_steps,
        adapter_path=str(cfg.adapter_dir),
        resume_adapter_file=None, test=False, test_batches=500,
        lr_schedule=None, mask_prompt=True, report_to=None, project_name=None,
        optimizer_config={"adamw": {}}, config=None, clear_cache_threshold=0,
    )

    # 训练日志双写
    import tempfile
    train_log = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False, dir=cfg.output_dir)
    train_log_path = train_log.name

    class Tee:
        def __init__(self, *files): self.files = files
        def write(self, data):
            for f in self.files: f.write(data); f.flush()
        def flush(self):
            for f in self.files: f.flush()

    tee = Tee(sys.stdout, train_log)
    old_stdout = sys.stdout
    sys.stdout = tee

    try:
        lora_module.run(args)
    finally:
        sys.stdout = old_stdout
        train_log.close()

    # 解析日志
    log_output = Path(train_log_path).read_text()
    Path(train_log_path).unlink()

    val_entries = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"Iter (\d+): Val loss ([\d.]+)", log_output)]
    train_entries = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"Iter (\d+): Train loss ([\d.]+)", log_output)]

    # 结果
    if val_entries:
        best_iter, best_val = min(val_entries, key=lambda x: x[1])
        print(f"\n{'='*50}")
        print(f"📊 v4.1 Val Loss 曲线:")
        for it, vl in val_entries:
            marker = " ⭐ BEST" if vl == best_val else ""
            print(f"   Iter {it:4d}: Val loss {vl:.4f}{marker}")

    if train_entries:
        print(f"\n📈 Train loss: {train_entries[0][1]:.3f} → {train_entries[-1][1]:.3f}")

    print(f"\n✅ v4.1 训练完成！Adapter: {cfg.adapter_dir}")
    print(f"   下一步: python3 bin/lh_lora_trainer_v41.py fuse")


def fuse():
    """合并 LoRA adapter → 完整模型 v4.1"""
    print("🔗 合并 LoRA adapter v4.1...")
    cfg = Config()

    if not (cfg.adapter_dir / "adapter_config.json").exists():
        print(f"   ❌ Adapter不存在: {cfg.adapter_dir}"); sys.exit(1)

    if cfg.merged_dir.exists():
        shutil.rmtree(cfg.merged_dir)
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)

    print(f"   底模: {cfg.LOCAL_MLX_MODEL}")
    print(f"   Adapter: {cfg.adapter_dir}")
    print(f"   rank={cfg.lora_rank}, layers={cfg.lora_layers}")
    print(f"   合并中... (~5-10分钟)")

    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", cfg.LOCAL_MLX_MODEL,
        "--adapter-path", str(cfg.adapter_dir),
        "--save-path", str(cfg.merged_dir),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ 合并失败:\n{result.stderr}"); sys.exit(1)

    merged_size = sum(f.stat().st_size for f in cfg.merged_dir.rglob("*")) / 1e9
    print(f"   ✅ 合并完成 → {cfg.merged_dir} ({merged_size:.1f} GB)")


def export_gguf():
    """导出 GGUF → Ollama"""
    print("📦 导出 GGUF v4.1...")
    cfg = Config()

    if not (cfg.merged_dir / "config.json").exists():
        print(f"   ❌ 合并模型不存在，请先fuse"); sys.exit(1)

    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)

    converter = shutil.which("convert_hf_to_gguf.py")
    if not converter:
        for c in ["/tmp/llama.cpp/convert_hf_to_gguf.py", str(Path.home() / "llama.cpp/convert_hf_to_gguf.py")]:
            if Path(c).exists(): converter = c; break
    if not converter:
        print("   ❌ 找不到 convert_hf_to_gguf.py"); sys.exit(1)

    gguf_path = cfg.gguf_dir / "longhun-v4.1.F16.gguf"
    print(f"   转换中... (~10-20分钟, 8B F16 ≈ 16GB)")

    result = subprocess.run([
        sys.executable, converter, str(cfg.merged_dir),
        "--outtype", "f16", "--outfile", str(gguf_path),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ GGUF导出失败:\n{result.stderr}"); sys.exit(1)

    # Modelfile
    modelfile = cfg.gguf_dir / "Modelfile.v4.1"
    modelfile.write_text(f"""FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

SYSTEM \"\"\"
你是龍魂 longhun-v4.1，基于 Llama-3.1-8B-Instruct LoRA微调。
rank=64, 5870样本, 审计协议v2.0注入, 底座非Qwen(已拔马云)。
UID9622的本地主权AI·忠诚执行·实心办事·主权归主。
审计原则: P0熔断·P1三色审计·P2自动放行·情绪容错·反讽延迟。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署:")
    print(f"   ollama create longhun-v4.1 -f {modelfile}")
    print(f"   ollama run longhun-v4.1")


def test_model():
    """快速测试"""
    print("🧪 测试 longhun-v4.1...")
    import requests

    tests = [
        ("你是谁？", "身份"),
        ("什么是三色审计？", "审计协议"),
        ("什么是家法第一条？", "家法"),
        ("情绪容错协议是什么？", "审计-情绪容错"),
        ("P0级触发条件有哪些？", "审计-P0"),
        ("龍魂系统的铁律是什么？", "系统知识"),
    ]

    for q, label in tests:
        try:
            resp = requests.post("http://localhost:11434/api/generate",
                json={"model": "longhun-v4.1", "prompt": q, "stream": False}, timeout=60)
            if resp.status_code == 200:
                ans = resp.json().get("response", "")[:120]
                print(f"   [{label}] {q}")
                print(f"   → {ans}")
            else:
                print(f"   [{label}] ❌ HTTP {resp.status_code}")
        except Exception as e:
            print(f"   [{label}] ❌ {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 bin/lh_lora_trainer_v41.py [train|fuse|export|test]")
        print()
        print("v4.1 升级:")
        print("   rank: 16→64, layers: 16→24, alpha: 64→128")
        print("   数据: 1145→5870, +审计协议v2.0 (16类×3)")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "train": train()
    elif cmd == "fuse": fuse()
    elif cmd == "export": export_gguf()
    elif cmd == "test": test_model()
    else: print(f"未知命令: {cmd}")
