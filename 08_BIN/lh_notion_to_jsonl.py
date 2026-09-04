#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_NOTION_TO_JSONL-9F32FFD3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-NOTION-TO-JSONL-v1.0
"""
🐉 龍魂 · Notion 导出 → 训练 jsonl 转换器 v1.0

把 docs/notion_full_export/ 下的 .md 页面和 .jsonl 数据库行
转换成 instruction 格式，供 mlx_lm LoRA 训练使用。
"""

import argparse
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
    "请总结以下内容的核心要点：\n\n{content}",
    "根据龍魂体系，解释这段内容：\n\n{content}",
    "把下面内容提炼成可执行的行动清单：\n\n{content}",
    "这段文字在龍魂协议中属于哪个层级？请说明：\n\n{content}",
    "用一句话概括：\n\n{content}",
]


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text: str) -> str:
    """清洗文本：去重空行、限制长度。"""
    text = text.replace("龙", "龍")
    # 压缩连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 1500) -> list:
    """把长文本切分成训练块。"""
    text = clean_text(text)
    if len(text) <= max_chars:
        return [text]
    chunks = []
    # 按段落切分
    paragraphs = text.split("\n\n")
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 2 > max_chars and current:
            chunks.append(current.strip())
            current = p
        else:
            current = current + "\n\n" + p if current else p
    if current:
        chunks.append(current.strip())
    return chunks


def to_chat_sample(system: str, user: str, assistant: str, source: str, dna: str) -> dict:
    """生成 mlx_lm 支持的 chat 格式样本。"""
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "source": source,
        "dna": dna,
    }


def md_to_samples(md_path: Path) -> list:
    """把 Markdown 文件转成 chat 样本。"""
    text = md_path.read_text(encoding="utf-8")
    chunks = chunk_text(text)
    samples = []
    for chunk in chunks:
        if len(chunk) < 50:
            continue
        prompt = random.choice(PROMPT_TEMPLATES).format(content=chunk[:800])
        samples.append(to_chat_sample(
            system=SYSTEM_PROMPT,
            user=prompt,
            assistant=chunk,
            source=str(md_path.name),
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-NOTION-MD-{md_path.stem}",
        ))
    return samples


def db_row_to_samples(row: dict, db_name: str) -> list:
    """把数据库行转成 chat 样本。"""
    properties = row.get("properties", {})
    texts = []
    for prop in properties.values():
        if prop.get("type") == "title":
            texts.append("".join(t.get("plain_text", "") for t in prop.get("title", [])))
        elif prop.get("type") == "rich_text":
            texts.append("".join(t.get("plain_text", "") for t in prop.get("rich_text", [])))
        elif prop.get("type") == "select":
            select = prop.get("select") or {}
            if isinstance(select, dict) and select.get("name"):
                texts.append(select["name"])
            elif isinstance(select, str):
                texts.append(select)
        elif prop.get("type") == "multi_select":
            for ms in prop.get("multi_select", []):
                if isinstance(ms, dict) and ms.get("name"):
                    texts.append(ms["name"])
                elif isinstance(ms, str):
                    texts.append(ms)
    content = " | ".join(t for t in texts if t).strip()
    if len(content) < 30:
        return []
    return [to_chat_sample(
        system=SYSTEM_PROMPT,
        user=f"请说明这条龍魂数据库记录的含义：\n\n{content[:600]}",
        assistant=content,
        source=db_name,
        dna=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-NOTION-DB-{row.get('id', 'X')}",
    )]


def main():
    parser = argparse.ArgumentParser(description="龍魂 · Notion 导出转训练 jsonl")
    parser.add_argument("--input", default="docs/notion_full_export", help="导出目录")
    parser.add_argument("--output", default="docs/notion_full_export/data", help="输出数据目录")
    parser.add_argument("--valid-ratio", type=float, default=0.05, help="验证集比例")
    parser.add_argument("--seed", type=int, default=9622, help="随机种子")
    args = parser.parse_args()

    random.seed(args.seed)
    in_root = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    samples = []

    # 1. 处理页面 Markdown
    pages_dir = in_root / "pages"
    if pages_dir.exists():
        md_files = sorted(pages_dir.glob("*.md"))
        print(f"[{_now()}] 📄 发现 {len(md_files)} 个 Markdown 页面")
        for md_path in md_files:
            samples.extend(md_to_samples(md_path))
    else:
        print(f"[{_now()}] ⚠️ 未找到 pages 目录")

    # 2. 处理数据库 JSONL
    dbs_dir = in_root / "databases"
    if dbs_dir.exists():
        jsonl_files = sorted(dbs_dir.glob("*.jsonl"))
        print(f"[{_now()}] 🗃️ 发现 {len(jsonl_files)} 个数据库文件")
        for jl_path in jsonl_files:
            with open(jl_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        row = json.loads(line)
                        samples.extend(db_row_to_samples(row, jl_path.name))
                    except json.JSONDecodeError:
                        continue
    else:
        print(f"[{_now()}] ⚠️ 未找到 databases 目录")

    if not samples:
        print(f"[{_now()}] ❌ 没有生成任何样本")
        return

    # 3. 打乱并拆分
    random.shuffle(samples)
    split_idx = max(1, int(len(samples) * (1 - args.valid_ratio)))
    train = samples[:split_idx]
    valid = samples[split_idx:] if split_idx < len(samples) else [samples[-1]]

    # 4. 保存
    train_path = out_dir / "train.jsonl"
    valid_path = out_dir / "valid.jsonl"
    with open(train_path, "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(valid_path, "w", encoding="utf-8") as f:
        for s in valid:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"[{_now()}] ✅ 生成训练样本: {len(train)} | 验证样本: {len(valid)}")
    print(f"[{_now()}]    {train_path}")
    print(f"[{_now()}]    {valid_path}")


if __name__ == "__main__":
    main()
