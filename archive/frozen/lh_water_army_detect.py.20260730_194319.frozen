#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_WATER_ARMY_DETECT-v1.0-5b186423
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh water-army-detect — 龍魂水军识别引擎 v1.0

防御性水军行为检测：只标记不封禁、只降权不删号、可申诉可追溯。

六维检测：
  1. 文本重复度（哈希去重 + 余弦相似度）
  2. 账号生命周期（新号高频/休眠激活）
  3. 时间窗口协同（协同举报/刷评/定时发布）
  4. 内容模式（情绪操控/导向性话术/语义漂移）
  5. 关联分析（IP/设备聚类）
  6. 举报信用（举报成功率）

用法：
  python3 bin/lh_water_army_detect.py scan "评论文本"
  python3 bin/lh_water_army_detect.py scan-file <文件路径>
  python3 bin/lh_water_army_detect.py batch <jsonl文件>
  python3 bin/lh_water_army_detect.py rules

DNA: #龍芯⚡️2026-07-06-WATER-ARMY-DETECT-v1.0-8A2C3F7E
"""

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ============================================
# 规则权重配置（所有参数可调）
# ============================================
WEIGHTS: Dict[str, float] = {
    "exact_dup": 0.25,         # 完全相同内容
    "high_similarity": 0.30,   # 高度相似
    "template_match": 0.15,    # 模板化内容
    "new_account_spam": 0.20,  # 新号高频
    "dormant_activate": 0.15,  # 休眠激活
    "coordinated_attack": 0.35, # 协同攻击
    "coordinated_spam": 0.25,  # 协同刷评
    "timed_batch": 0.10,       # 定时批量
    "emotional_manipulation": 0.15, # 情绪操控
    "directive_speech": 0.12,  # 导向性话术
    "semantic_drift": 0.08,    # 语义漂移
    "ip_cluster": 0.20,        # IP聚类
    "malicious_report": 0.30,  # 恶意举报
}

# 阈值配置
THRESHOLDS = {
    "exact_dup_count": 5,          # 完全相同 ≥ 5次
    "similarity_threshold": 0.85,  # 余弦相似度阈值
    "similarity_group_count": 10,  # 相似群组 ≥ 10/h
    "template_per_hour": 3,        # 模板化 ≥ 3/h
    "new_account_days": 7,         # 新号 < 7天
    "new_account_daily": 50,       # 新号日发言 > 50
    "new_account_extreme": 100,    # 新号日发言 > 100（极值）
    "dormant_days": 7,             # 休眠 > 7天
    "dormant_activate_daily": 30,  # 激活后日发言 > 30
    "coordinated_report_min": 5,   # 协同举报 ≥ 5账号
    "coordinated_window_min": 5,   # 时间窗口 5分钟
    "coordinated_spam_count": 10,  # 协同刷评 ≥ 10账号
    "coordinated_spam_window": 10, # 刷评窗口 10分钟
    "timed_batch_stddev": 5,       # 间隔标准差 < 5s
    "exclamation_ratio": 0.15,     # 感叹号占比 > 15%
    "repeat_ratio": 0.30,          # 重复率 > 30%
    "semantic_drift_topics": 5,    # 1h > 5个话题
    "ip_min_accounts": 3,          # 同IP ≥ 3账号
    "ip_serious_accounts": 10,     # 同IP ≥ 10账号
    "report_success_rate": 0.20,   # 举报成功率 < 20%
}

# ============================================
# 导向性话术模式库
# ============================================
DIRECTIVE_PATTERNS: List[str] = [
    r"必须转发",
    r"不转不是.{1,4}",
    r"不转就.{1,10}",
    r"都来看",
    r"赶紧看.*删",
    r"速看.*删",
    r"全网都在看",
    r"转发.*好运",
    r"转发.*保平安",
    r"看到.*必须转",
    r"顶上去",
    r"刷起来",
    r"大家快转发",
    r"扩散出去",
    r"让更多人看到",
]

# ============================================
# 模板化内容模式库
# ============================================
TEMPLATE_PATTERNS: List[str] = [
    r"^我也.{0,10}(觉得|认为|想说).{0,20}$",
    r"^(支持|赞同|同意|反对).{0,20}$",
    r"^(楼主|博主|小编).{0,10}(说得对|说得好|说得太好了).{0,20}$",
    r"^.{0,5}(加油|辛苦了|棒棒哒|赞|顶).{0,5}$",
    r"^(哈哈|呵呵|嘿嘿|嘻嘻)\1*$",
    r"^\++$",
    r"^[👍👏💪🔥❤️🎉✨💯🙏🤝🫡]+\s*$",
    r"^复制.{0,10}(这段|这个).{0,10}(评论|话|内容).{0,10}$",
    r"^(我也|同样|一模一样).{0,10}(遇到|经历|感受).{0,20}$",
]

# ============================================
# 情绪操控检测模式
# ============================================
EMOTIONAL_MANIPULATION_PATTERNS: List[str] = [
    r"[！!]{3,}",                        # 连续感叹号
    r"天啊|妈呀|卧槽|我的天",
    r"太.{0,2}了(吧|啊|哦)",
    r"震惊|难以置信|不敢相信",
    r"[哭|气|急|恨|怕|慌].{0,3}死了",
]

# ============================================
# AI生成内容检测模式（v1.1 新增·离火运升级）
# ============================================
# 来源: UID9622《浮躁的真相》— 水军AI化·诈骗精准化
# DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-WATER-ARMY-AI-UPGRADE-v1.1
AI_GENERATED_PATTERNS: List[str] = [
    # GPT系常见开头/结尾
    r"^(总的来说|综上所述|总而言之|从以上分析).{0,50}",
    r"^(值得注意的是|需要强调的是|不可忽视的是).{0,50}",
    r"^(在这个|在当今|在当下|随着.{2,6}的发展).{0,50}",
    r"^(作为|身为|作为一个).{0,20}(，|,).{0,20}(我认为|我觉得|我深知)",
    # LLM结构化用语
    r"^(首先.*其次.*(最后|再次))",
    r"^(一方面.*另一方面)",
    r"^(不仅.*而且.*(还|更))",
    r"^(从.*角度来看|从.*层面来说|从.*维度分析)",
    # AI典型空洞话术
    r"^(它不仅仅是.*更是)",
    r"^(我们应当|我们应该|我们需要).{0,10}(认识到|意识到|重视)",
    r"^(这提醒我们|这告诉我们|这启示我们)",
    # 过于工整的排比+总结
    r"^.{0,20}(，).{0,20}(，).{0,20}(。)$",  # 三段式工整句
    # AI常见劝导话术
    r"^(理性看待|客观分析|辩证地看|换位思考)",
    r"^(保持理性|保持冷静|保持克制)",
    # AI假人评论特征
    r"^说得太对了.{0,30}$",
    r"^深有同感.{0,30}$",
    r"^非常赞同.{0,30}$",
    r"^(分析得|写得|讲得).{0,10}(非常|很|太).{0,10}(到位|透彻|精彩|好)",
]

# AI生成文本特征权重
AI_WEIGHTS: Dict[str, float] = {
    "ai_pattern_match": 0.20,       # AI模式匹配
    "uniform_sentence_len": 0.10,   # 句子长度过于均匀
    "excessive_coherence": 0.08,    # 过度连贯（真人会有跳跃）
    "zero_typo": 0.05,              # 零错别字（真人几乎不可能）
    "multi_pattern_hit": 0.25,      # 命中了多个AI模式（强信号）
}

# ============================================
# 核心分析函数
# ============================================


def compute_text_hash(text: str) -> str:
    """计算文本 SHA256 哈希"""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def _jieba_cut(text: str) -> List[str]:
    """用 jieba 分词，不可用时退化为按字符切"""
    try:
        import jieba  # type: ignore[import-untyped]
        return list(jieba.cut(text))
    except ImportError:
        # 退化为2-gram字符切分
        result = []
        chars = list(text)
        for i in range(len(chars) - 1):
            result.append(chars[i] + chars[i + 1])
        for c in chars:
            result.append(c)
        return result


def _build_tfidf_vector(
    tokens: List[str], vocabulary: Optional[List[str]] = None
) -> Dict[str, float]:
    """构建 TF-IDF 向量"""
    tf = Counter(tokens)
    total = len(tokens) if tokens else 1
    vec: Dict[str, float] = {}
    if vocabulary:
        for w in vocabulary:
            vec[w] = tf.get(w, 0) / total
    else:
        vec = {w: c / total for w, c in tf.items()}
    return vec


def compute_cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """计算两个 TF-IDF 向量的余弦相似度"""
    all_words = set(vec1.keys()) | set(vec2.keys())

    dot = 0.0
    mag1 = 0.0
    mag2 = 0.0

    for w in all_words:
        v1 = vec1.get(w, 0.0)
        v2 = vec2.get(w, 0.0)
        dot += v1 * v2
        mag1 += v1 * v1
        mag2 += v2 * v2

    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0
    return dot / (math.sqrt(mag1) * math.sqrt(mag2))


def find_text_similarity_group(
    texts: List[str], idx: int, threshold: float
) -> List[int]:
    """找出与 texts[idx] 相似度高的文本索引列表"""
    tokens_all = [_jieba_cut(t) for t in texts]
    # 构建全局词汇表
    vocab: List[str] = []
    seen: set[str] = set()
    for tokens in tokens_all:
        for t in tokens:
            if t not in seen:
                vocab.append(t)
                seen.add(t)

    vectors = [_build_tfidf_vector(t, vocab) for t in tokens_all]
    target_vec = vectors[idx]
    similar_indices = []

    for j, vec in enumerate(vectors):
        if j == idx:
            continue
        sim = compute_cosine_similarity(target_vec, vec)
        if sim >= threshold:
            similar_indices.append(j)

    return similar_indices


# ============================================
# 六大检测器
# ============================================


def detect_text_duplication(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检测文本重复度
    - 完全相同内容 > 5次
    - 高度相似内容 > 10条/h
    - 模板化内容 > 3条/h
    """
    results: List[Dict[str, Any]] = []
    texts = [c.get("text", "") for c in comments]
    hashes = [compute_text_hash(t) for t in texts]

    # 1. 完全相同检测
    hash_counter = Counter(hashes)
    dup_hashes: Dict[str, List[int]] = defaultdict(list)
    for i, h in enumerate(hashes):
        if hash_counter[h] >= THRESHOLDS["exact_dup_count"]:
            dup_hashes[h].append(i)

    if dup_hashes:
        for h, indices in dup_hashes.items():
            if len(indices) >= THRESHOLDS["exact_dup_count"]:
                results.append({
                    "detector": "完全相同内容",
                    "level": "🔴",
                    "weight": WEIGHTS["exact_dup"],
                    "count": len(indices),
                    "threshold": THRESHOLDS["exact_dup_count"],
                    "sample_indices": indices[:5],
                    "detail": f"完全相同内容出现 {len(indices)} 次（阈值 ≥ {THRESHOLDS['exact_dup_count']}）",
                })

    # 2. 高度相似检测（采样检测，避免 O(n²)）
    if len(texts) > 1:
        sample_size = min(100, len(texts))
        sample_indices = list(range(0, len(texts), max(1, len(texts) // sample_size)))
        similar_groups: Dict[int, List[int]] = {}

        for si in sample_indices:
            group = find_text_similarity_group(
                texts, si, THRESHOLDS["similarity_threshold"]
            )
            if len(group) >= THRESHOLDS["similarity_group_count"] - 1:
                similar_groups[si] = group

        for si, group in similar_groups.items():
            results.append({
                "detector": "高度相似内容",
                "level": "🔴",
                "weight": WEIGHTS["high_similarity"],
                "count": len(group) + 1,
                "threshold": THRESHOLDS["similarity_group_count"],
                "sample_indices": [si] + group[:4],
                "detail": f"发现高度相似内容群组 {len(group) + 1} 条（相似度 > {THRESHOLDS['similarity_threshold']}，阈值 ≥ {THRESHOLDS['similarity_group_count']}）",
            })

    # 3. 模板化检测（去重：每个模板只报一次）
    reported_templates: set[str] = set()
    for tp in TEMPLATE_PATTERNS:
        if tp in reported_templates:
            continue
        template_hits = sum(
            1 for cc in comments if re.search(tp, cc.get("text", ""))
        )
        if template_hits >= THRESHOLDS["template_per_hour"]:
            # 找到第一个匹配的索引作为样本
            sample_idx = next(
                (j for j, cc in enumerate(comments) if re.search(tp, cc.get("text", ""))),
                0,
            )
            results.append({
                "detector": "模板化内容",
                "level": "🟡",
                "weight": WEIGHTS["template_match"],
                "pattern": tp,
                "count": template_hits,
                "threshold": THRESHOLDS["template_per_hour"],
                "sample_index": sample_idx,
                "detail": f"模板 '{tp}' 命中 {template_hits} 次（阈值 ≥ {THRESHOLDS['template_per_hour']}）",
            })
            reported_templates.add(tp)

    return results


def detect_account_lifecycle(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检测账号生命周期异常
    - 新号高频发言（注册 < 7天 + 日发言 > 50）
    - 休眠激活
    """
    results: List[Dict[str, Any]] = []

    if not comments:
        return results

    # 按账号分组
    accounts: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for c in comments:
        uid = c.get("user_id", c.get("uid", "unknown"))
        accounts[uid].append(c)

    for uid, msgs in accounts.items():
        reg_time_str = msgs[0].get("registration_time") or msgs[0].get("created_at")
        msg_count = len(msgs)

        if reg_time_str:
            try:
                reg_time = datetime.fromisoformat(reg_time_str.replace("Z", "+00:00"))
                now = datetime.now().astimezone()
                account_age_days = (now - reg_time).days

                # 新号检测
                if account_age_days < THRESHOLDS["new_account_days"]:
                    is_extreme = msg_count > THRESHOLDS["new_account_extreme"]
                    is_high = msg_count > THRESHOLDS["new_account_daily"]

                    if is_extreme:
                        results.append({
                            "detector": "新号极限发言",
                            "level": "🔴",
                            "weight": WEIGHTS["new_account_spam"],
                            "user_id": uid,
                            "account_age_days": account_age_days,
                            "daily_count": msg_count,
                            "detail": f"账号 {uid} 注册仅 {account_age_days} 天，发言 {msg_count} 条（阈值 > {THRESHOLDS['new_account_extreme']}）",
                        })
                    elif is_high:
                        results.append({
                            "detector": "新号高频发言",
                            "level": "🟡",
                            "weight": WEIGHTS["new_account_spam"],
                            "user_id": uid,
                            "account_age_days": account_age_days,
                            "daily_count": msg_count,
                            "detail": f"账号 {uid} 注册仅 {account_age_days} 天，发言 {msg_count} 条（阈值 > {THRESHOLDS['new_account_daily']}）",
                        })

                # 休眠激活检测
                msg_times = sorted(
                    [
                        datetime.fromisoformat(
                            (m.get("timestamp") or m.get("time", "2000-01-01"))
                            .replace("Z", "+00:00")
                        )
                        for m in msgs
                        if m.get("timestamp") or m.get("time")
                    ]
                )
                if len(msg_times) >= 2:
                    last_active = msg_times[0]
                    recent = msg_times[-1]
                    dormant_days = (recent - last_active).days
                    if dormant_days > THRESHOLDS["dormant_days"] and msg_count > THRESHOLDS["dormant_activate_daily"]:
                        results.append({
                            "detector": "休眠激活",
                            "level": "🟡",
                            "weight": WEIGHTS["dormant_activate"],
                            "user_id": uid,
                            "dormant_days": dormant_days,
                            "activate_count": msg_count,
                            "detail": f"账号 {uid} 休眠 {dormant_days} 天后突然发言 {msg_count} 条",
                        })
            except (ValueError, TypeError):
                pass

    return results


def detect_coordinated_behavior(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检测时间窗口协同行为
    - 协同举报（5min内 ≥ 5账号举报同目标）
    - 协同刷评（10min内 ≥ 10账号评论同内容）
    - 定时发布（间隔标准差 < 5s）
    """
    results: List[Dict[str, Any]] = []

    if len(comments) < THRESHOLDS["coordinated_report_min"]:
        return results

    # 按时间排序
    sorted_comments = sorted(
        comments,
        key=lambda c: c.get("timestamp") or c.get("time", "2000-01-01"),
    )

    # 检测数据中是否包含举报相关字段
    has_report_data = any(
        c.get("action_type") == "report"
        or "report" in str(c.get("type", "")).lower()
        or c.get("target_id") is not None
        for c in comments
    )

    # 协同检测：滑动窗口
    coord_configs = [
        ("协同举报", THRESHOLDS["coordinated_report_min"],
         THRESHOLDS["coordinated_window_min"],
         WEIGHTS["coordinated_attack"], "🔴"),
        ("协同刷评", THRESHOLDS["coordinated_spam_count"],
         THRESHOLDS["coordinated_spam_window"],
         WEIGHTS["coordinated_spam"], "🟡"),
    ]
    if not has_report_data:
        # 没有举报数据，协同举报降级为"多账号协同行动"
        coord_configs[0] = (
            "多账号协同行动", THRESHOLDS["coordinated_report_min"],
            THRESHOLDS["coordinated_window_min"],
            WEIGHTS["coordinated_attack"] * 0.6, "🟡"
        )

    for window_min in coord_configs:
        name, min_accounts, win_min, weight, level = window_min
        for i in range(len(sorted_comments)):
            try:
                t0 = datetime.fromisoformat(
                    (sorted_comments[i].get("timestamp") or sorted_comments[i].get("time", ""))
                    .replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                continue

            window_end = t0 + timedelta(minutes=win_min)
            window_accounts: set[str] = set()
            window_indices: List[int] = []

            for j in range(i, len(sorted_comments)):
                try:
                    tj = datetime.fromisoformat(
                        (sorted_comments[j].get("timestamp") or sorted_comments[j].get("time", ""))
                        .replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    continue
                if tj > window_end:
                    break
                uid = sorted_comments[j].get("user_id", sorted_comments[j].get("uid", f"unknown_{j}"))
                if uid not in window_accounts:
                    window_accounts.add(uid)
                    window_indices.append(j)

            if len(window_accounts) >= min_accounts:
                results.append({
                    "detector": name,
                    "level": level,
                    "weight": weight,
                    "account_count": len(window_accounts),
                    "threshold": min_accounts,
                    "time_window_min": win_min,
                    "detail": f"检测到 {name}：{win_min} 分钟内 {len(window_accounts)} 个账号集中行动",
                })
                break  # 每组只报一次

    # 定时发布检测
    if len(sorted_comments) >= 3:
        try:
            intervals: List[float] = []
            for i in range(1, len(sorted_comments)):
                t1 = datetime.fromisoformat(
                    (sorted_comments[i - 1].get("timestamp") or sorted_comments[i - 1].get("time", ""))
                    .replace("Z", "+00:00")
                )
                t2 = datetime.fromisoformat(
                    (sorted_comments[i].get("timestamp") or sorted_comments[i].get("time", ""))
                    .replace("Z", "+00:00")
                )
                intervals.append((t2 - t1).total_seconds())

            if intervals:
                avg = sum(intervals) / len(intervals)
                var = sum((x - avg) ** 2 for x in intervals) / len(intervals)
                std = math.sqrt(var)
                if std < THRESHOLDS["timed_batch_stddev"]:
                    results.append({
                        "detector": "定时批量发布",
                        "level": "🟡",
                        "weight": WEIGHTS["timed_batch"],
                        "stddev_seconds": round(std, 2),
                        "threshold": THRESHOLDS["timed_batch_stddev"],
                        "avg_interval": round(avg, 2),
                        "detail": f"发布间隔标准差 {std:.2f}s < {THRESHOLDS['timed_batch_stddev']}s，疑似定时批量",
                    })
        except (ValueError, TypeError):
            pass

    return results


def detect_content_patterns(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检测内容模式异常
    - 情绪操控（感叹号密集 + 短句重复）
    - 导向性话术
    - 语义漂移
    """
    results: List[Dict[str, Any]] = []

    for c in comments:
        text = c.get("text", "")

        # 情绪操控检测
        exclamation_count = text.count("!") + text.count("！")
        char_count = len(text) if text else 1
        exclamation_ratio = exclamation_count / char_count

        # 重复率检测
        if len(text) >= 4:
            chunks = [text[i:i+2] for i in range(len(text) - 1)]
            chunk_counter = Counter(chunks)
            repeat_ratio = max(chunk_counter.values()) / len(chunks) if chunks else 0
        else:
            repeat_ratio = 0.0

        # 情绪操纵模式匹配
        emotion_hits = sum(
            1 for ep in EMOTIONAL_MANIPULATION_PATTERNS if re.search(ep, text)
        )

        if exclamation_ratio > THRESHOLDS["exclamation_ratio"] and repeat_ratio > THRESHOLDS["repeat_ratio"]:
            results.append({
                "detector": "情绪操控",
                "level": "🟡",
                "weight": WEIGHTS["emotional_manipulation"],
                "exclamation_ratio": round(exclamation_ratio, 3),
                "repeat_ratio": round(repeat_ratio, 3),
                "emotion_pattern_hits": emotion_hits,
                "detail": f"感叹号占比 {exclamation_ratio:.1%} > {THRESHOLDS['exclamation_ratio']:.0%}，重复率 {repeat_ratio:.1%} > {THRESHOLDS['repeat_ratio']:.0%}",
            })

    # 导向性话术检测（去重：每个模式只报一次，加命中计数）
    reported_directives: set[str] = set()
    for dp in DIRECTIVE_PATTERNS:
        if dp in reported_directives:
            continue
        hit_count = sum(1 for cc in comments if re.search(dp, cc.get("text", "")))
        if hit_count > 0:
            results.append({
                "detector": "导向性话术",
                "level": "🟡",
                "weight": WEIGHTS["directive_speech"],
                "pattern": dp,
                "hit_count": hit_count,
                "detail": f"检测到导向性话术：模式 '{dp}' 命中 {hit_count} 次",
            })
            reported_directives.add(dp)

    # 语义漂移检测（按同一账号）
    accounts: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for c in comments:
        uid = c.get("user_id", c.get("uid", "unknown"))
        accounts[uid].append(c)

    for uid, msgs in accounts.items():
        if len(msgs) < THRESHOLDS["semantic_drift_topics"]:
            continue
        # 简化：用文本长度剧烈变化作为话题漂移的近似指标
        lengths = [len(m.get("text", "")) for m in msgs]
        if lengths:
            avg_len = sum(lengths) / len(lengths)
            var = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std = math.sqrt(var)
            if avg_len > 0 and std / avg_len > 1.5 and len(msgs) > THRESHOLDS["semantic_drift_topics"]:
                results.append({
                    "detector": "语义漂移",
                    "level": "🟡",
                    "weight": WEIGHTS["semantic_drift"],
                    "user_id": uid,
                    "msg_count": len(msgs),
                    "length_std_ratio": round(std / avg_len, 2) if avg_len > 0 else 0,
                    "detail": f"账号 {uid} 短时间 {len(msgs)} 条发言，文本长度方差比 > 1.5，疑似多话题跳跃",
                })

    return results


def detect_ip_clustering(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检测 IP/设备聚类
    """
    results: List[Dict[str, Any]] = []
    ip_accounts: Dict[str, set[str]] = defaultdict(set)

    for c in comments:
        ip = c.get("ip", c.get("ip_address", c.get("remote_addr", "")))
        uid = c.get("user_id", c.get("uid", "unknown"))
        if ip:
            ip_accounts[ip].add(uid)

    for ip, accounts in ip_accounts.items():
        if len(accounts) >= THRESHOLDS["ip_serious_accounts"]:
            results.append({
                "detector": "IP严重聚类",
                "level": "🔴",
                "weight": WEIGHTS["ip_cluster"],
                "ip": ip,
                "account_count": len(accounts),
                "detail": f"IP {ip} 关联 {len(accounts)} 个账号（阈值 ≥ {THRESHOLDS['ip_serious_accounts']}）",
            })
        elif len(accounts) >= THRESHOLDS["ip_min_accounts"]:
            results.append({
                "detector": "IP聚类",
                "level": "🟡",
                "weight": WEIGHTS["ip_cluster"],
                "ip": ip,
                "account_count": len(accounts),
                "detail": f"IP {ip} 关联 {len(accounts)} 个账号（阈值 ≥ {THRESHOLDS['ip_min_accounts']}）",
            })

    return results


def detect_malicious_reporting(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检测恶意举报行为
    """
    results: List[Dict[str, Any]] = []

    for c in comments:
        total_reports = c.get("total_reports", c.get("report_count", 0))
        successful_reports = c.get("successful_reports", c.get("report_success", 0))

        if total_reports > 0:
            success_rate = successful_reports / total_reports
            if success_rate < THRESHOLDS["report_success_rate"]:
                uid = c.get("user_id", c.get("uid", "unknown"))
                results.append({
                    "detector": "恶意举报",
                    "level": "🟡",
                    "weight": WEIGHTS["malicious_report"],
                    "user_id": uid,
                    "success_rate": round(success_rate, 3),
                    "threshold": THRESHOLDS["report_success_rate"],
                    "detail": f"账号 {uid} 举报成功率 {success_rate:.1%} < {THRESHOLDS['report_success_rate']:.0%}%，举报权重归零",
                })

    return results


# ============================================
# 汇总审计
# ============================================


def audit_summary(all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    汇总所有检测结果，生成三色审计报告
    """
    if not all_results:
        return {
            "overall_level": "🟢",
            "overall_score": 0.0,
            "confidence": "正常",
            "findings_count": 0,
            "red_count": 0,
            "yellow_count": 0,
            "max_weight": 0.0,
            "recommendation": "未检测到水军特征，正常通行",
        }

    red_results = [r for r in all_results if r.get("level") == "🔴"]
    yellow_results = [r for r in all_results if r.get("level") == "🟡"]

    total_weight = sum(r.get("weight", 0.0) for r in all_results)
    max_weight = max((r.get("weight", 0.0) for r in all_results), default=0.0)
    red_weight = sum(r.get("weight", 0.0) for r in red_results)

    # 综合判定
    if red_results:
        overall_level = "🔴"
        confidence = "高风险·水军特征明显"
        recommendation = "标记可疑账号，举报权重归零，建议人工复核但不自动封禁。可申诉。"
    elif total_weight >= 0.6:
        overall_level = "🟡"
        confidence = "中风险·可疑行为"
        recommendation = "标记可疑，建议延迟发布或人工复核。新增举报需二次审核。"
    elif total_weight >= 0.2:
        overall_level = "🟡"
        confidence = "低风险·轻度可疑"
        recommendation = "记录观察，不干预正常发布。持续跟踪该账号后续行为。"
    else:
        overall_level = "🟢"
        confidence = "正常"
        recommendation = "未检测到显著水军特征，偶发信号已记录但不干预"

    return {
        "overall_level": overall_level,
        "overall_score": round(total_weight, 3),
        "confidence": confidence,
        "findings_count": len(all_results),
        "red_count": len(red_results),
        "yellow_count": len(yellow_results),
        "max_weight": round(max_weight, 3),
        "recommendation": recommendation,
    }


def format_report(
    all_results: List[Dict[str, Any]],
    summary: Dict[str, Any],
    source: str = "",
) -> str:
    """生成可读报告"""
    lines: List[str] = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 龍魂水军识别引擎 · 审计报告")
    lines.append("=" * 64)
    if source:
        lines.append(f"  来源: {source}")
    lines.append(f"  DNA: #龍芯⚡️2026-07-06-WATER-ARMY-DETECT-v1.0-8A2C3F7E")
    lines.append(f"  时间: {datetime.now().isoformat()}")
    lines.append("")
    lines.append(f"  📊 综合判定: {summary['overall_level']}  {summary['confidence']}")
    lines.append(f"  风险评分: {summary['overall_score']:.2f}")
    lines.append(f"  发现问题: {summary['findings_count']} 个")
    lines.append(f"    🔴 严重: {summary['red_count']}")
    lines.append(f"    🟡 可疑: {summary['yellow_count']}")
    lines.append("")
    lines.append(f"  💡 建议: {summary['recommendation']}")
    lines.append("")
    lines.append("-" * 64)
    lines.append("  检测详情:")
    lines.append("-" * 64)

    if not all_results:
        lines.append("  ✅ 未检测到任何水军特征。")
    else:
        for i, r in enumerate(all_results, 1):
            lines.append(f"  {i}. {r.get('level', '?')} [{r.get('detector', 'unknown')}] (权重: {r.get('weight', 0):.2f})")
            lines.append(f"     {r.get('detail', '')}")

    lines.append("")
    lines.append("=" * 64)
    lines.append("  铁律：只标记不封禁 · 只降权不删号 · 可申诉可追溯")
    lines.append("  防御性检测，不做主动进攻。")
    lines.append("=" * 64)

    return "\n".join(lines)


# ============================================
# 主分析流程
# ============================================


def scan_comments(
    comments: List[Dict[str, Any]], source: str = ""
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """执行完整的水军检测扫描"""
    all_results: List[Dict[str, Any]] = []

    all_results.extend(detect_text_duplication(comments))
    all_results.extend(detect_account_lifecycle(comments))
    all_results.extend(detect_coordinated_behavior(comments))
    all_results.extend(detect_content_patterns(comments))
    all_results.extend(detect_ip_clustering(comments))
    all_results.extend(detect_malicious_reporting(comments))

    # IP聚类去重
    seen_ips: set[str] = set()
    deduped: List[Dict[str, Any]] = []
    for r in all_results:
        if r.get("detector", "").startswith("IP"):
            key = r.get("ip", "")
            if key in seen_ips:
                continue
            seen_ips.add(key)
        deduped.append(r)

    summary = audit_summary(deduped)
    return deduped, summary


# ============================================
# 命令行解析
# ============================================


def parse_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """解析 JSONL 文件"""
    comments: List[Dict[str, Any]] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    # 支持嵌套结构：{ "comments": [...] } 或直接数组元素
                    if "comments" in obj and isinstance(obj["comments"], list):
                        comments.extend(obj["comments"])
                    else:
                        comments.append(obj)
                elif isinstance(obj, list):
                    comments.extend(obj)
            except json.JSONDecodeError:
                # 普通文本行
                comments.append({"text": line, "timestamp": datetime.now().isoformat()})
    return comments


def parse_text_file(filepath: str) -> List[Dict[str, Any]]:
    """解析普通文本文件（每行一条评论）"""
    comments: List[Dict[str, Any]] = []
    now = datetime.now().isoformat()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            comments.append({"text": line, "timestamp": now})
    return comments


def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂水军识别引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_water_army_detect.py scan "这是一条测试评论"
  python3 bin/lh_water_army_detect.py scan-file ./test_comments.txt
  python3 bin/lh_water_army_detect.py batch ./comments.jsonl
  python3 bin/lh_water_army_detect.py rules
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # scan
    scan_parser = subparsers.add_parser("scan", help="扫描单条或少量文本")
    scan_parser.add_argument("text", nargs="+", help="要检测的文本")

    # scan-file
    scan_file_parser = subparsers.add_parser("scan-file", help="扫描文本文件")
    scan_file_parser.add_argument("file", help="文件路径（每行一条评论）")

    # batch
    batch_parser = subparsers.add_parser("batch", help="批量扫描 JSONL 文件")
    batch_parser.add_argument("file", help="JSONL 文件路径")
    batch_parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # rules
    subparsers.add_parser("rules", help="显示所有检测规则和阈值")

    args = parser.parse_args()

    if args.command == "scan":
        # 将多条文本包装为评论列表
        now = datetime.now().isoformat()
        comments = [{"text": t, "timestamp": now} for t in args.text]
        results, summary = scan_comments(comments, source="命令行输入")
        print(format_report(results, summary, "命令行输入"))

    elif args.command == "scan-file":
        filepath = args.file
        if not Path(filepath).exists():
            print(f"❌ 文件不存在: {filepath}", file=sys.stderr)
            sys.exit(1)
        comments = parse_text_file(filepath)
        if not comments:
            print(f"⚠️ 文件为空或无法解析: {filepath}", file=sys.stderr)
            sys.exit(0)
        results, summary = scan_comments(comments, source=filepath)
        print(format_report(results, summary, filepath))

    elif args.command == "batch":
        filepath = args.file
        if not Path(filepath).exists():
            print(f"❌ 文件不存在: {filepath}", file=sys.stderr)
            sys.exit(1)
        comments = parse_jsonl(filepath)
        if not comments:
            print(f"⚠️ 文件为空或无法解析: {filepath}", file=sys.stderr)
            sys.exit(0)
        results, summary = scan_comments(comments, source=filepath)

        if args.json:
            print(json.dumps({
                "dna": "#龍芯⚡️2026-07-06-WATER-ARMY-DETECT-v1.0-8A2C3F7E",
                "source": filepath,
                "total_comments": len(comments),
                "summary": summary,
                "findings": results,
                "timestamp": datetime.now().isoformat(),
            }, ensure_ascii=False, indent=2))
        else:
            print(format_report(results, summary, filepath))

    elif args.command == "rules":
        print("")
        print("=" * 64)
        print("  🐉 龍魂水军识别引擎 · 检测规则总表")
        print("=" * 64)
        print("")
        print("  六维检测体系 + 权重配置:")
        print("")
        print(f"  {'检测维度':<16} {'权重':<8} {'默认阈值':<30} {'严重度'}")
        print(f"  {'-'*16} {'-'*8} {'-'*30} {'-'*8}")
        rules_def = [
            ("完全相同内容", 0.25, f"哈希相同 ≥ {THRESHOLDS['exact_dup_count']} 次", "🔴"),
            ("高度相似内容", 0.30, f"余弦相似度 > {THRESHOLDS['similarity_threshold']}，群组 ≥ {THRESHOLDS['similarity_group_count']}", "🔴"),
            ("模板化内容", 0.15, f"模式匹配 ≥ {THRESHOLDS['template_per_hour']}/h", "🟡"),
            ("新号极限发言", 0.20, f"注册 < {THRESHOLDS['new_account_days']}天，日发言 > {THRESHOLDS['new_account_extreme']}", "🔴"),
            ("新号高频发言", 0.20, f"注册 < {THRESHOLDS['new_account_days']}天，日发言 > {THRESHOLDS['new_account_daily']}", "🟡"),
            ("休眠激活", 0.15, f"休眠 > {THRESHOLDS['dormant_days']}天，激活后 > {THRESHOLDS['dormant_activate_daily']}条", "🟡"),
            ("协同举报", 0.35, f"{THRESHOLDS['coordinated_window_min']}min内 ≥ {THRESHOLDS['coordinated_report_min']}账号举报同目标", "🔴"),
            ("协同刷评", 0.25, f"{THRESHOLDS['coordinated_spam_window']}min内 ≥ {THRESHOLDS['coordinated_spam_count']}账号评论同内容", "🟡"),
            ("定时批量发布", 0.10, f"发布间隔标准差 < {THRESHOLDS['timed_batch_stddev']}s", "🟡"),
            ("情绪操控", 0.15, f"感叹号占比 > {THRESHOLDS['exclamation_ratio']:.0%}，重复率 > {THRESHOLDS['repeat_ratio']:.0%}", "🟡"),
            ("导向性话术", 0.12, "匹配导向性话术模式库", "🟡"),
            ("语义漂移", 0.08, f"1h内 > {THRESHOLDS['semantic_drift_topics']}个不相关话题", "🟡"),
            ("IP严重聚类", 0.20, f"同IP ≥ {THRESHOLDS['ip_serious_accounts']}个账号", "🔴"),
            ("IP聚类", 0.20, f"同IP ≥ {THRESHOLDS['ip_min_accounts']}个账号", "🟡"),
            ("恶意举报", 0.30, f"举报成功率 < {THRESHOLDS['report_success_rate']:.0%}", "🟡"),
        ]
        for name, weight, threshold, level in rules_def:
            print(f"  {name:<14}  {weight:<8.2f}  {threshold:<30} {level}")
        print("")
        print("  综合判定规则:")
        print("    🔴 综合风险: 任一🔴命中 或 总权重 ≥ 0.60 → 高风险")
        print("    🟡 综合风险: 总权重 ≥ 0.20 → 中/低风险")
        print("    🟢 综合风险: 总权重 < 0.20 → 正常")
        print("")
        print("  铁律：只标记不封禁 · 只降权不删号 · 可申诉可追溯")
        print("=" * 64)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
