#!/usr/bin/env python3
#龍芯⚡️2026-07-19-DESKTOP-ARTICLES-INGEST-v4.0.7
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 桌面文章全量摄入脚本 v4.0.7
扫描 ~/Desktop 全部 .md/.txt 文章，生成训练样本。
冲突检测：与焊死协议比对，输出冲突报告。
DNA: #龍芯⚡️2026-07-19-DESKTOP-ARTICLES-INGEST-v4.0.7
"""

import json
import os
import re
import random
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "desktop_ingested_data_v407"
OUT.mkdir(parents=True, exist_ok=True)

DESKTOP = Path.home() / "Desktop"
LONGHUN_ROOT = PROJECT.resolve()

# 排除项
SKIP_NAMES = {".DS_Store", ".localized", "credentials.csv", "SecretKey.csv"}
SKIP_PATTERNS = [
    r".*apiKey.*\.csv$",
    r".*credentials.*$",
    r".*SecretKey.*$",
    r".*身份证.*$",
]
SKIP_DIRS = {"身份证_已压缩"}

# 焊死协议关键词（用于冲突检测）
WELDED_CORE = {
    "家法第一条": [
        "文化卖国罪", "文化数据", "境外", "非中国主权", "熔断", "黑名单", "耻辱柱",
        "数据主权", "国家文化安全"
    ],
    "零号协议": ["世界老百姓最高", "不可覆盖", "不可弱化", "不可篡改", "不可资本收割"],
    "数据主权": ["本地优先", "不出境", "不上云", "数据根留中国"],
    "只冻结不删除": ["不删除", "只冻结", "不灭证"],
    "底座焊死": ["369不动点", "河图洛书", "易经", "CNSH-L0", "非Qwen", "拔掉马云"],
    "人民原声": ["不阉割", "人民原声", "不替人闭嘴"],
    "DNA追溯": ["DNA追溯码", "来源可查", "去向可追", "责任可究"],
}


def should_skip(path: Path) -> bool:
    if path.name in SKIP_NAMES:
        return True
    try:
        if path.stat().st_size > 2_000_000:  # >2MB 跳过
            return True
    except (FileNotFoundError, OSError):
        return True  # 坏符号链接或不可读
    if path.is_symlink():
        try:
            target = path.resolve()
            if str(target).startswith(str(LONGHUN_ROOT)):
                return True  # 已纳入 longhun-system 的符号链接
        except Exception:
            return True
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    for pat in SKIP_PATTERNS:
        if re.match(pat, path.name, re.I):
            return True
    return False


def clean_text(text: str) -> str:
    # 移除 markdown 图片/链接占位
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # 合并多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_title(path: Path, content: str) -> str:
    # 从文件名或首行 # 标题提取
    title = path.stem
    m = re.search(r"^#+\s*(.+)$", content, re.M)
    if m:
        title = m.group(1).strip()
    return title[:120]


def chunk_text(text: str, max_chars: int = 1500, overlap: int = 200) -> list:
    """按段落分块，保持语义完整。"""
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) > max_chars and current:
            chunks.append(current.strip())
            current = current[-overlap:] if len(current) > overlap else ""
        current += "\n\n" + p if current else p
    if current:
        chunks.append(current.strip())
    return chunks if chunks else [text[:max_chars]]


def make_sample(system: str, user: str, assistant: str, metadata: dict) -> dict:
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": metadata,
    }


def detect_conflicts(content: str, source: str) -> list:
    """轻量冲突检测：识别与焊死核心可能矛盾的表述。"""
    conflicts = []
    lower = content.lower()
    # 检测家法第一条被弱化/改写
    if "家法第一条" in content:
        if not any(k in lower for k in WELDED_CORE["家法第一条"]):
            conflicts.append(("家法第一条", "提及家法第一条但缺核心关键词（文化主权/境外/熔断）", source))
    # 检测删除/阉割人民声音
    if re.search(r"删除.{0,10}声音|阉割.{0,10}原声|替人.{0,5}闭嘴", content):
        conflicts.append(("人民原声", "出现删除/阉割/闭嘴人民声音的表述", source))
    # 检测数据可出境
    if re.search(r"数据.{0,10}出境|上传.{0,10}云端|同步.{0,10}iCloud", content):
        conflicts.append(("数据主权", "出现数据出境/上云表述", source))
    # 检测底座为Qwen/阿里
    if re.search(r"底座.{0,20}Qwen|底座.{0,20}通义千问|基于.{0,20}Qwen|马云", content):
        conflicts.append(("底座焊死", "出现底座=Qwen/阿里的表述", source))
    return conflicts


def generate_samples(path: Path, content: str) -> list:
    title = extract_title(path, content)
    system = (
        "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。"
        "你正在学习桌面知识库中的文章，回答需忠于原文，不编造。"
    )
    rel_path = str(path.relative_to(DESKTOP))
    meta_base = {"source": "desktop", "file": rel_path, "title": title}

    samples = []

    # 1. 全文概要样本
    summary = content[:800].strip()
    if len(content) > 800:
        summary = summary[:summary.rfind("\n")] if "\n" in summary else summary
    samples.append(make_sample(
        system,
        f"请概括文章《{title}》的核心内容。",
        summary,
        {**meta_base, "type": "summary"},
    ))

    # 2. 按块生成 QA
    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks[:8]):  # 每篇文章最多8块，防过载
        # 块概括
        samples.append(make_sample(
            system,
            f"文章《{title}》第{i+1}部分讲了什么？",
            chunk[:1000],
            {**meta_base, "type": f"chunk_{i+1}"},
        ))
        # 提取关键句做问答
        sentences = re.split(r"(?<=[。！？])", chunk)
        for s in sentences[:2]:
            s = s.strip()
            if len(s) >= 20 and len(s) <= 200:
                samples.append(make_sample(
                    system,
                    f"根据文章《{title}》，解释这句话：{s}",
                    s,
                    {**meta_base, "type": "quote"},
                ))

    # 3. 标题→内容映射（用于检索式问答）
    samples.append(make_sample(
        system,
        f"请引用文章《{title}》的原文要点。",
        content[:1200],
        {**meta_base, "type": "raw_excerpt"},
    ))

    return samples


def main():
    print("=" * 60)
    print("🐉 桌面文章全量摄入 v4.0.7")
    print("=" * 60)

    files = []
    for root, dirs, files_list in os.walk(DESKTOP):
        # 跳过敏感目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files_list:
            path = Path(root) / f
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            if should_skip(path):
                continue
            files.append(path)

    print(f"📁 发现可摄入文件: {len(files)} 个")

    all_samples = []
    all_conflicts = []
    skipped = []
    domain_counter = Counter()

    random.seed(42)
    # 限制单文件处理数，避免过大
    for idx, path in enumerate(files, 1):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            skipped.append((str(path), f"read_error: {e}"))
            continue

        if len(content.strip()) < 50:
            skipped.append((str(path), "too_short"))
            continue

        content = clean_text(content)
        rel_dir = path.parent.relative_to(DESKTOP)
        domain = str(rel_dir).split(os.sep)[0] if str(rel_dir) != "." else "root"
        domain_counter[domain] += 1

        conflicts = detect_conflicts(content, str(path.relative_to(DESKTOP)))
        all_conflicts.extend(conflicts)

        samples = generate_samples(path, content)
        all_samples.extend(samples)

        if idx % 200 == 0:
            print(f"   已处理 {idx}/{len(files)}，样本 {len(all_samples)}")

    print(f"\n✅ 生成样本: {len(all_samples)}")
    print(f"⚠️  跳过文件: {len(skipped)}")
    print(f"🔥 冲突项: {len(all_conflicts)}")
    print(f"📊 域分布: {dict(domain_counter.most_common(10))}")

    # 划分训练/验证
    random.shuffle(all_samples)
    split = int(len(all_samples) * 0.95)
    train, val = all_samples[:split], all_samples[split:]

    with open(OUT / "train.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUT / "valid.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # 冲突报告
    conflict_report = {
        "scan_time": "2026-07-19",
        "files_scanned": len(files),
        "samples_generated": len(all_samples),
        "conflicts_count": len(all_conflicts),
        "conflicts": [{"domain": d, "issue": i, "source": s} for d, i, s in all_conflicts],
        "skipped": skipped[:50],
        "domains": dict(domain_counter.most_common(20)),
    }
    with open(OUT / "ingest_report.json", "w", encoding="utf-8") as f:
        json.dump(conflict_report, f, ensure_ascii=False, indent=2)

    print(f"\n💾 输出目录: {OUT}")
    print(f"   train: {len(train)} | valid: {len(val)}")


if __name__ == "__main__":
    main()
