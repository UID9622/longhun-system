#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_CLEAN_TRAINING_DA-46F208B1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-TRAIN-DATA-CLEANER-v1.0
"""
🐉 龍魂 · 训练数据清洗器 v1.0

清洗规则：
  1. 输出长度 150 ~ 1500 字之间
  2. 每条样本按来源去重（输出 MD5）
  3. 每个来源最多保留 100 条，避免单一来源垄断
  4. 长段落按自然段落再切分，减少截断
  5. 过滤含大量代码/表格/无意义列表的样本
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
    """简体龙 → 繁体龍。"""
    return text.replace("龙", "龍")


def is_low_quality(text: str) -> bool:
    """判断是否为低质量内容。"""
    if not text or len(text) < 150:
        return True
    # 太多代码符号
    code_chars = text.count("```") + text.count("|") + text.count("---")
    if code_chars > 15:
        return True
    # 太多连续数字编号，像列表
    if len(re.findall(r"^\d+\.", text, re.M)) > 20:
        return True
    # 重复段落过多
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) > 3:
        uniq = set(hashlib.md5(p.encode()).hexdigest()[:16] for p in paragraphs)
        if len(uniq) / len(paragraphs) < 0.5:
            return True
    return False


def split_paragraphs(text: str, max_chars: int = 1200, min_chars: int = 150) -> list:
    """按自然段落切分长文本。"""
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
    """把一个样本清洗成 0 或多个高质量样本。"""
    messages = obj.get("messages", [])
    if len(messages) < 3:
        return []
    output = guard_text(messages[2].get("content", ""))
    source = obj.get("source", "unknown")

    if is_low_quality(output):
        return []

    # 如果输出过长，切分
    if len(output) > 1500:
        chunks = split_paragraphs(output)
        results = []
        for chunk in chunks:
            if is_low_quality(chunk):
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

    prompt = random.choice(PROMPT_TEMPLATES).format(content=output[:500])
    return [{
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": output},
        ],
        "source": source,
        "dna": obj.get("dna", ""),
    }]


def clean_file(in_path: Path, out_path: Path, max_per_source: int = 100) -> dict:
    """清洗单个 jsonl 文件。"""
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
                # 去重
                h = hashlib.md5(new_obj["messages"][2]["content"].encode()).hexdigest()
                if h in seen_hashes:
                    dropped += 1
                    continue
                # 限制来源数量
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
    parser = argparse.ArgumentParser(description="龍魂 · 训练数据清洗")
    parser.add_argument("--input-dir", default="docs/notion_full_export/data", help="输入目录")
    parser.add_argument("--output-dir", default="docs/notion_full_export/data_clean", help="输出目录")
    parser.add_argument("--max-per-source", type=int, default=100, help="每个来源最大样本数")
    parser.add_argument("--seed", type=int, default=9622, help="随机种子")
    args = parser.parse_args()

    random.seed(args.seed)
    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{_now()}] 🧹 开始清洗训练数据...")
    train_stat = clean_file(in_dir / "train.jsonl", out_dir / "train.jsonl", args.max_per_source)
    valid_stat = clean_file(in_dir / "valid.jsonl", out_dir / "valid.jsonl", args.max_per_source)

    print(f"[{_now()}] ✅ 训练集: {train_stat['kept']} 条保留, {train_stat['dropped']} 条去重, 来源数 {train_stat['sources']}")
    print(f"[{_now()}] ✅ 验证集: {valid_stat['kept']} 条保留, {valid_stat['dropped']} 条去重, 来源数 {valid_stat['sources']}")
    print(f"[{_now()}]    输出: {out_dir}")


if __name__ == "__main__":
    main()
