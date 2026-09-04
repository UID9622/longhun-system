#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_MODEL_TEST-1F984359
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-MODEL-TEST-v1.0
"""
🐉 龍魂 · 小模型推理测试 v1.0

加载底模 + LoRA adapter，对几个龍魂核心问题进行生成测试。
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from mlx_lm import load, generate
import mlx.core as mx


SYSTEM_PROMPT = (
    "你是龍魂系统助手，核心原则：人民数据主权、平台服务降级、"
    "创作者主权优先。回答需符合龍魂君子协议、CNSH 语义规范和 DNA 追溯要求。"
)

TEST_PROMPTS = [
    "什么是龍魂系统？",
    "请解释龍魂君子协议的核心原则。",
    "什么是CNSH？",
    "三才主权指数是什么？",
    "UID9622 是谁？",
    "请说明 DNA 追溯在龍魂系统中的作用。",
]


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_messages(system: str, user: str) -> list:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def make_sampler(temperature: float):
    """构造温度采样器。"""
    def sampler(logits):
        if temperature == 0:
            return mx.argmax(logits, axis=-1)
        return mx.random.categorical(logits / temperature)
    return sampler


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 模型推理测试")
    parser.add_argument("--base", default="models/qwen-1.5b-instruct", help="底模路径")
    parser.add_argument("--adapter", default="models/longhun-small-instruct-v1.3/adapter/best", help="adapter 路径")
    parser.add_argument("--max-tokens", type=int, default=256, help="最大生成 token 数")
    parser.add_argument("--temp", type=float, default=0.7, help="采样温度")
    parser.add_argument("--prompt", default=None, help="单独测试一个 prompt")
    args = parser.parse_args()

    print(f"[{_now()}] 📦 加载底模: {args.base}")
    print(f"[{_now()}] 🔌 加载 adapter: {args.adapter}")
    model, tokenizer = load(args.base, adapter_path=args.adapter, tokenizer_config={"trust_remote_code": True})

    prompts = [args.prompt] if args.prompt else TEST_PROMPTS

    results = []
    for idx, user_prompt in enumerate(prompts, 1):
        messages = build_messages(SYSTEM_PROMPT, user_prompt)
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        print(f"\n[{_now()}] ❓ [{idx}/{len(prompts)}] {user_prompt}")
        t0 = time.time()
        output = generate(
            model,
            tokenizer,
            prompt=prompt_text,
            max_tokens=args.max_tokens,
            sampler=make_sampler(args.temp),
            verbose=False,
        )
        elapsed = time.time() - t0
        print(f"[{_now()}] 💬 回答 ({elapsed:.1f}s):")
        print(output)

        results.append({
            "prompt": user_prompt,
            "output": output,
            "elapsed": elapsed,
        })

    # 保存测试结果
    out_path = Path(args.adapter).parent / "test_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "dna": f"#龍芯⚡️{_now()}-MODEL-TEST",
            "base": args.base,
            "adapter": args.adapter,
            "max_tokens": args.max_tokens,
            "temp": args.temp,
            "results": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n[{_now()}] ✅ 测试结果已保存: {out_path}")


if __name__ == "__main__":
    main()
