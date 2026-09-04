#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-KNOWLEDGE-v2.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 全自动AI智能体 · 知识提取模块 v2.0
AutoAgent Knowledge — 关键词提取 + 6类分类 + 图谱存储 + 索引搜索

DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-KNOWLEDGE-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

6 大类别: 概念 / 人物 / 代码 / 流程 / 数字 / 观点
置信度: 依据关键词命中密度 + 文本长度计算
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unittest
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AGENT_DIR = Path.home() / ".longhun" / "agent"
KNOWLEDGE_DIR = AGENT_DIR / "knowledge"
GRAPH_FILE = KNOWLEDGE_DIR / "graph.json"

# 六类关键词库
CATEGORY_KEYWORDS = {
    "概念":   ["概念", "定义", "本质", "原理", "什么是", "架构", "机制", "范式", "方法论"],
    "人物":   ["人物", "作者", "创始人", "专家", "学者", "老兵", "老大", "老师"],
    "代码":   ["代码", "函数", "API", "脚本", "引擎", "模块", "接口", "Python", "SDK", "git"],
    "流程":   ["流程", "步骤", "部署", "流水线", "链路", "闭环", "操作", "路径", "搭建"],
    "数字":   ["数字", "占比", "百分比", "数值", "排名", "版本", "v2", "v3", "369", "512", "1024", "端口"],
    "观点":   ["观点", "认为", "立场", "底线", "原则", "建议", "判断", "主权", "承诺"],
}


@dataclass
class KnowledgePoint:
    """知识点"""
    keyword: str
    category: str
    confidence: float
    source: str
    ts: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TextExtractor:
    """文本提取器: 关键词匹配 + 6类分类 + 置信度"""

    def __init__(self):
        self.category_keywords = {k: set(v) for k, v in CATEGORY_KEYWORDS.items()}

    def extract(self, text: str, source: str = "") -> List[KnowledgePoint]:
        """从文本提取知识点"""
        points: List[KnowledgePoint] = []
        seen = set()
        for category, keywords in self.category_keywords.items():
            hits = [kw for kw in keywords if kw in text]
            if hits:
                for kw in hits[:5]:
                    if kw in seen:
                        continue
                    seen.add(kw)
                    confidence = self._confidence(text, kw, category)
                    points.append(KnowledgePoint(
                        keyword=kw, category=category, confidence=confidence,
                        source=source,
                        ts=datetime.now(timezone.utc).isoformat(),
                    ))
        # 按置信度降序
        points.sort(key=lambda p: p.confidence, reverse=True)
        return points

    def _confidence(self, text: str, keyword: str, category: str) -> float:
        """置信度: 命中密度 + 文本长度 + 类别词占比"""
        density = min(text.count(keyword) / max(len(text), 1) * 100, 10)
        length_bonus = min(len(text) / 500, 0.5)
        cat_hits = sum(1 for kw in self.category_keywords[category] if kw in text)
        cat_bonus = min(cat_hits / max(len(self.category_keywords[category]), 1), 0.4)
        return round(min(density + length_bonus + cat_bonus, 1.0), 3)


class KnowledgeGraph:
    """知识图谱存储 + 索引搜索"""

    def __init__(self):
        self.points: List[KnowledgePoint] = []
        self._load()

    def add(self, points: List[KnowledgePoint]):
        for p in points:
            self.points.append(p)
        self._persist()

    def search(self, keyword: str, category: Optional[str] = None, limit: int = 10) -> List[KnowledgePoint]:
        results = [p for p in self.points if keyword in p.keyword]
        if category:
            results = [p for p in results if p.category == category]
        results.sort(key=lambda p: p.confidence, reverse=True)
        return results[:limit]

    def stats(self) -> Dict[str, Any]:
        by_cat: Dict[str, int] = {}
        for p in self.points:
            by_cat[p.category] = by_cat.get(p.category, 0) + 1
        return {"total": len(self.points), "by_category": by_cat}

    def _persist(self):
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        GRAPH_FILE.touch(exist_ok=True)
        GRAPH_FILE.chmod(0o600)
        data = [p.to_dict() for p in self.points]
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load(self):
        if GRAPH_FILE.exists():
            try:
                with open(GRAPH_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.points = [KnowledgePoint(**d) for d in data]
            except Exception:
                self.points = []


def main():
    parser = argparse.ArgumentParser(prog="lh_auto_knowledge", description="龍魂全自动AI智能体·知识提取模块 v2.0")
    parser.add_argument("--input", type=str, help="提取文本")
    parser.add_argument("--search", type=str, help="搜索关键词")
    parser.add_argument("--category", type=str, help="分类过滤")
    parser.add_argument("--stats", action="store_true", help="图谱统计")
    parser.add_argument("--version", action="store_true", help="版本信息")
    parser.add_argument("--test", action="store_true", help="运行锚点测试")
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAutoKnowledge)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    if args.version:
        print(f"龍魂全自动AI智能体 · 知识提取 v2.0\nDNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-KNOWLEDGE-v2.0\n确认码: {CONFIRM_CODE}\nGPG: {GPG_KEY}")
        sys.exit(0)
    if args.stats:
        print(json.dumps(KnowledgeGraph().stats(), ensure_ascii=False, indent=2))
        sys.exit(0)
    if args.search:
        graph = KnowledgeGraph()
        results = graph.search(args.search, args.category)
        for p in results:
            print(f"[{p.category}·{p.confidence}] {p.keyword}")
        print(f"共 {len(results)} 条")
        sys.exit(0)
    if args.input:
        extractor = TextExtractor()
        points = extractor.extract(args.input)
        graph = KnowledgeGraph()
        graph.add(points)
        for p in points:
            print(f"[{p.category}·{p.confidence}] {p.keyword}")
        print(f"提取 {len(points)} 个知识点")
        sys.exit(0)
    parser.print_help()


class TestAutoKnowledge(unittest.TestCase):
    """知识提取 6 项锚点断言"""

    def test_01_extract(self):
        """① 文本提取出知识点"""
        ext = TextExtractor()
        points = ext.extract("Python引擎的架构原理和API接口，部署流程是第一步，作者是老兵")
        self.assertGreater(len(points), 0)

    def test_02_categories(self):
        """② 六大类别分类"""
        ext = TextExtractor()
        text = "这个概念的定义是架构原理，代码API函数，流程步骤部署，作者人物，数字369占比，观点认为主权"
        points = ext.extract(text)
        cats = {p.category for p in points}
        self.assertGreaterEqual(len(cats), 4)

    def test_03_confidence(self):
        """③ 置信度在 (0, 1] 区间"""
        ext = TextExtractor()
        points = ext.extract("部署流程步骤：先搭建架构，再写代码API")
        for p in points:
            self.assertGreater(p.confidence, 0)
            self.assertLessEqual(p.confidence, 1.0)

    def test_04_graph_persist(self):
        """④ 图谱持久化存储"""
        graph = KnowledgeGraph()
        ext = TextExtractor()
        points = ext.extract("引擎原理测试文本")
        graph.add(points)
        graph2 = KnowledgeGraph()  # 重新加载
        self.assertGreaterEqual(graph2.stats()["total"], len(points))

    def test_05_search(self):
        """⑤ 索引搜索"""
        graph = KnowledgeGraph()
        graph.add([KnowledgePoint("引擎", "概念", 0.9, "test", "now")])
        results = graph.search("引擎")
        self.assertGreaterEqual(len(results), 1)

    def test_06_sort_by_confidence(self):
        """⑥ 置信度降序排序"""
        ext = TextExtractor()
        points = ext.extract("引擎引擎引擎引擎 概念 定义 原理 架构 流程")
        confs = [p.confidence for p in points]
        self.assertEqual(confs, sorted(confs, reverse=True))


if __name__ == "__main__":
    main()
