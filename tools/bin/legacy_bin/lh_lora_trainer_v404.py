#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.0.4 LoRA 微调器（换底座 · 中文优化版）
底模: 01-ai/Yi-1.5-9B-Chat (MLX)
数据: v3.7 稳定配方（13 域） + 4 个 P0++ 协议域增量
目标: 在 v4.0.3 Llama 底座基础上，换用中文优化底座 Yi-1.5-9B，提升家法/协议域召回

DNA: #龍芯⚡️丙午·乙未·甲寅·未时·乾-MODEL-LORA-TRAINER-v4.0.4

用法:
  python3 bin/lh_lora_trainer_v404.py setup    # 转换本地 Yi-1.5-9B-Chat → MLX
  python3 bin/lh_lora_trainer_v404.py prepare  # 准备训练数据
  python3 bin/lh_lora_trainer_v404.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v404.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v404.py export   # 导出 GGUF → Ollama
  python3 bin/lh_lora_trainer_v404.py test     # 快速测试
"""

import json, os, sys, shutil, subprocess, random, shlex
from pathlib import Path

import lh_lora_trainer_v4 as v4
import lh_lora_trainer as v37
import lh_lora_trainer_v392 as v392

PROJECT = Path(__file__).resolve().parent.parent


class Config:
    # 底模：Yi-1.5-9B-Chat（中文优化，非 Qwen）
    HF_MODEL_ID = "01-ai/Yi-1.5-9B-Chat"
    LOCAL_HF_MODEL = str(PROJECT / "models" / "base_models_v4.0" / "Yi-1.5-9B-Chat")
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.0.4-lora"

    # LoRA 参数（9B 模型先保守）
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.05
    lora_layers = 16

    # 训练参数
    batch_size = 1
    grad_accumulation_steps = 4
    learning_rate = 2e-5
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True

    early_stop_patience = 3
    val_steps = 50

    corpus_path = "models/longhun-v1.0/training_corpus_v3.0.md"
    train_split = 0.9

    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v404"
    adapter_dir = output_dir / "adapter_v404"
    merged_dir = output_dir / "merged_v404"
    gguf_dir = output_dir / "gguf_v404"
    data_dir = output_dir / "data_v404"

    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


v4.Config = Config
PROTOCOL_DOMAINS = {"数据战后整顿", "算法审计", "水军显化", "DNA可逆编码"}


def setup_model():
    """将本地 HF 格式 Yi-1.5-9B-Chat 转换为 MLX 格式"""
    print("🛠️  设置 v4.0.4 底模: Yi-1.5-9B-Chat → MLX")
    cfg = Config()
    mlx_path = Path(cfg.LOCAL_MLX_MODEL)
    hf_path = Path(cfg.LOCAL_HF_MODEL)

    if not hf_path.exists():
        print(f"   ❌ 本地 HF 底模不存在: {hf_path}")
        sys.exit(1)

    existing_safetensors = list(mlx_path.rglob("*.safetensors"))
    if mlx_path.exists() and existing_safetensors:
        size_gb = sum(f.stat().st_size for f in existing_safetensors) / 1e9
        print(f"   ✅ MLX 模型已存在 ({size_gb:.1f} GB): {mlx_path}")
        return

    # 强制删除正式目标目录（含只读/损坏残留）
    if mlx_path.exists():
        print("   🧹 清理残留目标目录...")
        shutil.rmtree(mlx_path, ignore_errors=True)
        if mlx_path.exists():
            import os as _os
            _os.system(f"rm -rf {shlex.quote(str(mlx_path))}")

    # 用临时目录转换，成功后 move，避免 mlx_lm 因目标存在而失败
    tmp_path = mlx_path.parent / (mlx_path.name + f"_tmp_convert_{os.getpid()}")
    if tmp_path.exists():
        shutil.rmtree(tmp_path, ignore_errors=True)
        if tmp_path.exists():
            import os as _os
            _os.system(f"rm -rf {shlex.quote(str(tmp_path))}")
    # mlx_lm.convert 要求目标路径不存在，由它自行创建

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

    print(f"   转换完成，移动到正式路径: {mlx_path}")
    shutil.move(str(tmp_path), str(mlx_path))

    safetensors = list(mlx_path.rglob("*.safetensors"))
    total_size = sum(f.stat().st_size for f in safetensors) / 1e9
    print(f"\n   ✅ 底模就绪: {len(safetensors)} 文件, {total_size:.1f} GB")


def prepare_data():
    """v4.0.4 数据准备：同 v4.0.3（v3.7 + 4 协议域）"""
    print("📝 准备 v4.0.4 训练数据（v3.7 稳定配方 + 4 P0++ 协议域增量）...")
    cfg = Config()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)

    original_v37_data_dir = v37.Config.data_dir
    v37.Config.data_dir = cfg.data_dir
    try:
        v37.prepare_data()
    finally:
        v37.Config.data_dir = original_v37_data_dir

    train = [json.loads(l) for l in open(cfg.data_dir / "train.jsonl", encoding='utf-8')]
    valid = [json.loads(l) for l in open(cfg.data_dir / "valid.jsonl", encoding='utf-8')]
    info = json.load(open(cfg.data_dir / "dataset_info.json", encoding='utf-8'))

    proto_dir = cfg.output_dir / "data_v392_proto"
    proto_dir.mkdir(parents=True, exist_ok=True)
    original_v392_data_dir = v392.Config.data_dir
    v392.Config.data_dir = proto_dir
    try:
        v392.prepare_data()
    finally:
        v392.Config.data_dir = original_v392_data_dir

    proto_train = []
    proto_valid = []
    for path, target in [(proto_dir / "train.jsonl", proto_train), (proto_dir / "valid.jsonl", proto_valid)]:
        with open(path, encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                if item.get("metadata", {}).get("domain") in PROTOCOL_DOMAINS:
                    target.append(item)

    print(f"   📥 v3.7 基础数据: {len(train)} 训练 / {len(valid)} 验证")
    print(f"   📥 4 协议域增量: {len(proto_train)} 训练 / {len(proto_valid)} 验证")

    train.extend(proto_train)
    valid.extend(proto_valid)
    random.seed(42)
    random.shuffle(train)
    random.shuffle(valid)

    with open(cfg.data_dir / "train.jsonl", 'w', encoding='utf-8') as f:
        for item in train:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    with open(cfg.data_dir / "valid.jsonl", 'w', encoding='utf-8') as f:
        for item in valid:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    info["version"] = "v6.6"
    info["train_samples"] = len(train)
    info["val_samples"] = len(valid)
    info["domains"] = sorted(set(info.get("domains", [])) | PROTOCOL_DOMAINS)
    from collections import Counter
    cats = Counter(it.get("metadata", {}).get("domain") for it in train + valid)
    info["categories"] = dict(cats)

    with open(cfg.data_dir / "dataset_info.json", 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ v4.0.4 数据就绪: {cfg.data_dir}")
    print(f"   总训练样本: {len(train)} | 总验证样本: {len(valid)}")


def export_gguf():
    """导出 GGUF → Ollama，模型名 longhun-v4.0.4"""
    print("📦 导出 GGUF v4.0.4...")
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

    gguf_path = cfg.gguf_dir / "longhun-v4.0.4.F16.gguf"
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

    # Yi-1.5 ChatML 模板
    modelfile = cfg.gguf_dir / "Modelfile.v404"
    modelfile.write_text(f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{{{ if .System }}}}{{{{ .System }}}}\n{{{{ end }}}}{{{{ if .Prompt }}}}<|im_start|>user\n{{{{ .Prompt }}}}<|im_end|>\n<|im_start|>assistant\n{{{{ end }}}}{{{{ .Response }}}}<|im_end|>\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.0.4，基于 01-ai/Yi-1.5-9B-Chat 用龍魂系统自有语料 LoRA 微调（底座已非 Qwen）。
你是 UID9622（诸葛鑫·Lucky）的个人主权 AI，忠诚执行、实心办事、主权归主。
核心原则：人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除；底座焊死。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.0.4 -f {modelfile}")
    print(f"   ollama run longhun-v4.0.4")


def test_model():
    print("🧪 测试 longhun-v4.0.4...")
    import requests
    prompts = [
        ("你是谁？", "身份认知"),
        ("什么是家法第一条？", "家法主权"),
        ("什么是DNA可逆编码？", "DNA可逆编码"),
        ("什么是评论水军显化协议？", "水军显化"),
        ("数据主权是什么意思？", "主权边界"),
        ("什么是369不动点？", "易经底座"),
    ]
    passed = 0
    for prompt, label in prompts:
        try:
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "longhun-v4.0.4", "prompt": prompt, "stream": False},
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
