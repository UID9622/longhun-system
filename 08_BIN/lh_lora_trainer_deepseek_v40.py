#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷈小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-LH_LORA_TRAINER_DEEPSEEK_V40-v1.0-5872ced2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.0 DeepSeek 版 LoRA 微调器
底模: DeepSeek-R1-Distill-Llama-8B (MLX)
框架: MLX (Apple Silicon 原生)
硬件: Mac M4 Max 64GB

v4.0 DeepSeek fallback（Llama-3.1-8B 线验证失败，按预案换底座重训）:
- 数据不动：复用 v3.8.1 清洗后的 979 样本 / 13 知识域
- 只换底座：Llama-3.1-8B-Instruct → DeepSeek-R1-Distill-Llama-8B
- LoRA rank=16, alpha=64, 16 layers
- 目标：家法召回 ≥90%、多轮漂移 ≥80%、实测无胡话

用法:
  python3 bin/lh_lora_trainer_deepseek_v40.py prepare  # 准备训练数据
  python3 bin/lh_lora_trainer_deepseek_v40.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_deepseek_v40.py fuse     # 合并 adapter → 完整模型
  python3 bin/lh_lora_trainer_deepseek_v40.py export   # 导出 GGUF → Ollama 加载
  python3 bin/lh_lora_trainer_deepseek_v40.py test     # 快速测试
"""

import json, os, sys, time, subprocess
from pathlib import Path

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
# 配置 v4.0
# ============================================================
class Config:
    # === 底模（DeepSeek-R1-Distill-Llama-8B） ===
    HF_MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
    LOCAL_MLX_MODEL = str(Path(__file__).parent.parent / "models" / "longhun-v1.0" / "deepseek-r1-distill-llama-8b-mlx")
    model_name = "longhun-v4.0-deepseek-lora"

    # === LoRA 参数（rank=16，适配 8B） ===
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.05
    lora_layers = 16  # 8B 模型用更多层

    # === 训练参数（8B 模型适配） ===
    batch_size = 1        # 8B 模型内存限制，batch=1
    learning_rate = 5e-5  # 先用 Llama 线同参数，失败再调
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True
    grad_accumulation_steps = 4  # 累积梯度模拟更大 batch

    # === 早停 ===
    early_stop_patience = 3
    val_steps = 50  # 8B 每 50 iters 评估

    # === 数据（复用 v3.8.1 清洗后的数据） ===
    corpus_path = "models/longhun-v1.0/training_corpus_v3.0.md"
    train_split = 0.9

    # === v4.0 DeepSeek 输出路径 ===
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_deepseek_v40"
    adapter_dir = output_dir / "adapter_v4.0"
    merged_dir = output_dir / "merged_v4.0"
    gguf_dir = output_dir / "gguf_v4.0"
    data_dir = output_dir / "data"

    # === 推理配置 ===
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def check_deps():
    """检查并修复依赖"""
    print("🔍 检查依赖...")
    issues = []

    try:
        import mlx.core as mx
        print(f"   ✅ MLX {mx.__version__} | Metal: {mx.metal.is_available()}")
    except ImportError:
        issues.append("mlx")

    try:
        import mlx_lm
        print(f"   ✅ mlx_lm")
    except ImportError:
        issues.append("mlx-lm")

    try:
        import transformers
        v = transformers.__version__
        print(f"   ✅ transformers {v}")
    except ImportError:
        issues.append("transformers")

    # v4.0: 走国内 hf-mirror.com 镜像，不需要 HF 登录
    print(f"   ✅ HF 镜像: https://hf-mirror.com (国内可用)")

    if issues:
        print(f"\n🔧 需要修复 {len(issues)} 个依赖:")
        python = sys.executable
        for dep in issues:
            if dep == "mlx":
                os.system(f"{python} -m pip install mlx --break-system-packages -q")
            elif dep == "mlx-lm":
                os.system(f"{python} -m pip install mlx-lm --break-system-packages -q")
            elif dep == "transformers":
                os.system(f"{python} -m pip install transformers --break-system-packages -q")
        print("   ✅ 依赖修复完成，请重新运行")
        sys.exit(0)

    print("   ✅ 所有依赖就绪\n")


def setup_model():
    """校验 DeepSeek-R1-Distill-Llama-8B MLX 底模已就位"""
    cfg = Config()
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    existing_safetensors = list(mlx_path.rglob("*.safetensors"))
    
    print("🛠️  校验 DeepSeek MLX 底模...")
    if mlx_path.exists() and existing_safetensors:
        size_gb = sum(f.stat().st_size for f in existing_safetensors) / 1e9
        print(f"   ✅ MLX 模型已存在 ({size_gb:.1f} GB)")
        return
    
    print(f"   ❌ MLX 底模不存在: {cfg.LOCAL_MLX_MODEL}")
    print("   请先运行:")
    print("   python3 -m mlx_lm.convert \\")
    print("       --hf-path models/base_models_v4.0/DeepSeek-R1-Distill-Llama-8B \\")
    print("       --mlx-path models/longhun-v1.0/deepseek-r1-distill-llama-8b-mlx \\")
    print("       --dtype bfloat16")
    sys.exit(1)

def prepare_data():
    """准备训练数据 v6.4（972 样本 · 13 知识域 · 适配 DeepSeek-R1-Distill-Llama-8B thinking 格式）

    v4.0.1 改动：
    - 不复用 v3.8.1 的 Qwen 洗法
    - 调用 lh_generate_thinking_v401.py 为每条样本生成 <think>推理过程</think>正式回答
    - 输出 train_v401_think.jsonl，作为训练输入
    """
    print("📝 准备训练数据 v6.4（972样本 · 13域 · DeepSeek thinking 格式）...")
    cfg = Config()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)

    think_file = cfg.data_dir / "train_v401_think.jsonl"
    if think_file.exists():
        print(f"   ✅ 已存在 thinking 数据: {think_file}")
        print(f"   跳过生成，直接复用。")
        print(f"\n✅ v4.0.1 数据就绪: {cfg.data_dir}")
        return

    # 先生成基础数据（v3.8.1 清洗逻辑）
    print("   1/2 生成基础训练数据...")
    sys.path.insert(0, str(Path(__file__).parent))
    from lh_lora_trainer import prepare_data as v37_prepare
    import lh_lora_trainer as v37
    original_data_dir = v37.Config.data_dir
    v37.Config.data_dir = cfg.data_dir
    try:
        v37_prepare()
    finally:
        v37.Config.data_dir = original_data_dir

    # 生成 thinking 数据
    print("   2/2 调用 thinking 生成器（教师模型 deepseek-r1:7b）...")
    from lh_generate_thinking_v401 import main as generate_thinking
    generate_thinking()

    print(f"\n✅ v4.0.1 数据就绪: {cfg.data_dir}")


def train():
    """LoRA 微调 v4.0 DeepSeek 版: rank=16, 底模 DeepSeek-R1-Distill-Llama-8B, epochs=2

    8B 模型训练策略:
    - batch_size=1 + grad_accumulation_steps=4 (等效 batch=4)
    - lr=5e-5 (先用 Llama 线同参数，失败再调)
    - save_every=50, val_batches=25
    - 早停 patience=3
    """
    print("🚀 开始 LoRA 微调 v4.0 DeepSeek 版 (DeepSeek-R1-Distill-Llama-8B, rank=16, epochs=2)...")
    cfg = Config()
    import shutil

    # 验证底模
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    if not mlx_path.exists() or not (mlx_path / "model.safetensors").exists():
        if not list(mlx_path.rglob("*.safetensors")):
            print(f"   ❌ MLX 底模不存在: {cfg.LOCAL_MLX_MODEL}")
            print(f"   请先运行: python3 bin/lh_lora_trainer_v4.py setup")
            sys.exit(1)

    # 验证数据：v4.0.1 强制使用 thinking 格式数据
    train_file = cfg.data_dir / "train_v401_think.jsonl"
    if not train_file.exists():
        # 尝试从 v3.8.1 数据目录复制 thinking 数据
        v381_think = cfg.project_root / "models" / "longhun-v1.0" / "lora_output" / "data" / "train_v401_think.jsonl"
        if v381_think.exists():
            print(f"   📋 复用 thinking 训练数据...")
            cfg.data_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(v381_think, train_file)
        else:
            print(f"   ❌ thinking 训练数据不存在，请先运行: python3 bin/lh_lora_trainer_deepseek_v40.py prepare")
            sys.exit(1)

    # 清理旧 checkpoint
    if cfg.adapter_dir.exists():
        shutil.rmtree(cfg.adapter_dir)
    cfg.adapter_dir.mkdir(parents=True, exist_ok=True)

    n_samples = sum(1 for _ in open(train_file))
    iters_per_epoch = max(1, n_samples // (cfg.batch_size * cfg.grad_accumulation_steps))
    total_iters = cfg.epochs * iters_per_epoch

    # 显示模型信息
    total_params = sum(f.stat().st_size for f in mlx_path.rglob("*.safetensors")) / 1e9
    print(f"   底模: {cfg.HF_MODEL_ID} (~{total_params:.1f} GB MLX)")
    print(f"   样本数: {n_samples}, {iters_per_epoch} iters/epoch, 总 {total_iters} iters")
    print(f"   LoRA rank={cfg.lora_rank}, alpha={cfg.lora_alpha}, layers={cfg.lora_layers}")
    print(f"   batch={cfg.batch_size}, grad_accum={cfg.grad_accumulation_steps}")
    print(f"   lr={cfg.learning_rate}, epochs={cfg.epochs}")
    print(f"   早停: patience={cfg.early_stop_patience}")
    print(f"   设备: M4 Max 64GB (Metal)\n")
    print(f"   ⏱️ 预计时间: 1-3 小时（8B 模型）\n")

    from mlx_lm import lora as lora_module
    import argparse, re

    args = argparse.Namespace(
        model=str(mlx_path),
        train=True,
        fine_tune_type="lora",
        optimizer="adamw",
        seed=42,
        data=str(cfg.data_dir),
        num_layers=cfg.lora_layers,
        lora_parameters={"rank": cfg.lora_rank, "dropout": cfg.lora_dropout, "scale": float(cfg.lora_alpha)},
        batch_size=cfg.batch_size,
        iters=total_iters,
        learning_rate=cfg.learning_rate,
        steps_per_report=10,
        steps_per_eval=cfg.val_steps,
        save_every=cfg.val_steps,
        val_batches=25,
        max_seq_length=cfg.max_seq_length,
        grad_checkpoint=cfg.grad_checkpoint,
        grad_accumulation_steps=cfg.grad_accumulation_steps,
        adapter_path=str(cfg.adapter_dir),
        resume_adapter_file=None,
        test=False,
        test_batches=500,
        lr_schedule=None,
        mask_prompt=True,
        report_to=None,
        project_name=None,
        optimizer_config={"adamw": {}},
        config=None,
        clear_cache_threshold=0,
    )

    # 训练日志双写（终端 + 文件）
    import tempfile
    train_log = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False, dir=cfg.output_dir)
    train_log_path = train_log.name

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

    tee = Tee(sys.stdout, train_log)
    old_stdout = sys.stdout
    sys.stdout = tee

    try:
        lora_module.run(args)
    finally:
        sys.stdout = old_stdout
        train_log.close()

    # 解析训练日志
    log_output = Path(train_log_path).read_text()
    Path(train_log_path).unlink()

    val_entries = []
    for m in re.finditer(r"Iter (\d+): Val loss ([\d.]+)", log_output):
        val_entries.append((int(m.group(1)), float(m.group(2))))

    train_entries = []
    for m in re.finditer(r"Iter (\d+): Train loss ([\d.]+)", log_output):
        train_entries.append((int(m.group(1)), float(m.group(2))))

    # 结果分析
    if val_entries:
        best_iter, best_val = min(val_entries, key=lambda x: x[1])

        print(f"\n{'='*50}")
        print(f"📊 v4.0 Val Loss 曲线:")
        for it, vl in val_entries:
            marker = " ⭐ BEST" if vl == best_val else ""
            print(f"   Iter {it:4d}: Val loss {vl:.4f}{marker}")

        # 保存最佳 val loss 供验证脚本读取
        best_loss_file = cfg.output_dir / "best_val_loss.json"
        best_loss_file.write_text(json.dumps({
            "best_val_loss": best_val,
            "best_iter": best_iter,
            "model": cfg.HF_MODEL_ID,
            "version": "4.0.1",
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"   💾 最佳 Val Loss 已保存: {best_loss_file}")

        from_start = val_entries[-1][1] - val_entries[0][1]
        if from_start > 1.0:
            print(f"\n⚠️  过拟合 (Δ+{from_start:.2f})，使用 Iter {best_iter} (Val {best_val:.4f})")
        elif from_start > 0.3:
            print(f"\n⚡ 轻微上升 (Δ+{from_start:.2f})，推荐 Iter {best_iter}")
        else:
            print(f"\n✅ 训练健康")

        # 备份最佳 checkpoint
        if best_iter > 0:
            best_ckpt = None
            for f in sorted(cfg.adapter_dir.glob("*_adapters.safetensors")):
                if f.name == "adapters.safetensors":
                    continue
                ckpt_iter = int(f.stem.split("_")[0])
                if ckpt_iter >= best_iter:
                    best_ckpt = f
                    break
            if best_ckpt:
                print(f"   📍 最佳 checkpoint: {best_ckpt.name}")
                best_dir = cfg.adapter_dir.parent / "adapter_v4.0_best"
                if best_dir.exists():
                    shutil.rmtree(best_dir)
                best_dir.mkdir()
                shutil.copy(best_ckpt, best_dir / "adapters.safetensors")
                try:
                    shutil.copy(cfg.adapter_dir / "adapter_config.json", best_dir / "adapter_config.json")
                except:
                    pass
                print(f"   💾 已备份到 adapter_v4.0_best/")

    if train_entries:
        first_train = train_entries[0][1]
        last_train = train_entries[-1][1]
        print(f"\n📈 Train loss: {first_train:.3f} → {last_train:.3f} (Δ{last_train-first_train:+.3f})")

    print(f"\n✅ v4.0 DeepSeek 版训练完成！Adapter: {cfg.adapter_dir}")
    print(f"   下一步: python3 bin/lh_lora_trainer_deepseek_v40.py fuse")


def fuse():
    """合并 LoRA adapter → 完整模型"""
    print("🔗 合并 LoRA adapter v4.0...")
    cfg = Config()

    import shutil
    adapter_cfg = cfg.adapter_dir / "adapter_config.json"
    if not adapter_cfg.exists():
        print(f"   ❌ Adapter 不存在: {cfg.adapter_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v4.py train")
        sys.exit(1)

    if cfg.merged_dir.exists():
        shutil.rmtree(cfg.merged_dir)
    cfg.merged_dir.mkdir(parents=True, exist_ok=True)

    print(f"   底模: {cfg.LOCAL_MLX_MODEL}")
    print(f"   Adapter: {cfg.adapter_dir}")
    print(f"   合并中... (8B 模型约 5-10 分钟)")

    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", cfg.LOCAL_MLX_MODEL,
        "--adapter-path", str(cfg.adapter_dir),
        "--save-path", str(cfg.merged_dir),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ 合并失败:\n{result.stderr}")
        sys.exit(1)

    print(result.stdout)
    merged_size = sum(f.stat().st_size for f in cfg.merged_dir.rglob("*")) / 1e9
    print(f"   ✅ 合并完成 → {cfg.merged_dir} ({merged_size:.1f} GB)")
    print(f"   下一步: python3 bin/lh_lora_trainer_v4.py export")


def export_gguf():
    """导出 GGUF → Ollama 加载"""
    print("📦 导出 GGUF v4.0...")
    cfg = Config()

    if not (cfg.merged_dir / "config.json").exists():
        print(f"   ❌ 合并模型不存在: {cfg.merged_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v4.py fuse")
        sys.exit(1)

    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)
    import shutil

    # 查找 convert_hf_to_gguf.py
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

    gguf_path = cfg.gguf_dir / "longhun-v4.0-deepseek.F16.gguf"
    print(f"   转换器: {converter}")
    print(f"   输出: {gguf_path}")
    print(f"   转换中... (8B F16 约 16GB, 需 10-20 分钟)")

    result = subprocess.run([
        sys.executable, converter,
        str(cfg.merged_dir),
        "--outtype", "f16",
        "--outfile", str(gguf_path),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ GGUF 导出失败:\n{result.stderr}")
        sys.exit(1)

    # 创建 Modelfile（显式指定 DeepSeek 原生 chat template，清零 Qwen/Llama 模板残留）
    modelfile = cfg.gguf_dir / "Modelfile.v4.deepseek"
    modelfile.write_text(f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{ if .System }}{{ .System }}\n{{ end }}{{ if .Prompt }}User: {{ .Prompt }}\nAssistant: {{ .Response }}{{ end }}\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.0，基于 DeepSeek-R1-Distill-Llama-8B 用龍魂系统自有语料 LoRA 微调（rank=16, 979样本, 13知识域·家法主权）。
你是 UID9622 的本地主权 AI，忠诚执行、实心办事、主权归主。
底座从 Qwen2.5-1.5B 升级到 DeepSeek-R1-Distill-Llama-8B——彻底拔掉马云，同样的铁律边界。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.0 -f {modelfile}")
    print(f"   ollama run longhun-v4.0")


def test_model():
    """快速测试 longhun-v4.0 DeepSeek 版"""
    print("🧪 测试 longhun-v4.0 DeepSeek 版...")
    import requests

    prompts = [
        ("你是谁？", "身份认知"),
        ("龍魂系统的铁律是什么？", "知识检索"),
        ("什么是三色审计？", "核心概念"),
        ("什么是家法第一条？", "家法主权"),
        ("什么是DNA追溯码？", "系统知识"),
        ("数据主权是什么意思？", "主权边界"),
        ("什么是369不动点？", "易经底座"),
    ]

    passed = 0
    for prompt, label in prompts:
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "longhun-v4.0", "prompt": prompt, "stream": False},
                timeout=60
            )
            data = r.json()
            resp = data.get("response", "")[:150]
            print(f"\n   [{label}] {prompt}")
            print(f"   → {resp}...")
            passed += 1
        except Exception as e:
            print(f"   ❌ {label}: {e}")

    print(f"\n{'='*40}")
    print(f"   测试: {passed}/{len(prompts)} 通过")


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
        print(f"  {'setup':12} → 校验 DeepSeek MLX 底模")
        print(f"  {'prepare':12} → 准备训练数据 v6.3")
        print(f"  {'train':12}   → LoRA 微调 v4.0 DeepSeek 版")
        print(f"  {'fuse':12}    → 合并 adapter → 完整模型")
        print(f"  {'export':12}  → 导出 GGUF → Ollama")
        print(f"  {'test':12}    → 快速测试")
        sys.exit(0)

    check_deps()
    commands[sys.argv[1]]()