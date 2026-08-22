#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_CLEAN_TRAINING_DA-A134C8AC
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-TRAIN-DATA-CLEANER-LIGHT-v1.0
"""
🐉 龍魂 · 训练数据轻量清洗器 v1.0

轻量规则（保留更多信息）：
  1. 输出长度 50 ~ 2000 字之间
  2. 按输出内容 MD5 去重
  3. 每个来源最多保留 200 条，避免单一来源垄断
  4. 超长段落按自然段落切分
"""

import argparse
import hashlib
import json
import random
import re
from datetime import datetime
from pathlib import Path


SYSTEM_PROMPT = (
    "你是龍魂系统助手，核心原则：人民数据主权、平台服务降级、"
    "创作者主权优先。回答需符合龍魂君子协议、CNSH 语义规范和 DNA 追溯要求。"
)

PROMPT_TEMPLATES = [
    "请总结并解释以下内容：\n\n{content}",
    "根据龍魂体系，阐述这段内容：\n\n{content}",
    "下面这段内容在龍魂协议中意味着什么？\n\n{content}",
    "请提炼这段龍魂资料的要点：\n\n{content}",
]


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def guard_text(text: str) -> str:
    return text.replace("龙", "龍")


def split_paragraphs(text: str, max_chars: int = 1800, min_chars: int = 80) -> list:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 2 > max_chars and len(current) >= min_chars:
            chunks.append(current)
            current = p
        else:
            current = current + "\n\n" + p if current else p
    if current and len(current) >= min_chars:
        chunks.append(current)
    return chunks


def clean_sample(obj: dict) -> list:
    messages = obj.get("messages", [])
    if len(messages) < 3:
        return []
    output = guard_text(messages[2].get("content", ""))
    source = obj.get("source", "unknown")

    if not output or len(output) < 50:
        return []

    chunks = []
    if len(output) > 2000:
        chunks = split_paragraphs(output)
    else:
        chunks = [output]

    results = []
    for chunk in chunks:
        if len(chunk) < 50:
            continue
        prompt = random.choice(PROMPT_TEMPLATES).format(content=chunk[:500])
        results.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": chunk},
            ],
            "source": source,
            "dna": obj.get("dna", ""),
        })
    return results


def clean_file(in_path: Path, out_path: Path, max_per_source: int = 200) -> dict:
    seen_hashes = set()
    source_counts = {}
    kept = 0
    dropped = 0
    source_dropped = 0

    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    with open(in_path, "r", encoding="utf-8") as fin, open(tmp_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            for new_obj in clean_sample(obj):
                source = new_obj["source"]
                h = hashlib.md5(new_obj["messages"][2]["content"].encode()).hexdigest()
                if h in seen_hashes:
                    dropped += 1
                    continue
                if source_counts.get(source, 0) >= max_per_source:
                    source_dropped += 1
                    continue
                seen_hashes.add(h)
                source_counts[source] = source_counts.get(source, 0) + 1
                fout.write(json.dumps(new_obj, ensure_ascii=False) + "\n")
                kept += 1

    tmp_path.replace(out_path)
    return {
        "input": str(in_path),
        "output": str(out_path),
        "kept": kept,
        "dropped": dropped,
        "source_capped": source_dropped,
        "sources": len(source_counts),
    }


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 训练数据轻量清洗")
    parser.add_argument("--input-dir", default="docs/notion_full_export/data", help="输入目录")
    parser.add_argument("--output-dir", default="docs/notion_full_export/data_light", help="输出目录")
    parser.add_argument("--max-per-source", type=int, default=200, help="每个来源最大样本数")
    parser.add_argument("--seed", type=int, default=9622, help="随机种子")
    args = parser.parse_args()

    random.seed(args.seed)
    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{_now()}] 🧹 开始轻量清洗训练数据...")
    train_stat = clean_file(in_dir / "train.jsonl", out_dir / "train.jsonl", args.max_per_source)
    valid_stat = clean_file(in_dir / "valid.jsonl", out_dir / "valid.jsonl", args.max_per_source)

    print(f"[{_now()}] ✅ 训练集: {train_stat['kept']} 条保留, {train_stat['dropped']} 条去重, 来源数 {train_stat['sources']}")
    print(f"[{_now()}] ✅ 验证集: {valid_stat['kept']} 条保留, {valid_stat['dropped']} 条去重, 来源数 {valid_stat['sources']}")
    print(f"[{_now()}]    输出: {out_dir}")


if __name__ == "__main__":
    main()
