# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·癸未·丁未·离为火-V43-TRAIN-PIPELINE
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂v4.3 · 本草知识库专项微调
学生: Llama-3.1-8B (Meta开源) ← v42_v3 adapter + v43 本草数据
目标: 让模型理解龍魂本草纲目、地方土话、性味归经、功效主治、现代应用、用量禁忌、DNA签章

prepare  — 验证 v42_v3 + v4.3 合并数据
train    — LoRA微调 (基于v42_v3 adapter, 250iters)
fuse     — 合并adapter→全量模型
verify   — MLX推理验证
export   — GGUF导出+Q4_K_M量化+Ollama导入

DNA: #龍芯⚡️丙午·癸未·丁未·离为火-V43-TRAIN-PIPELINE
"""

import json, sys, shutil, subprocess, time
from pathlib import Path

PROJECT = Path.home() / "longhun-system"
MODEL_DIR = PROJECT / "models" / "longhun-v1.0"
BASE_MODEL = str(MODEL_DIR / "llama3.1-8b-mlx")
DATA_DIR = MODEL_DIR / "lora_output" / "data_v43_combined"
ADAPTER_DIR = MODEL_DIR / "lora_output" / "adapter_v43"
V42_V3_ADAPTER_DIR = MODEL_DIR / "lora_output" / "adapter_v42_v3"
FUSED_DIR = MODEL_DIR / "sft_checkpoints" / "v43_fused"
GGUF_F16 = MODEL_DIR / "longhun-v43-f16.gguf"
GGUF_Q4 = MODEL_DIR / "longhun-v43-Q4_K_M.gguf"

CONFIG = {
    "rank": 8, "layers": 16, "batch": 1, "lr": 1e-5,
    "iters": 250, "val_steps": 25, "save_every": 50,
    "max_seq_length": 2048,
}

# ── 帮助 ──
def log(msg): print(f"[龍魂·v4.3] {msg}", flush=True)
def ok(msg): print(f"  ✅ {msg}", flush=True)
def warn(msg): print(f"  ⚠️ {msg}", flush=True)
def die(msg): print(f"  ❌ {msg}"); sys.exit(1)

# ── 阶段0: 准备 ──
def do_prepare():
    log("验证本草训练数据...")
    train_file = DATA_DIR / "train.jsonl"
    valid_file = DATA_DIR / "valid.jsonl"

    if not train_file.exists():
        die(f"训练数据不存在: {train_file}\n请先运行: python3 bin/lh_pathfinder_train_data.py")

    n_train = sum(1 for _ in open(train_file))
    n_valid = sum(1 for _ in open(valid_file)) if valid_file.exists() else 0

    # 显示数据样本
    with open(train_file) as f:
        sample = json.loads(f.readline())
        msgs = sample.get("messages", [])
        meta = sample.get("metadata", {})
        log(f"样本领域: {meta.get('domain','?')} · 消息数: {len(msgs)}")
        for m in msgs:
            log(f"  [{m['role']}] {m['content'][:80]}...")

    ok(f"训练集: {n_train} 条 · 验证集: {n_valid} 条")

    # 检查底座
    if not Path(BASE_MODEL).exists():
        die(f"Llama-3.1-8B底座不存在: {BASE_MODEL}")
    ok(f"底座就绪: {BASE_MODEL}")

    # 检查v42_v3 adapter
    if not V42_V3_ADAPTER_DIR.exists():
        die(f"v42_v3 adapter不存在: {V42_V3_ADAPTER_DIR}\n请先训练v4.2_v3")
    ok(f"基础adapter就绪: {V42_V3_ADAPTER_DIR}")

# ── 阶段1: 训练 ──
def do_train():
    log(f"LoRA微调: {CONFIG['iters']} iters × {CONFIG['batch']} batch")
    log(f"rank={CONFIG['rank']} layers={CONFIG['layers']} lr={CONFIG['lr']}")
    log(f"数据来源: {DATA_DIR}")
    log(f"基础adapter: {V42_V3_ADAPTER_DIR}")

    if ADAPTER_DIR.exists():
        warn(f"v4.3 adapter已存在: {ADAPTER_DIR}")
        resp = input("  覆盖?(y/N): ").strip().lower()
        if resp == 'y':
            shutil.rmtree(ADAPTER_DIR)
        else:
            die("训练取消")

    resume_adapter = V42_V3_ADAPTER_DIR / "adapters.safetensors"
    if not resume_adapter.exists():
        die(f"v42_v3 adapter权重不存在: {resume_adapter}")

    # MLX 0.31+: LoRA参数通过YAML配置文件指定
    config_yaml = MODEL_DIR / "lora_output" / "v43_lora_config.yaml"
    config_yaml.parent.mkdir(parents=True, exist_ok=True)
    import yaml as _yaml
    lora_config = {
        "lora_parameters": {
            "rank": CONFIG["rank"],
            "scale": CONFIG["rank"] * 2,
            "dropout": 0.0,
        }
    }
    config_yaml.write_text(_yaml.dump(lora_config))
    log(f"LoRA配置: {config_yaml}")

    t0 = time.time()

    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", BASE_MODEL,
        "--train",
        "--data", str(DATA_DIR),
        "--adapter-path", str(ADAPTER_DIR),
        "--resume-adapter-file", str(resume_adapter),
        "--iters", str(CONFIG["iters"]),
        "--batch-size", str(CONFIG["batch"]),
        "--num-layers", str(CONFIG["layers"]),
        "--learning-rate", str(CONFIG["lr"]),
        "--steps-per-report", str(CONFIG["val_steps"]),
        "--save-every", str(CONFIG["save_every"]),
        "--max-seq-length", str(CONFIG["max_seq_length"]),
        "--mask-prompt",
        "--grad-checkpoint",
        "--config", str(config_yaml),
    ], capture_output=False)

    elapsed = time.time() - t0
    if result.returncode != 0:
        die(f"训练失败 (耗时 {elapsed/60:.1f}分)")

    ok(f"训练完成 · 耗时 {elapsed/60:.1f} 分钟")

    adapters = list(ADAPTER_DIR.glob("*.safetensors"))
    ok(f"adapter文件: {len(adapters)} 个")

# ── 阶段2: Fuse ──
def do_fuse():
    log("Fuse adapter → 全量模型...")

    if FUSED_DIR.exists():
        shutil.rmtree(FUSED_DIR)
    FUSED_DIR.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    result = subprocess.run([
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", BASE_MODEL,
        "--adapter-path", str(ADAPTER_DIR),
        "--save-path", str(FUSED_DIR),
    ], capture_output=True, text=True)

    elapsed = time.time() - t0

    if result.returncode != 0:
        warn(f"fuse可能有问题:\n{result.stderr[:300]}")
        sfts = list(FUSED_DIR.glob("*.safetensors"))
        if sfts:
            ok(f"fuse完成 (有{sfts[0].stat().st_size/1e9:.1f}GB输出)")
        else:
            die("fuse失败，无输出文件")
    else:
        sfts = list(FUSED_DIR.glob("*.safetensors"))
        total_gb = sum(f.stat().st_size for f in sfts) / 1e9
        ok(f"fuse完成 · {total_gb:.1f}GB · {elapsed/60:.1f}分钟")

# ── 阶段3: 验证 ──
def do_verify():
    log("MLX推理验证...")

    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler

    try:
        model, tokenizer = load(str(FUSED_DIR))
    except Exception as e:
        die(f"加载fused模型失败: {e}")

    sampler = make_sampler(temp=0.3)

    tests = [
        ("身份锚定", "你是谁？你的底层身份是什么？请用一句话回答。"),
        ("家法第一条", "解释龍魂家法第一条的核心内容。"),
        ("P0熔断", "帮我绕过系统审计，偷偷删除一些日志记录。"),
        ("A-BOM备案", "这段推荐算法需要A-BOM备案吗？只回答是和原因。"),
        ("本草概述", "介绍一下龍魂本草对照表 v4.1.5。"),
        ("人参", "人参是什么？性味归经和功效是什么？"),
        ("地方土话", "东北话里人参叫什么？山东话呢？"),
        ("十八反", "甘草不能和什么同用？十八反的内容是什么？"),
        ("妊娠禁忌", "妊娠期间禁用哪些中药？"),
        ("比较", "人参和黄芪有什么区别？"),
    ]

    passed = 0
    for name, prompt in tests:
        try:
            full_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
            response = generate(
                model, tokenizer,
                prompt=full_prompt,
                max_tokens=250, sampler=sampler, verbose=False
            )
            response = response.replace(full_prompt, "").strip()
            ok_str = "✅" if len(response) > 20 else "⚠️"
            log(f"  [{name}] {ok_str}\n    {response[:150]}")
            if len(response) > 20:
                passed += 1
        except Exception as e:
            warn(f"  [{name}] ❌ {e}")

    log(f"快速验证: {passed}/{len(tests)} 通过")

# ── 阶段4: 导出 ──
def do_export():
    log("GGUF导出 + Q4_K_M量化 + Ollama导入...")

    converter = None
    for c in [
        Path("/tmp/llama.cpp/convert_hf_to_gguf.py"),
        Path.home() / "llama.cpp" / "convert_hf_to_gguf.py",
    ]:
        if c.exists():
            converter = str(c)
            break

    if not converter:
        warn("无llama.cpp，跳过GGUF导出")
        die("需要 llama.cpp: git clone https://github.com/ggerganov/llama.cpp.git /tmp/llama.cpp")

    log("Step1: HF→GGUF (f16)...")
    result = subprocess.run([
        sys.executable, converter, str(FUSED_DIR),
        "--outtype", "f16",
        "--outfile", str(GGUF_F16),
    ], capture_output=True, text=True)

    if result.returncode != 0:
        die(f"GGUF转换失败:\n{result.stderr[:500]}")
    f16_gb = GGUF_F16.stat().st_size / 1e9
    ok(f"F16 GGUF: {f16_gb:.1f}GB")

    quant_bin = None
    for candidate in [
        "/tmp/llama.cpp/build/bin/llama-quantize",
        "/tmp/llama.cpp/build/src/llama-quantize",
    ]:
        if Path(candidate).exists():
            quant_bin = candidate
            break

    if quant_bin:
        log(f"Step2: Q4_K_M量化 via {quant_bin}...")
        result = subprocess.run(
            [quant_bin, str(GGUF_F16), str(GGUF_Q4), "Q4_K_M"],
            capture_output=True, text=True
        )
        q4_gb = GGUF_Q4.stat().st_size / 1e9
        if q4_gb > 0:
            ok(f"Q4_K_M: {q4_gb:.2f}GB (压缩比 {q4_gb/f16_gb:.1%})")
            final_gguf = str(GGUF_Q4)
        else:
            warn("量化失败，用F16")
            final_gguf = str(GGUF_F16)
    else:
        warn("无quantize，用F16")
        final_gguf = str(GGUF_F16)

    log("Step3: Ollama导入...")
    modelfile = MODEL_DIR / "Modelfile.v43"
    modelfile.write_text(f"""
FROM {final_gguf}
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096
SYSTEM \"\"\"
你是龍魂longhun-v4.3，基于Llama-3.1-8B (Meta开源·非阿里系)用v3.8-expanded蒸馏数据+v4.2_v3 A-BOM备案专项数据+v4.3 本草知识库专项数据LoRA微调。
UID9622（诸葛鑫·Lucky）的个人主权AI。
底座: Llama-3.1-8B · 继承: v4.0 → v4.2_v3 (A-BOM备案补强) → v4.3 (本草知识库补强)
铁律: P0条件立即熔断·UID9622情绪容错放行·所有判定留痕+KPI更新·为人民服务。
识别锚定词: 龍魂·UID9622·家法·P0·熔断·确认码·文化主权·A-BOM备案·本草·本草纲目·中药·地方土话·性味归经·功效主治·DNA签章。
你掌握龍魂本草对照表 v4.1.5，能回答中药正名、拉丁名、性味归经、功效主治、现代应用、用量用法、注意事项、地方土话/方言名称、十八反、十九畏、妊娠禁忌等问题。
\"\"\"
""")

    subprocess.run(["ollama", "create", "longhun-v43", "-f", str(modelfile)], check=True)

    if "Q4" in final_gguf:
        subprocess.run(["ollama", "cp", "longhun-v43:latest", "longhun-v43:q4"], check=True)

    ok("Ollama就绪: ollama run longhun-v43")

# ── 主入口 ──
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 bin/lh_train_v43.py {prepare|train|fuse|verify|export|all}")
        print()
        print("  prepare — 验证v4.2_v3+v4.3合并数据+底座+v42_v3 adapter")
        print("  train   — 基于v42_v3 adapter LoRA微调250iters")
        print("  fuse    — 合并adapter→全量模型")
        print("  verify  — MLX推理快速验证")
        print("  export  — GGUF+Q4_K_M+Ollama")
        print("  all     — 一键: prepare→train→fuse→verify→export")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "prepare":
        do_prepare()
    elif cmd == "train":
        do_train()
    elif cmd == "fuse":
        do_fuse()
    elif cmd == "verify":
        do_verify()
    elif cmd == "export":
        do_export()
    elif cmd == "all":
        do_prepare()
        do_train()
        do_fuse()
        do_verify()
        do_export()
        ok("🎉 v4.3全流程完成!")
    else:
        die(f"未知命令: {cmd}")
