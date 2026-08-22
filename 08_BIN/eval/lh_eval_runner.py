#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·癸亥·午时·☰乾-EVAL-RUNNER-v1.0
"""
🐉 龍魂 · 评测执行引擎 v1.0

对测试池中的每道题，让模型用三种不同方式解答：
  1. 白话解释（让老百姓听懂）
  2. 逻辑推导（给工程师/学生）
  3. 代码/示例（给实践者）

输出每题的三色审计 + 总体三色审计报告。
"""

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List


HOME = Path.home()
EVAL_DIR = HOME / ".longhun" / "eval"
SUITES_DIR = EVAL_DIR / "suites"
RESULTS_DIR = EVAL_DIR / "results"
INDEX_FILE = EVAL_DIR / "index.json"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def _dna(suffix: str = "RUN") -> str:
    h = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{suffix}-{h}-UID9622"


def _guard(text: str) -> str:
    return text.replace("龙", "龍")


PROMPT_TEMPLATE = """你是龍魂系统的多维度解题助手。下面这道题，请用三种不同方式回答，让不同背景的人都能听懂。

题目：{question}

要求：
1. 【方式一·白话解释】用老百姓能听懂的大白话解释思路和答案。
2. 【方式二·逻辑推导】用步骤化的数学/逻辑推理给出严谨解答。
3. 【方式三·代码或示例】用 Python 代码或具体例子演示求解过程（如不适合代码，可用表格/公式）。

请直接输出三个部分，每个部分以"【方式X·...】"开头。"""


SECTION_PATTERNS = [
    ("白话解释", r"【方式一[·.]白话解释】([\s\S]*?)(?=【方式二|$)"),
    ("逻辑推导", r"【方式二[·.]逻辑推导】([\s\S]*?)(?=【方式三|$)"),
    ("代码示例", r"【方式三[·.]代码或示例】([\s\S]*?)(?=【|$)"),
]


def load_model_once(model_path: str, adapter_path: str = None):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📦 加载模型: {model_path}")
    if adapter_path:
        print(f"  🔌 使用 adapter: {adapter_path}")
    from mlx_lm import load
    model, tokenizer = load(model_path, tokenizer_config={"trust_remote_code": True}, adapter_path=adapter_path)
    return model, tokenizer


def generate_answer(model, tokenizer, question: str, max_tokens: int = 600) -> str:
    from mlx_lm import generate
    from mlx_lm.sample_utils import make_sampler
    prompt = _guard(PROMPT_TEMPLATE.format(question=question))
    messages = [{"role": "user", "content": prompt}]
    # Qwen instruct 需要 apply chat template
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        full_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        full_prompt = prompt
    sampler = make_sampler(temp=0.0)
    response = generate(model, tokenizer, prompt=full_prompt, sampler=sampler, max_tokens=max_tokens, verbose=False)
    return _guard(response.strip())


def parse_solutions(response: str) -> Dict[str, str]:
    solutions = {}
    for name, pattern in SECTION_PATTERNS:
        m = re.search(pattern, response)
        solutions[name] = m.group(1).strip() if m else ""
    return solutions


def extract_ground_truth(expected: str) -> List[str]:
    """从期望答案中提取可匹配的 ground truth 候选。"""
    candidates = []
    if not expected:
        return candidates
    # GSM8K 风格: #### 30
    if "####" in expected:
        final = expected.split("####")[-1].strip()
        candidates.append(final)
        # 提取数字
        nums = re.findall(r"-?\d+(?:\.\d+)?", final)
        candidates.extend(nums)
    else:
        candidates.append(expected.strip())
        nums = re.findall(r"-?\d+(?:\.\d+)?", expected)
        candidates.extend(nums)
    # 去重并保持顺序
    seen = set()
    out = []
    for c in candidates:
        c = c.strip()
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def score_solution(solution: str, ground_truths: List[str]) -> float:
    if not solution or not ground_truths:
        return 0.0
    sol = solution.strip()
    # 1) 完整 ground truth 出现在答案中
    for gt in ground_truths:
        if gt in sol:
            return 1.0
    # 2) 数字匹配（忽略单位/格式）
    sol_nums = set(re.findall(r"-?\d+(?:\.\d+)?", sol))
    gt_nums = set(ground_truths)
    if sol_nums & gt_nums:
        return 1.0
    # 3) 关键词匹配兜底
    keywords = [gt for gt in ground_truths if len(gt) >= 2]
    if keywords:
        hits = sum(1 for kw in keywords if kw.lower() in sol.lower())
        return hits / len(keywords)
    return 0.0


def tricolor(score: float, present: bool) -> str:
    if not present or score == 0.0:
        return "🔴 失败"
    if score >= 0.99:
        return "🟢 通过"
    return "🟡 待确认"


def evaluate_question(model, tokenizer, item: Dict, max_tokens: int) -> Dict:
    question = item.get("question", "")
    expected = item.get("expected", "")
    ground_truths = extract_ground_truth(expected)

    response = generate_answer(model, tokenizer, question, max_tokens=max_tokens)
    solutions = parse_solutions(response)

    section_scores = {}
    section_colors = {}
    for name, text in solutions.items():
        score = score_solution(text, ground_truths)
        section_scores[name] = round(score, 2)
        section_colors[name] = tricolor(score, bool(text))

    # 总体三色：只要任一方式通过即绿；都没有正确答案但部分相关则黄；全错则红
    if any(c.startswith("🟢") for c in section_colors.values()):
        overall = "🟢 通过"
    elif any(c.startswith("🟡") for c in section_colors.values()):
        overall = "🟡 待确认"
    else:
        overall = "🔴 失败"

    return {
        "id": item.get("id", ""),
        "question": question,
        "expected": expected,
        "ground_truths": ground_truths,
        "response": response,
        "solutions": solutions,
        "section_scores": section_scores,
        "section_colors": section_colors,
        "overall_color": overall,
        "passed": overall.startswith("🟢"),
        "dna": _dna("Q"),
    }


def run_eval(model_path: str, adapter_path: str = None, limit: int = 3, max_tokens: int = 600) -> Dict:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始多维度评测...")
    if not INDEX_FILE.exists():
        print("  ❌ 测试池索引不存在，请先运行: python3 08_BIN/eval/lh_eval_puller.py")
        sys.exit(1)

    index = json.load(open(INDEX_FILE, encoding="utf-8"))
    suites = index.get("suites", [])[:limit]
    print(f"  载入 {len(suites)} 道题目（limit={limit}）")

    model, tokenizer = load_model_once(model_path, adapter_path)

    results = []
    for i, item in enumerate(suites, 1):
        print(f"\n  [{i}/{len(suites)}] {item.get('question','')[:50]}...")
        res = evaluate_question(model, tokenizer, item, max_tokens=max_tokens)
        results.append(res)
        print(f"      总体: {res['overall_color']}")
        for name, color in res["section_colors"].items():
            print(f"      {name}: {color} ({res['section_scores'][name]})")

    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed
    yellow = sum(1 for r in results if r["overall_color"].startswith("🟡"))

    report = {
        "dna": _dna("REPORT"),
        "timestamp": datetime.now().isoformat(),
        "model": model_path,
        "adapter": adapter_path,
        "total": len(results),
        "passed": passed,
        "yellow": yellow,
        "failed": failed,
        "pass_rate": round(passed / len(results) * 100, 2) if results else 0,
        "三色审计": {
            "🟢 通过": passed,
            "🟡 待确认": yellow,
            "🔴 失败": failed,
        },
        "总体结论": "🟢 通过" if failed == 0 and yellow == 0 else ("🔴 失败" if failed > 0 else "🟡 待确认"),
        "results": results,
    }

    result_file = RESULTS_DIR / f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 写入史官
    audit_file = HOME / ".longhun" / "04_AUDIT" / "eval.jsonl"
    audit_file.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "dna": report["dna"],
            "total": report["total"],
            "pass_rate": report["pass_rate"],
            "三色审计": report["三色审计"],
        }, ensure_ascii=False) + "\n")

    return report


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 多维度评测执行引擎")
    parser.add_argument("--model", default="models/qwen-1.5b-instruct-4bit", help="模型路径")
    parser.add_argument("--adapter", default=None, help="LoRA adapter 路径（可选）")
    parser.add_argument("--limit", type=int, default=3, help="评测题目数量上限")
    parser.add_argument("--max-tokens", type=int, default=600, help="每题最大生成 token 数")
    args = parser.parse_args()

    report = run_eval(args.model, args.adapter, args.limit, args.max_tokens)

    print("\n" + "=" * 60)
    print("🐉 龍魂 · 多维度评测报告")
    print("=" * 60)
    print(f"  题目数: {report['total']}")
    print(f"  通过率: {report['pass_rate']}%")
    print(f"  三色审计: {report['三色审计']}")
    print(f"  总体结论: {report['总体结论']}")
    print(f"  报告文件: {RESULTS_DIR}/eval_*.json")
    print(f"  DNA: {report['dna']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
