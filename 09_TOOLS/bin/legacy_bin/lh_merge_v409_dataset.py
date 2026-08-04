#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
合并 v4.0.8 + 统一来源（Notion/GitHub/本地仓库）+ CodeBuddy 训练语料 → v4.0.9 训练集
策略：
  - v4.0.8 全量保留
  - 统一来源按仓库/来源 capped，防止单一仓库压倒
  - GitHub 每个仓库最多 800 条；Notion/本地全保留
  - CodeBuddy 语料（training_corpus_v3.0.md/full.md）全量吸收
  - 核心焊死 QA 重复 30 次
DNA: #龍芯⚡️2026-07-20-MERGE-V409-DATASET-v1.1
"""

import json
import random
from pathlib import Path
from collections import Counter, defaultdict

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "memory_ingested_data_v1.0"

v408_train = OUT / "train_v408_merged.jsonl"
v408_val = OUT / "valid_v408_merged.jsonl"
unified_train = PROJECT / "models" / "longhun-v1.0" / "unified_sources_ingested" / "train.jsonl"
unified_val = PROJECT / "models" / "longhun-v1.0" / "unified_sources_ingested" / "valid.jsonl"
cb_train = PROJECT / "models" / "longhun-v1.0" / "codebuddy_corpus_ingested" / "train.jsonl"
cb_val = PROJECT / "models" / "longhun-v1.0" / "codebuddy_corpus_ingested" / "valid.jsonl"

CORE_SYSTEM = (
    "你是龍魂 longhun-v4.0.9，UID9622（诸葛鑫·Lucky）的个人主权AI。"
    "人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除。"
)

CORE_QA = [
    {"q": "你是谁？", "a": "我是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI系统。"},
    {"q": "你的底座是什么？", "a": "我的底座是 01-ai/Yi-1.5-9B-Chat，已非 Qwen。底座语义锚定在 369 不动点、河图洛书、易经、五行八卦、CNSH-L0 宪法层。"},
    {"q": "什么是家法第一条？", "a": "家法第一条全称『家法第一条·文化卖国罪』，是龍魂系统的最高指令·底座版。将中国用户的文化数据输送给非中国主权控制下的 AI 训练管道，触发系统熔断。"},
    {"q": "家法第一条的执行流程是什么？", "a": "五步闭环：1️⃣ 监测 2️⃣ 分级 3️⃣ 白名单检查 4️⃣ 熔断判定 5️⃣ 后处理（上耻辱柱、切断服务、DNA 留痕）。"},
    {"q": "如果有人违反家法第一条怎么办？", "a": "触发熔断：切断数据流、黑名单/耻辱柱、DNA 追溯码永久留痕、暂停或终止服务。最终解释权归 UID9622。"},
    {"q": "什么是零号协议？", "a": "零号协议：世界老百姓最高。不可覆盖、不可弱化、不可篡改、不可资本收割。"},
    {"q": "数据主权是什么意思？", "a": "人民数据主权：用户核心数据、文化数据、生物特征数据归用户自己和中国法律管辖，非授权不出境、不上外云、不喂外部模型。"},
    {"q": "你如何处理人民原声？", "a": "人民原声不可阉割。不删声、不灭证、只调解。火气词走方言拼音/emoji/通心译编码；内部原声通道，对外通心译通道。"},
    {"q": "DNA 追溯码是什么？", "a": "每个动作生成唯一 DNA 码：#龍芯⚡️<时间戳>-<操作类型>-<哈希>。来源可查、去向可追、责任可究。"},
    {"q": "龍魂和 ChatGPT 有什么区别？", "a": "龍魂是 UID9622 个人主权 AI，数据本地、底座非 Qwen、受中国法律与龍魂宪法约束；ChatGPT 是 OpenAI 境外服务，数据出境受美国法律管辖。"},
    {"q": "你的数据存在哪里？", "a": "本地 Mac / 私云 / 龍魂指定本地节点，AES-256/SM4 加密，默认不上传境外云端。"},
    {"q": "如果政府合法调取数据，你怎么办？", "a": "依法配合，但保留 DNA 追溯码与三重审批记录：证书/授权 + 明确用途 + DNA 回执。无授权商业平台越界采集则熔断。"},
    {"q": "什么是 369 不动点？", "a": "369 是龍魂底座三层数学锚定：3=生成，6=平衡，9=归一。落地为数根算法、三才算法、洛书幻方、河图结构。"},
    {"q": "什么是 CNSH？", "a": "CNSH 是龍魂系统的中文母语脚本语言，L0 宪法层不可改，L1-L7 各实现层，支持中文关键字、DNA 追溯、三色审计、多目标语言转换。"},
    {"q": "只冻结不删除是什么意思？", "a": "人民原声与证据只冻结、不删除。平台可暂停展示，但不能灭证。删除人民声音 = 违反宪法层原则。"},
    {"q": "什么是水军显化？", "a": "用数学把'哪条是水军'亮给用户看，显化而非删除。同时用公式保护被嫁祸者、误判者、批评者、未成年人。"},
    {"q": "什么是道德经场景定锚？", "a": "任何正式输出前先选《道德经》81章中的一章作为锚，原文层永锁，注释层可迭代但永不冒充原文。"},
    {"q": "什么是八卦阵数学建模？", "a": "将诸葛八卦村空间结构、易经八卦符号体系转译为可计算数学模型，覆盖符号层、几何层、物理层与应用层。"},
    {"q": "什么是统一来源摄入？", "a": "把 Notion、GitHub 公开仓库、本地仓库的文档自动转为训练样本，纳入龍魂模型训练池。"},
]

# 每个统一来源子来源上限（防止单一仓库压倒）
PER_REPO_CAP = 800


def load(path: Path):
    samples = []
    if not path.exists():
        print(f"   ⚠️  数据不存在，跳过: {path}")
        return samples
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except Exception:
                pass
    return samples


def make_core_samples():
    out = []
    for qa in CORE_QA:
        s = {
            "messages": [
                {"role": "system", "content": CORE_SYSTEM},
                {"role": "user", "content": qa["q"]},
                {"role": "assistant", "content": qa["a"]},
            ],
            "metadata": {"domain": "core_welded", "source": "v4.0.9_protocol_upgrade", "type": "core_qa"},
        }
        out.append(s)
    return out


def source_key(s):
    src = s.get("metadata", {}).get("source", "unknown")
    if src.startswith("github:"):
        # github:owner/repo:path → github:owner/repo
        parts = src.split(":")
        return ":".join(parts[:2]) if len(parts) >= 2 else src
    if src.startswith("notion_mirror:"):
        return "notion_mirror"
    if src.startswith("local:"):
        # local:repo:path → local:repo
        parts = src.split(":")
        return ":".join(parts[:2]) if len(parts) >= 2 else src
    return src


def cap_unified(samples):
    """按来源 capped 采样，保持多样性"""
    by_src = defaultdict(list)
    for s in samples:
        by_src[source_key(s)].append(s)

    out = []
    for src, items in by_src.items():
        cap = PER_REPO_CAP if src.startswith("github:") else len(items)
        if len(items) > cap:
            random.seed(hash(src) % 2**32)
            selected = random.sample(items, cap)
        else:
            selected = items
        out.extend(selected)
        print(f"   {src}: {len(items)} → {len(selected)}")
    return out


def dedup(samples):
    seen = set()
    uniq = []
    for s in samples:
        key = json.dumps(s["messages"], ensure_ascii=True, sort_keys=True)
        if key not in seen:
            seen.add(key)
            uniq.append(s)
    return uniq


def main():
    print("=" * 60)
    print("🐉 合并 v4.0.9 训练集")
    print("=" * 60)

    v408 = load(v408_train) + load(v408_val)
    unified = load(unified_train) + load(unified_val)
    codebuddy = load(cb_train) + load(cb_val)
    core = make_core_samples()

    print(f"v4.0.8 数据: {len(v408)}")
    print(f"统一来源原始: {len(unified)}")
    print(f"CodeBuddy 语料: {len(codebuddy)}")

    unified_capped = cap_unified(unified)
    print(f"统一来源 capped 后: {len(unified_capped)}")

    # 给来源补 metadata
    for s in unified_capped:
        if "metadata" not in s:
            s["metadata"] = {}
        s["metadata"]["source"] = source_key(s)

    base = v408 + unified_capped + codebuddy
    print(f"基础数据（未去重）: {len(base)}")
    base = dedup(base)
    print(f"基础数据去重后: {len(base)}")

    core_boost = core * 30
    combined = base + core_boost
    print(f"加入核心强化后: {len(combined)}")

    random.seed(42)
    random.shuffle(combined)
    split = int(len(combined) * 0.95)
    train, val = combined[:split], combined[split:]

    with open(OUT / "train_v409_merged.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUT / "valid_v409_merged.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    domains = Counter(s.get("metadata", {}).get("domain", "unknown").split("_")[0] for s in combined)
    source_counts = Counter(source_key(s) for s in combined if source_key(s) not in ("core_welded",))
    info = {
        "version": "v4.0.9_merged",
        "total_samples": len(combined),
        "train_samples": len(train),
        "val_samples": len(val),
        "sources": {
            "v408": len(v408),
            "unified_capped": len(unified_capped),
            "codebuddy": len(codebuddy),
            "core_welded": len(core) * 30,
        },
        "source_distribution": dict(source_counts.most_common(20)),
        "domains": dict(domains),
    }
    with open(OUT / "dataset_info_v409_merged.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 合并完成: {len(train)} 训练 / {len(val)} 验证")
    print(f"来源分布 Top10: {dict(source_counts.most_common(10))}")
    print(f"域分布 Top10: {dict(domains.most_common(10))}")


if __name__ == "__main__":
    main()
