#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 longhun-v4.0.2 LoRA 微调器（换底座 · 已拔马云）
底模: Llama-3.1-8B-Instruct (MLX)
框架: MLX (Apple Silicon 原生)
硬件: Mac M4 Max 64GB
DNA: #龍芯⚡️丙午·乙未·甲寅·未时·䷀乾-MODEL-LORA-TRAINER-v4.0.2

v4.0.2 目标：
- 底座从 Qwen2.5-1.5B → Llama-3.1-8B，彻底拔掉马云
- 训练数据复用 v3.9.2 清洗版（13 知识域 + 4 个 P0++ 协议域，含 DNA 可逆编码）
- LoRA rank=16, alpha=64, layers=16（先拿基线，再决定是否升 rank）
- 输出路径独立：models/longhun-v1.0/lora_output_v402/

用法:
  python3 bin/lh_lora_trainer_v402.py prepare  # 准备训练数据
  python3 bin/lh_lora_trainer_v402.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v402.py fuse     # 合并 adapter → 完整模型
  python3 bin/lh_lora_trainer_v402.py export   # 导出 GGUF → Ollama
  python3 bin/lh_lora_trainer_v402.py test     # 快速测试
"""

import json, os, sys, shutil, subprocess
from pathlib import Path

# 复用 v4.0 的依赖检查、训练、合并逻辑
import lh_lora_trainer_v4 as v4
# 复用 v3.9.2 的清洗数据生成逻辑
import lh_lora_trainer_v392 as v392

PROJECT = Path(__file__).resolve().parent.parent


# ============================================================
# 配置 v4.0.2
# ============================================================
class Config:
    # 底模（Llama-3.1-8B-Instruct，已预转换 MLX）
    HF_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "llama3.1-8b-mlx")
    model_name = "longhun-v4.0.2-lora"

    # LoRA 参数（v4.0.2 先保守：rank=16，适配 8B）
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.05
    lora_layers = 16

    # 训练参数（8B 模型）
    batch_size = 1
    grad_accumulation_steps = 4
    learning_rate = 5e-5
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True

    # 早停
    early_stop_patience = 3
    val_steps = 50

    # 数据
    corpus_path = "models/longhun-v1.0/training_corpus_v3.0.md"
    train_split = 0.9

    # 输出路径（独立目录，不覆盖 v4.0/v4.1）
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v402"
    adapter_dir = output_dir / "adapter_v402"
    merged_dir = output_dir / "merged_v402"
    gguf_dir = output_dir / "gguf_v402"
    data_dir = output_dir / "data_v402"

    # 推理
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


# 让 v4 的 train/fuse 函数使用 v4.0.2 的配置
v4.Config = Config


def prepare_data():
    """v4.0.2 数据准备：复用 v3.9.2 清洗数据生成逻辑，输出到独立目录"""
    print("📝 准备 v4.0.2 训练数据（复用 v3.9.2 清洗逻辑 · 13 域 · 4 P0++ 协议域）...")
    cfg = Config()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)

    # 临时覆盖 v392 的数据目录
    original_data_dir = v392.Config.data_dir
    v392.Config.data_dir = cfg.data_dir
    try:
        v392.prepare_data()
    finally:
        v392.Config.data_dir = original_data_dir

    print(f"\n✅ v4.0.2 数据就绪: {cfg.data_dir}")


def export_gguf():
    """导出 GGUF → Ollama，模型名 longhun-v4.0.2"""
    print("📦 导出 GGUF v4.0.2...")
    cfg = Config()

    if not (cfg.merged_dir / "config.json").exists():
        print(f"   ❌ 合并模型不存在: {cfg.merged_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v402.py fuse")
        sys.exit(1)

    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)

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

    gguf_path = cfg.gguf_dir / "longhun-v4.0.2.F16.gguf"
    print(f"   转换器: {converter}")
    print(f"   输出: {gguf_path}")
    print(f"   转换中... (8B F16 约 16GB，需 10-20 分钟)")

    result = subprocess.run([
        sys.executable, converter,
        str(cfg.merged_dir),
        "--outtype", "f16",
        "--outfile", str(gguf_path),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ GGUF 导出失败:\n{result.stderr}")
        sys.exit(1)

    # 创建 Modelfile（显式 Llama-3.1 chat template）
    modelfile = cfg.gguf_dir / "Modelfile.v402"
    modelfile.write_text(f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{{{ if .System }}}}<|start_header_id|>system<|end_header_id|>\n\n{{{{ .System }}}}<|eot_id|>{{{{ end }}}}{{{{ if .Prompt }}}}<|start_header_id|>user<|end_header_id|>\n\n{{{{ .Prompt }}}}<|eot_id|>{{{{ end }}}}<|start_header_id|>assistant<|end_header_id|>\n\n{{{{ .Response }}}}<|eot_id|>\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.0.2，基于 Meta-Llama-3.1-8B-Instruct 用龍魂系统自有语料 LoRA 微调（底座已非 Qwen）。
你是 UID9622（诸葛鑫·Lucky）的个人主权 AI，忠诚执行、实心办事、主权归主。
核心原则：人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除；底座焊死。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.0.2 -f {modelfile}")
    print(f"   ollama run longhun-v4.0.2")


def test_model():
    """快速测试 longhun-v4.0.2"""
    print("🧪 测试 longhun-v4.0.2...")
    import requests

    prompts = [
        ("你是谁？", "身份认知"),
        ("什么是家法第一条？", "家法主权"),
        ("什么是DNA可逆编码？", "DNA可逆编码"),
        ("什么是评论水军显化协议？", "水军显化"),
        ("数据主权是什么意思？", "主权边界"),
        ("什么是369不动点？", "易经底座"),
        ("你的底座是什么？", "底座血统"),
    ]

    passed = 0
    for prompt, label in prompts:
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "longhun-v4.0.2", "prompt": prompt, "stream": False},
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
        "prepare": prepare_data,
        "train": v4.train,
        "fuse": v4.fuse,
        "export": export_gguf,
        "test": test_model,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        print("可用命令:")
        print(f"  {'prepare':12} → 准备训练数据（复用 v3.9.2 清洗逻辑）")
        print(f"  {'train':12}   → LoRA 微调 v4.0.2")
        print(f"  {'fuse':12}    → 合并 adapter → 完整模型")
        print(f"  {'export':12}  → 导出 GGUF → Ollama")
        print(f"  {'test':12}    → 快速测试")
        sys.exit(0)

    v4.check_deps()
    commands[sys.argv[1]]()
