#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 分词器
DNA: #龍芯⚡️2026-06-28-LONGHUN-TRAIN-TOKENIZER-v1.0

中文字符级分词器：每个独立汉字/符号一个 ID，简单、可解释、可焊。
后续可替换为 BPE / SentencePiece / CNSH 专用分词。
"""
import json
from pathlib import Path
from collections import Counter


class CharTokenizer:
    """字符级分词器，支持保存/加载词表。"""

    def __init__(self, vocab_size=8000, special=None):
        self.vocab_size = vocab_size
        self.special = special or {
            "[PAD]": 0,
            "[UNK]": 1,
            "[BOS]": 2,
            "[EOS]": 3,
        }
        self.pad_id = self.special["[PAD]"]
        self.unk_id = self.special["[UNK]"]
        self.bos_id = self.special["[BOS]"]
        self.eos_id = self.special["[EOS]"]
        self.char2id = dict(self.special)
        self.id2char = {v: k for k, v in self.special.items()}
        self.dna = "#龍芯⚡️2026-06-28-LONGHUN-TRAIN-TOKENIZER-v1.0"

    def fit(self, texts):
        """从语料中学习词表。"""
        counter = Counter()
        for text in texts:
            counter.update(text)
        # 按频率取前 vocab_size - special 个字符
        most_common = counter.most_common(self.vocab_size - len(self.special))
        for idx, (char, _) in enumerate(most_common, start=len(self.special)):
            self.char2id[char] = idx
            self.id2char[idx] = char
        return self

    def encode(self, text, add_bos=False, add_eos=False, max_len=None):
        """文本 -> ID 列表。"""
        ids = []
        if add_bos:
            ids.append(self.bos_id)
        for ch in text:
            ids.append(self.char2id.get(ch, self.unk_id))
        if add_eos:
            ids.append(self.eos_id)
        if max_len:
            ids = ids[:max_len]
        return ids

    def decode(self, ids, skip_special=True):
        """ID 列表 -> 文本。"""
        chars = []
        for i in ids:
            ch = self.id2char.get(i, "[UNK]")
            if skip_special and ch.startswith("[") and ch.endswith("]"):
                continue
            chars.append(ch)
        return "".join(chars)

    def save(self, path):
        """保存词表到 JSON。"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "vocab_size": self.vocab_size,
                    "special": self.special,
                    "char2id": self.char2id,
                    "dna": self.dna,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    def load(self, path):
        """从 JSON 加载词表。"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.vocab_size = data["vocab_size"]
        self.special = data["special"]
        self.char2id = data["char2id"]
        self.id2char = {v: k for k, v in self.char2id.items()}
        self.pad_id = self.special["[PAD]"]
        self.unk_id = self.special["[UNK]"]
        self.bos_id = self.special["[BOS]"]
        self.eos_id = self.special["[EOS]"]
        return self

    def __len__(self):
        return len(self.char2id)
