#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·壬戌·子时·需-TIKU-SELF-SOLVE-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · 题库自解引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·子时·䷄需-TIKU-SELF-SOLVE-v1.0
功能:
  1. 加载底模 + LoRA adapter（默认 step_600，避开训练中的 best）
  2. 让模型对题库题目自己解题
  3. 对照标准答案判断对错
  4. 输出 题目→模型解题过程 训练样本 JSONL
用法:
  python3 08_BIN/lh_tiku_self_solve.py [--start N] [--limit M] [--lang X] [--adapter PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime
from pathlib import Path

# transformers 4.49 与 Qwen2 新 tokenizer 兼容 patch：
# _set_model_specific_special_tokens 期望 dict，Qwen2 传 list
try:
    import transformers.tokenization_utils_base as _tub
    _orig_set = _tub.PreTrainedTokenizerBase._set_model_specific_special_tokens

    def _safe_set(self, special_tokens):
        if isinstance(special_tokens, list):
            special_tokens = {t: t for t in special_tokens}
        return _orig_set(self, special_tokens)

    _tub.PreTrainedTokenizerBase._set_model_specific_special_tokens = _safe_set
except Exception:
    pass

from mlx_lm import load, generate
import mlx.core as mx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TIKU_DIR = PROJECT_ROOT / "models" / "longhun-small-instruct-v1.3" / "tiku"
BASE = "models/qwen-1.5b-instruct-4bit"
ADAPTER = "models/longhun-small-instruct-v1.3/adapter_frozen_v1/step_600"

SYSTEM_PROMPT = (
    "你是龍魂解题引擎。用户给你一道编程/计算机笔试题，你需要：\n"
    "1. 先给出你的答案（选择题给选项字母+内容；判断题给 正确/错误；简答和编程题给完整解答）\n"
    "2. 再给出简要的推理过程。\n"
    "回答要准确、简洁、直接。"
)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_sampler(temperature: float = 0.3):
    def sampler(logits):
        return mx.random.categorical(logits / temperature)
    return sampler


def build_prompt(q: dict) -> str:
    lines = [f"【题目】{q['text']}"]
    if q["options"]:
        for opt in q["options"]:
            lines.append(f"{opt['key']}. {opt['text']}")
    lines.append("请作答：")
    return "\n".join(lines)


def check_answer(q: dict, output: str) -> str:
    """自动判定对错。返回 correct/incorrect/unknown。"""
    ans = (q["answer"] or q["reference"] or "").strip()
    if not ans:
        return "unknown"

    if q["type"] == "选择题":
        std_keys = re.findall(r"[A-H]", ans)
        if std_keys:
            out_keys = set(re.findall(r"答案[：:]\s*([A-H])", output))
            out_keys |= set(re.findall(r"(?:正确答案|答案为|答案)\s*[为是：:]?\s*\**\s*[（(]?([A-H])[)）]?\s*\**\s*[.、。]?", output))
            out_keys |= set(re.findall(r"([A-H])\s*[.、)）]", output))
            out_keys |= set(re.findall(r"[（(]([A-H])[)）]", output))
            out_keys |= set(re.findall(r"^\s*([A-H])\s*$", output, re.M))
            if any(k in out_keys for k in std_keys):
                return "correct"
            return "incorrect"
        return "unknown"

    if q["type"] == "判断题":
        norm = output.strip().lower()
        if re.search(r"正确|√|对", ans) and re.search(r"正确|√|对|true|yes", norm):
            return "correct"
        if re.search(r"错误|×|错", ans) and re.search(r"错误|×|错|false|no", norm):
            return "correct"
        return "incorrect"

    # 简答/编程/程序分析：关键词重合率粗判
    ans_norm = re.sub(r"[^\w\u4e00-\u9fff]", "", ans.lower())
    out_norm = re.sub(r"[^\w\u4e00-\u9fff]", "", output.lower())
    if not ans_norm or len(ans_norm) < 4:
        return "unknown"
    keywords = [w for w in re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z_]{4,}", ans_norm) if len(w) >= 2]
    if not keywords:
        return "unknown"
    hit = sum(1 for w in keywords if w in out_norm)
    ratio = hit / len(keywords)
    if ratio >= 0.6:
        return "correct"
    if ratio >= 0.3:
        return "unknown"
    return "incorrect"


def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂题库自解引擎")
    ap.add_argument("--base", default=BASE, help="底模路径（支持 merged 完整模型）")
    ap.add_argument("--adapter", default=ADAPTER)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0, help="0=全部")
    ap.add_argument("--lang", default=None, help="只解某语言")
    ap.add_argument("--types", default=None, help="逗号分隔题型过滤，如 选择题,判断题")
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--temp", type=float, default=0.3)
    ap.add_argument("--out", default=None, help="输出JSON路径(默认self_solve_results.json)")
    args = ap.parse_args()

    all_q = json.loads((TIKU_DIR / "all_questions.json").read_text(encoding="utf-8"))
    if args.lang:
        all_q = [q for q in all_q if q["lang"] == args.lang]
    if args.types:
        types = {t.strip() for t in args.types.split(",") if t.strip()}
        all_q = [q for q in all_q if q["type"] in types]
    if args.limit:
        all_q = all_q[args.start:args.start + args.limit]
    else:
        all_q = all_q[args.start:]

    print(f"[{_now()}] 📦 加载模型: {args.base}")
    use_adapter = args.adapter and args.adapter != "none"
    print(f"[{_now()}] 🔌 加载 adapter: {args.adapter if use_adapter else '(无·merged完整模型)'}")
    print(f"[{_now()}] 🎯 待解题目: {len(all_q)}")
    model, tokenizer = load(
        args.base,
        adapter_path=args.adapter if use_adapter else None,
        tokenizer_config={"trust_remote_code": True},
    )

    results = []
    correct = incorrect = unknown = 0
    t_total = time.time()

    for i, q in enumerate(all_q, 1):
        prompt = build_prompt(q)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False,
                                                    add_generation_prompt=True)
        t0 = time.time()
        try:
            output = generate(
                model, tokenizer, prompt=prompt_text,
                max_tokens=args.max_tokens,
                sampler=make_sampler(args.temp),
                verbose=False,
            )
        except Exception as e:
            output = f"[ERROR] {e}"
        elapsed = time.time() - t0

        verdict = check_answer(q, output)
        if verdict == "correct":
            correct += 1
        elif verdict == "incorrect":
            incorrect += 1
        else:
            unknown += 1

        results.append({
            "lang": q["lang"],
            "num": q["num"],
            "type": q["type"],
            "stars": q["stars"],
            "question": q["text"],
            "options": q["options"],
            "std_answer": q["answer"],
            "std_reference": q["reference"],
            "model_output": output,
            "verdict": verdict,
            "elapsed": round(elapsed, 1),
        })

        if i % 20 == 0 or i == len(all_q):
            eta = (time.time() - t_total) / i * (len(all_q) - i) / 60
            print(f"[{_now()}] ⏳ [{i}/{len(all_q)}] 对/错/未知="
                  f"{correct}/{incorrect}/{unknown} | 剩余≈{eta:.0f}分钟")

    elapsed_total = time.time() - t_total
    out_path = TIKU_DIR / (args.out or "self_solve_results.json")
    out_path.write_text(json.dumps({
        "dna": f"#龍芯⚡️{_now()}-TIKU-SELF-SOLVE",
        "adapter": args.adapter,
        "total": len(all_q),
        "correct": correct,
        "incorrect": incorrect,
        "unknown": unknown,
        "accuracy": round(correct / max(len(all_q), 1) * 100, 1),
        "elapsed_min": round(elapsed_total / 60, 1),
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[{_now()}] ✅ 自解完成: {len(all_q)} 题 | "
          f"对 {correct} / 错 {incorrect} / 待核 {unknown}")
    print(f"[{_now()}] 🎯 自动判定正确率: {correct}/{len(all_q)} "
          f"({round(correct / max(len(all_q), 1) * 100, 1)}%)")
    print(f"[{_now()}] 💾 结果已保存: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
