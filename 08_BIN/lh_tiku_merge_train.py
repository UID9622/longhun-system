#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-TIKU-MERGE-TRAIN-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 题库自解结果合并训练引擎 v1.0

功能:
  1. 读取模型自解结果 JSON（默认 self_solve_choice.json）
  2. 过滤 verdict=correct 的样本（答错/待核一律丢弃，防止教错模型）
  3. 模型输出过龍字守卫（简体「龙」→ 繁体「龍」，跳过 URL/代码上下文）
  4. 组装训练格式 messages（system=龍魂解题引擎 / user=题目+选项 / assistant=模型解题过程）
  5. 按题目文本去重，合并追加到训练源 train.jsonl（source_data_dir，避免被 prepare_data 覆盖）

用法:
  python3 08_BIN/lh_tiku_merge_train.py [--solve-json PATH] [--train-jsonl PATH] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TIKU_DIR = PROJECT_ROOT / "models" / "longhun-small-instruct-v1.3" / "tiku"
DEFAULT_SOLVE = TIKU_DIR / "self_solve_choice.json"
DEFAULT_TRAIN = PROJECT_ROOT / "docs" / "notion_full_export" / "data_light" / "train.jsonl"

SYSTEM_PROMPT = (
    "你是龍魂解题引擎。用户给你一道编程/计算机笔试题，你需要：\n"
    "1. 先给出你的答案（选择题给选项字母+内容；判断题给 正确/错误；简答和编程题给完整解答）\n"
    "2. 再给出简要的推理过程。\n"
    "回答要准确、简洁、直接。"
)

# 保护上下文（不改写的片段）
_SKIP_PATTERNS = [
    r"https?://\S+",
    r"\b[a-fA-F0-9]{6,}\b",
    r"`[^`\n]+`",
    r":\w+:",
]


def dragon_guard(text: str) -> str:
    """简体「龙」→ 繁体「龍」。URL/代码/hex/emoji 短码等上下文保持原样。"""
    if not text:
        return text
    protects: list[str] = []

    def _hold(m: re.Match) -> str:
        protects.append(m.group(0))
        return f"\x00PH{len(protects) - 1}\x00"

    masked = text
    for pat in _SKIP_PATTERNS:
        masked = re.sub(pat, _hold, masked)
    masked = masked.replace("龙", "龍").replace("泷", "瀧")
    for i, p in enumerate(protects):
        masked = masked.replace(f"\x00PH{i}\x00", p)
    return masked


def build_user_prompt(q: dict) -> str:
    text = q.get("question") or q.get("text") or ""
    lines = [f"【题目】{text}"]
    if q.get("options"):
        for opt in q["options"]:
            lines.append(f"{opt['key']}. {opt['text']}")
    lines.append("请作答：")
    return "\n".join(lines)


def digest(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def load_solve(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_existing_train(path: Path) -> tuple[set[str], list[dict]]:
    """返回 (user内容hash集合, 已解析样本列表)。"""
    seen: set[str] = set()
    samples: list[dict] = []
    if not path.exists():
        return seen, samples
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        samples.append(obj)
        for msg in obj.get("messages", []):
            if msg.get("role") == "user":
                seen.add(digest(msg["content"]))
                break
    return seen, samples


def main() -> int:
    ap = argparse.ArgumentParser(description="🐉 龍魂 · 题库自解结果合并训练引擎")
    ap.add_argument("--solve-json", default=str(DEFAULT_SOLVE))
    ap.add_argument("--train-jsonl", default=str(DEFAULT_TRAIN))
    ap.add_argument("--dry-run", action="store_true", help="只统计不写入")
    args = ap.parse_args()

    solve_path = Path(args.solve_json)
    train_path = Path(args.train_jsonl)

    if not solve_path.exists():
        print(f"❌ 自解结果不存在: {solve_path}")
        return 1

    data = load_solve(solve_path)
    results = data.get("results", [])
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 📊 自解结果: 共 {len(results)} 题 | "
          f"对 {data.get('correct')} / 错 {data.get('incorrect')} / 待核 {data.get('unknown')}")

    corrects = [r for r in results if r.get("verdict") == "correct"]
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 🎯 答对样本: {len(corrects)} 题")

    if not corrects:
        print("⚠️ 没有答对样本可合并，直接结束。")
        return 0

    # 题型分布
    by_type: dict[str, int] = {}
    for r in corrects:
        by_type[r.get("type", "?")] = by_type.get(r.get("type", "?"), 0) + 1
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 题型分布: {by_type}")

    seen, existing = load_existing_train(train_path)
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 训练源现有: {len(existing)} 条")

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    added = 0
    skipped = 0
    new_lines: list[str] = []

    for r in corrects:
        user_prompt = build_user_prompt(r)
        h = digest(user_prompt)
        if h in seen:
            skipped += 1
            continue
        seen.add(h)
        assistant = dragon_guard(r.get("model_output", "")).strip()
        if not assistant or "[ERROR]" in assistant:
            skipped += 1
            continue
        sample = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": assistant},
            ],
            "source": f"tiku_self_solve_{r.get('lang', '?')}_{r.get('num', '?')}",
            "dna": f"#龍芯⚡️{date_str}-TIKU-SELF-SOLVE-CORRECT",
        }
        new_lines.append(json.dumps(sample, ensure_ascii=False))
        added += 1

    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ✅ 新样本 {added} 条 | 去重跳过 {skipped} 条")

    if args.dry_run:
        print(f"🔍 dry-run 模式，未写入。预计追加 {added} 条 → {train_path}")
        return 0

    if added == 0:
        print("ℹ️ 无新增样本，训练源不变。")
        return 0

    with open(train_path, "a", encoding="utf-8") as f:
        for line in new_lines:
            f.write(line + "\n")

    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 💾 已追加 {added} 条 → {train_path}")
    print(f"   训练源现在: {len(existing) + added} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
