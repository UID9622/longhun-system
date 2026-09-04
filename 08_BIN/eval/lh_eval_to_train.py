# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-8441ff0f
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·癸亥·午时·☰乾-EVAL-TO-TRAIN-v1.0
"""
🐉 龍魂 · 题库 → 训练数据生成器

用多维度评测引擎把测试池里的题目生成“三种解法”答案，
只保留三色审计全绿的样本，写成 instruct 训练 jsonl。
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lh_eval_runner as ev


HOME = Path.home()
TRAIN_FILE = HOME / ".longhun" / "eval" / "train_ready.jsonl"


def build_train_sample(item: dict, response: str) -> dict:
    system = "你是龍魂系统的多维度解题助手。回答问题时，请用【方式一·白话解释】【方式二·逻辑推导】【方式三·代码或示例】三个维度，让不同背景的人都能听懂。"
    user = f"题目：{item.get('question', '')}\n\n请用三种不同方式回答。"
    return {
        "messages": [
            {"role": "system", "content": ev._guard(system)},
            {"role": "user", "content": ev._guard(user)},
            {"role": "assistant", "content": ev._guard(response)},
        ],
        "source": item.get("source", "eval"),
        "type": item.get("type", "unknown"),
        "dna": ev._dna("TRAIN"),
    }


def generate_train_data(model_path: str, adapter_path: str = None, limit: int = 106, max_tokens: int = 600):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始生成训练数据...")
    if not ev.INDEX_FILE.exists():
        print("  ❌ 测试池索引不存在，请先运行 lh_eval pull")
        sys.exit(1)

    index = json.load(open(ev.INDEX_FILE, encoding="utf-8"))
    suites = index.get("suites", [])[:limit]
    print(f"  载入 {len(suites)} 道题目")

    model, tokenizer = ev.load_model_once(model_path, adapter_path)

    kept = 0
    skipped = 0
    TRAIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRAIN_FILE, "w", encoding="utf-8") as fout:
        for i, item in enumerate(suites, 1):
            q = item.get("question", "")[:60]
            print(f"\n  [{i}/{len(suites)}] {q}...")
            response = ev.generate_answer(model, tokenizer, item.get("question", ""), max_tokens=max_tokens)
            solutions = ev.parse_solutions(response)
            ground_truths = ev.extract_ground_truth(item.get("expected", ""))

            # 三色审计
            all_green = True
            any_present = False
            for name, text in solutions.items():
                score = ev.score_solution(text, ground_truths)
                present = bool(text)
                any_present = any_present or present
                if not (present and score >= 0.99):
                    all_green = False

            if all_green and any_present:
                sample = build_train_sample(item, response)
                fout.write(json.dumps(sample, ensure_ascii=False) + "\n")
                kept += 1
                print(f"      ✅ 全绿，保留（累计 {kept}）")
            else:
                skipped += 1
                print(f"      ⚠️ 未全绿，跳过（累计 {skipped}）")
            time.sleep(0.2)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 完成: 保留 {kept} 条, 跳过 {skipped} 条")
    print(f"  训练数据: {TRAIN_FILE}")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 题库转训练数据")
    parser.add_argument("--model", default="models/qwen-1.5b-instruct-4bit", help="模型路径")
    parser.add_argument("--adapter", default=None, help="LoRA adapter 路径（可选）")
    parser.add_argument("--limit", type=int, default=106, help="处理题目数量上限")
    parser.add_argument("--max-tokens", type=int, default=600, help="每题最大生成 token 数")
    args = parser.parse_args()
    generate_train_data(args.model, args.adapter, args.limit, args.max_tokens)


if __name__ == "__main__":
    main()
