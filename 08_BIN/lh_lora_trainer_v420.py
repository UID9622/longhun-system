#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·甲申·申时·䷎谦-MODEL-LORA-TRAINER-v4.2.0-AUTO
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 longhun-v4.2.0 LoRA 微调器
DNA: #龍芯⚡️丙午·丙申·甲申·申时·䷎谦-MODEL-LORA-TRAINER-v4.2.0-AUTO

v4.2.0 = 从 v4.1.9 best 自动续训（Val 0.8115 @iter600）
  · 复用 v4.1.9 冻结数据（25635 train + 1312 valid·26947 条·不重建·跨 run 可比）
  · 收敛面极保守档（run2 NaN 修复）：lr=1e-7·warmup=300·dropout=0.08·epochs=1·patience=5
  · 目标：收敛面上最小步幅走 1 epoch 验证可否净改善；不可得则 0.8115 即同数据面天花板

用法:
  python3 bin/lh_lora_trainer_v420.py test     # 冒烟测试（5 iter）
  python3 bin/lh_lora_trainer_v420.py train    # 开始 LoRA 微调
  python3 bin/lh_lora_trainer_v420.py fuse     # 合并 adapter
  python3 bin/lh_lora_trainer_v420.py export   # GGUF → Ollama
  python3 bin/lh_lora_trainer_v420.py all      # 一键: train→fuse→export

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "bin"))

# 复用 v4.1.8 训练引擎，注入 v4.2.0 配置
import lh_lora_trainer_v418 as v418


class ConfigV420:
    DNA = "丙午·丙申·甲申·申时·☰乾-MODEL-LORA-TRAINER-v4.2.0-AUTO"

    # 底模不变：Yi-1.5-9B-Chat
    LOCAL_MLX_MODEL = str(PROJECT / "models" / "longhun-v1.0" / "yi1.5-9b-chat-mlx")
    model_name = "longhun-v4.2.0-lora"

    # LoRA — 与 v4.1.9 一致，避免扰动已优化面
    lora_rank = 16
    lora_alpha = 64
    lora_dropout = 0.08
    lora_layers = 12

    # 训练 — 收敛面极保守档（2026-09-03 run2 同分布二次训练 NaN 根因修复）
    #   run2 实证: 从 v4.1.9 final best(0.8115) 续训同冻结数据 + lr2e-7/warmup100
    #   → iter106+ 连续 nan 止损退出（= v4.1.6 同分布再训 NaN 先例复发）
    #   → 收敛面上 lr 到峰即梯度爆。降峰一半 + warmup 拉长 3 倍 + 单 epoch 最小扰动。
    batch_size = 1
    grad_accumulation_steps = 2
    lr_peak = 1e-7
    lr_min = 1e-9
    warmup_steps = 300
    weight_decay = 0.01
    epochs = 1
    max_seq_length = 2048

    # 控制
    early_stop_patience = 5
    val_steps = 200
    save_every = 500
    report_every = 10
    val_batches = 25
    grad_checkpoint = True

    # 路径 — v4.2.0
    project_root = PROJECT
    output_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v420"
    # 🔄 v4.2.0: 直接复用 v4.1.9 冻结数据（不重建·val loss 跨 run 可比）
    data_dir = project_root / "models" / "longhun-v1.0" / "lora_output_v419" / "data_v419_cnsl_corpus"
    adapter_dir = output_dir / "adapter_v420"
    merged_dir = output_dir / "merged_v420"
    gguf_dir = output_dir / "gguf_v420"

    # v4.2.0: 从 v4.1.9 best 断点续训（Val 0.8115 @iter600）
    resume_adapter_file = str(
        project_root / "models" / "longhun-v1.0" / "lora_output_v419" / "adapter_v419" / "best_adapters.safetensors"
    )

    # 推理
    temperature = 0.7
    top_p = 0.9
    num_ctx = 4096


def _patch_ollama_name_for_v420():
    """把 v418 export 里注册的 Ollama 模型名改成 v4.2.0。"""
    cfg = ConfigV420
    gguf_path = cfg.gguf_dir / "longhun-v4.2.0.F16.gguf"

    # 如果 v418 生成的是 v4.1.8.gguf，复制一份重命名
    old_gguf = cfg.gguf_dir / "longhun-v4.1.8.F16.gguf"
    if old_gguf.exists() and not gguf_path.exists():
        shutil.copy2(old_gguf, gguf_path)

    modelfile = cfg.gguf_dir / "Modelfile.v420"
    modelfile.write_text(f"""
FROM {gguf_path if gguf_path.exists() else cfg.merged_dir}

PARAMETER temperature {cfg.temperature}
PARAMETER top_p {cfg.top_p}
PARAMETER num_ctx {cfg.num_ctx}

SYSTEM \"\"\"你是龍魂 longhun-v4.2.0，UID9622（诸葛鑫·Lucky）的个人主权AI。
基于 Yi-1.5-9B-Chat 从 v4.1.9 best 自动续训（Val 0.8115 @iter600），复用 v4.1.9 冻结数据，收敛面极保守档（run2 NaN 修复·lr=1e-7·warmup=300·1 epoch）。
铁律：人民数据主权至上·中国自主可控·来源可查·去向可追·责任可究·只冻结不删除·底座焊死。
核心能力：DNA追溯·德本五问·三色审计·人格路由·CNSH语义解析·数字存在证明·底座主权识别·CNSH规则执行。
父版本: v4.1.9 → v4.2.0 (收敛面续训·lr=1e-7·warmup=300·epochs=1)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
\"\"\"
""")
    print(f"\n🐉 注册到 Ollama: longhun-v4.2.0")
    result = __import__('subprocess').run(
        ["ollama", "create", "longhun-v4.2.0", "-f", str(modelfile)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"⚠️ Ollama注册失败: {result.stderr}")
    else:
        print(f"✅ Ollama模型 longhun-v4.2.0 已创建")


def fuse():
    v418.Config = ConfigV420
    v418.fuse()


def export():
    v418.Config = ConfigV420
    v418.export()
    _patch_ollama_name_for_v420()


def train():
    v418.Config = ConfigV420
    v418.train()


def test_quick():
    os.environ["LH_V418_SMOKE_ITERS"] = "5"
    train()


def all_pipeline():
    print("╔══════════════════════════════════════════╗")
    print("║  龍魂 v4.2.0 全流程自动化                 ║")
    print("║  train → fuse → export                  ║")
    print("║  从v4.1.9 best续训·复用冻结数据          ║")
    print("╚══════════════════════════════════════════╝")
    print()
    train()
    print("\n" + "=" * 50)
    fuse()
    print("\n" + "=" * 50)
    export()
    print("\n🎉 v4.2.0 全流程完成！龍魂心脏升级就绪。")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="龍魂 v4.2.0 LoRA训练器·从v4.1.9 best自动续训")
    p.add_argument("action", choices=["train", "fuse", "export", "test", "all"],
                   default="train", nargs="?")
    args = p.parse_args()

    {
        "train": train, "fuse": fuse, "export": export,
        "test": test_quick, "all": all_pipeline,
    }[args.action]()
