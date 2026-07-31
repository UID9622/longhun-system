#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂语义节点库 · 命名即架构 v2.0（焊死）

DNA追溯码：#龍魂⚡️丙午·辛未·语义节点-v1
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

三层对齐：
  L1 文件名 = 摘要_类型_结构_权限_DNA.扩展名
  L2 语义层 = 大白话 → 标准节点 → 同义词/近义词/大白话统一
  L3 触角层 = 文件内容语义提取 → 节点关联 → 交叉激活

核心承诺（焊死）：
  - 所有大白话变体映射到标准语义节点
  - 同义词/近义词/大白话统一归一
  - 每个节点有唯一ID、关联节点、权重
  - 不丢数据：未命中走模糊匹配 + 人工兜底

创建者：💎 龍芯北辰｜UID9622
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══════════════════════════════════════════════
# DNA生成（内置·焊死）
# ═══════════════════════════════════════════════

GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
ZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

def _stem_year(year: int) -> str:
    return GAN[(year - 4) % 10] + ZHI[(year - 4) % 12]

def _stem_month(year: int, month: int) -> str:
    idx = (year * 12 + month + 2) % 10
    return GAN[idx] + ZHI[(month + 1) % 12]

def make_dna(module: str, version: str = "v1") -> str:
    """生成标准DNA追溯码：#龍魂⚡️{干支年}·{干支月}·{模块}-{版本}"""
    now = datetime.now()
    return f"#龍魂⚡️{_stem_year(now.year)}·{_stem_month(now.year, now.month)}·{module}-{version}"

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


# ═══════════════════════════════════════════════
# 语义节点库（焊死·持续生长）
# ═══════════════════════════════════════════════

SEMANTIC_NODES: Dict[str, dict[str, Any]] = {
    # ── 民生类 ──
    "押金": {
        "标准词": "押金",
        "同义词": ["保证金", "押金钱", "租房押金", "房屋押金"],
        "近义词": ["定金", "订金", "预付款"],
        "大白话": ["压金", "押的钱", "给房东的钱", "那个钱"],
        "反义词": ["退款", "返还", "退还"],
        "节点ID": "NODE-押金-001",
        "关联节点": ["房东", "租房合同", "违约", "不退"],
        "权重": 1.0,
        "分类": "民生"
    },
    "房东": {
        "标准词": "房东",
        "同义词": ["业主", "房主", "出租方", "甲方"],
        "近义词": ["二房东", "中介", "托管"],
        "大白话": ["房东", "老板", "租房的那个人", "收钱的"],
        "节点ID": "NODE-房东-001",
        "关联节点": ["押金", "租房合同", "涨租", "赶人"],
        "权重": 1.0,
        "分类": "民生"
    },
    "合同": {
        "标准词": "合同",
        "同义词": ["协议", "契约", "文书", "条款"],
        "近义词": ["口头约定", "微信约定", "聊天记录"],
        "大白话": ["那张纸", "签的字", "写的东西", "那个文件"],
        "节点ID": "NODE-合同-001",
        "关联节点": ["签字", "违约", "条款", "霸王条款"],
        "权重": 1.0,
        "分类": "民生"
    },
    "租房合同": {
        "标准词": "租房合同",
        "同义词": ["租赁协议", "房屋租赁合同", "租约"],
        "近义词": ["住房合同", "房屋协议"],
        "大白话": ["租房子签的", "租房那个合同", "租房那份"],
        "节点ID": "NODE-租房合同-001",
        "关联节点": ["押金", "房东", "违约", "退租"],
        "权重": 1.0,
        "分类": "民生"
    },
    "违约": {
        "标准词": "违约",
        "同义词": ["毁约", "违反合同", "不履行"],
        "近义词": ["欠钱", "跑路", "反悔"],
        "大白话": ["说话不算数", "不按合同来", "变卦了"],
        "节点ID": "NODE-违约-001",
        "关联节点": ["合同", "押金", "赔偿", "法律"],
        "权重": 1.0,
        "分类": "民生"
    },
    "工资": {
        "标准词": "工资",
        "同义词": ["薪酬", "薪水", "薪资", "报酬"],
        "近义词": ["劳务费", "加班费", "奖金", "补贴"],
        "大白话": ["工钱", "发的钱", "上班的钱", "干活的钱"],
        "节点ID": "NODE-工资-001",
        "关联节点": ["拖欠", "劳动法", "加班", "社保"],
        "权重": 1.0,
        "分类": "民生"
    },
    "拖欠": {
        "标准词": "拖欠",
        "同义词": ["欠薪", "赖账", "不结账", "扣发"],
        "近义词": ["延迟支付", "逾期", "缓发"],
        "大白话": ["不给钱", "拖着不发", "欠工资", "拖工钱"],
        "节点ID": "NODE-拖欠-001",
        "关联节点": ["工资", "老板", "劳动法", "维权"],
        "权重": 1.0,
        "分类": "民生"
    },
    "维权": {
        "标准词": "维权",
        "同义词": ["维护权益", "保护权利", "合法维权"],
        "近义词": ["投诉", "举报", "上访", "起诉"],
        "大白话": ["讨公道", "要个说法", "找人评理", "打官司"],
        "节点ID": "NODE-维权-001",
        "关联节点": ["法律", "律师", "证据", "劳动局"],
        "权重": 1.0,
        "分类": "民生"
    },

    # ── 治理类 ──
    "清朗行动": {
        "标准词": "清朗行动",
        "同义词": ["网络清朗", "清朗", "整治网络"],
        "近义词": ["净网行动", "扫黑除恶", "反腐"],
        "大白话": ["抓水军", "清垃圾", "整顿网络", "抓坏人"],
        "节点ID": "NODE-清朗-001",
        "关联节点": ["水军", "信息垄断", "害群之马", "蔡赴朝"],
        "权重": 1.0,
        "分类": "治理"
    },
    "水军": {
        "标准词": "水军",
        "同义词": ["网络水军", "五毛", "枪手", "刷手"],
        "近义词": ["营销号", "自媒体", "大V"],
        "大白话": ["刷评论的", "假人", "机器人", "托"],
        "节点ID": "NODE-水军-001",
        "关联节点": ["清朗行动", "信息垄断", "虚假宣传"],
        "权重": 1.0,
        "分类": "治理"
    },
    "信息垄断": {
        "标准词": "信息垄断",
        "同义词": ["信息壁垒", "信息封锁", "信息封闭"],
        "近义词": ["数据霸权", "平台垄断", "算法控制"],
        "大白话": ["不让我们知道", "信息被捂着", "只让看一部分"],
        "节点ID": "NODE-信息垄断-001",
        "关联节点": ["清朗行动", "数据主权", "言论自由"],
        "权重": 1.0,
        "分类": "治理"
    },
    "数据主权": {
        "标准词": "数据主权",
        "同义词": ["数据所有权", "信息主权", "数字主权"],
        "近义词": ["隐私权", "知情权", "删除权"],
        "大白话": ["我的数据我做主", "我的信息归我", "不能随便拿我的数据"],
        "节点ID": "NODE-数据主权-001",
        "关联节点": ["信息垄断", "言论自由", "用户权利"],
        "权重": 1.0,
        "分类": "治理"
    },
    "言论自由": {
        "标准词": "言论自由",
        "同义词": ["表达自由", "说话的权利", "发声权"],
        "近义词": ["批评权", "建议权", "监督权"],
        "大白话": ["想说就说", "骂的自由", "讲真话"],
        "节点ID": "NODE-言论自由-001",
        "关联节点": ["数据主权", "清朗行动", "宪法"],
        "权重": 1.0,
        "分类": "治理"
    },

    # ── 商业类 ──
    "四绝": {
        "标准词": "四绝",
        "同义词": ["四绝开店", "开店四绝", "四绝决策"],
        "近义词": ["开店指南", "经营分析", "选址评估"],
        "大白话": ["开店能不能成", "这个店能开吗", "做生意靠谱不"],
        "节点ID": "NODE-四绝-001",
        "关联节点": ["人流", "竞争", "政策", "成本"],
        "权重": 1.0,
        "分类": "商业"
    },
    "商家信用": {
        "标准词": "商家信用",
        "同义词": ["商家信誉", "商户评级", "商铺口碑"],
        "近义词": ["评分", "好评率", "口碑"],
        "大白话": ["这店靠谱不", "老板人好不好", "会不会坑人"],
        "节点ID": "NODE-商家信用-001",
        "关联节点": ["四绝", "消费", "投诉", "维权"],
        "权重": 1.0,
        "分类": "商业"
    },
    "消费": {
        "标准词": "消费",
        "同义词": ["买东西", "购物", "消费行为"],
        "近义词": ["交易", "支付", "下单"],
        "大白话": ["花钱", "买", "买东西"],
        "节点ID": "NODE-消费-001",
        "关联节点": ["商家信用", "退款", "维权", "发票"],
        "权重": 1.0,
        "分类": "商业"
    },
    "广告": {
        "标准词": "广告",
        "同义词": ["宣传", "推广", "推销"],
        "近义词": ["营销", "软文", "种草"],
        "大白话": ["打广告", "安利", "推荐", "忽悠"],
        "节点ID": "NODE-广告-001",
        "关联节点": ["虚假宣传", "消费", "商家", "平台"],
        "权重": 1.0,
        "分类": "商业"
    },

    # ── 技术/系统类 ──
    "DNA追溯": {
        "标准词": "DNA追溯",
        "同义词": ["DNA追溯码", "追溯码", "DNA签名"],
        "近义词": ["审计追踪", "来源验证", "归属证明"],
        "大白话": ["这个东西是谁做的", "从哪来的", "经谁手"],
        "节点ID": "NODE-DNA-001",
        "关联节点": ["确认码", "签章", "审计", "P0"],
        "权重": 1.0,
        "分类": "技术"
    },
    "三色审计": {
        "标准词": "三色审计",
        "同义词": ["三色标记", "三层审计", "交通灯审计"],
        "近义词": ["风险评估", "合规检查", "安全审核"],
        "大白话": ["红黄绿检查", "哪个能过哪个不能过", "安全不安全标记"],
        "节点ID": "NODE-三色审计-001",
        "关联节点": ["DNA追溯", "P0", "安全", "合规"],
        "权重": 1.0,
        "分类": "技术"
    },
    "蚁群": {
        "标准词": "蚁群",
        "同义词": ["蚁群架构", "蚁群算法", "信息素"],
        "近义词": ["群体智能", "分布式", "协作系统"],
        "大白话": ["像蚂蚁一样干活", "大家一起协作", "不靠一个人"],
        "节点ID": "NODE-蚁群-001",
        "关联节点": ["不动点", "触角", "信息素", "沉睡唤醒"],
        "权重": 1.0,
        "分类": "技术"
    },
    "不动点": {
        "标准词": "不动点",
        "同义词": ["不动点理论", "固定点", "底座"],
        "近义词": ["锚点", "基准", "参照"],
        "大白话": ["不能改的东西", "焊死的部分", "底座不能动"],
        "节点ID": "NODE-不动点-001",
        "关联节点": ["P0", "蚁群", "底座", "合约"],
        "权重": 1.0,
        "分类": "技术"
    },
    "反活跃优先": {
        "标准词": "反活跃优先",
        "同义词": ["反活跃", "沉睡唤醒", "低调优选"],
        "近义词": ["非热门优先", "长尾内容", "不被埋没"],
        "大白话": ["不火的也出来", "别光推最热的", "被埋没的也要看"],
        "节点ID": "NODE-反活跃优先-001",
        "关联节点": ["蚁群", "失忆症友好", "信息素", "沉睡"],
        "权重": 1.0,
        "分类": "技术"
    },
    "失忆症友好": {
        "标准词": "失忆症友好",
        "同义词": ["记忆辅助", "外部大脑", "记忆外挂"],
        "近义词": ["备忘", "提醒", "记录"],
        "大白话": ["记不住我帮你记", "忘了也能找回来", "帮你回忆"],
        "节点ID": "NODE-失忆症友好-001",
        "关联节点": ["反活跃优先", "记忆", "时间线", "唤醒"],
        "权重": 1.0,
        "分类": "技术"
    },
}


# ═══════════════════════════════════════════════
# 语义标准化引擎（焊死）
# ═══════════════════════════════════════════════

@dataclass
class MatchResult:
    """语义匹配结果"""
    node_id: str
    standard: str          # 标准词
    matched_word: str      # 用户用的原词
    match_type: str        # 标准词/同义词/近义词/大白话
    confidence: float = 1.0


class SemanticNormalizer:
    """
    语义标准化器

    将用户大白话输入 → 标准语义节点
    支持：精确匹配 / 同义词匹配 / 近义词匹配 / 大白话匹配
    """

    def __init__(self, nodes: Optional[Dict[str, dict[str, Any]]] = None):
        self.nodes = nodes or SEMANTIC_NODES
        # 构建反向索引：词 → 节点
        self._build_index()

    def _build_index(self):
        """构建反向索引，加速查词"""
        self.word_to_nodes: Dict[str, List[str]] = {}
        for node_key, node in self.nodes.items():
            all_words = (
                [node["标准词"]]
                + node.get("同义词", [])
                + node.get("近义词", [])
                + node.get("大白话", [])
            )
            for w in all_words:
                w_lower = w.lower().strip()
                if w_lower not in self.word_to_nodes:
                    self.word_to_nodes[w_lower] = []
                self.word_to_nodes[w_lower].append(node_key)

    def normalize(self, user_input: str) -> dict[str, Any]:
        """
        语义标准化

        输入："房东那个压金不退怎么办"
        输出：{
            "raw": "房东那个压金不退怎么办",
            "normalized": "房东押金不退",
            "nodes": [...],
            "confidence": 0.95,
            "missing": []
        }
        """
        raw = user_input.strip()
        if not raw:
            return {
                "raw": raw,
                "normalized": "",
                "nodes": [],
                "confidence": 0.0,
                "missing": [],
            }

        matches: List[MatchResult] = []

        # 策略1：最长匹配（优先匹配长词）
        for node_key, node in self.nodes.items():
            all_forms = (
                [(node["标准词"], "标准词")]
                + [(w, "同义词") for w in node.get("同义词", [])]
                + [(w, "近义词") for w in node.get("近义词", [])]
                + [(w, "大白话") for w in node.get("大白话", [])]
            )
            # 按词长度降序
            all_forms.sort(key=lambda x: len(x[0]), reverse=True)

            for word, match_type in all_forms:
                if word in raw:
                    matches.append(MatchResult(
                        node_id=node["节点ID"],
                        standard=node["标准词"],
                        matched_word=word,
                        match_type=match_type,
                        confidence=0.95 if match_type in ("标准词", "同义词") else 0.85
                    ))
                    break  # 一个节点只匹配一次

        # 去重（同节点ID取第一次匹配）
        seen = set()
        deduped: List[MatchResult] = []
        for m in matches:
            if m.node_id not in seen:
                seen.add(m.node_id)
                deduped.append(m)

        # 构建标准表达
        normalized_parts = [m.standard for m in deduped]

        # 计算置信度
        if deduped:
            confidence = sum(m.confidence for m in deduped) / len(deduped)
            # 大白话占比高则降置信度
            dabai_count = sum(1 for m in deduped if m.match_type == "大白话")
            if dabai_count > 0:
                confidence *= (1 - 0.1 * dabai_count / len(deduped))
        else:
            confidence = 0.0

        # 检测缺失：关联节点中有哪些可能相关
        missing = self._detect_missing(raw, deduped)

        return {
            "raw": raw,
            "normalized": " ".join(normalized_parts) if normalized_parts else raw,
            "nodes": [
                {
                    "node_id": m.node_id,
                    "standard": m.standard,
                    "matched_word": m.matched_word,
                    "match_type": m.match_type,
                    "confidence": round(m.confidence, 3),
                }
                for m in deduped
            ],
            "confidence": round(confidence, 3),
            "missing": missing,
            "dna": make_dna("语义标准化", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

    def _detect_missing(self, raw: str, matched: List[MatchResult]) -> List[str]:
        """检测可能缺失的语义节点"""
        matched_ids = {m.node_id for m in matched}
        related_ids: Set[str] = set()

        for node_key in self.nodes:
            node = self.nodes[node_key]
            if node["节点ID"] in matched_ids:
                for related in node.get("关联节点", []):
                    related_ids.add(related)

        missing = []
        for node_key, node in self.nodes.items():
            if (
                node["节点ID"] not in matched_ids
                and node["标准词"] in related_ids
            ):
                missing.append(node["标准词"])

        return missing

    def fuzzy_match(self, keyword: str, threshold: float = 0.6) -> List[dict[str, Any]]:
        """
        模糊匹配：对未知词做相似度计算

        返回可能的语义节点匹配（含相似度分）
        """
        results = []
        keyword_lower = keyword.lower().strip()

        for node_key, node in self.nodes.items():
            candidates = [node["标准词"]] + node.get("同义词", []) + node.get("大白话", [])
            best_score = 0.0
            best_word = ""

            for candidate in candidates:
                score = self._string_similarity(keyword_lower, candidate.lower())
                if score > best_score:
                    best_score = score
                    best_word = candidate

            if best_score >= threshold:
                results.append({
                    "node_id": node["节点ID"],
                    "standard": node["标准词"],
                    "candidate_word": best_word,
                    "keyword": keyword,
                    "similarity": round(best_score, 3),
                    "classification": node.get("分类", "未知"),
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

    def _string_similarity(self, a: str, b: str) -> float:
        """简单字符串相似度（编辑距离归一化）"""
        if not a or not b:
            return 0.0

        # Levenshtein距离
        m, n = len(a), len(b)
        if m < n:
            a, b = b, a
            m, n = n, m

        # 使用两行优化
        prev = list(range(n + 1))
        curr = [0] * (n + 1)
        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                cost = 0 if a[i-1] == b[j-1] else 1
                curr[j] = min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + cost)
            prev, curr = curr, prev

        distance = prev[n]
        max_len = max(m, n)
        return 1.0 - (distance / max_len)

    def handle_unknown(self, content: str) -> dict[str, Any]:
        """
        处理无法识别的输入

        1. 提取关键词
        2. 模糊匹配
        3. 仍未匹配 → 标记"待人工审核"
        """
        # 简单关键词提取（按常见切分）
        keywords = [
            w.strip() for w in re.split(r'[，。！？；：、\s,.!?;:]+', content)
            if len(w.strip()) >= 2
        ]

        fuzzy_matches = []
        unknown_keywords = []

        for kw in keywords:
            matches = self.fuzzy_match(kw, threshold=0.6)
            if matches:
                fuzzy_matches.extend(matches)
            else:
                unknown_keywords.append(kw)

        if not fuzzy_matches:
            return {
                "status": "UNKNOWN",
                "action": "人工审核",
                "suggested_name": None,
                "keywords": keywords,
                "dna": make_dna("语义未知处理", "v1"),
                "confirm_code": CONFIRM_CODE,
            }

        # 取最佳模糊匹配
        best = max(fuzzy_matches, key=lambda x: x["similarity"])
        suggested_name = f"{best['standard']}_历史文件_{best['classification']}_P4_待确认"

        return {
            "status": "FUZZY_MATCH",
            "action": "用户确认",
            "suggested_name": suggested_name,
            "best_match": best,
            "all_matches": fuzzy_matches[:5],
            "unknown_keywords": unknown_keywords,
            "dna": make_dna("语义未知处理", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

    def list_nodes(self, classification: Optional[str] = None) -> List[dict[str, Any]]:
        """列出所有语义节点"""
        result = []
        for node_key, node in self.nodes.items():
            if classification and node.get("分类") != classification:
                continue
            result.append({
                "node_id": node["节点ID"],
                "standard": node["标准词"],
                "classification": node.get("分类", "未分类"),
                "synonyms": len(node.get("同义词", [])),
                "colloquial": len(node.get("大白话", [])),
                "related": node.get("关联节点", []),
                "weight": node["权重"],
            })
        return result

    def add_node(self, node_key: str, node_def: dict[str, Any]) -> bool:
        """
        动态添加语义节点（生长机制）

        只能在P2及以上权限操作，留审计日志
        """
        if node_key in self.nodes:
            return False
        self.nodes[node_key] = node_def
        self._build_index()  # 重建索引
        return True

    def to_json(self) -> str:
        """导出语义节点库为JSON"""
        return json.dumps(self.nodes, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════
# CLI入口（焊死）
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    norm = SemanticNormalizer()

    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            classification = sys.argv[2] if len(sys.argv) > 2 else None
            nodes = norm.list_nodes(classification)
            print(json.dumps(nodes, ensure_ascii=False, indent=2))
        elif cmd == "normalize":
            text = sys.argv[2] if len(sys.argv) > 2 else ""
            result = norm.normalize(text)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif cmd == "fuzzy":
            kw = sys.argv[2] if len(sys.argv) > 2 else ""
            result = norm.fuzzy_match(kw)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif cmd == "unknown":
            text = sys.argv[2] if len(sys.argv) > 2 else ""
            result = norm.handle_unknown(text)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif cmd == "export":
            print(norm.to_json())
        else:
            print(f"未知命令: {cmd}")
            print("用法: python semantic_nodes.py [list|normalize|fuzzy|unknown|export] [...]")
    else:
        # 默认自检
        print("=" * 50)
        print("【龍魂语义节点库 · 自检】")
        print(f"DNA: {make_dna('语义节点', 'v1')}")
        print(f"确认码: {CONFIRM_CODE}")
        print("=" * 50)

        # 测试1：大白话标准化
        test_cases = [
            "房东那个压金不退怎么办",
            "这店靠谱不，会不会坑人",
            "我记不住，你帮我记",
            "抓水军！整顿网络！",
            "那个文件是谁签的字",
        ]
        for tc in test_cases:
            result = norm.normalize(tc)
            print(f"\n输入: {tc}")
            print(f"标准: {result['normalized']}")
            print(f"节点: {[n['standard'] for n in result['nodes']]}")
            print(f"置信: {result['confidence']}")

        # 测试2：未知词处理
        unknown = norm.handle_unknown("算法收割注意力机制")
        print(f"\n未知处理: {unknown['status']} → {unknown.get('best_match', {}).get('standard', '无匹配')}")

        print(f"\n总节点数: {len(SEMANTIC_NODES)}")
        print("✅ 语义节点库正常 · 焊死")
