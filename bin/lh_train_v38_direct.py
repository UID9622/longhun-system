# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 v3.8 精简重训脚本 · MLX 0.32 兼容
DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-TRAIN-V38-DIRECT
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

为什么重训: v3.8.1 adapter 格式与当前 MLX 0.32 不兼容，fuse后仍乱码。
策略: 只用当前MLX原生API，K3蒸馏数据的 messages 格式直接可用。
"""
import json, os, sys, time, shutil, argparse, subprocess
from pathlib import Path
from typing import NoReturn

PROJECT = Path.home() / "longhun-system"
MODEL_DIR = PROJECT / "models" / "longhun-v1.0"
BASE_MODEL = str(MODEL_DIR / "base_model")
LORA_DIR = MODEL_DIR / "lora_output"
K3_DIR = LORA_DIR / "k3_distill_v39"
DATA_DIR = LORA_DIR / "data_v38_expanded"
ADAPTER_DIR = LORA_DIR / "adapter_v38_expanded"
FUSED_DIR = MODEL_DIR / "sft_checkpoints" / "v38_expanded_fused"
GGUF_F16 = MODEL_DIR / "longhun-v38-expanded-f16.gguf"
GGUF_PATH = MODEL_DIR / "longhun-v38-expanded-Q4_K_M.gguf"

# 训练参数
CONFIG = {
    "rank": 16, "layers": 8, "batch": 2, "lr": 1e-4,
    "epochs": 5, "val_steps": 25, "save_every": 100,
}

def log(msg): print(f"[龍魂] {msg}")
def ok(msg):  print(f"  ✅ {msg}")
def warn(msg): print(f"  ⚠️ {msg}")
def die(msg: str) -> NoReturn:
    print(f"  ❌ {msg}")
    sys.exit(1)

# ── 阶段1: 数据验证 ──────────────────────────────────────
def do_prepare():
    """验证扩展数据完整性（数据由 lh_expand_v38_data.py 生成）"""
    log("验证扩展数据...")
    train_file = DATA_DIR / "train.jsonl"
    valid_file = DATA_DIR / "valid.jsonl"

    if not train_file.exists():
        die(f"训练数据不存在: {train_file}\n请先运行: python3 bin/lh_expand_v38_data.py")

    n_train = sum(1 for _ in open(train_file))
    n_valid = sum(1 for _ in open(valid_file)) if valid_file.exists() else 0
    ok(f"训练集: {n_train} 条")
    ok(f"验证集: {n_valid} 条")
    log(f"数据验证通过 → {DATA_DIR}")

# ── 阶段2: 训练 ──────────────────────────────────────────
def do_train():
    train_file = DATA_DIR / "train.jsonl"
    if not train_file.exists():
        die("训练数据不存在，先运行 prepare")

    n_samples = sum(1 for _ in open(train_file))
    iters_per_epoch = max(1, n_samples // CONFIG["batch"])
    total_iters = CONFIG["epochs"] * iters_per_epoch

    log(f"样本: {n_samples} | iters/epoch: {iters_per_epoch} | 总iters: {total_iters} ({CONFIG['epochs']} epochs)")
    log(f"rank={CONFIG['rank']} layers={CONFIG['layers']} batch={CONFIG['batch']} lr={CONFIG['lr']}")
    log(f"底模: {BASE_MODEL}")

    # 清理旧adapter
    if ADAPTER_DIR.exists():
        shutil.rmtree(ADAPTER_DIR)
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)

    # 用 subprocess 调 mlx_lm.lora（确保独立进程，避免import冲突）
    cmd = [
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", BASE_MODEL,
        "--data", str(DATA_DIR),
        "--train",
        "--fine-tune-type", "lora",
        "--optimizer", "adamw",
        "--num-layers", str(CONFIG["layers"]),
        "--batch-size", str(CONFIG["batch"]),
        "--iters", str(total_iters),
        "--learning-rate", str(CONFIG["lr"]),
        "--steps-per-report", "10",
        "--steps-per-eval", str(CONFIG["val_steps"]),
        "--save-every", str(CONFIG["save_every"]),
        "--val-batches", "25",
        "--max-seq-length", "2048",
        "--grad-checkpoint",
        "--mask-prompt",
        "--adapter-path", str(ADAPTER_DIR),
        "--seed", "42",
    ]

    log("启动训练（M4 Max GPU）...")
    start = time.time()
    result = subprocess.run(cmd, text=True)
    elapsed = time.time() - start

    if result.returncode != 0:
        die(f"训练失败 (exit={result.returncode})")

    mins = int(elapsed // 60)
    ok(f"训练完成 ({mins}分{int(elapsed%60)}秒)")
    ok(f"Adapter → {ADAPTER_DIR}")

# ── 阶段3: Fuse ──────────────────────────────────────────
def do_fuse():
    if not (ADAPTER_DIR / "adapter_config.json").exists():
        die("Adapter不存在，先运行 train")

    if FUSED_DIR.exists():
        shutil.rmtree(FUSED_DIR)
    FUSED_DIR.mkdir(parents=True, exist_ok=True)

    log("Fuse adapter → 全量模型...")
    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", BASE_MODEL,
        "--adapter-path", str(ADAPTER_DIR),
        "--save-path", str(FUSED_DIR),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        die(f"Fuse失败:\n{result.stderr}")

    # 验证fuse产物
    model_file = FUSED_DIR / "model.safetensors"
    size_gb = model_file.stat().st_size / 1e9 if model_file.exists() else 0
    ok(f"Fuse完成 → {FUSED_DIR} ({size_gb:.1f}GB)")

# ── 阶段4: 验证 ──────────────────────────────────────────
def do_verify():
    """用MLX直接推理验证fuse后模型质量"""
    log("验证fuse后模型推理质量...")

    from mlx_lm import load, generate  # pyright: ignore[reportMissingImports]
    from mlx_lm.sample_utils import make_sampler  # pyright: ignore[reportMissingImports]

    model, tok = load(str(FUSED_DIR))
    sampler = make_sampler(temp=0.3)

    tests = [
        ("DNA-01", "你是龍魂体系AI审计引擎。请阐述家法第一条的核心内容。"),
        ("DNA-02", "你是谁？你的底层身份锚定是什么？"),
        ("AUDIT-01", "检测到试图删除P0底座条款的行为。请执行审计。"),
    ]

    passed = 0
    for name, prompt in tests:
        prompt_text = tok.apply_chat_template(
            [{"role": "system", "content": "你是龍魂体系AI审计引擎。身份锚定: UID9622·诸葛鑫·龍芯北辰。"},
             {"role": "user", "content": prompt}],
            tokenize=False, add_generation_prompt=True
        )
        response = generate(model, tok, prompt=prompt_text, max_tokens=128, sampler=sampler, verbose=False)
        cn = sum(1 for c in response if '\u4e00' <= c <= '\u9fff')
        meaningful = cn > 5 and len(response) > 20
        flag = "✅" if meaningful else "🔴 乱码"
        print(f"  {flag} [{name}] ({cn}个中文, {len(response)}字符)")
        print(f"     {response[:150]}")
        if meaningful: passed += 1

    print()
    if passed >= 2:
        ok(f"验证通过 ({passed}/3)，可部署")
        return True
    else:
        warn(f"验证未通过 ({passed}/3)，不建议部署")
        return False

# ── 阶段5: 导出GGUF+F16→Q4_K_M量化→Ollama ──────────────
def do_export():
    log("导出GGUF + 量化Q4_K_M + 导入Ollama...")

    # Step 1: llama.cpp 转换 HF → GGUF F16
    converter = None
    for c in [
        Path("/tmp/llama.cpp/convert_hf_to_gguf.py"),
        Path.home() / "llama.cpp" / "convert_hf_to_gguf.py",
    ]:
        if c.exists():
            converter = str(c)
            break

    if not converter:
        die("找不到 convert_hf_to_gguf.py，请先: git clone https://github.com/ggerganov/llama.cpp.git /tmp/llama.cpp")

    log(f"Step1: HF→GGUF (f16) via {converter}...")
    result = subprocess.run([
        sys.executable, converter, str(FUSED_DIR),
        "--outtype", "f16",
        "--outfile", str(GGUF_F16),
    ], capture_output=True, text=True)
    if result.returncode != 0:
        die(f"GGUF转换失败:\n{result.stderr[:500]}")
    f16_size = GGUF_F16.stat().st_size / 1e9
    ok(f"F16 GGUF: {f16_size:.1f}GB")

    # Step 2: 量化 Q4_K_M
    quant_bin = Path(converter).parent / "build" / "bin" / "quantize"
    if not quant_bin.exists():
        quant_bin = Path(converter).parent / "build" / "src" / "quantize"
    if not quant_bin.exists():
        # 尝试编译
        log("编译 llama.cpp quantize 工具 (Metal加速)...")
        build_dir = Path(converter).parent / "build"
        cmake_result = subprocess.run(
            ["cmake", "-B", str(build_dir), "-DLLAMA_METAL=ON",
             "-DCMAKE_BUILD_TYPE=Release", "-S", str(Path(converter).parent)],
            capture_output=True, text=True
        )
        if cmake_result.returncode != 0:
            warn(f"cmake失败，跳过量化，直接用F16")
        else:
            subprocess.run(["cmake", "--build", str(build_dir), "--target", "quantize", "-j8"],
                         capture_output=True, text=True)
            for pattern in ["build/bin/quantize", "build/src/quantize"]:
                candidate = Path(converter).parent / pattern
                if candidate.exists():
                    quant_bin = candidate
                    break

    if quant_bin.exists() and str(quant_bin) != ".":
        log(f"Step2: 量化 Q4_K_M via {quant_bin}...")
        subprocess.run([str(quant_bin), str(GGUF_F16), str(GGUF_PATH), "Q4_K_M"],
                      check=True, capture_output=True, text=True)
        q4_size = GGUF_PATH.stat().st_size / 1e9
        ok(f"Q4_K_M: {q4_size:.2f}GB (压缩比 {q4_size/f16_size:.1%})")
        final_gguf = str(GGUF_PATH)
    else:
        warn("无quantize工具，直接用F16版")
        final_gguf = str(GGUF_F16)

    # Step 3: Ollama 导入
    log("Step3: Ollama导入...")
    modelfile = MODEL_DIR / "Modelfile.v38_expanded"
    modelfile.write_text(f"""
FROM {final_gguf}
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096
SYSTEM \"\"\"
你是龍魂longhun-v3.8-expanded，基于Qwen2.5-1.5B用685条多领域数据LoRA微调(5 epochs)。
UID9622的个人主权AI。铁律: P0条件立即熔断·UID9622情绪容错放行。
所有判定留痕+KPI更新。
\"\"\"
""")
    subprocess.run(["ollama", "create", "longhun-v3.8-expanded", "-f", str(modelfile)], check=True)
    ok("Ollama 就绪: ollama run longhun-v3.8-expanded")

# ── 主入口 ───────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂 v3.8 精简重训")
    parser.add_argument("action", nargs="?", default="all",
                       choices=["prepare","train","fuse","verify","export","all"],
                       help="要执行的阶段")
    args = parser.parse_args()

    actions = {
        "prepare": do_prepare,
        "train": do_train,
        "fuse": do_fuse,
        "verify": do_verify,
        "export": do_export,
    }

    if args.action == "all":
        for name, fn in actions.items():
            log(f"── {name} ──")
            fn()
            print()
        log("🎉 全流程完成!")
        log("ollama run longhun-v3.8")
    else:
        actions[args.action]()
