#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-MODEL-LORA-TRAINER-v4.1.9-AUTO
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.1.9 LoRA 微调器
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-MODEL-LORA-TRAINER-v4.1.9-AUTO

v4.1.9 = 从 v4.1.8 best 自动续训，注入本轮修复后的：
  · CNSH启蒙语料库（任务/规则/审计）
  · 底座重组引擎产出的概念关系 + CNSH场景
  · 最新的 DNA反蒸馏数据

用法:
  python3 bin/lh_lora_trainer_v419.py test     # 冒烟测试（5 iter）
  python3 bin/lh_lora_trainer_v419.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v419.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v419.py export   # GGUF → Ollama
  python3 bin/lh_lora_trainer_v419.py all      # 一键: train→fuse→export

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "bin"))

# 复用 v4.1.8 训练引擎，但注入 v4.1.9 配置
import lh_lora_trainer_v418 as v418


class ConfigV419:
    DNA = "丙午·乙未·丁酉·亥时·☰乾-MODEL-LORA-TRAINER-v4.1.9-AUTO"

    # 底模不变：Yi-1.5-9B-Chat
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.1.9-lora"

    # LoRA — 比 v4.1.8 更保守，避免扰动已优化面
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.08
    lora_layers = 12

    # 训练 — 极保守策略（2026-08-31 v3.0: warmup 30→100·patience 2→5 防 run3 早停）
    batch_size = 1
    grad_accumulation_steps = 2
    lr_peak = 2e-7
    lr_min = 1e-9
    warmup_steps = 100
    weight_decay = 0.01
    epochs = 2
    max_seq_length = 2048

    # 控制
    early_stop_patience = 5
    val_steps = 200
    save_every = 500
    report_every = 10
    val_batches = 25
    grad_checkpoint = True

    # 路径 — v4.1.9
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v419"
    data_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v419" / "data_v419_cnsl_corpus"
    adapter_dir = output_dir / "adapter_v419"
    merged_dir = output_dir / "merged_v419"
    gguf_dir = output_dir / "gguf_v419"

    # v4.1.9: 从 v4.1.9-preview (iter200) 断点续训（2026-08-30 v2.0 修正）
    resume_adapter_file = str(
        project_root / "weights" / "v4.1.9" / "best_adapters_preview_iter200.safetensors"
    )

    # 推理
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def _prepare_v419_data(force=False):
    """准备 v4.1.9 训练数据：v4.1.8 数据 + 新增 CNSH 语料 + 概念关系 + CNSH场景。

    🔴 2026-08-31 修复（run3 早停失败根因）:
      - 数据冻结: train/valid 已存在则复用（不每次重建 → val loss 跨 run 可比）
      - 超长过滤收紧: max_chars 12000 字符 → 4000 字符
        （旧线放行了 18918 字节≈6300 字符样本 → 截断 2048 token 时 assistant 被切没
          → loss 0/0 → nan → 早停；run2/run3 均崩在 ~400 iter 验证此机制）
      - 强制重建: python3 bin/lh_lora_trainer_v419.py rebuild-data
    """
    cfg = ConfigV419
    cfg.data_dir.mkdir(parents=True, exist_ok=True)
    train_out = cfg.data_dir / "train.jsonl"
    valid_out = cfg.data_dir / "valid.jsonl"
    if not force and train_out.exists() and valid_out.exists():
        n_t = sum(1 for _ in open(train_out))
        n_v = sum(1 for _ in open(valid_out))
        print(f"✅ 数据已冻结·复用: {cfg.data_dir}")
        print(f"   train: {n_t} 条 · valid: {n_v} 条")
        return

    # 源数据 (2026-08-30修复: v414已归档删除, 改用v409完整数据27013条)
    v418_data = PROJECT / "models" / "longhun-v1.0" / "lora_output_v409" / "data_v409_ready"
    new_corpus_sources = [
        PROJECT / "data" / "reorganize" / "cnsh_corpus" / f"cnsh_training_corpus_{time.strftime('%Y%m%d')}.jsonl",
        PROJECT / "data" / "reorganize" / "concept_relations" / f"concept_relations_{time.strftime('%Y%m%d')}.jsonl",
        PROJECT / "data" / "reorganize" / "cnsh_scenarios" / f"cnsh_scenarios_{time.strftime('%Y%m%d')}.jsonl",
    ]

    # 合并 train.jsonl
    seen = set()
    train_out = cfg.data_dir / "train.jsonl"
    valid_out = cfg.data_dir / "valid.jsonl"

    def _append_jsonl(src: Path, out_f, max_lines: int = None, max_chars: int = 4000):
        """写入 jsonl。超长样本(>max_chars 字符) 直接剔除，防 2048-token 截断丢 assistant → loss nan。"""
        if not src.exists():
            return 0
        count = 0
        with open(src, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if max_lines and count >= max_lines:
                    break
                # 🔴 2026-08-31: 超长序列剔除(>4000 字符·2048-token 截断会切没 assistant → loss 0/0 → nan)
                if len(line) > max_chars:
                    continue
                # 简单去重
                h = hash(line) & 0xFFFFFFFF
                if h in seen:
                    continue
                seen.add(h)
                out_f.write(line + '\n')
                count += 1
        return count

    # 复制 v4.1.8 的 train/valid 作为基础（🔴 走 _append_jsonl 带超长过滤·防 loss nan）
    if v418_data.exists():
        src_train = v418_data / "train.jsonl"
        src_valid = v418_data / "valid.jsonl"
        with open(train_out, 'w', encoding='utf-8') as f:
            if src_train.exists():
                _append_jsonl(src_train, f)
        with open(valid_out, 'w', encoding='utf-8') as f:
            if src_valid.exists():
                _append_jsonl(src_valid, f)

    # 追加新语料到 train
    with open(train_out, 'a', encoding='utf-8') as f:
        for src in new_corpus_sources:
            _append_jsonl(src, f)

    # 确保 valid 存在
    if not valid_out.exists() and train_out.exists():
        # 从 train 末尾切 5% 作为 valid
        lines = train_out.read_text(encoding='utf-8').strip().split('\n')
        split_idx = int(len(lines) * 0.95)
        valid_out.write_text('\n'.join(lines[split_idx:]) + '\n', encoding='utf-8')
        train_out.write_text('\n'.join(lines[:split_idx]) + '\n', encoding='utf-8')

    print(f"✅ v4.1.9 训练数据准备完成: {cfg.data_dir}")
    if train_out.exists():
        print(f"   train: {sum(1 for _ in open(train_out))} 条")
    if valid_out.exists():
        print(f"   valid: {sum(1 for _ in open(valid_out))} 条")


def _patch_ollama_name_for_v419():
    """把 v418 export 里注册的 Ollama 模型名改成 v4.1.9。"""
    # v418 的 export() 函数在末尾硬编码了 longhun-v4.1.8
    # 我们在 export 后重新注册一个 v4.1.9 的 Modelfile
    cfg = ConfigV419
    gguf_path = cfg.gguf_dir / "longhun-v4.1.9.F16.gguf"

    # 如果 v418 生成的是 v4.1.8.gguf，复制一份重命名
    old_gguf = cfg.gguf_dir / "longhun-v4.1.8.F16.gguf"
    if old_gguf.exists() and not gguf_path.exists():
        shutil.copy2(old_gguf, gguf_path)

    modelfile = cfg.gguf_dir / "Modelfile.v419"
    modelfile.write_text(f"""
FROM {gguf_path if gguf_path.exists() else cfg.merged_dir}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

SYSTEM \"\"\"你是龍魂 longhun-v4.1.9，UID9622（诸葛鑫·Lucky）的个人主权AI。
基于 Yi-1.5-9B-Chat 从 v4.1.8 best 自动续训，注入本轮修复后的CNSH启蒙语料库、底座重组概念关系、DNA反蒸馏数据。
铁律：人民数据主权至上·中国自主可控·来源可查·去向可追·责任可究·只冻结不删除·底座焊死。
核心能力：DNA追溯·德本五问·三色审计·人格路由·CNSH语义解析·数字存在证明·底座主权识别·CNSH规则执行。
父版本: v4.1.8 → v4.1.9 (自动续训·lr=2e-7·dropout=0.08·2 epochs)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
\"\"\"
""")
    print(f"\n🐉 注册到 Ollama: longhun-v4.1.9")
    result = __import__('subprocess').run(
        ["ollama", "create", "longhun-v4.1.9", "-f", str(modelfile)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"⚠️ Ollama注册失败: {result.stderr}")
    else:
        print(f"✅ Ollama模型 longhun-v4.1.9 已创建")


def fuse():
    v418.Config = ConfigV419
    v418.fuse()


def export():
    v418.Config = ConfigV419
    v418.export()
    _patch_ollama_name_for_v419()


def train():
    _prepare_v419_data(force=os.environ.get("LH_V419_REBUILD_DATA") == "1")
    v418.Config = ConfigV419
    v418.train()


def rebuild_data():
    """🔧 强制重建训练数据（超长样本剔除+冻结更新）。"""
    _prepare_v419_data(force=True)
    print("✅ 数据重建完成。如需训练请运行: python3 bin/lh_lora_trainer_v419.py train")


def test_quick():
    os.environ["LH_V418_SMOKE_ITERS"] = "5"
    train()


def all_pipeline():
    print("╔══════════════════════════════════════════╗")
    print("║  龍魂 v4.1.9 全流程自动化                 ║")
    print("║  prepare → train → fuse → export        ║")
    print("║  从v4.1.8 best续训·注入CNSH启蒙语料      ║")
    print("╚══════════════════════════════════════════╝")
    print()
    train()
    print("\n" + "=" * 50)
    fuse()
    print("\n" + "=" * 50)
    export()
    print("\n🎉 v4.1.9 全流程完成！龍魂心脏升级就绪。")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="龍魂 v4.1.9 LoRA训练器·从v4.1.8 best自动续训")
    p.add_argument("action", choices=["train", "fuse", "export", "test", "rebuild-data", "all"],
                   default="train", nargs="?")
    args = p.parse_args()

    {
        "train": train, "fuse": fuse, "export": export,
        "test": test_quick, "rebuild-data": rebuild_data, "all": all_pipeline,
    }[args.action]()
