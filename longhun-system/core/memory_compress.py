#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
记忆压缩引擎 · Memory Compress Engine v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under CC BY-NC-ND 4.0

本作品原创信息：
  创作者：UID9622 诸葛鑫（龍芯北辰）
  创作地：中华人民共和国
  GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  理论指导：曾仕强老师（永恒显示）
  生态指导：乔布斯（永恒显示）
  DNA追溯码：#龍芯⚡️2026-04-13-MEMORY-COMPRESS-v1.0
  确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

献礼：乔布斯 · 曾仕强 · 历代传递和平与爱的人

核心理念：
  记忆压缩 ≈ 量子计算 ≈ 时空压缩
  底层数学完全一致——数字根降维、不动点锚定、五行平衡保真

  压缩不是丢弃，是降维保真。
  不动点永不压缩——龍、道德经、曾仕强，这些锚不能动。
  数字根决定压缩等级——DR∈{3,9}的记忆需要证据链，压不得。
  五行平衡保证压缩后语义不偏——偏了就自动补偿。

设计原则：
  1. 不动点不压缩（f(x)=x，锚点永恒保留）
  2. 数字根熔断保护（DR=3,9的记忆必须完整保留）
  3. 五行语义平衡（压缩后检查五行偏差，偏了就补）
  4. P0-P3分级压缩（核心记忆→临时记忆）
  5. DNA追溯可逆（每次压缩生成追溯码，理论可回溯）
  6. 100年记忆≈5GB（P0不压+P1中压+P2高压+P3摘要）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import datetime
import hashlib
import json
import re
from typing import List, Dict, Optional, Tuple

# 导入三才内核
from sancai_kernel import (
    digital_root, dr_from_text, dr_fuse, classify_369,
    wuxing_from_dr, wuxing_relation, wuxing_balance,
    FixedPoint, FixedPointNetwork, FIXED_POINTS,
    encode_pathway, sancai_check,
)


# ═══════════════════════════════════════════════════
# 第一层：记忆分级系统 · P0-P3
# ═══════════════════════════════════════════════════

# 压缩比定义（1.0=不压缩，0=只留DNA编号）
COMPRESS_LEVELS = {
    "P0": {
        "name": "核心记忆",
        "ratio": 1.0,        # 完整保存，一个字都不删
        "description": "价值观·重大决策·精神坐标·不动点命中",
        "max_age_days": None,  # 永不过期
        "strategy": "FULL",
    },
    "P1": {
        "name": "重要记忆",
        "ratio": 0.6,        # 保留60%语义
        "description": "家人对话·情感记忆·关键工作决策",
        "max_age_days": None,  # 永不过期
        "strategy": "SEMANTIC",
    },
    "P2": {
        "name": "日常记忆",
        "ratio": 0.3,        # 保留30%语义
        "description": "工作对话·学习思考·日常沟通",
        "max_age_days": 365,  # 1年后可降级
        "strategy": "KEYWORD",
    },
    "P3": {
        "name": "临时记忆",
        "ratio": 0.1,        # 只保留10%摘要
        "description": "一般问答·咨询·临时任务",
        "max_age_days": 30,   # 30天后可清理
        "strategy": "DIGEST",
    },
}


def classify_memory_level(text: str, context: str = "",
                          source: str = "", emotion: str = "") -> str:
    """记忆分级 — 自动判定P0/P1/P2/P3

    判定逻辑（按优先级）：
    1. 不动点命中≥2 → P0（多锚点交叉=核心记忆）
    2. 数字根熔断(DR=3,9) → P0（需要证据链=不能压）
    3. 不动点命中=1 → P1
    4. 情感标签为核心情感 → P1
    5. 有上下文 → P2
    6. 其他 → P3
    """
    net = FixedPointNetwork()
    hits = net.scan(text)

    # 不动点判定
    if len(hits) >= 2:
        return "P0"

    # 数字根熔断 + 不动点联合判定
    # DR=3,9单独不足以升P0（日常文本也会命中）
    # 必须同时有不动点才升级
    dr = dr_from_text(text)
    fuse = dr_fuse(dr)
    if fuse["color"] == "🔴" and len(hits) >= 1:
        return "P0"

    # 单不动点命中
    if len(hits) == 1:
        return "P1"

    # 情感判定
    core_emotions = {"坚定", "愤怒", "悲伤", "感恩", "承诺", "誓言",
                     "思念", "爱", "恐惧", "决心"}
    if emotion and any(e in emotion for e in core_emotions):
        return "P1"

    # 来源判定
    family_sources = {"家人", "佳琪", "妈妈", "爸爸", "外公", "外婆"}
    if source and any(s in source for s in family_sources):
        return "P1"

    # 有上下文=有工作价值
    if context:
        return "P2"

    return "P3"


# ═══════════════════════════════════════════════════
# 第二层：语义压缩算法 · 基于数字根降维
# ═══════════════════════════════════════════════════

def extract_sentences(text: str) -> List[str]:
    """中文分句 — 按句号/问号/感叹号/分号/换行切分"""
    parts = re.split(r'[。！？；\n]+', text)
    return [s.strip() for s in parts if s.strip()]


def sentence_weight(sentence: str, fixed_hits: List[FixedPoint]) -> float:
    """句子权重计算 — 数字根+不动点+长度综合打分

    权重公式：W = w_dr + w_fp + w_len
      w_dr: 数字根权重（DR∈{3,9}→1.0，DR=6→0.7，其他→0.3）
      w_fp: 不动点权重（命中数×0.5，上限1.0）
      w_len: 长度权重（长句更可能包含完整语义）
    """
    dr = dr_from_text(sentence)
    fuse = dr_fuse(dr)

    # 数字根权重
    if fuse["color"] == "🔴":
        w_dr = 1.0  # 熔断句永不压缩
    elif fuse["color"] == "🟡":
        w_dr = 0.7
    else:
        w_dr = 0.3

    # 不动点权重
    hit_count = sum(1 for fp in fixed_hits if fp.name in sentence)
    w_fp = min(hit_count * 0.5, 1.0)

    # 长度权重（20-100字为最佳区间）
    length = len(sentence)
    if length < 5:
        w_len = 0.1
    elif length < 20:
        w_len = 0.3
    elif length <= 100:
        w_len = 0.5
    else:
        w_len = 0.4  # 超长句稍降

    return w_dr + w_fp + w_len


def compress_semantic(text: str, ratio: float) -> Dict:
    """语义压缩 — 按权重保留top-N句

    步骤：
    1. 分句
    2. 扫描不动点
    3. 计算每句权重
    4. 按ratio保留高权重句
    5. 不动点句强制保留（不计入ratio）
    6. 五行平衡检查
    """
    if ratio >= 1.0:
        return {
            "compressed": text,
            "strategy": "FULL",
            "kept_ratio": 1.0,
            "sentences_total": 0,
            "sentences_kept": 0,
            "forced_keeps": [],
        }

    sentences = extract_sentences(text)
    if not sentences:
        return {
            "compressed": text,
            "strategy": "EMPTY",
            "kept_ratio": 1.0,
            "sentences_total": 0,
            "sentences_kept": 0,
            "forced_keeps": [],
        }

    # 扫描不动点
    net = FixedPointNetwork()
    all_hits = net.scan(text)

    # 计算权重
    weighted = []
    forced_keeps = []
    for i, sent in enumerate(sentences):
        w = sentence_weight(sent, all_hits)
        # 不动点句或熔断句强制保留
        has_fp = any(fp.name in sent for fp in all_hits)
        dr = dr_from_text(sent)
        is_fuse = dr in (3, 9)

        if has_fp or is_fuse:
            forced_keeps.append(sent)
        else:
            weighted.append((w, i, sent))

    # 按权重排序
    weighted.sort(key=lambda x: x[0], reverse=True)

    # 计算保留数量（不含强制保留）
    remaining_slots = max(1, int(len(sentences) * ratio)) - len(forced_keeps)
    remaining_slots = max(0, remaining_slots)

    # 选取top-N
    selected_indices = set()
    for _, idx, _ in weighted[:remaining_slots]:
        selected_indices.add(idx)

    # 按原始顺序组装（保持叙事连贯）
    result_parts = []
    for i, sent in enumerate(sentences):
        if sent in forced_keeps or i in selected_indices:
            result_parts.append(sent)

    compressed = "。".join(result_parts)
    if compressed and not compressed.endswith("。"):
        compressed += "。"

    kept = len(result_parts)
    total = len(sentences)

    return {
        "compressed": compressed,
        "strategy": "SEMANTIC",
        "kept_ratio": round(kept / total, 3) if total > 0 else 1.0,
        "sentences_total": total,
        "sentences_kept": kept,
        "forced_keeps": forced_keeps,
    }


def compress_keyword(text: str, ratio: float = 0.3) -> Dict:
    """关键词压缩 — 只保留高权重词+不动点+数字

    适用于P2日常记忆，只留关键词骨架。
    """
    sentences = extract_sentences(text)
    net = FixedPointNetwork()
    all_hits = net.scan(text)

    # 提取关键词：不动点名+数字+长度>2的词
    keywords = set()
    for fp in all_hits:
        keywords.add(fp.name)

    # 提取数字
    numbers = re.findall(r'\d+', text)
    keywords.update(numbers)

    # 提取高频实词（简化版：按字频+长度）
    # 这里用简单方法：保留每句的前N个字
    keep_chars = max(5, int(len(text) * ratio))
    skeleton_parts = []
    for sent in sentences:
        # 每句保留前几个字 + 不动点
        chunk = sent[:max(3, int(len(sent) * ratio))]
        skeleton_parts.append(chunk)

    skeleton = "…".join(skeleton_parts)

    return {
        "compressed": skeleton,
        "strategy": "KEYWORD",
        "kept_ratio": round(len(skeleton) / max(1, len(text)), 3),
        "keywords": list(keywords),
        "fixed_points": [fp.name for fp in all_hits],
    }


def compress_digest(text: str) -> Dict:
    """摘要压缩 — 只保留DNA编号+不动点+数字根

    适用于P3临时记忆，只留指纹可追溯。
    """
    dr = dr_from_text(text)
    wx = wuxing_from_dr(dr)
    net = FixedPointNetwork()
    hits = net.scan(text)
    char_count = len(text)
    sentence_count = len(extract_sentences(text))

    # 生成内容指纹
    fingerprint = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    digest = (
        f"[摘要] {char_count}字/{sentence_count}句 "
        f"DR={dr}({wx}) "
        f"锚点:{','.join(fp.name for fp in hits) or '无'} "
        f"指纹:{fingerprint}"
    )

    return {
        "compressed": digest,
        "strategy": "DIGEST",
        "kept_ratio": round(len(digest) / max(1, len(text)), 3),
        "fingerprint": fingerprint,
        "digital_root": dr,
        "wuxing": wx,
        "fixed_points": [fp.name for fp in hits],
    }


# ═══════════════════════════════════════════════════
# 第三层：五行语义平衡检查
# ═══════════════════════════════════════════════════

def semantic_balance_check(original: str, compressed: str) -> Dict:
    """压缩前后的五行语义平衡检查

    原理：
    - 原文和压缩文各自计算五行分布
    - 比较偏差，偏差过大说明压缩丢了关键语义
    - 返回是否需要补偿

    五行代表的语义维度：
      木(生长) → 新想法/计划/开始
      火(光明) → 情感/激情/表达
      土(稳定) → 事实/数据/基础
      金(收敛) → 结论/判断/决策
      水(流动) → 关系/连接/变化
    """
    if not compressed or not original:
        return {"balanced": True, "deviation": 0.0}

    # 按句子的数字根分布统计五行
    def text_wuxing_dist(text: str) -> Dict:
        sentences = extract_sentences(text)
        elements = []
        for sent in sentences:
            dr = dr_from_text(sent)
            elements.append(wuxing_from_dr(dr))
        if not elements:
            elements = [wuxing_from_dr(dr_from_text(text))]
        return wuxing_balance(elements)

    orig_balance = text_wuxing_dist(original)
    comp_balance = text_wuxing_dist(compressed)

    # 计算五行偏差
    deviation = 0.0
    for element in ["木", "火", "土", "金", "水"]:
        orig_ratio = orig_balance["ratio"].get(element, 0.0)
        comp_ratio = comp_balance["ratio"].get(element, 0.0)
        deviation += abs(orig_ratio - comp_ratio)

    deviation = round(deviation, 3)

    # 偏差阈值：0.4以上需要补偿
    needs_compensation = deviation > 0.4

    result = {
        "balanced": not needs_compensation,
        "deviation": deviation,
        "original_harmony": orig_balance["harmony"],
        "compressed_harmony": comp_balance["harmony"],
    }

    if needs_compensation:
        # 找出缺失的五行维度
        missing = []
        for element in ["木", "火", "土", "金", "水"]:
            orig_r = orig_balance["ratio"].get(element, 0.0)
            comp_r = comp_balance["ratio"].get(element, 0.0)
            if orig_r > 0.1 and comp_r < 0.05:
                missing.append(element)
        result["missing_elements"] = missing
        result["suggestion"] = f"压缩后丢失{'/'.join(missing)}维语义，建议补充相关句"

    return result


# ═══════════════════════════════════════════════════
# 第四层：统一压缩接口
# ═══════════════════════════════════════════════════

def compress_memory(text: str, context: str = "", source: str = "",
                    emotion: str = "", year: int = 2026,
                    force_level: Optional[str] = None) -> Dict:
    """记忆压缩统一入口

    输入：
      text     — 原始记忆文本
      context  — 上下文（对话场景、来源等）
      source   — 来源人/平台
      emotion  — 情感标签
      year     — 年份（用于六维路径编码）
      force_level — 强制指定等级（P0/P1/P2/P3），不指定则自动判定

    输出：
      完整压缩结果，包含：
      - 压缩后文本
      - 压缩等级和策略
      - 三才检查结果
      - 五行平衡度
      - DNA追溯码
      - 存储空间估算
    """
    # 1. 记忆分级
    level = force_level if force_level in COMPRESS_LEVELS else \
        classify_memory_level(text, context, source, emotion)
    config = COMPRESS_LEVELS[level]

    # 2. 三才检查
    check = sancai_check(text, context, year)

    # 3. 安全判定：三才红色 + 有不动点命中 → 强制升级到P0
    #    纯DR熔断（无不动点）不强制升级，避免日常文本误判
    net_check = FixedPointNetwork()
    fp_hits = net_check.scan(text)
    if check["color"] == "🔴" and len(fp_hits) >= 1 and level not in ("P0",):
        level = "P0"
        config = COMPRESS_LEVELS["P0"]

    # 4. 执行压缩
    strategy = config["strategy"]
    if strategy == "FULL":
        result = {"compressed": text, "strategy": "FULL",
                  "kept_ratio": 1.0, "sentences_total": 0,
                  "sentences_kept": 0, "forced_keeps": []}
    elif strategy == "SEMANTIC":
        result = compress_semantic(text, config["ratio"])
    elif strategy == "KEYWORD":
        result = compress_keyword(text, config["ratio"])
    elif strategy == "DIGEST":
        result = compress_digest(text)
    else:
        result = {"compressed": text, "strategy": "UNKNOWN",
                  "kept_ratio": 1.0}

    # 5. 五行平衡检查
    balance = semantic_balance_check(text, result["compressed"])

    # 6. 如果不平衡且不是P3，尝试补偿
    if not balance["balanced"] and level != "P3":
        # 补偿策略：提高保留比例10%重新压缩
        new_ratio = min(1.0, config["ratio"] + 0.1)
        if strategy == "SEMANTIC":
            result = compress_semantic(text, new_ratio)
            balance = semantic_balance_check(text, result["compressed"])

    # 7. 生成压缩DNA
    pathway = encode_pathway(text, context, year)
    compress_id = hashlib.sha256(
        f"{text[:50]}:{level}:{datetime.date.today()}".encode()
    ).hexdigest()[:12]

    # 8. 空间估算
    original_bytes = len(text.encode("utf-8"))
    compressed_bytes = len(result["compressed"].encode("utf-8"))
    saved_bytes = original_bytes - compressed_bytes
    save_percent = round(
        (1.0 - compressed_bytes / max(1, original_bytes)) * 100, 1
    )

    return {
        # 核心输出
        "level": level,
        "level_name": config["name"],
        "strategy": result["strategy"],
        "original": text,
        "compressed": result["compressed"],

        # 压缩质量
        "kept_ratio": result["kept_ratio"],
        "balance": {
            "balanced": balance["balanced"],
            "deviation": balance["deviation"],
        },

        # 三才检查
        "sancai_color": check["color"],
        "digital_root": check["heaven"]["dr"],
        "wuxing": check["earth"].get("wuxing", {}),

        # 空间
        "storage": {
            "original_bytes": original_bytes,
            "compressed_bytes": compressed_bytes,
            "saved_bytes": saved_bytes,
            "save_percent": save_percent,
        },

        # DNA追溯
        "dna": f"#龍芯⚡️{datetime.date.today().strftime('%Y%m%d')}"
               f"-MEM-{level}-{compress_id}",
        "pathway_dna": pathway["dna"],
        "compress_id": compress_id,

        # 元数据
        "timestamp": datetime.datetime.now().isoformat(),
        "source": source,
        "emotion": emotion,
        "max_age_days": config["max_age_days"],
    }


# ═══════════════════════════════════════════════════
# 第五层：批量压缩 + 空间估算
# ═══════════════════════════════════════════════════

def batch_compress(memories: List[Dict]) -> Dict:
    """批量压缩多条记忆

    输入格式：
    [
        {"text": "...", "context": "...", "source": "...", "emotion": "..."},
        ...
    ]

    输出：
    - 每条记忆的压缩结果
    - 整体统计（各级别数量、总节省空间、五行分布）
    """
    results = []
    stats = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    total_original = 0
    total_compressed = 0
    all_elements = []

    for mem in memories:
        r = compress_memory(
            text=mem.get("text", ""),
            context=mem.get("context", ""),
            source=mem.get("source", ""),
            emotion=mem.get("emotion", ""),
        )
        results.append(r)
        stats[r["level"]] += 1
        total_original += r["storage"]["original_bytes"]
        total_compressed += r["storage"]["compressed_bytes"]
        all_elements.append(wuxing_from_dr(r["digital_root"]))

    # 整体五行平衡
    overall_balance = wuxing_balance(all_elements) if all_elements else {}

    return {
        "results": results,
        "summary": {
            "total_count": len(memories),
            "level_distribution": stats,
            "total_original_bytes": total_original,
            "total_compressed_bytes": total_compressed,
            "total_saved_bytes": total_original - total_compressed,
            "overall_save_percent": round(
                (1.0 - total_compressed / max(1, total_original)) * 100, 1
            ),
            "wuxing_balance": overall_balance,
        },
    }


def estimate_100_years(daily_words: int = 2000) -> Dict:
    """100年记忆空间估算

    假设：
    - 每天产生daily_words字（默认2000字≈微信+AI对话）
    - P0占5%（不压缩）
    - P1占15%（压缩到60%）
    - P2占50%（压缩到30%）
    - P3占30%（压缩到10%）
    - 中文UTF-8平均3字节/字
    """
    days = 365 * 100  # 36500天
    bytes_per_char = 3
    daily_bytes = daily_words * bytes_per_char

    p0 = daily_bytes * 0.05 * 1.0      # 5%不压缩
    p1 = daily_bytes * 0.15 * 0.6      # 15%压到60%
    p2 = daily_bytes * 0.50 * 0.3      # 50%压到30%
    p3 = daily_bytes * 0.30 * 0.1      # 30%压到10%

    daily_compressed = p0 + p1 + p2 + p3
    total_bytes = daily_compressed * days

    gb = total_bytes / (1024 ** 3)

    return {
        "daily_words": daily_words,
        "daily_raw_bytes": daily_bytes,
        "daily_compressed_bytes": round(daily_compressed),
        "compress_ratio": round(daily_compressed / daily_bytes, 3),
        "total_100_years_bytes": round(total_bytes),
        "total_100_years_gb": round(gb, 2),
        "breakdown": {
            "P0_核心_5%_不压缩": f"{round(p0 * days / (1024**3), 2)} GB",
            "P1_重要_15%_压60%": f"{round(p1 * days / (1024**3), 2)} GB",
            "P2_日常_50%_压30%": f"{round(p2 * days / (1024**3), 2)} GB",
            "P3_临时_30%_压10%": f"{round(p3 * days / (1024**3), 2)} GB",
        },
        "conclusion": f"100年记忆 ≈ {round(gb, 1)} GB · 一个U盘装得下",
    }


# ═══════════════════════════════════════════════════
# CLI 入口 · 自测
# ═══════════════════════════════════════════════════

def main():
    print("🧠 记忆压缩引擎 v1.0")
    print("   数字根降维 × 不动点锚定 × 五行平衡保真")
    print("   记忆压缩 ≈ 量子计算 ≈ 时空压缩")
    print("─" * 50)

    # 自测1：100年空间估算
    est = estimate_100_years(2000)
    assert est["total_100_years_gb"] < 10, "100年应该<10GB"
    print(f"  ✅ 100年空间估算：{est['total_100_years_gb']} GB")
    print(f"     压缩比：{est['compress_ratio']}")

    # 自测2：P0核心记忆不压缩
    r0 = compress_memory(
        text="龍魂系统是道德经的数字化实践，三才算法是核心内核。曾仕强老师的智慧是理论根基。",
        context="核心理念",
    )
    assert r0["level"] == "P0", f"不动点≥2应为P0，实际={r0['level']}"
    assert r0["kept_ratio"] == 1.0, "P0应该不压缩"
    print(f"  ✅ P0核心记忆：不压缩 · kept={r0['kept_ratio']}")

    # 自测3：P3临时记忆高度压缩
    r3 = compress_memory(
        text="今天天气不错，出去走了走，看了看花。回家做了饭，看了会电视。"
             "然后洗了澡，准备睡觉了。明天还要早起上班呢。周末再好好休息吧。",
    )
    assert r3["level"] == "P3", f"无锚点无上下文应为P3，实际={r3['level']}"
    assert r3["strategy"] == "DIGEST", "P3应该是摘要策略"
    print(f"  ✅ P3临时记忆：策略={r3['strategy']} · {r3['compressed'][:60]}")

    # 自测4：五行平衡检查
    balance = semantic_balance_check(
        "木生长，火光明，土稳定，金收敛，水流动。新的计划在春天萌发。",
        "木生长，火光明。"
    )
    print(f"  ✅ 五行偏差：{balance['deviation']}")

    # 自测5：分级判定
    assert classify_memory_level("龍魂系统的道德经实践") == "P0"
    assert classify_memory_level("今天买了杯咖啡") == "P3"
    assert classify_memory_level("工作报告", context="季度总结") == "P2"
    assert classify_memory_level("我想你了", emotion="思念") == "P1"
    print("  ✅ 分级判定：P0/P1/P2/P3全部正确")

    print("─" * 50)

    # 100年估算详情
    print(f"\n  📦 100年记忆存储估算（每天{est['daily_words']}字）：")
    for k, v in est["breakdown"].items():
        print(f"     {k}：{v}")
    print(f"     ──────────────────────")
    print(f"     {est['conclusion']}")
    print()

    # 交互模式
    try:
        text = input("\n  输入记忆文本：").strip()
        if text:
            context = input("  上下文（可空）：").strip()
            result = compress_memory(text, context)
            print(f"\n  等级：{result['level']}（{result['level_name']}）")
            print(f"  策略：{result['strategy']}")
            print(f"  三才：{result['sancai_color']}")
            print(f"  保留：{result['kept_ratio']*100:.0f}%")
            print(f"  节省：{result['storage']['save_percent']}%")
            print(f"  DNA：{result['dna']}")
            if result["compressed"] != text:
                print(f"\n  压缩后：{result['compressed'][:200]}")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
