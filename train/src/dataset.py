#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 数据集
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-DATASET-v1.0
"""
from pathlib import Path
from torch.utils.data import Dataset


class LonghunDataset(Dataset):
    """把多个语料目录下的 .txt / .md 切成固定长度样本。"""

    def __init__(self, data_dirs, tokenizer, max_seq_len=512, max_samples=None):
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        self.max_samples = max_samples
        self.samples = []

        if isinstance(data_dirs, (str, Path)):
            data_dirs = [data_dirs]

        files = []
        for d in data_dirs:
            d = Path(d)
            if not d.exists():
                continue
            files.extend(d.rglob("*.txt"))
            files.extend(d.rglob("*.md"))

        for file in files:
            if self.max_samples and len(self.samples) >= self.max_samples:
                break
            try:
                text = file.read_text(encoding="utf-8")
            except Exception as e:
                print(f"⚠️ 读取失败 {file}: {e}")
                continue

            # 按段落切分，过滤太短的片段
            for para in text.split("\n\n"):
                if self.max_samples and len(self.samples) >= self.max_samples:
                    break
                para = para.strip()
                if len(para) < 20:
                    continue
                ids = self.tokenizer.encode(para, max_len=self.max_seq_len + 1)
                if len(ids) < 2:
                    continue
                self.samples.append(ids)

        self.dna = "#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-DATASET-v1.1"

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        ids = self.samples[idx]
        # 输入：前 n-1 个 token；目标：后 n-1 个 token（错位一位）
        x = ids[:-1]
        y = ids[1:]
        # padding 到 max_seq_len
        if len(x) < self.max_seq_len:
            pad_len = self.max_seq_len - len(x)
            x = x + [self.tokenizer.pad_id] * pad_len
            y = y + [self.tokenizer.pad_id] * pad_len
        return x, y
