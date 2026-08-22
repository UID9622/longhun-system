#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·语义反馈引擎 v1.0 — 一言既出·驷马难追

不是在翻译器上再加一层冷冰冰的规则。
是让有信誉的人来校准语义——一个人说"这个词是这个意思"，
高信誉的人说的话权重更重，争议大的条目自动标记待审。

DNA: #龍芯⚡️丙午·乙未·戊午·申时·䷤家人-FEEDBACK-ENGINE-v1.0

核心原则：
  🀄 一言既出，驷马难追 — 反馈永久留存，不可删改，只能追加新反馈
  ⚖️ 信誉加权 — 不是人人平等投票，而是人品高的人话语权重自然高
  🔍 争议透明 — 有争议的条目标记出来，不是隐藏掉
  🙋 人人可说话 — 每个人的意见都值得尊重，但权重取决于人品

三层评分体系：
  ① 个人评分 → 1-5星 + 文字说明
  ② 信誉加权 → 评分×信誉系数 = 有效评分
  ③ 共识分 → 所有有效评分的加权平均 → 反映"大家怎么说"

用法：
  from bin.lh_semantic_feedback_engine import 语义反馈引擎
  fb = 语义反馈引擎()

  # 添加反馈
  fb.添加反馈("统一", "入口/界面", "user_dna_hash", 5, "这个理解很准")

  # 查共识
  consensus = fb.查共识("统一", "入口/界面")

  # 争议列表
  disputed = fb.争议条目()

  # 命令行
  python3 bin/lh_semantic_feedback_engine.py --consensus 统一 入口/界面
  python3 bin/lh_semantic_feedback_engine.py --disputed
"""

import json
import time
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import defaultdict

DNA = "#龍芯⚡️丙午·乙未·戊午·申时·䷤家人-FEEDBACK-ENGINE-v1.0"
ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = ROOT / "L7_数据层" / "semantic_feedback_ledger.json"
TRUST_REGISTRY_PATH = ROOT / "L7_数据层" / "trust_score_registry.json"

# ── 评分常数 ──
MAX_RATING = 5
MIN_TRUST_FOR_FULL_WEIGHT = 50  # 信任分 ≥50 = 满分话语权
MIN_TRUST_FOR_VOICE = 5         # 信任分 <5 = 低权但仍有话语权
CONTROVERSY_STDDEV_THRESHOLD = 1.5  # 标准差 >1.5 → 争议中
LOW_CONSENSUS_THRESHOLD = 2.5       # 共识分 <2.5 → 质量存疑


class 语义反馈引擎:
    """
    语义反馈采集·信誉加权·争议检测。
    一言既出驷马难追——所有反馈永久append-only。
    """

    def __init__(self):
        self.ledger = self._加载账本()
        self.trust_registry = self._加载信任注册表()

    # ═══════════════════════════════════════
    # 数据加载
    # ═══════════════════════════════════════

    def _加载账本(self) -> Dict[str, Any]:
        if LEDGER_PATH.exists():
            try:
                return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "_meta": {
                "title": "🐉 龍魂·语义反馈账本 — 一言既出·驷马难追",
                "version": "v1.0",
                "DNA": DNA,
                "principle": "所有反馈永久append-only，不可删改。信誉高者话语权重自然重。",
                "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            "feedback": {},  # {"统一::入口/界面": [feedbacks]}
        }

    def _保存账本(self):
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_text(json.dumps(self.ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    def _加载信任注册表(self) -> Dict[str, float]:
        """从信任积分注册表加载用户信誉分。若不存在则创建空表。"""
        if TRUST_REGISTRY_PATH.exists():
            try:
                data = json.loads(TRUST_REGISTRY_PATH.read_text(encoding="utf-8"))
                return data.get("users", {})
            except Exception:
                pass
        # 创建默认注册表
        default = {
            "_meta": {"title": "龍魂·信任积分注册表", "note": "user_dna_hash → trust_score"},
            "users": {}
        }
        TRUST_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        TRUST_REGISTRY_PATH.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return {}

    def _获取用户信誉(self, user_dna: str) -> float:
        """查询用户信誉分，无记录则返回基线分10"""
        return self.trust_registry.get(user_dna, 10.0)

    def _信誉权重(self, trust_score: float) -> float:
        """
        信誉 → 话语权重 映射函数。
        信任分≥50 → 权重1.0（一言九鼎）
        信任分 5-50 → 线性映射 (0.2~1.0)
        信任分<5 → 最低0.1（仍有微弱话语权，不被静音）
        """
        if trust_score >= MIN_TRUST_FOR_FULL_WEIGHT:
            return 1.0
        if trust_score < MIN_TRUST_FOR_VOICE:
            return 0.1
        return 0.2 + 0.8 * (trust_score - MIN_TRUST_FOR_VOICE) / (MIN_TRUST_FOR_FULL_WEIGHT - MIN_TRUST_FOR_VOICE)

    # ═══════════════════════════════════════
    # 核心 API
    # ═══════════════════════════════════════

    def _entry_key(self, word: str, context_type: str) -> str:
        return f"{word}::{context_type}"

    def 添加反馈(self, word: str, context_type: str, user_dna: str,
               rating: int, comment: str = "", user_name: str = "") -> Dict[str, Any]:
        """
        添加一条语义反馈。一言既出驷马难追——不可删改。

        Args:
            word: 关键词（如"统一"）
            context_type: 语境类型（如"入口/界面"）
            user_dna: 用户DNA哈希
            rating: 1-5星评分
            comment: 文字反馈
            user_name: 可选用户名

        Returns:
            {"status": "ok", "feedback_dna": "...", "weight": 0.85}
        """
        # 校验评分
        rating = max(1, min(MAX_RATING, int(rating)))

        # 查信誉
        trust = self._获取用户信誉(user_dna)
        weight = self._信誉权重(trust)

        key = self._entry_key(word, context_type)

        entry = {
            "user_dna": user_dna,
            "user_name": user_name or f"用户-{user_dna[:8]}",
            "trust_score": trust,
            "weight": round(weight, 3),
            "rating": rating,
            "effective_rating": round(rating * weight, 2),
            "comment": comment,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "feedback_dna": f"#龍芯⚡️FB-{word}-{context_type.replace('/', '-')}-{user_dna[:8]}-{int(time.time()) % 10000:04d}",
            "status": "active",  # active | disputed | resolved
        }

        self.ledger.setdefault("feedback", {}).setdefault(key, []).append(entry)
        self._保存账本()

        return {
            "status": "ok",
            "feedback_dna": entry["feedback_dna"],
            "weight": weight,
            "trust_score": trust,
        }

    def 查反馈(self, word: str, context_type: str) -> List[Dict[str, Any]]:
        """查某个语义条目的所有反馈"""
        key = self._entry_key(word, context_type)
        return self.ledger.get("feedback", {}).get(key, [])

    def 查共识(self, word: str, context_type: str) -> Dict[str, Any]:
        """
        计算某个语义条目的共识分数。

        Returns:
            {
                "word": "统一",
                "context_type": "入口/界面",
                "consensus_score": 4.2,       # 信誉加权平均分
                "total_ratings": 12,           # 总评分数
                "total_weight": 9.5,           # 总话语权重
                "controversy_level": "low",    # low | medium | high
                "stddev": 0.8,                 # 标准差
                "top_voices": [...],            # 高信誉用户的反馈
                "recent_feedback": [...],       # 最近5条
            }
        """
        entries = self.查反馈(word, context_type)
        if not entries:
            return {
                "word": word,
                "context_type": context_type,
                "consensus_score": 0,
                "total_ratings": 0,
                "total_weight": 0,
                "controversy_level": "no_data",
                "stddev": 0,
                "message": "暂无反馈数据，这条语义映射还未经人校准",
            }

        # 计算加权平均
        weights = [e["weight"] for e in entries]
        ratings = [e["rating"] for e in entries]
        effective = [e["effective_rating"] for e in entries]

        total_weight = sum(weights)
        if total_weight > 0:
            consensus = sum(effective) / total_weight
        else:
            consensus = sum(ratings) / len(ratings)

        # 计算加权标准差
        mean = sum(r * w for r, w in zip(ratings, weights)) / total_weight if total_weight > 0 else sum(ratings) / len(ratings)
        variance = sum(w * (r - mean) ** 2 for r, w in zip(ratings, weights)) / total_weight if total_weight > 0 else 0
        stddev = variance ** 0.5

        # 争议等级
        if stddev > CONTROVERSY_STDDEV_THRESHOLD:
            controversy = "high"
        elif stddev > 1.0:
            controversy = "medium"
        else:
            controversy = "low"

        # 质量警告
        if consensus < LOW_CONSENSUS_THRESHOLD and len(entries) >= 3:
            controversy = "high"  # 评分太低 → 升级为高争议

        # 高信誉用户的声音（信任分≥50）
        top_voices = sorted(
            [e for e in entries if e["trust_score"] >= MIN_TRUST_FOR_FULL_WEIGHT],
            key=lambda e: -e["trust_score"]
        )[:5]

        # 最近反馈
        recent = sorted(entries, key=lambda e: e["timestamp"], reverse=True)[:5]

        return {
            "word": word,
            "context_type": context_type,
            "consensus_score": round(consensus, 2),
            "raw_avg": round(sum(ratings) / len(ratings), 2),
            "total_ratings": len(entries),
            "total_weight": round(total_weight, 2),
            "controversy_level": controversy,
            "stddev": round(stddev, 2),
            "top_voices": top_voices,
            "recent_feedback": recent,
            "quality_note": self._质量说明(consensus, controversy),
        }

    def 争议条目(self, threshold: str = "all") -> List[Dict[str, Any]]:
        """
        列出争议/低分的语义条目。

        Args:
            threshold: "high" (高争议) | "medium" (中等) | "all" (全部争议)
        """
        results = []
        feedback = self.ledger.get("feedback", {})

        for key, entries in feedback.items():
            word, context_type = key.split("::", 1)
            consensus = self.查共识(word, context_type)

            if consensus["total_ratings"] == 0:
                continue

            level = consensus["controversy_level"]
            if threshold == "high" and level != "high":
                continue
            if threshold == "medium" and level not in ("medium", "high"):
                continue
            if level == "low":
                continue

            results.append(consensus)

        # 按争议程度排序：高争议在前
        results.sort(key=lambda r: (
            0 if r["controversy_level"] == "high" else 1,
            r["stddev"],
            -r["consensus_score"],
        ))

        return results

    def 全局统计(self) -> Dict[str, Any]:
        """反馈系统的全局统计"""
        fb = self.ledger.get("feedback", {})
        total_entries = sum(len(v) for v in fb.values())
        total_keys = len(fb)

        # 争议统计
        disputed_high = len(self.争议条目("high"))
        disputed_medium = len(self.争议条目("medium"))

        # 词维度统计
        word_stats: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0.0, "avg_rating": 0.0})
        for key, entries in fb.items():
            word, _ = key.split("::", 1)
            word_stats[word]["count"] += len(entries)
            word_stats[word]["avg_rating"] += sum(e["rating"] for e in entries)

        for w in word_stats:
            word_stats[w]["avg_rating"] = round(word_stats[w]["avg_rating"] / word_stats[w]["count"], 2)

        most_feedbacked = sorted(word_stats.items(), key=lambda x: -x[1]["count"])[:10]

        return {
            "总反馈条数": total_entries,
            "覆盖语义条目数": total_keys,
            "高争议条目": disputed_high,
            "中等争议条目": disputed_medium,
            "反馈最多的词Top10": [(w, s["count"], s["avg_rating"]) for w, s in most_feedbacked],
        }

    # ═══════════════════════════════════════
    # 辅助
    # ═══════════════════════════════════════

    def _质量说明(self, consensus: float, controversy: str) -> str:
        """根据共识分和争议等级给出自然语言说明"""
        if consensus == 0:
            return "🌟 这条语义映射还未有人校准，诚邀你留下第一条反馈。"
        if controversy == "high":
            return "⚠️ 这条语义映射存在较大争议，建议人工复核。不同人理解差异大，暂不宜作为唯一参考。"
        if controversy == "medium":
            return "📋 这条语义映射有轻微争议，多数人基本认同但存在不同声音。"
        return "✅ 大家对这条语义理解基本一致，可作为可靠参考。"

    # ═══════════════════════════════════════
    # 注册用户信任分
    # ═══════════════════════════════════════

    def 注册用户信任(self, user_dna: str, trust_score: float, user_name: str = ""):
        """手动注册/更新用户信任分"""
        self.trust_registry[user_dna] = trust_score
        data = self._加载信任注册表_原始()
        if data is None:
            data = {"_meta": {}, "users": {}}
        data["users"][user_dna] = trust_score
        if user_name:
            data.setdefault("names", {})[user_dna] = user_name
        TRUST_REGISTRY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _加载信任注册表_原始(self) -> Optional[Dict[str, Any]]:
        if TRUST_REGISTRY_PATH.exists():
            try:
                return json.loads(TRUST_REGISTRY_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        return None


# ═══════════════════════════════════════
# CLI
# ═══════════════════════════════════════

if __name__ == "__main__":
    fb = 语义反馈引擎()

    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("\n命令：")
        print("  python3 bin/lh_semantic_feedback_engine.py --consensus <词> <语境>")
        print("  python3 bin/lh_semantic_feedback_engine.py --disputed")
        print("  python3 bin/lh_semantic_feedback_engine.py --stats")
        print("  python3 bin/lh_semantic_feedback_engine.py --demo    # 演示数据")
        sys.exit(0)

    if sys.argv[1] == "--consensus":
        if len(sys.argv) < 4:
            print("用法: --consensus <词> <语境>")
            sys.exit(1)
        result = fb.查共识(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif sys.argv[1] == "--disputed":
        results = fb.争议条目()
        if not results:
            print("🟢 暂无争议条目")
        else:
            print(f"🔍 争议条目（{len(results)}个）:\n")
            for r in results:
                level_icon = "🔴" if r["controversy_level"] == "high" else "🟡"
                print(f"  {level_icon} {r['word']} :: {r['context_type']}")
                print(f"     共识分={r['consensus_score']} 标准差={r['stddev']} 评分人数={r['total_ratings']}")
                print(f"     {r.get('quality_note', '')}\n")

    elif sys.argv[1] == "--stats":
        stats = fb.全局统计()
        for k, v in stats.items():
            print(f"{k}: {v}")

    elif sys.argv[1] == "--demo":
        print("🔧 生成演示反馈数据...\n")

        # 先注册几个模拟用户（不同信任等级）
        fb.注册用户信任("uid9622_master_hash", 95.0, "UID9622·诸葛鑫")
        fb.注册用户信任("high_trust_contributor_a", 72.0, "高信誉贡献者A")
        fb.注册用户信任("mid_trust_user_b", 35.0, "中等信誉用户B")
        fb.注册用户信任("new_user_c", 8.0, "新用户C")
        fb.注册用户信任("low_trust_visitor_d", 3.0, "游客D")

        # 场景1: 高共识条目 "统一 :: 入口/界面"
        fb.添加反馈("统一", "入口/界面", "uid9622_master_hash", 5, "入口统一是系统设计初衷，这个理解很准。")
        fb.添加反馈("统一", "入口/界面", "high_trust_contributor_a", 5, "完全符合系统设计理念。")
        fb.添加反馈("统一", "入口/界面", "mid_trust_user_b", 4, "大部分人理解一致，少数情况可能是指数据统一。")
        fb.添加反馈("统一", "入口/界面", "new_user_c", 4, "我觉得挺对的。")

        # 场景2: 争议条目 "统一 :: 数据/同步"
        fb.添加反馈("统一", "数据/同步", "uid9622_master_hash", 4, "多数情况是对的，但'统一'在数据语境有时也指格式统一。")
        fb.添加反馈("统一", "数据/同步", "high_trust_contributor_a", 2, "数据统一更多是指数据格式标准化，不是合并视图。")
        fb.添加反馈("统一", "数据/同步", "mid_trust_user_b", 5, "我就觉得数据统一就是合并视图，没毛病。")

        # 场景3: 低分条目 "对齐 :: 命令/脚本"
        fb.添加反馈("对齐", "命令/脚本", "uid9622_master_hash", 1, "'对齐'不是对齐命令，是对齐UID9622这个人——他的价值观。这个语境归类错了。")
        fb.添加反馈("对齐", "命令/脚本", "high_trust_contributor_a", 2, "同意，'对齐'在命令语境下意义很弱。")
        fb.添加反馈("对齐", "命令/脚本", "mid_trust_user_b", 3, "勉强能用但不是最佳理解。")

        # 场景4: 收口语境高共识
        fb.添加反馈("收口", "窗口管理", "uid9622_master_hash", 5, "守恒收口——这是龍魂系统核心术语，理解完全正确。")
        fb.添加反馈("收口", "窗口管理", "high_trust_contributor_a", 5, "系统内大家都懂这个意思。")

        # 打印共识结果
        for word, ctx in [("统一", "入口/界面"), ("统一", "数据/同步"), ("对齐", "命令/脚本"), ("收口", "窗口管理")]:
            r = fb.查共识(word, ctx)
            level_icon = {"low": "🟢", "medium": "🟡", "high": "🔴", "no_data": "⚪"}[r["controversy_level"]]
            print(f"{level_icon} {word} :: {ctx}")
            print(f"   共识分={r['consensus_score']}/5  原始均分={r['raw_avg']}  人数={r['total_ratings']}  标准差={r['stddev']}")
            print(f"   高信誉声音: {[v['user_name'] for v in r['top_voices']]}")
            print(f"   说明: {r.get('quality_note', '')}\n")

        # 全局统计
        stats = fb.全局统计()
        print(f"📊 全局: 总反馈={stats['总反馈条数']} 高争议={stats['高争议条目']} 中争议={stats['中等争议条目']}")

    else:
        print("未知命令，试试 --help")
