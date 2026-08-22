#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# -*- coding: utf-8 -*-
"""
龍魂自研模型 · 对话推理入口
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷐随-LONGHUN-CHAT-ENTRY-v1.0

用法:
  python3 scripts/chat.py "提示词" [max_new_tokens] [temperature]
  例: python3 scripts/chat.py "龍魂是什么" 60 0.8
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from config import Config
from tokenizer import CharTokenizer
from model import LonghunLM
import torch

cfg = Config()
model_path = cfg.model_dir / f"{cfg.model_name}.pt"
tokenizer_path = cfg.tokenizer_path

def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/chat.py \"提示词\" [max_new_tokens] [temperature]")
        sys.exit(1)
    prompt = sys.argv[1]
    max_new = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    temp = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8

    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    model_cfg = ckpt["config"]
    from types import SimpleNamespace
    mcfg = SimpleNamespace(
        vocab_size=model_cfg.get("vocab_size", 12000),
        hidden_size=model_cfg.get("hidden_size", 512),
        max_seq_len=model_cfg.get("max_seq_len", 512),
        pad_id=model_cfg.get("pad_id", 0),
        dropout=model_cfg.get("dropout", 0.1),
        num_layers=model_cfg.get("num_layers", 4),
    )
    model = LonghunLM(mcfg)
    model.load_state_dict(ckpt["model_state_dict"])
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model.to(device).eval()
    tokenizer = CharTokenizer().load(tokenizer_path)

    out = model.generate(tokenizer, prompt, max_new_tokens=max_new, temperature=temp)
    print(f"[提示] {prompt}")
    print(f"[输出] {out}")
    print(f"[DNA] {ckpt.get('dna', 'N/A')}")

if __name__ == "__main__":
    main()
