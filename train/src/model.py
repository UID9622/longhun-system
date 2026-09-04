#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 模型结构
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-MODEL-v1.0

初始结构：Embedding + LSTM + 输出头。
后续可焊：Transformer、RoPE、RMSNorm、LoRA、专家混合……随你拆。
"""
import torch
import torch.nn as nn


class LonghunLM(nn.Module):
    """龍魂语言模型 v1.0"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.vocab_size = config.vocab_size
        self.hidden_size = config.hidden_size
        self.max_seq_len = config.max_seq_len

        self.embedding = nn.Embedding(config.vocab_size, config.hidden_size, padding_idx=config.pad_id)
        self.lstm = nn.LSTM(
            input_size=config.hidden_size,
            hidden_size=config.hidden_size,
            num_layers=config.num_layers,
            batch_first=True,
            dropout=config.dropout if config.num_layers > 1 else 0,
        )
        self.norm = nn.LayerNorm(config.hidden_size)
        self.fc = nn.Linear(config.hidden_size, config.vocab_size)

        self.dna = "#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-MODEL-v1.0"

    def forward(self, input_ids, targets=None):
        """
        input_ids: [batch, seq_len]
        targets:   [batch, seq_len]
        """
        x = self.embedding(input_ids)           # [batch, seq, hidden]
        x, _ = self.lstm(x)                     # [batch, seq, hidden]
        x = self.norm(x)
        logits = self.fc(x)                     # [batch, seq, vocab]

        loss = None
        if targets is not None:
            # 忽略 padding 位置
            loss_fct = nn.CrossEntropyLoss(ignore_index=self.config.pad_id)
            loss = loss_fct(logits.view(-1, self.vocab_size), targets.view(-1))

        return logits, loss

    @torch.no_grad()
    def generate(self, tokenizer, prompt, max_new_tokens=50, temperature=1.0):
        """简单自回归生成。"""
        self.eval()
        input_ids = tokenizer.encode(prompt, add_bos=True, max_len=self.max_seq_len)
        input_ids = torch.tensor([input_ids], dtype=torch.long).to(next(self.parameters()).device)

        for _ in range(max_new_tokens):
            if input_ids.size(1) >= self.max_seq_len:
                break
            logits, _ = self.forward(input_ids)
            logits = logits[:, -1, :] / temperature
            probs = torch.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            input_ids = torch.cat([input_ids, next_id], dim=1)

        output_ids = input_ids[0].tolist()
        return tokenizer.decode(output_ids, skip_special=True)
