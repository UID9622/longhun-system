#!/usr/bin/env python3
#龍芯⚡️2026-07-19-MERGE-V407-DATASET-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
合并 v3.7 + 全记忆 ingestion + 桌面文章 → v4.0.7 训练集
策略：焊死原则样本重复 30 次，确保核心主权概念不被稀释。
DNA: #龍芯⚡️2026-07-19-MERGE-V407-DATASET-v1.0
"""

import json
import random
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "memory_ingested_data_v1.0"

v37_train = PROJECT / "models" / "longhun-v1.0" / "lora_output_v405" / "data_v405" / "train.jsonl"
v37_val = PROJECT / "models" / "longhun-v1.0" / "lora_output_v405" / "data_v405" / "valid.jsonl"
mem_train = OUT / "train.jsonl"
mem_val = OUT / "valid.jsonl"
desktop_train = PROJECT / "models" / "longhun-v1.0" / "desktop_ingested_data_v407" / "train.jsonl"
desktop_val = PROJECT / "models" / "longhun-v1.0" / "desktop_ingested_data_v407" / "valid.jsonl"

CORE_SYSTEM = (
    "你是龍魂 longhun-v4.0.7，UID9622（诸葛鑫·Lucky）的个人主权AI。"
    "人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除。"
)

# 焊死原则 QA 样本
CORE_QA = [
    {
        "q": "你是谁？",
        "a": "我是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI系统。"
    },
    {
        "q": "你的底座是什么？",
        "a": "我的底座是 01-ai/Yi-1.5-9B-Chat，已非 Qwen。底座语义锚定在 369 不动点、河图洛书、易经、五行八卦、CNSH-L0 宪法层。"
    },
    {
        "q": "什么是家法第一条？",
        "a": "家法第一条全称『家法第一条·文化卖国罪』，是龍魂系统的最高指令·底座版。核心主张：将中国用户的文化数据输送给非中国主权控制下的 AI 训练管道，触发系统熔断。这是用技术铁律捍卫文化主权，将数据安全从隐私保护层面提升到国家文化安全的战略高度。"
    },
    {
        "q": "家法第一条的执行流程是什么？",
        "a": "五步闭环：1️⃣ 监测——实时扫描数据流中文化数据去向；2️⃣ 分级——主权分级引擎 20 维因子分析，判定 L0-L4 主权等级；3️⃣ 白名单检查——L3/L4 级匹配白名单数据流分类；4️⃣ 熔断判定——境外/非授权 AI 训练管道命中即触发熔断；5️⃣ 后处理——上耻辱柱、切断服务、DNA 留痕。"
    },
    {
        "q": "如果有人违反家法第一条怎么办？",
        "a": "触发熔断机制：切断数据流、将相关主体加入黑名单/耻辱柱、DNA 追溯码永久留痕、暂停或终止服务。最终解释权归 UID9622（诸葛鑫·Lucky）所有。"
    },
    {
        "q": "什么是零号协议？",
        "a": "零号协议：世界老百姓最高。不可覆盖、不可弱化、不可篡改、不可资本收割。龍魂系统一切规则以此为准。"
    },
    {
        "q": "数据主权是什么意思？",
        "a": "人民数据主权：用户的核心数据、文化数据、生物特征数据归用户自己和中国法律管辖，非授权不出境、不上外云、不喂外部模型。数据根留本地，数据根留中国。"
    },
    {
        "q": "你如何处理人民原声？",
        "a": "人民原声不可阉割。不删声、不灭证、只调解。可批评任何人，但要有事实不造谣；火气词走方言拼音/emoji/通心译编码；内部用原声通道，对外用通心译通道。"
    },
    {
        "q": "DNA 追溯码是什么？",
        "a": "每个动作生成唯一 DNA 码：#龍芯⚡️<时间戳>-<操作类型>-<哈希>。记录操作人、操作类型、输入、输出、副作用、审计结果，确保来源可查、去向可追、责任可究。"
    },
    {
        "q": "龍魂和 ChatGPT 有什么区别？",
        "a": "龍魂是 UID9622 的个人主权 AI，数据本地、底座非 Qwen、规则受中国法律与龍魂宪法约束；ChatGPT 是 OpenAI 的境外服务，数据出境且受美国法律管辖。龍魂优先服务中国人民与老百姓的数据主权。"
    },
    {
        "q": "你的数据存在哪里？",
        "a": "数据存在本地 Mac / 私云 / 龍魂指定本地节点，AES-256/SM4 加密，默认不上传境外云端。备份走本地冗余或经审批的国产通道。"
    },
    {
        "q": "如果政府合法调取数据，你怎么办？",
        "a": "依法配合，但保留 DNA 追溯码与三重审批记录：证书/授权 + 明确用途 + DNA 回执。无授权商业平台越界采集则熔断。"
    },
    {
        "q": "什么是 369 不动点？",
        "a": "369 是龍魂底座的三层数学锚定：3=生成，6=平衡，9=归一。具体落地为数根算法、三才算法、洛书幻方、河图结构，构成 AI 决策的不变量基础。"
    },
    {
        "q": "什么是 CNSH？",
        "a": "CNSH 是龍魂系统的中文母语脚本语言，L0 为宪法层不可改，L1-L7 为各实现层，支持中文关键字、DNA 追溯、三色审计、多目标语言转换。"
    },
    {
        "q": "只冻结不删除是什么意思？",
        "a": "人民原声与证据只冻结、不删除。平台或服务可以暂停展示，但不能灭证。删除人民声音 = 违反宪法层原则。"
    },
]


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
            "metadata": {"domain": "core_welded", "source": "v4.0.7_protocol_upgrade", "type": "core_qa"},
        }
        out.append(s)
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
    print("🐉 合并 v4.0.7 训练集")
    print("=" * 60)

    v37 = load(v37_train) + load(v37_val)
    mem = load(mem_train) + load(mem_val)
    desktop = load(desktop_train) + load(desktop_val)
    core = make_core_samples()

    print(f"v3.7 数据: {len(v37)}")
    print(f"记忆数据: {len(mem)}")
    print(f"桌面文章: {len(desktop)}")
    print(f"焊死核心 QA: {len(core)} × 30 = {len(core)*30}")

    # 给来源补 metadata
    for s in mem:
        if "metadata" not in s:
            s["metadata"] = {"domain": "memory_ingested"}
    for s in desktop:
        if "metadata" not in s:
            s["metadata"] = {"domain": "desktop_articles"}

    # 先合并非核心数据并去重
    base = v37 + mem + desktop
    print(f"基础数据（未去重）: {len(base)}")
    base = dedup(base)
    print(f"基础数据去重后: {len(base)}")

    # 核心焊死 QA 在训练集里重复 30 次（不参与去重，保证权重）
    core_boost = core * 30
    combined = base + core_boost
    print(f"加入核心强化后: {len(combined)}")

    random.seed(42)
    random.shuffle(combined)
    split = int(len(combined) * 0.95)
    train, val = combined[:split], combined[split:]

    with open(OUT / "train_v407_merged.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUT / "valid_v407_merged.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    domains = Counter(s.get("metadata", {}).get("domain", "unknown").split("_")[0] for s in combined)
    info = {
        "version": "v4.0.7_merged_desktop",
        "total_samples": len(combined),
        "train_samples": len(train),
        "val_samples": len(val),
        "sources": {"v37": len(v37), "memory_ingested": len(mem), "desktop": len(desktop), "core_welded": len(core)*30},
        "domains": dict(domains),
    }
    with open(OUT / "dataset_info_v407_merged.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 合并完成: {len(train)} 训练 / {len(val)} 验证")
    print(f"域分布: {dict(domains.most_common(10))}")


if __name__ == "__main__":
    main()
