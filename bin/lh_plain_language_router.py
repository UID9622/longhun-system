# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·午时·离-PLAIN-LANGUAGE-ROUTER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🗣️ 龍魂·大话语义路由器 v1.0 — 无论用户怎么用大白话说，都能理解意图
DNA: #龍芯⚡️丙午·丙申·丙辰·午时·离-PLAIN-LANGUAGE-ROUTER-v1.0

核心设计：
  🇨🇳 用户用任何大白话/口语/方言/脏话说 → 语义匹配 → 找到最接近的命令意图
  ⚡ 不依赖固定触发词，靠描述理解语义
  🔒 中文轨专属，英文轨走精准匹配不经过这里

三层策略：
  1. 精确触发词匹配 → 已有的 semantic_parser 关键词路径（快）
  2. 大白话语义匹配 → 本路由器：把用户输入和所有命令描述做相似度比对（准）
  3. LLM 意图理解   → semantic_parser 的 _llm_intent_parse（兜底）

用法:
  python3 bin/lh_plain_language_router.py "咱们那个东西还在转吗"
  python3 bin/lh_plain_language_router.py "帮我把文章发出去"
  python3 bin/lh_plain_language_router.py "看看有没有什么安全问题"
  python3 bin/lh_plain_language_router.py --list
"""

import sys
import json
import os
from pathlib import Path
from typing import Optional, Tuple, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·丙申·丙辰·午时·离-PLAIN-LANGUAGE-ROUTER-v1.0"

# ═══════════════════════════════════════════════════════════════
# 意图目录 — 每个意图有名字和描述，用来做语义匹配
# 新增命令只需在这加一行，不用写触发词
# ═══════════════════════════════════════════════════════════════

INTENT_CATALOG = [
    # ── 系统状态/运行 ──
    ("系统状态", "查看系统运行状态、健康检查、还活着吗、怎么样、正常吗、跑着没、在转吗、东西还在吗、挂了没"),
    ("共生体状态", "查看共生体、知识矩阵、神经网络状态"),
    ("启动", "启动核心服务、跑起来、开机、整起来、开始干活"),
    ("停止", "停止核心服务、关掉、停机、歇了、别跑了"),
    ("重启", "重启核心服务、重来、刷新、重新跑、再来一次"),
    ("自愈", "系统自我修复、自己修一下、自己搞好、自检修复"),
    ("评估", "系统评估打分、看看系统怎么样、系统好不好"),
    # ── 安全/审计 ──
    ("审计", "全面安全审计、检查有没有问题、有没有安全问题、漏洞扫描、安全吗"),
    ("熔断状态", "查看熔断阻断安全封锁状态"),
    ("临时放行", "临时放行被阻断的域名或IP、让某个过一下、放行一下"),
    ("阻断", "封禁拉黑屏蔽域名IP、封了、屏蔽掉、拉黑"),
    ("全局熔断", "紧急全部熔断、一级戒备、全部锁死、紧急封锁"),
    ("熔断申诉", "人工审计申诉、复核、我不服、凭什么、申诉"),
    ("一票否决", "高危操作拦截、上传删除sudo密钥"),
    ("审核过滤", "三色审计、水军对抗、审核内容"),
    # ── 发文/内容 ──
    ("发文", "发布同步文章到CSDN博客、把文章发出去、推送文章、发博客"),
    ("notion同步", "同步到Notion知识库"),
    ("知识图谱", "知识图谱构建查询、知识整理"),
    # ── 编辑器/开发 ──
    ("编辑器", "打开中文代码编辑器、写代码、编程序、帮我写个功能"),
    ("记忆", "归集整理记忆、归档记住的东西、整理记忆"),
    ("帮助", "帮助信息、怎么用、命令列表、有哪些功能、能干嘛"),
    ("错误翻译", "翻译系统报错、报错什么意思、这个错误是什么"),
    # ── 签名/加密 ──
    ("签名", "给文件加GPG数字签名、签字盖章、署名"),
    ("身份验证", "验证身份、看看是谁、身份确认"),
    ("DNA验证", "DNA追溯码验证"),
    ("河图DNA", "生成DNA追溯码、打个DNA"),
    ("国密加密", "国密SM2 SM3 SM4加密引擎、国密算法"),
    # ── 人格/能力 ──
    ("人格列表", "列出所有AI人格、有哪些人格、人格清单"),
    ("能力列表", "列出所有能力、能干什么、有什么本事"),
    ("调度", "指挥调度中心、派活、安排任务"),
    # ── 控制台 ──
    ("主控台", "打开龍魂主控台路由矩阵、控制面板"),
    ("操作台", "打开操作台、记忆压缩DNA存证"),
    # ── 法律/治理 ──
    ("维权", "法律维权助手、法律援助、法律问题"),
    ("宪法", "显示系统宪法治理规则、系统规矩"),
    ("神圣锁", "显示P0永恒锁、不可改的规则"),
    ("对外不骗", "龍魂对外不骗一人、诚实原则"),
    ("大白话先讲", "行话前必先大白话、说人话"),
    # ── 情绪/决策 ──
    ("情绪海绵", "情绪温度检测、降温重写、吸收情绪、心情不好"),
    ("决策来源卡", "全链路算法透明决策来源卡、凭啥这么说、决策依据"),
    # ── 工具 ──
    ("龍芯许愿池", "人民资源池治理、缴费查询、公益"),
    ("万年历", "日程任务管理、今天有什么要做的、日程安排、日历"),
    ("记录器", "实时记录留痕、记录一下"),
    ("调度", "指挥调度中心、派活"),
]

# ═══════════════════════════════════════════════════════════════
# 语义相似度计算 — 轻量级，无外部依赖
# ═══════════════════════════════════════════════════════════════

def _char_bigrams(text: str) -> set[str]:
    """提取字符级 bigram 集合（中文友好）"""
    chars = list(text)
    return set(tuple(chars[i:i+2]) for i in range(len(chars) - 1))


def _char_overlap(a: str, b: str) -> float:
    """字符重叠率 — 用户输入中多少字符出现在描述中（反之亦然，取平均）"""
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    # 双向 Jaccard 平均，避免一方字符太少导致偏高
    score_ab = len(set_a & set_b) / len(set_a)
    score_ba = len(set_a & set_b) / len(set_b)
    return (score_ab + score_ba) / 2


def _bigram_similarity(a: str, b: str) -> float:
    """Bigram Jaccard 相似度"""
    ba = _char_bigrams(a)
    bb = _char_bigrams(b)
    if not ba or not bb:
        return 0.0
    return len(ba & bb) / len(ba | bb)


def _substring_score(text: str, desc: str) -> float:
    """描述中的词是否在用户输入中出现（逐2-4字滑动窗口比对）"""
    hits = 0
    total = 0
    for window_size in (2, 3, 4):
        for i in range(len(desc) - window_size + 1):
            token = desc[i:i+window_size]
            if len(token.strip()) >= 2 and token in text:
                hits += 1
            total += 1
    return hits / total if total > 0 else 0.0


def _similarity(a: str, b: str) -> float:
    """
    混合语义相似度（中文优化）：
    - 字符重叠 40%
    - Bigram 相似 30%
    - 子串命中 30%
    """
    return (
        _char_overlap(a, b) * 0.4
        + _bigram_similarity(a, b) * 0.3
        + _substring_score(a, b) * 0.3
    )


def _keyword_score(text: str, catalog_entry: Tuple[str, str]) -> float:
    """
    综合评分：名字匹配 + 描述匹配，加权。
    - 名字命中 权重 0.3（精确意图优先）
    - 描述命中 权重 0.7（语义理解）
    """
    name, desc = catalog_entry
    name_sim = _similarity(text, name)
    desc_sim = _similarity(text, desc)
    return name_sim * 0.3 + desc_sim * 0.7


def semantic_match(text: str, threshold: float = 0.04) -> Optional[Tuple[str, str, float]]:
    """
    对用户输入和所有意图目录做语义相似度匹配。

    返回: (命令名, 描述, 相似度分数) 或 None
    """
    candidates = []
    for name, desc in INTENT_CATALOG:
        score = _keyword_score(text, (name, desc))
        if score >= threshold:
            candidates.append((name, desc, score))

    if not candidates:
        return None

    candidates.sort(key=lambda x: -x[2])
    return candidates[0]


def match_with_fallback(text: str) -> dict[str, Any]:
    """
    完整的匹配流程：先试大话语义匹配，再试精确触发词。
    返回: {"command": ..., "name": ..., "source": ..., "score": ...}
    """
    # 1. 先试精确触发词（简单版本：名字是否包含在输入中）
    for name, desc in INTENT_CATALOG:
        if name in text:
            return {
                "command": name,
                "name": name,
                "source": "精确触发词",
                "score": 1.0,
            }

    # 2. 大话语义匹配
    result = semantic_match(text)
    if result:
        name, desc, score = result
        return {
            "command": name,
            "name": name,
            "source": "大话语义",
            "score": round(score, 4),
        }

    return {
        "command": None,
        "name": "无法识别",
        "source": "无匹配",
        "score": 0.0,
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("用法:")
        print("  python3 bin/lh_plain_language_router.py \"大白话输入\"")
        print("  python3 bin/lh_plain_language_router.py --list")
        print("  python3 bin/lh_plain_language_router.py --test")
        sys.exit(0)

    if sys.argv[1] == "--list":
        print("\n🗣️ 大话语义路由器 · 意图目录\n")
        print(f"{'命令名':<16} {'描述'}")
        print("-" * 60)
        for name, desc in INTENT_CATALOG:
            print(f"{name:<16} {desc}")
        sys.exit(0)

    if sys.argv[1] == "--test":
        tests = [
            "咱们那个东西还在转吗",
            "帮我把文章发出去",
            "看看有没有什么安全问题",
            "系统还好吗",
            "把那个IP封了",
            "紧急情况，全部锁死",
            "帮我归集一下记忆",
            "有哪些人格",
            "怎么看系统的宪法",
            "我不服，我要申诉",
            "这个文件帮我签个名",
            "翻译一下这个报错",
            "今天有什么要做的",
            "帮我写段代码",
            "帮我查个法律问题",
        ]
        print("\n🧪 大话语义匹配测试\n")
        for t in tests:
            r = match_with_fallback(t)
            print(f"  输入: {t}")
            print(f"  → {r['name']} [{r['source']}] (分数: {r['score']})")
            print()
        sys.exit(0)

    text = " ".join(sys.argv[1:])
    result = match_with_fallback(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
