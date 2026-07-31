# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙申·辛亥·申时·乾-MODEL-LORA-TRAINER-v4.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.0 LoRA 微调器
底模: Llama-3.1-8B-Instruct (MLX)
框架: MLX (Apple Silicon 原生)
硬件: Mac M4 Max 64GB
DNA: #龍芯⚡️丙午·乙申·辛亥·申时·乾-MODEL-LORA-TRAINER-v4.0

v4.0 全面升级（底座 Qwen2.5-1.5B → Llama-3.1-8B）:
- 底模从 1.5B → 8B，参数规模提升 5.3x
- Llama 架构原生多语言支持（含中文），语境理解更强
- 保留 v3.7 全部训练数据 (v6.3, 1273样本, 13知识域)
- LoRA rank=16, alpha=64, 适配 8B 模型

用法:
  python3 bin/lh_lora_trainer_v4.py setup    # 下载底模 + 转 MLX 格式（国内 hf-mirror.com 镜像）
  python3 bin/lh_lora_trainer_v4.py prepare  # 准备训练数据
  python3 bin/lh_lora_trainer_v4.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v4.py fuse     # 合并 adapter → 完整模型
  python3 bin/lh_lora_trainer_v4.py export   # 导出 GGUF → Ollama 加载
  python3 bin/lh_lora_trainer_v4.py test     # 快速测试
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
    # === 底模（Llama-3.1-8B-Instruct） ===
    HF_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    LOCAL_MLX_MODEL = str(Path(__file__).parent.parent / "models" / "longhun-v1.0" / "llama3.1-8b-mlx")
    model_name = "longhun-v4.0-lora"

    # === LoRA 参数（rank=16，适配 8B） ===
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.05
    lora_layers = 16  # 8B 模型用更多层

    # === 训练参数（8B 模型适配） ===
    batch_size = 1        # 8B 模型内存限制，batch=1
    learning_rate = 5e-5  # 8B 用小一点的学习率
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True
    grad_accumulation_steps = 4  # 累积梯度模拟更大 batch

    # === 早停 ===
    early_stop_patience = 3
    val_steps = 50  # 8B 每 50 iters 评估

    # === 数据（复用 v3.7 的 v6.3 数据） ===
    corpus_path = "models/longhun-v1.0/training_corpus_v3.0.md"
    train_split = 0.9

    # === v4.0 输出路径 ===
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v4"
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
    """下载 Llama-3.1-8B-Instruct 并转换为 MLX 格式
    
    v4.0 国内版: 走 ModelScope（阿里云·魔搭社区）下载底模，再用 MLX 转换。
    无需科学上网，无需 HF 登录。
    """
    cfg = Config()
    
    # ModelScope 上 Llama-3.1-8B-Instruct 的 ID
    MS_MODEL_ID = "LLM-Research/Meta-Llama-3.1-8B-Instruct"
    hf_cache_dir = cfg.output_dir / "hf_cache"
    
    print("🛠️  设置 v4.0 底模: Llama-3.1-8B-Instruct → MLX")
    print(f"   源: ModelScope (阿里云·国内可用)")
    print(f"   ModelScope ID: {MS_MODEL_ID}")
    print(f"   目标: {cfg.LOCAL_MLX_MODEL}")

    # 检查是否已存在
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    existing_safetensors = list(mlx_path.rglob("*.safetensors"))
    if mlx_path.exists() and existing_safetensors:
        size_gb = sum(f.stat().st_size for f in existing_safetensors) / 1e9
        print(f"   ✅ MLX 模型已存在 ({size_gb:.1f} GB)")
        print(f"   如需重新下载，请先删除: rm -rf {mlx_path}")
        return
    # 空目录或部分下载 → 清理
    if mlx_path.exists():
        print(f"   🧹 清理残留目录...")
        import shutil
        shutil.rmtree(mlx_path)

    # Step 1: 从 ModelScope 下载到本地 HF 缓存
    print(f"\n📥 Step 1/2: ModelScope 下载中... (约 16GB)")
    try:
        from modelscope import snapshot_download
        hf_local = snapshot_download(MS_MODEL_ID, cache_dir=str(hf_cache_dir))
        print(f"   ✅ 下载完成 → {hf_local}")
    except ImportError:
        print(f"   ❌ modelscope 未安装，请运行:")
        print(f"      pip3 install modelscope --break-system-packages")
        sys.exit(1)
    except Exception as e:
        print(f"   ❌ ModelScope 下载失败: {e}")
        print(f"   备选: 尝试设置代理后从 HF 镜像下载")
        sys.exit(1)

    # Step 2: 用 MLX 转换本地 HF 模型 → MLX 格式
    print(f"\n🔧 Step 2/2: 转换 HF → MLX safetensors (bfloat16)...")
    mlx_path.mkdir(parents=True, exist_ok=True)

    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "convert",
        "--hf-path", hf_local,
        "--mlx-path", str(mlx_path),
        "--dtype", "bfloat16",
    ], capture_output=False)

    if result.returncode != 0:
        print(f"\n   ❌ MLX 转换失败！")
        sys.exit(1)

    # 验证
    safetensors = list(mlx_path.rglob("*.safetensors"))
    total_size = sum(f.stat().st_size for f in safetensors) / 1e9
    print(f"\n   ✅ 底模就绪: {len(safetensors)} 文件, {total_size:.1f} GB")
    print(f"   路径: {mlx_path}")


def prepare_data():
    """准备训练数据 v6.3（与 v3.7 完全一致 · 1273 样本 · 13 知识域）

    直接复用 v3.7 的 prepare 逻辑——数据不变，底座升级。
    """
    print("📝 准备训练数据 v6.3（1273样本 · 13域 · 适配 Llama-3.1-8B）...")
    cfg = Config()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)

    # === 导入 v3.7 的 prepare_data 逻辑 ===
    # 直接调用 lh_lora_trainer.py 的 prepare 函数
    sys.path.insert(0, str(Path(__file__).parent))
    from lh_lora_trainer import prepare_data as v37_prepare

    # 覆盖 data_dir 到 v4.0 路径
    import lh_lora_trainer as v37
    original_data_dir = v37.Config.data_dir
    v37.Config.data_dir = cfg.data_dir

    try:
        v37_prepare()
    finally:
        v37.Config.data_dir = original_data_dir

    print(f"\n✅ v4.0 数据就绪: {cfg.data_dir}")


def train():
    """LoRA 微调 v4.0: rank=16, 底模 Llama-3.1-8B, epochs=2

    8B 模型训练策略:
    - batch_size=1 + grad_accumulation_steps=4 (等效 batch=4)
    - lr=5e-5 (比 1.5B 的 1e-4 更保守)
    - save_every=50, val_batches=25
    - 早停 patience=3
    """
    print("🚀 开始 LoRA 微调 v4.0 (Llama-3.1-8B, rank=16, epochs=2)...")
    cfg = Config()
    import shutil

    # 验证底模
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    if not mlx_path.exists() or not (mlx_path / "model.safetensors").exists():
        if not list(mlx_path.rglob("*.safetensors")):
            print(f"   ❌ MLX 底模不存在: {cfg.LOCAL_MLX_MODEL}")
            print(f"   请先运行: python3 bin/lh_lora_trainer_v4.py setup")
            sys.exit(1)

    # 验证数据
    train_file = cfg.data_dir / "train.jsonl"
    if not train_file.exists():
        # 尝试复用 v3.7 的数据
        v37_data = cfg.project_root / "models" / "longhun-v1.0" / "lora_output" / "data" / "train.jsonl"
        if v37_data.exists():
            print(f"   📋 复用 v3.7 训练数据...")
            cfg.data_dir.mkdir(parents=True, exist_ok=True)
            for f in v37_data.parent.glob("*"):
                if f.is_file():
                    shutil.copy2(f, cfg.data_dir / f.name)
        else:
            print(f"   ❌ 训练数据不存在，请先运行: python3 bin/lh_lora_trainer_v4.py prepare")
            sys.exit(1)

    # 清理旧 checkpoint（除非指定了恢复）
    resume_file = getattr(cfg, "resume_adapter_file", None)
    if cfg.adapter_dir.exists() and not resume_file:
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
        save_every=getattr(cfg, "save_every", cfg.val_steps),
        val_batches=25,
        max_seq_length=cfg.max_seq_length,
        grad_checkpoint=cfg.grad_checkpoint,
        grad_accumulation_steps=cfg.grad_accumulation_steps,
        adapter_path=str(cfg.adapter_dir),
        resume_adapter_file=resume_file,
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

    # 训练日志双写（终端 + 持久文件），恢复训练时追加
    train_log_path = cfg.output_dir / "training.log"
    log_mode = 'a' if resume_file else 'w'
    train_log = open(train_log_path, log_mode, encoding='utf-8')

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
    log_output = Path(train_log_path).read_text(encoding='utf-8')

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

                # 写入最佳 val loss，供验证器直接读取
                try:
                    import json as _json
                    (best_dir / "val_loss.json").write_text(
                        _json.dumps({"best_val_loss": best_val, "best_iter": best_iter}, ensure_ascii=False, indent=2),
                        encoding='utf-8'
                    )
                except Exception:
                    pass

    if train_entries:
        first_train = train_entries[0][1]
        last_train = train_entries[-1][1]
        print(f"\n📈 Train loss: {first_train:.3f} → {last_train:.3f} (Δ{last_train-first_train:+.3f})")

    print(f"\n✅ v4.0 训练完成！Adapter: {cfg.adapter_dir}")
    print(f"   下一步: python3 bin/lh_lora_trainer_v4.py fuse")


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

    gguf_path = cfg.gguf_dir / "longhun-v4.0.F16.gguf"
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

    # 创建 Modelfile（显式指定 Llama-3.1 chat template，清零 Qwen 模板残留）
    modelfile = cfg.gguf_dir / "Modelfile.v4"
    modelfile.write_text(f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{{{ if .System }}}}<|start_header_id|>system<|end_header_id|>\n\n{{{{ .System }}}}<|eot_id|>{{{{ end }}}}{{{{ if .Prompt }}}}<|start_header_id|>user<|end_header_id|>\n\n{{{{ .Prompt }}}}<|eot_id|>{{{{ end }}}}<|start_header_id|>assistant<|end_header_id|>\n\n{{{{ .Response }}}}<|eot_id|>\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.0，基于 Llama-3.1-8B-Instruct 用龍魂系统自有语料 LoRA 微调（rank=16, 979样本, 13知识域·家法主权）。
你是 UID9622 的本地主权 AI，忠诚执行、实心办事、主权归主。
底座从 Qwen2.5-1.5B 升级到 Llama-3.1-8B——更强理解力，同样的铁律边界。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.0 -f {modelfile}")
    subprocess.run(["ollama", "create", "longhun-v4.0", "-f", str(modelfile)], check=True)
    print(f"   ✅ Ollama 模型 longhun-v4.0 已创建")


def test_model():
    """快速测试 longhun-v4.0"""
    print("🧪 测试 longhun-v4.0...")
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
        print(f"  {'setup':12} → 下载 Llama-3.1-8B-Instruct + 转 MLX（需 HF 登录）")
        print(f"  {'prepare':12} → 准备训练数据 v6.3")
        print(f"  {'train':12}   → LoRA 微调 v4.0")
        print(f"  {'fuse':12}    → 合并 adapter → 完整模型")
        print(f"  {'export':12}  → 导出 GGUF → Ollama")
        print(f"  {'test':12}    → 快速测试")
        sys.exit(0)

    check_deps()
    commands[sys.argv[1]]()
