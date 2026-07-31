# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_FAKE_REVIEW_DETECTOR-v1.0-4b6a829c
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh_fake_review_detector — 龍魂·虚假评论检测引擎 v1.0

专门针对虚假评论/刷评/未实名评论的深度检测

七维检测体系：
  1. 身份锚定 — 未实名/空资料/新号/虚拟号
  2. 评论-内容关联 — 评论与原文/商品的实际相关性
  3. 情感操控 — 极端好评/差评的聚类模式
  4. 模板匹配 — 模板化好评/差评识别
  5. 时间模式 — 定时刷评/集中好评/评分操纵
  6. 账号关联 — 同一团伙的账号指纹
  7. 语义空洞 — 无实质内容的占位评论

用法：
  python3 bin/lh_fake_review_detector.py --file reviews.jsonl
  python3 bin/lh_fake_review_detector.py --text "评论内容" --product "商品名"
  python3 bin/lh_fake_review_detector.py batch --dir ./reviews/

DNA: #龍芯⚡️丙午·辛未·FAKE-REVIEW-DETECTOR-v1.0-9C4B1E7D
"""

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

DNA = "#龍芯⚡️丙午·辛未·FAKE-REVIEW-DETECTOR-v1.0-9C4B1E7D"
DNA_HASH = hashlib.sha256(DNA.encode()).hexdigest()[:16]

AUDIT_GREEN = "🟢"
AUDIT_YELLOW = "🟡"
AUDIT_RED = "🔴"

# ============================================
# 检测阈值配置
# ============================================
THRESHOLDS = {
    # 身份锚定
    "min_text_length": 3,            # 最短有效评论长度
    "suspicious_name_patterns": 5,   # 可疑命名模式匹配数
    "new_account_days": 7,           # 新号阈值
    "profile_empty_ratio": 0.6,      # 空资料比例

    # 情感操控
    "extreme_rating_ratio": 0.4,     # 极端评分比例（1星或5星）
    "sentiment_cluster_size": 5,     # 情感聚类最小规模
    "sentiment_cluster_window_m": 30, # 聚类时间窗口（分钟）

    # 模板匹配
    "template_rate_threshold": 0.3,  # 模板化率阈值
    "min_template_group_size": 3,    # 模板群组最小规模

    # 时间模式
    "burst_window_minutes": 10,      # 爆发窗口
    "burst_min_count": 5,            # 爆发最小数量
    "night_active_ratio": 0.3,       # 夜间活跃比例

    # 语义空洞
    "hollow_score_threshold": 0.6,   # 空洞评分阈值
    "min_content_words": 5,          # 最少内容词数
}

# ============================================
# 虚假评论模板库
# ============================================

FAKE_REVIEW_TEMPLATES = {
    "空洞好评": [
        r"^(好|很好|非常好|太棒了|不错|还行|可以|OK|ok).{0,5}$",
        r"^(好评|好评好评|好评好评好评).{0,10}$",
        r"^(赞|顶|支持|推荐|加油).{0,5}$",
        r"^(质量很好|品质不错|值得购买|物超所值).{0,5}$",
        r"^[👍👏💪🔥❤️🎉✨💯🙏🤝🫡⭐🌟]+\s*$",
        r"^(卖家|老板|店家|客服).{0,5}(很好|不错|好评).{0,5}$",
    ],
    "空洞差评": [
        r"^(差|垃圾|烂|坑|骗|假|太差|很差|非常差).{0,5}$",
        r"^(差评|差评差评|垃圾垃圾).{0,10}$",
        r"^(千万别买|不要买|别上当|骗人的|假的).{0,5}$",
        r"^(后悔|失望|无语|醉了|服了).{0,5}$",
    ],
    "刷单好评": [
        r"^.{0,10}(质量很好|做工精细|手感不错|颜值很高|性价比高).{0,10}(推荐|好评|赞).{0,5}$",
        r"^.{0,5}(收到了|到货了|拿到了).{0,5}(很喜欢|很不错|很满意|超出预期).{0,10}$",
        r"^.{0,10}(已经用了|用了一段时间|买了好几次|回购).{0,10}(很好|推荐|不错).{0,5}$",
        r"^.{0,10}(客服|物流|包装|发货).{0,10}(很快|很好|不错|满意).{0,10}$",
        r"^.{0,15}(推荐购买|值得入手|强烈推荐|必须推荐).{0,5}$",
    ],
    "竞品抹黑": [
        r"^.{0,10}(不如|比不上|没有|差远了).{0,10}(某某|XX|某品牌|竞品).{0,10}$",
        r"^.{0,10}(还是|不如|建议).{0,5}(买|选|看看).{0,10}(某某|别的|其他|另外).{0,10}$",
        r"^.{0,10}(跟.{0,5}比|比起.{0,5}|和.{0,5}相比).{0,5}(差|垃圾|不如|不行).{0,10}$",
    ],
    "带节奏评论": [
        r"^.{0,10}(大家|所有人|每个|谁都).{0,10}(都|一定|必须|肯定).{0,10}$",
        r"^.{0,5}(不是我说|说句公道话|客观来讲|有一说一).{0,10}$",
        r"^.{0,5}(我是老用户|我是过来人|我是业内人|我是专业的).{0,10}$",
    ],
}

# ============================================
# 可疑账号命名模式
# ============================================
SUSPICIOUS_NAME_PATTERNS = [
    r"^[a-zA-Z]{1,3}\d{5,}$",          # 字母+数字流水号
    r"^user\d{5,}$",                     # user+数字
    r"^\d{11}$",                         # 手机号
    r"^tb\d{5,}$",                       # tb+数字
    r"^[A-Z][a-z]+\d{3,}$",             # 英文名+数字
    r"^(用户|匿名|游客|路人).{0,5}$",       # 默认命名
    r"^.{20,}$",                          # 超长随机名
    r"^[a-zA-Z0-9_]{8,}$",               # 纯字母数字
]


# ============================================
# 核心检测函数
# ============================================

def detect_identity_anchor(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """身份锚定检测 — 未实名/空资料/虚拟号"""
    findings = []
    total = len(reviews)

    unverified = 0
    empty_profile = 0
    suspicious_name = 0
    new_account = 0
    default_avatar = 0

    for r in reviews:
        user = r.get("user", {})
        if isinstance(user, dict):
            if not user.get("verified", True):
                unverified += 1
            if not user.get("profile_complete", True) or not user.get("bio"):
                empty_profile += 1
            if not user.get("avatar") or user.get("avatar") == "default":
                default_avatar += 1

            reg_time = user.get("registration_time") or user.get("created_at")
            if reg_time:
                try:
                    reg_dt = datetime.fromisoformat(str(reg_time).replace("Z", "+00:00"))
                    if (datetime.now().astimezone() - reg_dt).days < THRESHOLDS["new_account_days"]:
                        new_account += 1
                except (ValueError, TypeError):
                    pass

            name = user.get("name", user.get("nickname", ""))
            for pattern in SUSPICIOUS_NAME_PATTERNS:
                if re.search(pattern, str(name)):
                    suspicious_name += 1
                    break

    # 未实名
    if unverified > total * 0.5:
        findings.append({
            "type": "未实名比例异常",
            "level": AUDIT_RED,
            "weight": 0.30,
            "count": unverified,
            "ratio": round(unverified / max(total, 1), 2),
            "detail": f"未实名评论 {unverified}/{total}，占比 {unverified/max(total,1):.0%}",
        })

    # 空资料
    if empty_profile > total * THRESHOLDS["profile_empty_ratio"]:
        findings.append({
            "type": "空资料账号异常",
            "level": AUDIT_YELLOW,
            "weight": 0.20,
            "count": empty_profile,
            "ratio": round(empty_profile / max(total, 1), 2),
            "detail": f"空资料/无简介账号 {empty_profile} 个",
        })

    # 可疑命名
    if suspicious_name > total * 0.3:
        findings.append({
            "type": "可疑命名模式",
            "level": AUDIT_YELLOW,
            "weight": 0.15,
            "count": suspicious_name,
            "detail": f"可疑命名模式（流水号/随机字符）{suspicious_name} 个",
        })

    # 新号
    if new_account > total * 0.3:
        findings.append({
            "type": "新号集中评论",
            "level": AUDIT_RED,
            "weight": 0.25,
            "count": new_account,
            "detail": f"注册不足{THRESHOLDS['new_account_days']}天新号 {new_account} 个",
        })

    return findings


def detect_content_relevance(
    reviews: List[Dict[str, Any]],
    target_content: Optional[str] = None,
    target_keywords: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """评论与内容关联检测"""
    findings = []

    if not target_content and not target_keywords:
        return findings

    keywords = target_keywords or []
    if target_content:
        # 提取目标内容的关键词（简化：高频词）
        words = re.findall(r'[\u4e00-\u9fff]{2,}', target_content)
        kw_counter = Counter(words)
        keywords = [w for w, _ in kw_counter.most_common(10)]

    # 检测评论是否与目标内容相关
    irrelevant_count = 0
    for r in reviews:
        text = r.get("text", "")
        if len(text) < THRESHOLDS["min_text_length"]:
            irrelevant_count += 1
            continue
        relevance = sum(1 for kw in keywords if kw in text)
        if relevance == 0 and len(text) > 20:
            irrelevant_count += 1

    if irrelevant_count > len(reviews) * 0.4:
        findings.append({
            "type": "评论-内容不相关",
            "level": AUDIT_YELLOW,
            "weight": 0.18,
            "count": irrelevant_count,
            "ratio": round(irrelevant_count / max(len(reviews), 1), 2),
            "detail": f"{irrelevant_count} 条评论与目标内容无明显关联，疑似批量灌水",
        })

    return findings


def detect_sentiment_manipulation(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """情感操控检测 — 极端评分/情感聚类"""
    findings = []

    ratings = []
    for r in reviews:
        rating = r.get("rating", r.get("score"))
        if rating is not None:
            try:
                ratings.append(float(rating))
            except (ValueError, TypeError):
                pass

    if ratings:
        max_rating = max(ratings)
        extreme_count = sum(1 for r in ratings if r <= 1 or r >= max_rating)
        extreme_ratio = extreme_count / len(ratings)

        if extreme_ratio > THRESHOLDS["extreme_rating_ratio"]:
            findings.append({
                "type": "极端评分操控",
                "level": AUDIT_RED,
                "weight": 0.28,
                "extreme_count": extreme_count,
                "extreme_ratio": round(extreme_ratio, 2),
                "detail": f"极端评分（最低/最高）占比 {extreme_ratio:.0%}，疑似评分操纵",
            })

        # 评分分布检测
        unique_ratings = set(ratings)
        if len(unique_ratings) <= 2 and len(ratings) >= 5:
            findings.append({
                "type": "评分单一化",
                "level": AUDIT_YELLOW,
                "weight": 0.15,
                "unique_ratings": len(unique_ratings),
                "detail": f"仅有 {len(unique_ratings)} 种评分值，缺乏多样性，疑似刷分",
            })

    # 情感聚类时间检测
    timestamps = []
    for r in reviews:
        t = r.get("timestamp") or r.get("time") or r.get("created_at")
        if t:
            try:
                timestamps.append(datetime.fromisoformat(str(t).replace("Z", "+00:00")))
            except (ValueError, TypeError):
                pass

    if len(timestamps) >= THRESHOLDS["sentiment_cluster_size"]:
        sorted_ts = sorted(timestamps)
        window = timedelta(minutes=THRESHOLDS["sentiment_cluster_window_m"])
        max_cluster = 0
        current = 1

        for i in range(1, len(sorted_ts)):
            if sorted_ts[i] - sorted_ts[i - 1] <= window:
                current += 1
            else:
                max_cluster = max(max_cluster, current)
                current = 1
        max_cluster = max(max_cluster, current)

        if max_cluster >= THRESHOLDS["sentiment_cluster_size"]:
            findings.append({
                "type": "集中评论时间聚类",
                "level": AUDIT_YELLOW,
                "weight": 0.18,
                "cluster_size": max_cluster,
                "window_minutes": THRESHOLDS["sentiment_cluster_window_m"],
                "detail": f"{THRESHOLDS['sentiment_cluster_window_m']}分钟内 {max_cluster} 条集中评论，疑似刷评",
            })

    return findings


def detect_template_reviews(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """模板化评论检测"""
    findings = []

    template_hits: Dict[str, List[int]] = defaultdict(list)
    for i, r in enumerate(reviews):
        text = r.get("text", "")
        if len(text) < THRESHOLDS["min_text_length"]:
            continue
        for category, patterns in FAKE_REVIEW_TEMPLATES.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    template_hits[category].append(i)
                    break

    for category, indices in template_hits.items():
        if len(indices) >= THRESHOLDS["min_template_group_size"]:
            findings.append({
                "type": f"模板化评论-{category}",
                "level": AUDIT_YELLOW,
                "weight": 0.18,
                "count": len(indices),
                "ratio": round(len(indices) / max(len(reviews), 1), 2),
                "sample_texts": [reviews[i].get("text", "")[:50] for i in indices[:3]],
                "detail": f"检测到 {len(indices)} 条'{category}'模板化评论",
            })

    # 检查整体模板化率
    total_template = sum(len(indices) for indices in template_hits.values())
    template_rate = total_template / max(len(reviews), 1)
    if template_rate > THRESHOLDS["template_rate_threshold"]:
        findings.append({
            "type": "整体模板化率过高",
            "level": AUDIT_RED if template_rate > 0.5 else AUDIT_YELLOW,
            "weight": 0.25,
            "rate": round(template_rate, 2),
            "detail": f"整体模板化率 {template_rate:.0%}，远超正常水平",
        })

    return findings


def detect_temporal_patterns(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """时间模式异常检测"""
    findings = []

    timestamps = []
    for r in reviews:
        t = r.get("timestamp") or r.get("time") or r.get("created_at")
        if t:
            try:
                timestamps.append(datetime.fromisoformat(str(t).replace("Z", "+00:00")))
            except (ValueError, TypeError):
                pass

    if not timestamps:
        return findings

    # 爆发检测
    sorted_ts = sorted(timestamps)
    burst_windows: List[int] = []
    window = timedelta(minutes=THRESHOLDS["burst_window_minutes"])

    i = 0
    while i < len(sorted_ts):
        window_end = sorted_ts[i] + window
        count = 1
        j = i + 1
        while j < len(sorted_ts) and sorted_ts[j] <= window_end:
            count += 1
            j += 1
        if count >= THRESHOLDS["burst_min_count"]:
            burst_windows.append(count)
        i += 1

    if burst_windows:
        max_burst = max(burst_windows)
        findings.append({
            "type": "评论爆发",
            "level": AUDIT_RED if max_burst >= 10 else AUDIT_YELLOW,
            "weight": 0.22,
            "burst_windows": len(burst_windows),
            "max_burst": max_burst,
            "detail": f"检测到 {len(burst_windows)} 次评论爆发，最大 {max_burst} 条/{THRESHOLDS['burst_window_minutes']}分钟",
        })

    # 夜间活跃检测
    night_hours = sum(1 for t in timestamps if t.hour < 6 or t.hour >= 23)
    night_ratio = night_hours / len(timestamps)
    if night_ratio > THRESHOLDS["night_active_ratio"]:
        findings.append({
            "type": "夜间异常活跃",
            "level": AUDIT_YELLOW,
            "weight": 0.12,
            "night_ratio": round(night_ratio, 2),
            "detail": f"深夜/凌晨评论占比 {night_ratio:.0%}，疑似机器刷评",
        })

    # 间隔规律性检测
    if len(sorted_ts) >= 5:
        intervals = [(sorted_ts[i] - sorted_ts[i - 1]).total_seconds() for i in range(1, len(sorted_ts))]
        if intervals:
            import math
            avg = sum(intervals) / len(intervals)
            variance = sum((x - avg) ** 2 for x in intervals) / len(intervals)
            std = math.sqrt(variance)
            if avg > 0 and std / avg < 0.1 and len(intervals) >= 5:
                findings.append({
                    "type": "定时规律发布",
                    "level": AUDIT_YELLOW,
                    "weight": 0.15,
                    "avg_interval_seconds": round(avg, 1),
                    "std_ratio": round(std / max(avg, 0.001), 3),
                    "detail": f"发布间隔高度规律（标准差/均值={std/avg:.3f}），疑似定时脚本",
                })

    return findings


def detect_account_fingerprint(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """账号指纹关联检测"""
    findings = []

    # 检测同一设备/浏览器指纹
    fingerprints: Dict[str, List[int]] = defaultdict(list)
    for i, r in enumerate(reviews):
        fp = r.get("fingerprint") or r.get("device_id") or r.get("browser_fingerprint")
        if fp:
            fingerprints[fp].append(i)

    shared_fp = {fp: indices for fp, indices in fingerprints.items() if len(indices) >= 2}
    if shared_fp:
        max_shared = max(len(indices) for indices in shared_fp.values())
        findings.append({
            "type": "设备指纹共享",
            "level": AUDIT_RED if max_shared >= 5 else AUDIT_YELLOW,
            "weight": 0.25,
            "shared_fingerprints": len(shared_fp),
            "max_accounts_per_fp": max_shared,
            "detail": f"检测到 {len(shared_fp)} 个设备指纹被多账号共享，最多 {max_shared} 个账号共用",
        })

    # 检测文本相似度（使用简单哈希）
    text_hashes: Dict[str, List[int]] = defaultdict(list)
    for i, r in enumerate(reviews):
        text = r.get("text", "")
        if len(text) < 10:
            continue
        h = hashlib.md5(text.strip().encode()).hexdigest()
        text_hashes[h].append(i)

    dup_texts = {h: indices for h, indices in text_hashes.items() if len(indices) >= 2}
    if dup_texts:
        findings.append({
            "type": "完全重复评论",
            "level": AUDIT_RED,
            "weight": 0.30,
            "dup_text_count": len(dup_texts),
            "detail": f"发现 {len(dup_texts)} 组完全相同的评论，疑似复制粘贴刷评",
        })

    return findings


def detect_semantic_hollowness(reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """语义空洞检测 — 无实质内容的占位评论"""
    findings = []

    hollow_scores = []
    for r in reviews:
        text = r.get("text", "")
        if len(text) < THRESHOLDS["min_text_length"]:
            hollow_scores.append(1.0)
            continue

        # 计算内容词比例
        content_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(text)
        content_ratio = content_chars / max(total_chars, 1)

        # 计算唯一字符比例
        unique_chars = len(set(text))
        unique_ratio = unique_chars / max(total_chars, 1)

        # 感叹号/表情比例
        emoji_count = len(re.findall(r'[!！👍👏💪🔥❤️🎉✨💯🙏]', text))
        emoji_ratio = emoji_count / max(total_chars, 1)

        # 空洞评分：内容词少 + 高重复 + 多表情 = 空洞
        hollow = (1 - content_ratio) * 0.5 + (1 - unique_ratio) * 0.3 + emoji_ratio * 0.2
        hollow_scores.append(hollow)

    high_hollow = sum(1 for s in hollow_scores if s > THRESHOLDS["hollow_score_threshold"])
    hollow_ratio = high_hollow / max(len(reviews), 1)

    if hollow_ratio > 0.3:
        findings.append({
            "type": "语义空洞评论",
            "level": AUDIT_YELLOW,
            "weight": 0.15,
            "hollow_count": high_hollow,
            "hollow_ratio": round(hollow_ratio, 2),
            "detail": f"{high_hollow} 条评论语义空洞（无实质内容），占比 {hollow_ratio:.0%}",
        })

    return findings


# ============================================
# 主检测入口
# ============================================

def detect_fake_reviews(
    reviews: List[Dict[str, Any]],
    target_content: Optional[str] = None,
    target_keywords: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """虚假评论检测主入口"""
    all_findings = []

    all_findings.extend(detect_identity_anchor(reviews))
    all_findings.extend(detect_content_relevance(reviews, target_content, target_keywords))
    all_findings.extend(detect_sentiment_manipulation(reviews))
    all_findings.extend(detect_template_reviews(reviews))
    all_findings.extend(detect_temporal_patterns(reviews))
    all_findings.extend(detect_account_fingerprint(reviews))
    all_findings.extend(detect_semantic_hollowness(reviews))

    # 汇总
    total_weight = sum(f.get("weight", 0) for f in all_findings)
    red_count = sum(1 for f in all_findings if f.get("level") == AUDIT_RED)
    yellow_count = sum(1 for f in all_findings if f.get("level") == AUDIT_YELLOW)

    if red_count >= 2 or total_weight >= 0.8:
        overall_level = AUDIT_RED
        verdict = "高度疑似虚假评论/刷评团伙，建议立即处理"
    elif red_count >= 1 or total_weight >= 0.4:
        overall_level = AUDIT_YELLOW
        verdict = "存在虚假评论嫌疑，建议人工复核"
    elif yellow_count > 0:
        overall_level = AUDIT_YELLOW
        verdict = "存在轻度异常，持续观察"
    else:
        overall_level = AUDIT_GREEN
        verdict = "评论质量正常，未发现显著虚假特征"

    return {
        "phase": "虚假评论检测",
        "status": "completed",
        "dna": DNA,
        "level": overall_level,
        "verdict": verdict,
        "total_reviews": len(reviews),
        "findings_count": len(all_findings),
        "red_count": red_count,
        "yellow_count": yellow_count,
        "total_weight": round(total_weight, 3),
        "findings": all_findings,
        "timestamp": datetime.now().isoformat(),
    }


# ============================================
# 格式化输出
# ============================================

def format_report(result: Dict[str, Any]) -> str:
    """格式化检测报告"""
    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 龍魂·虚假评论检测引擎 · 审计报告")
    lines.append("=" * 64)
    lines.append(f"  DNA: {DNA}")
    lines.append(f"  评论总数: {result.get('total_reviews', 0)}")
    lines.append(f"  判定: {result.get('level', '?')}  {result.get('verdict', '')}")
    lines.append(f"  发现问题: {result.get('findings_count', 0)} 个")
    lines.append(f"    🔴 严重: {result.get('red_count', 0)}")
    lines.append(f"    🟡 可疑: {result.get('yellow_count', 0)}")
    lines.append(f"  综合权重: {result.get('total_weight', 0):.2f}")
    lines.append("")

    findings = result.get("findings", [])
    if findings:
        lines.append("-" * 64)
        lines.append("  检测详情:")
        lines.append("-" * 64)
        for i, f in enumerate(findings, 1):
            lines.append(f"  {i}. {f['level']} [{f['type']}] (权重: {f.get('weight', 0):.2f})")
            lines.append(f"     {f['detail']}")
            if f.get("sample_texts"):
                for st in f["sample_texts"][:2]:
                    lines.append(f"     样本: \"{st}\"")
    else:
        lines.append("  ✅ 未检测到虚假评论特征。")

    lines.append("")
    lines.append("=" * 64)
    lines.append("  虚假评论 = 数字欺诈 · 未实名=无责任 · 刷评=欺骗消费者")
    lines.append("=" * 64)

    return "\n".join(lines)


# ============================================
# 命令行入口
# ============================================

def parse_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """解析JSONL文件"""
    reviews: List[Dict[str, Any]] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    reviews.append(obj)
                elif isinstance(obj, list):
                    reviews.extend(obj)
            except json.JSONDecodeError:
                reviews.append({"text": line, "timestamp": datetime.now().isoformat()})
    return reviews


def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂·虚假评论检测引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 文件检测
    file_parser = subparsers.add_parser("file", help="检测JSONL文件")
    file_parser.add_argument("--file", required=True, help="JSONL文件路径")
    file_parser.add_argument("--target", help="目标内容（检测评论相关性）")
    file_parser.add_argument("--keywords", nargs="*", help="目标关键词")

    # 单条检测
    text_parser = subparsers.add_parser("text", help="检测单条评论")
    text_parser.add_argument("--text", required=True, help="评论文本")
    text_parser.add_argument("--user", help="用户信息JSON")

    # JSON输出
    json_parser = subparsers.add_parser("json", help="直接传入JSON数据")
    json_parser.add_argument("--data", required=True, help="JSON评论数组字符串")

    args = parser.parse_args()

    if args.command == "file":
        reviews = parse_jsonl(args.file)
        if not reviews:
            print(f"⚠️ 未解析到有效评论: {args.file}", file=sys.stderr)
            sys.exit(0)
        result = detect_fake_reviews(
            reviews,
            target_content=args.target,
            target_keywords=args.keywords,
        )
        print(format_report(result))

    elif args.command == "text":
        user_info = {}
        if args.user:
            try:
                user_info = json.loads(args.user)
            except json.JSONDecodeError:
                pass

        review = {"text": args.text, "user": user_info, "timestamp": datetime.now().isoformat()}
        result = detect_fake_reviews([review])
        print(format_report(result))

    elif args.command == "json":
        reviews = json.loads(args.data)
        if isinstance(reviews, dict):
            reviews = [reviews]
        result = detect_fake_reviews(reviews)
        print(format_report(result))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
