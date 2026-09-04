#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 配置中心
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-CONFIG-v1.0
"""
from pathlib import Path


class Config:
    """全部参数集中在这里，想怎么改就怎么改。"""

    # 模型命名
    model_name = "龍魂-0.5B"

    # 词表
    vocab_size = 12000         # 字符级词表上限，实际按语料动态构建
    pad_id = 0
    unk_id = 1
    bos_id = 2
    eos_id = 3

    # 模型结构
    # 龍魂自研 LM · 从零训练（不依赖任何底座）
    hidden_size = 512
    num_layers = 4
    num_heads = 8
    max_seq_len = 512
    dropout = 0.1

    # 训练
    batch_size = 16
    learning_rate = 3e-4
    epochs = 16                 # 16 轮强化训练（第一版 8 轮 Loss 1.383，续炼收敛）
    num_workers = 0            # macOS 建议 0，避免 multiprocessing 问题
    gradient_clip = 1.0

    # 数据限制（自研模型要吃够龍魂语料）
    auto_corpus_max_files = 400      # 自动收集最多文件数
    auto_corpus_max_total_mb = 60    # 自动收集总大小上限
    dataset_max_samples = 60000      # 数据集最大样本数

    # 路径
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    auto_corpus_dir = processed_dir / "auto_corpus"
    output_dir = project_root / "output"
    model_dir = output_dir / "models"
    tokenizer_path = model_dir / f"{model_name}_tokenizer.json"

    # 自动语料收集（全量接入龍魂核心知识库）
    auto_corpus_enabled = True
    auto_corpus_sources = [
        project_root / ".." / "01_protocols",      # 协议 1157 md
        project_root / ".." / "papers",            # 论文 94 md
        project_root / ".." / "skills",            # 技能 65 md
        project_root / ".." / "articles",          # 文章 203 md
        project_root / ".." / "04_ENGINES",        # 引擎 8 md
        project_root / ".." / "12_DOCS",           # 全量文档 10356 md
    ]
    auto_corpus_exclude = [
        "*.bak", "*.tmp", "*.log",
        "*/node_modules/*", "*/.venv/*", "*/__pycache__/*", "*/.git/*",
    ]

    # 设备
    device = "cpu"             # 默认 CPU，MPS/CUDA 可在 trainer 里自动检测

    # DNA
    dna = "#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-CONFIG-v1.1"
