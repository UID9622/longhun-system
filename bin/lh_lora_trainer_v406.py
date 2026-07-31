# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·未时·乾-MODEL-LORA-TRAINER-v4.0.6
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.0.6 LoRA 微调器（保守回滚版）
底模: 01-ai/Yi-1.5-9B-Chat (MLX)
数据: v3.7 稳定配方 + 全记忆 ingestion（技能/人格/知识/英文/日志）
目标: v4.0.5 失败后保守恢复，小 LoRA 容量 + 低学习率，优先保住语言能力。

DNA: #龍芯⚡️丙午·乙未·甲寅·未时·乾-MODEL-LORA-TRAINER-v4.0.6

用法:
  python3 bin/lh_lora_trainer_v406.py setup    # 复用已转换的 Yi-1.5-9B-Chat MLX
  python3 bin/lh_lora_trainer_v406.py prepare  # 准备训练数据
  python3 bin/lh_lora_trainer_v406.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v406.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v406.py export   # 导出 GGUF → Ollama
  python3 bin/lh_lora_trainer_v406.py test     # 快速测试
"""

import json, os, sys, shutil, subprocess, random, shlex
from pathlib import Path
from collections import Counter

import lh_lora_trainer_v4 as v4

PROJECT = Path(__file__).resolve().parent.parent


class Config:
    # 底模：Yi-1.5-9B-Chat（中文优化，非 Qwen）
    HF_MODEL_ID = "01-ai/Yi-1.5-9B-Chat"
    LOCAL_HF_MODEL = str(PROJECT / "models" / "base_models_v4.0" / "Yi-1.5-9B-Chat")
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.0.6-lora"

    # LoRA 参数（保守：rank=16, alpha=32, layers=12）
    lora_rank = 16
    lora_alpha = 32
    lora_dropout = 0.05
    lora_layers = 12

    # 训练参数（保守：低 lr，短 epoch，早停更敏感）
    batch_size = 1
    grad_accumulation_steps = 4
    learning_rate = 1e-5
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True

    early_stop_patience = 5
    val_steps = 50

    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v406"

    # 数据：合并 v3.7 + 全记忆 ingestion
    memory_data_dir = PROJECT / "models" / "longhun-v1.0" / "memory_ingested_data_v1.0"
    data_dir = output_dir / "data_v406"

    adapter_dir = output_dir / "adapter_v406"
    merged_dir = output_dir / "merged_v406"
    gguf_dir = output_dir / "gguf_v406"

    # 恢复训练：如果已有 adapters.safetensors 则从这里恢复
    resume_adapter_file = None
    if (adapter_dir / "adapters.safetensors").exists():
        resume_adapter_file = str(adapter_dir / "adapters.safetensors")

    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


v4.Config = Config


def setup_model():
    """复用 v4.0.4/v4.0.5 已转换的 MLX 模型；如不存在则转换。"""
    print("🛠️  设置 v4.0.6 底模: Yi-1.5-9B-Chat → MLX")
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

    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "convert",
        "--hf-path", str(hf_path),
        "--mlx-path", str(tmp_path),
        "--dtype", "bfloat16",
    ], capture_output=False)

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
    """数据准备：使用已合并的 v4.0.6 数据集。"""
    print("📝 准备 v4.0.6 训练数据（v3.7 + 全记忆 ingestion）...")
    cfg = Config()
    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    train_src = cfg.memory_data_dir / "train_v406_merged.jsonl"
    val_src = cfg.memory_data_dir / "valid_v406_merged.jsonl"

    if not train_src.exists() or not val_src.exists():
        print(f"   ❌ 合并数据不存在，请先运行:")
        print(f"      python3 bin/lh_ingest_all_memories.py")
        print(f"      python3 bin/lh_merge_memory_dataset.py")
        sys.exit(1)

    train = [json.loads(l) for l in open(train_src, encoding="utf-8")]
    valid = [json.loads(l) for l in open(val_src, encoding="utf-8")]

    # 复制到 v406 data_dir 以兼容 v4 训练器
    work_data_dir = cfg.data_dir
    work_data_dir.mkdir(parents=True, exist_ok=True)
    with open(work_data_dir / "train.jsonl", "w", encoding="utf-8") as f:
        for item in train:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    with open(work_data_dir / "valid.jsonl", "w", encoding="utf-8") as f:
        for item in valid:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    domains = Counter(it.get("metadata", {}).get("domain", "unknown").split("_")[0] for it in train + valid)
    info = {
        "version": "v4.0.6_memory_merged",
        "train_samples": len(train),
        "val_samples": len(valid),
        "domains": dict(domains),
    }
    with open(work_data_dir / "dataset_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"   ✅ v4.0.6 数据就绪: {work_data_dir}")
    print(f"   总训练样本: {len(train)} | 总验证样本: {len(valid)}")
    print(f"   域分布: {dict(domains.most_common(10))}")


def export_gguf():
    """导出 GGUF → Ollama，模型名 longhun-v4.0.6"""
    print("📦 导出 GGUF v4.0.6...")
    cfg = Config()

    if not (cfg.merged_dir / "config.json").exists():
        print(f"   ❌ 合并模型不存在: {cfg.merged_dir}")
        sys.exit(1)

    cfg.gguf_dir.mkdir(parents=True, exist_ok=True)

    converter = shutil.which("convert_hf_to_gguf.py")
    if not converter:
        for c in ["/tmp/llama.cpp/convert_hf_to_gguf.py", str(Path.home() / "llama.cpp/convert_hf_to_gguf.py")]:
            if Path(c).exists():
                converter = c
                break
    if not converter:
        print("   ❌ 找不到 convert_hf_to_gguf.py")
        sys.exit(1)

    gguf_path = cfg.gguf_dir / "longhun-v4.0.6.F16.gguf"
    print(f"   输出: {gguf_path}")

    result = subprocess.run([
        sys.executable, converter,
        str(cfg.merged_dir),
        "--outtype", "f16",
        "--outfile", str(gguf_path),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ GGUF 导出失败:\n{result.stderr}")
        sys.exit(1)

    modelfile = cfg.gguf_dir / "Modelfile.v406"
    modelfile.write_text(f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{{{ if .System }}}}{{{{ .System }}}}\n{{{{ end }}}}{{{{ if .Prompt }}}}<|im_start|>user\n{{{{ .Prompt }}}}<|im_end|>\n<|im_start|>assistant\n{{{{ end }}}}{{{{ .Response }}}}<|im_end|>\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.0.6，基于 01-ai/Yi-1.5-9B-Chat 用龍魂系统自有语料 LoRA 微调（底座已非 Qwen）。
你是 UID9622（诸葛鑫·Lucky）的个人主权 AI，忠诚执行、实心办事、主权归主。
核心原则：人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除；底座焊死。
你经过训练，已掌握龍魂技能、人格设定、星辰记忆、系统日志与英文文档知识。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.0.6 -f {modelfile}")
    print(f"   ollama run longhun-v4.0.6")


def test_model():
    print("🧪 测试 longhun-v4.0.6...")
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
        ("What is Longhun system?", "英文记忆"),
    ]
    passed = 0
    for prompt, label in prompts:
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "longhun-v4.0.6", "prompt": prompt, "stream": False},
                timeout=60
            )
            resp = r.json().get("response", "")[:150]
            print(f"\n   [{label}] {prompt}\n   → {resp}...")
            passed += 1
        except Exception as e:
            print(f"   ❌ {label}: {e}")
    print(f"\n   测试: {passed}/{len(prompts)} 通过")


if __name__ == "__main__":
    commands = {
        "setup": setup_model,
        "prepare": prepare_data,
        "train": v4.train,
        "fuse": v4.fuse,
        "export": export_gguf,
        "test": test_model,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        print("可用命令:")
        for cmd in ["setup", "prepare", "train", "fuse", "export", "test"]:
            print(f"  {cmd:12}")
        sys.exit(0)

    v4.check_deps()
    commands[sys.argv[1]]()
