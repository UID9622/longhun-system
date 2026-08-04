#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 配置中心
DNA: #龍芯⚡️2026-06-28-LONGHUN-TRAIN-CONFIG-v1.0
"""
from pathlib import Path


class Config:
    """全部参数集中在这里，想怎么改就怎么改。"""

    # 模型命名
    model_name = "龍魂-0.1B"

    # 词表
    vocab_size = 8000          # 字符级词表上限，实际按语料动态构建
    pad_id = 0
    unk_id = 1
    bos_id = 2
    eos_id = 3

    # 模型结构
    # 默认小而快，3 分钟内跑完第一遍；想炼大模型改这里
    hidden_size = 256
    num_layers = 2
    num_heads = 4
    max_seq_len = 256
    dropout = 0.1

    # 训练
    batch_size = 8
    learning_rate = 1e-3
    epochs = 3                 # 默认 3 轮，快速验证；想炼大的改 10/50/100
    num_workers = 0            # macOS 建议 0，避免 multiprocessing 问题
    gradient_clip = 1.0

    # 数据限制（防止第一次跑就爆）
    auto_corpus_max_files = 100      # 自动收集最多文件数
    auto_corpus_max_total_mb = 20    # 自动收集总大小上限
    dataset_max_samples = 1000       # 数据集最大样本数

    # 路径
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    auto_corpus_dir = processed_dir / "auto_corpus"
    output_dir = project_root / "output"
    model_dir = output_dir / "models"
    tokenizer_path = model_dir / f"{model_name}_tokenizer.json"

    # 自动语料收集
    auto_corpus_enabled = True
    auto_corpus_sources = [
        project_root / ".." / "01_protocols",
        project_root / ".." / "papers",
        project_root / ".." / "docs",
        project_root / ".." / "memory-universe",
        project_root / ".." / "skills",
        project_root / ".." / "06_技術文檔",
    ]
    auto_corpus_exclude = [
        "*.bak", "*.tmp", "*.log",
        "*/node_modules/*", "*/.venv/*", "*/__pycache__/*", "*/.git/*",
    ]

    # 设备
    device = "cpu"             # 默认 CPU，MPS/CUDA 可在 trainer 里自动检测

    # DNA
    dna = "#龍芯⚡️2026-06-28-LONGHUN-TRAIN-CONFIG-v1.1"
