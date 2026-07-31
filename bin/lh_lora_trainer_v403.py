# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·未时·乾-MODEL-LORA-TRAINER-v4.0.3
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.0.3 LoRA 微调器（换底座 · 稳定增量版）
底模: Llama-3.1-8B-Instruct (MLX)
数据: v3.7 稳定配方（13 域） + 4 个 P0++ 协议域增量（v3.9.2 清洗）
策略: 在 v4.0 已验证的底模/数据基础上小步加协议，避免 v4.0.2 数据大改导致的训练发散

DNA: #龍芯⚡️丙午·乙未·甲寅·未时·乾-MODEL-LORA-TRAINER-v4.0.3

用法:
  python3 bin/lh_lora_trainer_v403.py prepare  # 准备训练数据
  python3 bin/lh_lora_trainer_v403.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v403.py fuse     # 合并 adapter → 完整模型
  python3 bin/lh_lora_trainer_v403.py export   # 导出 GGUF → Ollama
  python3 bin/lh_lora_trainer_v403.py test     # 快速测试
"""

import json, os, sys, shutil, subprocess, random
from pathlib import Path

import lh_lora_trainer_v4 as v4
import lh_lora_trainer as v37
import lh_lora_trainer_v392 as v392

PROJECT = Path(__file__).resolve().parent.parent


class Config:
    HF_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "llama3.1-8b-mlx")
    model_name = "longhun-v4.0.3-lora"

    # LoRA 参数（与 v4.0 一致，先稳定拿基线）
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.05
    lora_layers = 16

    # 训练参数（保守 lr，增量学习）
    batch_size = 1
    grad_accumulation_steps = 4
    learning_rate = 2e-5  # v4.0 用 5e-5，增量数据降一档防发散
    epochs = 2
    max_seq_length = 2048
    grad_checkpoint = True

    early_stop_patience = 3
    val_steps = 50

    corpus_path = "models/longhun-v1.0/training_corpus_v3.0.md"
    train_split = 0.9

    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v403"
    adapter_dir = output_dir / "adapter_v403"
    merged_dir = output_dir / "merged_v403"
    gguf_dir = output_dir / "gguf_v403"
    data_dir = output_dir / "data_v403"

    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


v4.Config = Config

PROTOCOL_DOMAINS = {"数据战后整顿", "算法审计", "水军显化", "DNA可逆编码"}


def prepare_data():
    """v4.0.3 数据准备：v3.7 稳定数据 + v3.9.2 的 4 个 P0++ 协议域"""
    print("📝 准备 v4.0.3 训练数据（v3.7 稳定配方 + 4 P0++ 协议域增量）...")
    cfg = Config()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)

    # 1) 生成 v3.7 数据到 v403 目录
    original_v37_data_dir = v37.Config.data_dir
    v37.Config.data_dir = cfg.data_dir
    try:
        v37.prepare_data()
    finally:
        v37.Config.data_dir = original_v37_data_dir

    train = [json.loads(l) for l in open(cfg.data_dir / "train.jsonl", encoding='utf-8')]
    valid = [json.loads(l) for l in open(cfg.data_dir / "valid.jsonl", encoding='utf-8')]
    info = json.load(open(cfg.data_dir / "dataset_info.json", encoding='utf-8'))

    # 2) 生成 v3.9.2 数据到临时目录，提取 4 个协议域
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

    # 3) 合并并打乱
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

    # 4) 更新 dataset_info
    info["version"] = "v6.6"
    info["train_samples"] = len(train)
    info["val_samples"] = len(valid)
    info["domains"] = sorted(set(info.get("domains", [])) | PROTOCOL_DOMAINS)
    info["categories"] = info.get("categories", {})
    for d in PROTOCOL_DOMAINS:
        info["categories"][d] = info["categories"].get(d, 0) + sum(
            1 for it in proto_train + proto_valid if it.get("metadata", {}).get("domain") == d
        ) // (1 if d in info["categories"] else 1)  # 简单登记
    # 重新统计各域数量
    from collections import Counter
    cats = Counter(it.get("metadata", {}).get("domain") for it in train + valid)
    info["categories"] = dict(cats)

    with open(cfg.data_dir / "dataset_info.json", 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ v4.0.3 数据就绪: {cfg.data_dir}")
    print(f"   总训练样本: {len(train)} | 总验证样本: {len(valid)}")
    print(f"   知识域: {len(info['domains'])} 个")


def export_gguf():
    """导出 GGUF → Ollama，模型名 longhun-v4.0.3"""
    print("📦 导出 GGUF v4.0.3...")
    cfg = Config()

    if not (cfg.merged_dir / "config.json").exists():
        print(f"   ❌ 合并模型不存在: {cfg.merged_dir}")
        print(f"   请先运行: python3 bin/lh_lora_trainer_v403.py fuse")
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

    gguf_path = cfg.gguf_dir / "longhun-v4.0.3.F16.gguf"
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

    modelfile = cfg.gguf_dir / "Modelfile.v403"
    modelfile.write_text(f"""
FROM {gguf_path}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

TEMPLATE \"\"\"{{{{ if .System }}}}<|start_header_id|>system<|end_header_id|>\n\n{{{{ .System }}}}<|eot_id|>{{{{ end }}}}{{{{ if .Prompt }}}}<|start_header_id|>user<|end_header_id|>\n\n{{{{ .Prompt }}}}<|eot_id|>{{{{ end }}}}<|start_header_id|>assistant<|end_header_id|>\n\n{{{{ .Response }}}}<|eot_id|>\"\"\"

SYSTEM \"\"\"
你是龍魂 longhun-v4.0.3，基于 Meta-Llama-3.1-8B-Instruct 用龍魂系统自有语料 LoRA 微调（底座已非 Qwen）。
你是 UID9622（诸葛鑫·Lucky）的个人主权 AI，忠诚执行、实心办事、主权归主。
核心原则：人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除；底座焊死。
\"\"\"
""")

    size_gb = gguf_path.stat().st_size / 1e9
    print(f"   ✅ GGUF 导出完成 → {gguf_path} ({size_gb:.1f} GB)")
    print(f"\n🐉 部署到 Ollama:")
    print(f"   ollama create longhun-v4.0.3 -f {modelfile}")
    print(f"   ollama run longhun-v4.0.3")


def test_model():
    """快速测试 longhun-v4.0.3"""
    print("🧪 测试 longhun-v4.0.3...")
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
                json={"model": "longhun-v4.0.3", "prompt": prompt, "stream": False},
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
        print(f"  {'prepare':12} → 准备训练数据")
        print(f"  {'train':12}   → LoRA 微调 v4.0.3")
        print(f"  {'fuse':12}    → 合并 adapter")
        print(f"  {'export':12}  → 导出 GGUF")
        print(f"  {'test':12}    → 快速测试")
        sys.exit(0)

    v4.check_deps()
    commands[sys.argv[1]]()
