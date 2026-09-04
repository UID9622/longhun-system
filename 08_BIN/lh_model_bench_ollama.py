#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_MODEL_BENCH_OLLAM-F7D32F51
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·癸酉·午时·䷒临-MODEL-BENCH-OLLAMA-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CREATOR: 诸葛鑫 (UID9622)
"""
🐉 龍魂 · 统一考场 v1.0（Ollama API 版）

对 ollama 模型跑 309 道选择题统一基准，判定逻辑与 lh_tiku_self_solve.py 完全一致
（保证与历史 64.4% 成绩可比），通过 HTTP API 调用，支持批量多模型。

用法:
  python3 bin/lh_model_bench_ollama.py --model longhun-v4.1.1-bind:latest --limit 30 --out logs/bench_v411bind_30.json
  python3 bin/lh_model_bench_ollama.py --models "longhun-v4.1.4:latest,longhun-v4.1.1-bind:latest" --limit 30 --out logs/bench_smoke.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TIKU_DIR = PROJECT_ROOT / "models" / "longhun-small-instruct-v1.3" / "tiku"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = (
    "你是龍魂解题引擎。用户给你一道编程/计算机笔试题，你需要：\n"
    "1. 先给出你的答案（选择题给选项字母+内容；判断题给 正确/错误；简答和编程题给完整解答）\n"
    "2. 再给出简要的推理过程。\n"
    "回答要准确、简洁、直接。"
)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _dna(suffix: str = "BENCH") -> str:
    return f"#龍芯⚡️{_now()}-{suffix}"


def ollama_generate(model: str, prompt: str, max_tokens: int = 200, temp: float = 0.3,
                    timeout: int = 180) -> tuple[str, float]:
    """调用 ollama /api/generate，返回 (输出文本, 耗时秒)。"""
    payload = json.dumps({
        "model": model,
        "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": temp,
            "num_predict": max_tokens,
        },
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return data.get("response", ""), time.time() - t0
    except Exception as e:
        return f"[ERROR] {e}", time.time() - t0


def build_prompt(q: dict) -> str:
    lines = [f"【题目】{q['text']}"]
    if q.get("options"):
        for opt in q["options"]:
            lines.append(f"{opt['key']}. {opt['text']}")
    lines.append("请作答：")
    return "\n".join(lines)


def check_answer(q: dict, output: str) -> str:
    """与 lh_tiku_self_solve.py 完全一致的自动判定。"""
    ans = (q.get("answer") or q.get("reference") or "").strip()
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


def run_model(model: str, questions: list, max_tokens: int, temp: float,
              out_path: Path, resume: bool = True) -> dict:
    """对单个模型跑完整题集，输出 JSON。"""
    print(f"[{_now()}] ▶ 开始评估: {model} | 题数 {len(questions)}")

    results: list = []
    loaded = {}
    if resume and out_path.exists():
        try:
            prev = json.loads(out_path.read_text(encoding="utf-8"))
            results = prev.get("results", [])
            loaded = {f"{r['lang']}-{r['num']}" for r in results}
            print(f"[{_now()}] ↩ 已存在 {len(loaded)} 条结果，断点续跑")
        except Exception:
            loaded = set()

    correct = incorrect = unknown = 0
    for r in results:
        if r["verdict"] == "correct":
            correct += 1
        elif r["verdict"] == "incorrect":
            incorrect += 1
        else:
            unknown += 1

    t_total = time.time()
    todo = [q for q in questions if f"{q['lang']}-{q['num']}" not in loaded]
    for i, q in enumerate(todo, 1):
        prompt = build_prompt(q)
        output, elapsed = ollama_generate(model, prompt, max_tokens=max_tokens, temp=temp)
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
            "options": q.get("options", []),
            "std_answer": q.get("answer", ""),
            "std_reference": q.get("reference", ""),
            "model_output": output[:500],
            "verdict": verdict,
            "elapsed": round(elapsed, 1),
        })
        if i % 20 == 0 or i == len(todo):
            done = len(results)
            eta = (time.time() - t_total) / done * (len(questions) - done) / 60
            print(f"[{_now()}] ⏳ [{done}/{len(questions)}] 对/错/未知="
                  f"{correct}/{incorrect}/{unknown} | 剩余≈{eta:.0f}分钟")

        # 每 20 题落盘一次（防中断丢进度）
        if i % 20 == 0:
            _save(out_path, model, questions, correct, incorrect, unknown, results, 0)

    elapsed_total = time.time() - t_total
    _save(out_path, model, questions, correct, incorrect, unknown, results, elapsed_total)

    print(f"[{_now()}] ✅ {model} 完成: {len(questions)} 题 | "
          f"对 {correct} / 错 {incorrect} / 待核 {unknown} | "
          f"正确率 {round(correct / max(len(questions), 1) * 100, 1)}% | 耗时 {round(elapsed_total/60, 1)} 分钟")
    return {"model": model, "correct": correct, "incorrect": incorrect,
            "unknown": unknown, "total": len(questions),
            "accuracy": round(correct / max(len(questions), 1) * 100, 1)}


def _save(out_path: Path, model: str, questions: list, correct: int, incorrect: int,
          unknown: int, results: list, elapsed_total: float) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "dna": _dna("BENCH"),
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "total": len(questions),
        "correct": correct,
        "incorrect": incorrect,
        "unknown": unknown,
        "accuracy": round(correct / max(len(questions), 1) * 100, 1),
        "elapsed_min": round(elapsed_total / 60, 1),
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def load_choice_questions() -> list:
    """从 all_questions.json 抽取全部选择题（历史 309 道基准）。"""
    all_q = json.loads((TIKU_DIR / "all_questions.json").read_text(encoding="utf-8"))
    choices = [q for q in all_q if q.get("type") == "选择题"]
    return choices


def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂统一考场 v1.0（Ollama API）")
    ap.add_argument("--model", default=None, help="单个模型名")
    ap.add_argument("--models", default=None, help="逗号分隔多个模型名")
    ap.add_argument("--limit", type=int, default=0, help="每题集限制数（0=全部，冒烟用 30）")
    ap.add_argument("--out", default=None, help="输出JSON路径（多模型时作为前缀）")
    ap.add_argument("--max-tokens", type=int, default=200)
    ap.add_argument("--temp", type=float, default=0.3)
    ap.add_argument("--list-models", action="store_true", help="列出 ollama 模型")
    args = ap.parse_args()

    if args.list_models:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        for m in data.get("models", []):
            print(m["name"], f"{m.get('size',0)/1e9:.1f}GB")
        return 0

    models = []
    if args.models:
        models = [m.strip() for m in args.models.split(",") if m.strip()]
    elif args.model:
        models = [args.model]
    else:
        print("❌ 必须指定 --model 或 --models")
        return 1

    # 健康检查
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
    except Exception:
        print("❌ Ollama 未运行，请先启动: ollama serve")
        return 1

    questions = load_choice_questions()
    if args.limit:
        questions = questions[:args.limit]
    print(f"[{_now()}] 🎯 选择题基准: {len(questions)} 道 | 模型: {models}")

    report = {}
    for m in models:
        if args.out:
            # --out 作为前缀拼接模型名，避免多模型互相覆盖
            out_path = Path(f"{args.out}{m.replace(':', '_').replace('.', '_')}.json")
        else:
            out_path = Path(f"logs/bench_{m.replace(':', '_').replace('.', '_')}.json")
        res = run_model(m, questions, args.max_tokens, args.temp, out_path)
        report[m] = res
        # 模型间冷却 3 秒，释放显存
        time.sleep(3)

    print("\n" + "=" * 60)
    print("🏆 统一考场成绩单")
    print("=" * 60)
    for m, r in sorted(report.items(), key=lambda kv: -kv[1]["accuracy"]):
        print(f"  {m}: {r['accuracy']}% ({r['correct']}/{r['total']}) "
              f"错{r['incorrect']} 待核{r['unknown']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
