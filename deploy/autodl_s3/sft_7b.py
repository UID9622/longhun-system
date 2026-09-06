#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·未时·䷚颐-S3-AUTODL-SFT-7B-V0.1-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 作用: AutoDL 端 Qwen2.5-7B-Instruct 词表增量 + qlora SFT
#   数据: /root/autodl-tmp/s3_upload/data/{train,valid}.jsonl
#         (行={messages:[...]} 或 {prompt,response}·与本地 corpus 同格式)
#   卡型: 自动探测(>20GB → emb 增量模板;否则冻结 emb 冒烟模板)
#   诚实口径(v0.1):
#     - 全序列因果 LM(未做 assistant-mask;本地 mlx 用 mask_prompt=True → 两端 mask 策略
#       有差异·如实标·后续版本可对齐)
#     - 时长/显存推演级·以实跑日志为准
#   用法: python3 sft_7b.py --data_dir ... --model_dir ... --output ... [--epochs 1 --lr 1e-4]
import argparse
import json
import os
import sys
import torch
from pathlib import Path

def build_examples(path):
    exs = []
    if not Path(path).exists():
        print(f"⚠️ 数据缺失: {path}")
        return exs
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        msgs = o.get("messages")
        if msgs:
            exs.append(msgs)
            continue
        if "prompt" in o and "response" in o:
            exs.append([{"role": "user", "content": o["prompt"]},
                        {"role": "assistant", "content": o["response"]}])
        elif "instruction" in o:
            content = o.get("output") or o.get("answer") or ""
            exs.append([{"role": "user", "content": o["instruction"]},
                        {"role": "assistant", "content": content}])
        elif "text" in o:  # 扩源纯文本块(道德经81章/知识文·text 轨全序列续训)
            exs.append([{"_text": o["text"]}])
    return exs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--max_len", type=int, default=2048)
    args = ap.parse_args()

    assert torch.cuda.is_available(), "无 CUDA → 停"
    mem_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
    full_emb = mem_gb > 20  # 4090/24G → 词表增量模板
    print(f"GPU={torch.cuda.get_device_name(0)} · {mem_gb:.1f}GB · "
          f"模板={'emb增量(≥20G)' if full_emb else '冻结emb冒烟(<20G)'}")

    from transformers import (AutoModelForCausalLM, AutoTokenizer,
                              TrainingArguments, Trainer, BitsAndBytesConfig)
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

    tok = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    print(f"tokenizer vocab = {len(tok)}" +
          (" (迁移151832生效)" if len(tok) == 151832 else " (⚠️非151832·检查覆盖)"))

    train_msgs = build_examples(os.path.join(args.data_dir, "train.jsonl"))
    valid_msgs = build_examples(os.path.join(args.data_dir, "valid.jsonl"))
    print(f"数据: train {len(train_msgs)} · valid {len(valid_msgs)}")

    def tok_msgs(msgs):
        # text 块全序列续训(扩源知识轨·labels=全序列)
        if msgs and msgs[0].get("_text"):
            txt = msgs[0]["_text"]
        else:
            txt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)
        enc = tok(txt, max_length=args.max_len, truncation=True, return_tensors="pt")
        return {"input_ids": enc["input_ids"][0], "attention_mask": enc["attention_mask"][0],
                "labels": enc["input_ids"][0].clone()}

    train_ds = __import__("datasets").Dataset.from_list(
        [tok_msgs(m) for m in train_msgs])
    valid_ds = __import__("datasets").Dataset.from_list(
        [tok_msgs(m) for m in valid_msgs]) if valid_msgs else None

    # v0.3 修复: 自定义 collator·显式 pad(不等长批·labels 补 -100)
    # 背景: transformers 4.46 DLMC 对 fast tokenizer 批 pad 失效(实测 631/2048 撞 torch.tensor)
    #        dataset 取出的 input_ids 已为 list(非 tensor),兼容两型
    def _as_list(x):
        return x.tolist() if hasattr(x, "tolist") else list(x)

    def collate_fn(features):
        max_len = max(len(f["input_ids"]) for f in features)
        pad_id = tok.pad_token_id
        b_ii, b_am, b_lb = [], [], []
        for f in features:
            ii, am, lb = _as_list(f["input_ids"]), _as_list(f["attention_mask"]), _as_list(f["labels"])
            pad_n = max_len - len(ii)
            b_ii.append(ii + [pad_id] * pad_n)
            b_am.append(am + [0] * pad_n)
            b_lb.append(lb + [-100] * pad_n)
        import torch
        return {"input_ids": torch.tensor(b_ii, dtype=torch.long),
                "attention_mask": torch.tensor(b_am, dtype=torch.long),
                "labels": torch.tensor(b_lb, dtype=torch.long)}

    qcfg = BitsAndBytesConfig(load_in_4bit=True,
                              bnb_4bit_quant_type="nf4",
                              bnb_4bit_compute_dtype=torch.bfloat16 if full_emb else torch.float16,
                              bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_dir,
                                                 quantization_config=qcfg,
                                                 torch_dtype=torch.bfloat16,
                                                 trust_remote_code=True,
                                                 device_map="auto")
    model = prepare_model_for_kbit_training(model)
    lora = LoraConfig(
        r=32 if full_emb else 16,
        lora_alpha=64 if full_emb else 32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        modules_to_save=["embed_tokens", "lm_head"] if full_emb else None,
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    # v0.4: 4090D 实机 OOM(60/271 步·embed+lm_head 全量≈10GB 权重+梯度+8bit优化器)
    #        → full_emb 批 2→1 + accum 8→16 + max_len 2048→1536(run 传参) 保等效 batch 16
    targs = TrainingArguments(
        output_dir=args.output,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=16 if full_emb else 8,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=5,
        eval_strategy="steps" if valid_ds else "no",
        eval_steps=50,
        save_steps=200,
        bf16=full_emb, fp16=not full_emb,
        gradient_checkpointing=True,
        optim="paged_adamw_8bit",
        max_grad_norm=1.0,
        report_to=[],
        save_total_limit=2,
        seed=42,
    )
    trainer = Trainer(model=model, args=targs,
                      train_dataset=train_ds, eval_dataset=valid_ds,
                      tokenizer=tok, data_collator=collate_fn)
    trainer.train()
    model.save_pretrained(args.output + "_adapter")
    tok.save_pretrained(args.output + "_adapter")
    print(f"✅ 完成 · adapter 在 {args.output}_adapter")

if __name__ == "__main__":
    main()
